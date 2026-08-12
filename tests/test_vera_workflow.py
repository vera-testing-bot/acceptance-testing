"""Tests for .github/workflows/vera.yml structure and credential handling."""

from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / ".github" / "workflows" / "vera.yml"


@pytest.fixture(scope="module")
def workflow():
    with open(WORKFLOW_PATH) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def creds_step(workflow):
    steps = workflow["jobs"]["vera"]["steps"]
    return next(
        s
        for s in steps
        if s.get("id") == "creds" or s.get("name") == "Fetch job package"
    )


@pytest.fixture(scope="module")
def run_agent_step(workflow):
    steps = workflow["jobs"]["vera"]["steps"]
    return next(s for s in steps if s.get("name") in {"Run agent", "Run"})


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
    mask_idx = next((i for i, l in enumerate(lines) if "add-mask" in l), None)
    output_idx = next(
        (
            i
            for i, l in enumerate(lines)
            if "GITHUB_ENV" in l and 'echo "${k}=${v}"' in l
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
    assert "GITHUB_TOKEN" in gh_token, "GH_TOKEN must fall back to secrets.GITHUB_TOKEN"


def test_run_agent_uses_app_token_for_github_token(run_agent_step):
    env = run_agent_step["env"]
    github_token = env.get("GITHUB_TOKEN", "")
    assert "GITHUB_APP_TOKEN" in github_token, (
        "GITHUB_TOKEN must prefer GitHub App token"
    )
    assert "GITHUB_TOKEN" in github_token, (
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
    steps = workflow["jobs"]["vera"]["steps"]
    return next(s for s in steps if s.get("name") == "Report success")


@pytest.fixture(scope="module")
def failsafe_finalizer_step(workflow):
    steps = workflow["jobs"]["vera"]["steps"]
    return next(s for s in steps if s.get("name") == "Failsafe finalizer")


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


def test_failsafe_finalizer_step_reads_runtime_manifest(failsafe_finalizer_step):
    run = failsafe_finalizer_step["run"]
    assert "/tmp/vera_manifest.json" in run, (
        "Failsafe finalizer step must read the runtime manifest for attribution"
    )
    assert "MANIFEST_LABEL" in run, (
        "Failsafe finalizer must extract attribution from the runtime manifest"
    )


def test_credential_exchange_rejects_missing_inputs(creds_step):
    run = creds_step["run"]
    assert "runner-credential-exchange-failed: missing required inputs" in run, (
        "Missing inputs must surface a credential-exchange failure reason"
    )


def test_credential_exchange_rejects_non_retryable_http(creds_step):
    run = creds_step["run"]
    assert "runner-credential-exchange-failed: non-retryable HTTP" in run, (
        "Non-retryable HTTP responses must surface a credential-exchange failure reason"
    )
