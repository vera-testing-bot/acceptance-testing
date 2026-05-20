def can_create_job(committer_status):
    normalized_status = (committer_status or "").strip().lower()
    return normalized_status == "active"
