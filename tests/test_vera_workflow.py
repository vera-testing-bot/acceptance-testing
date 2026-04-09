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
    return next(s for s in steps if s.get("id") == "creds")


@pytest.fixture(scope="module")
def run_agent_step(workflow):
    steps = workflow["jobs"]["vera"]["steps"]
    return next(s for s in steps if s.get("name") == "Run agent")


def test_creds_step_extracts_github_app_token(creds_step):
    run = creds_step["run"]
    assert "github_token" in run, "Fetch credentials step must read github_token from API response"
    assert "github_app_token" in run, "Fetch credentials step must output github_app_token"


def test_creds_step_masks_github_app_token(creds_step):
    run = creds_step["run"]
    # The token must be masked before being written to output
    lines = run.splitlines()
    mask_idx = next(
        (i for i, l in enumerate(lines) if "add-mask" in l and "GITHUB_APP_TOKEN" in l),
        None,
    )
    output_idx = next(
        (i for i, l in enumerate(lines) if "github_app_token=" in l and "GITHUB_OUTPUT" in l),
        None,
    )
    assert mask_idx is not None, "github_app_token must be masked with ::add-mask::"
    assert output_idx is not None, "github_app_token must be written to GITHUB_OUTPUT"
    assert mask_idx < output_idx, "Token must be masked before being written to output"


def test_run_agent_uses_app_token_for_gh_token(run_agent_step):
    env = run_agent_step["env"]
    gh_token = env.get("GH_TOKEN", "")
    assert "github_app_token" in gh_token, "GH_TOKEN must prefer github_app_token"
    assert "GITHUB_TOKEN" in gh_token, "GH_TOKEN must fall back to secrets.GITHUB_TOKEN"


def test_run_agent_uses_app_token_for_github_token(run_agent_step):
    env = run_agent_step["env"]
    github_token = env.get("GITHUB_TOKEN", "")
    assert "github_app_token" in github_token, "GITHUB_TOKEN must prefer github_app_token"
    assert "GITHUB_TOKEN" in github_token, "GITHUB_TOKEN must fall back to secrets.GITHUB_TOKEN"


def test_run_agent_fallback_references_secrets(run_agent_step):
    env = run_agent_step["env"]
    # Both vars must reference secrets.GITHUB_TOKEN as fallback
    for var in ("GH_TOKEN", "GITHUB_TOKEN"):
        assert "secrets.GITHUB_TOKEN" in env.get(var, ""), (
            f"{var} must include secrets.GITHUB_TOKEN as fallback"
        )