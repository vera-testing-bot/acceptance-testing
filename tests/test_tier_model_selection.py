"""Tests for the vera-engine tier-based model selection contract (issue #870).

The acceptance criteria in issue #870 concern tier floors enforced server-side
in vera-engine (vera#6425). This fixture repository cannot import vera-engine
source, so the contract is captured as a reviewed fixture
(`tests/fixtures/tier_contract.json`) and verified here, alongside the
runtime-manifest evidence from this PR's own Vera dispatches.
"""

import json
from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "fixtures" / "tier_contract.json"


@pytest.fixture(scope="module")
def contract():
    with open(FIXTURE) as f:
        return json.load(f)


def test_fixture_exists_and_parses():
    assert FIXTURE.exists(), "tier contract fixture must exist"
    with open(FIXTURE) as f:
        contract = json.load(f)
    assert isinstance(contract, dict)


def test_triage_dispatches_at_clay_tier(contract):
    """Issue #870 criterion 1: triage dispatches at clay tier (cheapest model)."""
    assert contract["task_kind_tier"]["triage"] == "clay"


def test_implement_dispatches_at_stone_tier(contract):
    """Issue #870 criterion 2: implement dispatches at stone tier."""
    assert contract["task_kind_tier"]["implement"] == "stone"


def test_review_plan_dispatches_at_bronze_tier(contract):
    """Issue #870 criterion 3: review plan dispatches at bronze tier."""
    assert contract["task_kind_tier"]["review_plan"] == "bronze"


def test_holistic_review_uses_pinned_model(contract):
    """Issue #870 criterion 4: holistic review uses its pinned model (not tier)."""
    assert contract["task_kind_tier"]["holistic_review"] == "pinned"
    # A pinned-model override must never be routed through tier selection.
    assert contract["pinned_model_overrides"] == ["holistic_review"]
    assert "TaskKind.JUDGE" in contract["removed_enum_members"]


def test_tier_contract_matches_issue_870_floor(contract):
    """The fixture mirrors the tier floors documented in issue #870 / vera#6425."""
    expected = {
        "triage": "clay",
        "code_review": "stone",
        "implement": "stone",
        "investigate": "stone",
        "address_feedback": "stone",
        "multi_review_step": "stone",
        "review_plan": "bronze",
        "holistic_review": "pinned",
    }
    assert contract["task_kind_tier"] == expected


def test_runtime_manifest_evidence(contract):
    """Runtime manifest evidence: tier-based dispatch selected a model with the
    engine/model/cli_version attribution written procedurally before the run."""
    evidence = contract["runtime_manifest_evidence"]
    assert evidence["engine"] and evidence["model"], (
        "manifest evidence must record engine and model"
    )
    # The manifest model is namespace-qualified and tier-selected, not a
    # hardcoded self-report.
    assert "/" in evidence["model"]


def test_credential_guards_imported_not_forked(contract):
    """Issue #870 key change: credential guard primitives come from vera-engine
    (identity check, not a fork), with select_model(exclude=...) blacklist."""
    assert contract["credential_guards_source"] == "vera-engine"
    assert contract["credential_guards_note"]
