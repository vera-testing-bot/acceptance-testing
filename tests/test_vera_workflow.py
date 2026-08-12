"""Tests for .github/workflows/vera.yml structure, credential handling,
runtime manifest attribution, and credential-exchange failure guards."""

from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / ".github" / "workflows" / "vera.yml"


def _get_step(workflow, name):
    """Return the first step whose name matches *name* (or is in *name* if a set)."""
    steps = workflow["jobs"]["vera"]["steps"]
    names = name if isinstance(name, set) else {name}
    for step in steps:
        if step.get("name") in names:
            return step
    known = {s.get("name") for s in steps}
    raise AssertionError(f"No step named {name!r}; known names: {sorted(known)!r}")


@pytest.fixture(scope="module")
def workflow():
    with open(WORKFLOW_PATH) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def creds_step(workflow):
    return _get_step(workflow, "Fetch job package")


@pytest.fixture(scope="module")
def run_agent_step(workflow):
    return _get_step(workflow, {"Run agent", "Run"})


def _assert_failure_reason_before_exit(run, reason):
    """Assert a credential-exchange failure reason is written before any later `exit 1`."""
    lines = run.splitlines()
    reason_idx = next(
        (i for i, line in enumerate(lines) if reason in line), None
    )
    assert reason_idx is not None, f"Failure reason not found: {reason!r}"
    exit_after = next(
        (
            i
            for i, line in enumerate(lines)
            if i > reason_idx and line.strip() == "exit 1"
        ),
        None,
    )
    assert exit_after is not None, (
        f"Failure reason {reason!r} is not followed by an exit 1"
    )


def test_creds_step_extracts_github_app_token(creds_step):
    run = creds_step["run"]
    assert "jq -r" in run, "Fetch credentials step must parse API response JSON"
    assert "GITHUB_ENV" in run, (
        "Fetch credentials step must export credentials into environment"
    )
    assert ".secrets // {}" in run, (
        "Fetch credentials step must read secrets from API response"
    )
    assert "to_entries[]" in run, (
        "Fetch credentials step must iterate over secret entries"
    )


def test_creds_step_masks_github_app_token(creds_step):
    run = creds_step["run"]
    # Credentials must be masked before they are exported.
    lines = run.splitlines()
    mask_idx = next((i for i, line in enumerate(lines) if "add-mask" in line), None)
    output_idx = next(
        (
            i
            for i, line in enumerate(lines)
            if "GITHUB_ENV" in line and 'echo "${k}=${v}"' in line
        ),
        None,
    )
    assert mask_idx is not None, "Credentials must be masked with ::add-mask::"
    assert output_idx is not None, "Credentials must be written to GITHUB_ENV"
    assert mask_idx < output_idx, (
        "Credentials must be masked before being written to env"
    )


def test_run_agent_uses_app_token_for_gh_token(run_agent_step):
    env = run_agent_step["env"]
    gh_token = env.get("GH_TOKEN", "")
    assert "GITHUB_APP_TOKEN" in gh_token, "GH_TOKEN must prefer GitHub App token"
    assert "secrets.GITHUB_TOKEN" in gh_token, (
        "GH_TOKEN must fall back to secrets.GITHUB_TOKEN"
    )


def test_run_agent_uses_app_token_for_github_token(run_agent_step):
    env = run_agent_step["env"]
    github_token = env.get("GITHUB_TOKEN", "")
    assert "GITHUB_APP_TOKEN" in github_token, (
        "GITHUB_TOKEN must prefer GitHub App token"
    )
    assert "secrets.GITHUB_TOKEN" in github_token, (
        "GITHUB_TOKEN must fall back to secrets.GITHUB_TOKEN"
    )


def test_run_agent_fallback_references_secrets(run_agent_step):
    env = run_agent_step["env"]
    # Both vars must reference secrets.GITHUB_TOKEN as fallback
    for var in ("GH_TOKEN", "GITHUB_TOKEN"):
        assert "secrets.GITHUB_TOKEN" in env.get(var, ""), (
            f"{var} must include secrets.GITHUB_TOKEN as fallback"
        )


@pytest.fixture(scope="module")
def report_success_step(workflow):
    return _get_step(workflow, "Report success")


@pytest.fixture(scope="module")
def report_failure_step(workflow):
    return _get_step(workflow, "Report failure")


@pytest.fixture(scope="module")
def failsafe_finalizer_step(workflow):
    return _get_step(workflow, "Failsafe finalizer")


def test_report_success_step_reads_runtime_manifest(report_success_step):
    run = report_success_step["run"]
    assert "/tmp/vera_manifest.json" in run, (
        "Report success step must read the runtime manifest"
    )
    assert "MANIFEST_JSON=$(jq -c . /tmp/vera_manifest.json" in run, (
        "Report success step must parse the runtime manifest as compact JSON"
    )


def test_report_success_step_forwards_manifest_in_payload(report_success_step):
    run = report_success_step["run"]
    assert "{manifest:$manifest}" in run, (
        "Report success callback payload must include the manifest object"
    )
    assert "MANIFEST_JSON" in run, (
        "Report success step must compute MANIFEST_JSON from the runtime manifest"
    )


def test_report_failure_step_forwards_manifest_in_payload(report_failure_step):
    run = report_failure_step["run"]
    assert "/tmp/vera_manifest.json" in run, (
        "Report failure step must read the runtime manifest"
    )
    assert "MANIFEST_JSON=$(jq -c . /tmp/vera_manifest.json" in run, (
        "Report failure step must parse the runtime manifest as compact JSON"
    )
    assert "{manifest:$manifest}" in run, (
        "Report failure callback payload must include the manifest object"
    )
    assert "MANIFEST_JSON" in run, (
        "Report failure step must compute MANIFEST_JSON from the runtime manifest"
    )


def test_failsafe_finalizer_step_reads_runtime_manifest(failsafe_finalizer_step):
    run = failsafe_finalizer_step["run"]
    assert "/tmp/vera_manifest.json" in run, (
        "Failsafe finalizer step must read the runtime manifest for attribution"
    )
    assert "MANIFEST_LABEL" in run, (
        "Failsafe finalizer must extract attribution from the runtime manifest"
    )
    assert ".engine" in run, (
        "Failsafe finalizer must read the engine field from the manifest"
    )
    assert ".model" in run, (
        "Failsafe finalizer must read the model field from the manifest"
    )
    assert ".cli_version" in run, (
        "Failsafe finalizer must read the cli_version field from the manifest"
    )


def test_credential_exchange_rejects_missing_inputs(creds_step):
    run = creds_step["run"]
    reason = "runner-credential-exchange-failed: missing required inputs"
    assert reason in run, (
        "Missing inputs must surface a credential-exchange failure reason"
    )
    _assert_failure_reason_before_exit(run, reason)


def test_credential_exchange_rejects_non_retryable_http(creds_step):
    run = creds_step["run"]
    reason = "runner-credential-exchange-failed: non-retryable HTTP"
    assert reason in run, (
        "Non-retryable HTTP responses must surface a credential-exchange failure reason"
    )
    _assert_failure_reason_before_exit(run, reason)


def test_credential_exchange_rejects_non_ok_status(creds_step):
    run = creds_step["run"]
    assert "jq -r '.status // empty'" in run, (
        "Credential response body must be inspected for an ok status"
    )
    reason = (
        "runner-credential-exchange-failed: credential exchange returned a non-ok status"
    )
    assert reason in run, (
        "Credential exchange returning a non-ok status must surface a failure reason"
    )
    _assert_failure_reason_before_exit(run, reason)
