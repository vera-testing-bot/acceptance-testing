"""Tests for .github/workflows/vera.yml structure and credential handling."""

import yaml
import pytest
from pathlib import Path


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
    assert "GITHUB_ENV" in run, "Fetch credentials step must export credentials into environment"
    assert ".secrets // {}" in run, "Fetch credentials step must read secrets from API response"
    assert "to_entries[]" in run, "Fetch credentials step must iterate over secret entries"


def test_creds_step_masks_github_app_token(creds_step):
    run = creds_step["run"]
    # Credentials must be masked before they are exported.
    lines = run.splitlines()
    mask_idx = next((i for i, l in enumerate(lines) if "add-mask" in l), None)
    output_idx = next(
        (i for i, l in enumerate(lines) if "GITHUB_ENV" in l and "echo \"${k}=${v}\"" in l),
        None,
    )
    assert mask_idx is not None, "Credentials must be masked with ::add-mask::"
    assert output_idx is not None, "Credentials must be written to GITHUB_ENV"
    assert mask_idx < output_idx, "Credentials must be masked before being written to env"


def test_run_agent_uses_app_token_for_gh_token(run_agent_step):
    env = run_agent_step["env"]
    gh_token = env.get("GH_TOKEN", "")
    assert "env.GITHUB_APP_TOKEN" in gh_token, "GH_TOKEN must prefer GITHUB_APP_TOKEN"
    assert "secrets.GITHUB_TOKEN" in gh_token, "GH_TOKEN must fall back to secrets.GITHUB_TOKEN"


def test_run_agent_uses_app_token_for_github_token(run_agent_step):
    env = run_agent_step["env"]
    github_token = env.get("GITHUB_TOKEN", "")
    assert "env.GITHUB_APP_TOKEN" in github_token, "GITHUB_TOKEN must prefer GITHUB_APP_TOKEN"
    assert "secrets.GITHUB_TOKEN" in github_token, "GITHUB_TOKEN must fall back to secrets.GITHUB_TOKEN"


def test_run_agent_fallback_references_secrets(run_agent_step):
    env = run_agent_step["env"]
    for var in ("GH_TOKEN", "GITHUB_TOKEN"):
        assert "secrets.GITHUB_TOKEN" in env.get(var, ""), (
            f"{var} must include secrets.GITHUB_TOKEN as fallback"
        )
