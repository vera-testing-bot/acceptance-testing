from src.committer_status import can_create_job


def test_can_create_job_allows_active_committer_status():
    assert can_create_job("active") is True


def test_can_create_job_rejects_inactive_committer_status():
    assert can_create_job("inactive") is False


def test_can_create_job_rejects_blank_status():
    assert can_create_job("") is False


def test_can_create_job_normalizes_case_and_whitespace():
    assert can_create_job("  ACTIVE  ") is True
