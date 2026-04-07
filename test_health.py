from health import get_health_status


def test_get_health_status():
    result = get_health_status()
    assert result == {"status": "ok", "version": "1.0.0"}
