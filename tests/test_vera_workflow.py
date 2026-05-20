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
    return next(s for s in steps if s.get("name") == "Fetch job package")


@pytest.fixture(scope="module")
def run_agent_step(workflow):
    steps = workflow["jobs"]["vera"]["steps"]
    return next(s for s in steps if s.get("name") == "Run")


def test_creds_step_extracts_github_app_token(creds_step):
    run = creds_step["run"]
    assert ".secrets" in run, "Fetch credentials step must parse secrets from API response"
    assert "GITHUB_ENV" in run, "Fetch credentials step must export secrets to GITHUB_ENV"


def test_creds_step_masks_github_app_token(creds_step):
    run = creds_step["run"]
    assert "::add-mask::" in run, "Secrets must be masked before export"
    assert "echo \"${k}=${v}\" >> \"$GITHUB_ENV\"" in run, (
        "Secrets must be exported to GITHUB_ENV"
    )


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
