import pytest
from pydantic import ValidationError

import assemblyai as aai


@pytest.mark.parametrize(
    "field",
    [
        "http_timeout",
        "sync_http_timeout",
        "sync_live_http_timeout",
        "dictation_http_timeout",
        "llm_gateway_http_timeout",
    ],
)
@pytest.mark.parametrize("bad_val", [-10.0, -1.0, -0.001, 0.0, 0])
def test_settings_timeouts_reject_non_positive(field: str, bad_val: float):
    with pytest.raises(ValidationError):
        aai.Settings(**{field: bad_val})


def test_settings_keepalive_expiry_rejects_negative():
    with pytest.raises(ValidationError):
        aai.Settings(keepalive_expiry=-1.0)


def test_settings_keepalive_expiry_accepts_zero_and_positive():
    s = aai.Settings(keepalive_expiry=0)
    assert s.keepalive_expiry == 0
    s2 = aai.Settings(keepalive_expiry=120.0)
    assert s2.keepalive_expiry == 120.0


def test_settings_valid_timeout_values_are_accepted():
    s = aai.Settings(
        http_timeout=15.0,
        sync_http_timeout=30.0,
        sync_live_http_timeout=90.0,
        dictation_http_timeout=120.0,
        llm_gateway_http_timeout=10.0,
    )
    assert s.http_timeout == 15.0
    assert s.sync_http_timeout == 30.0
    assert s.sync_live_http_timeout == 90.0
    assert s.dictation_http_timeout == 120.0
    assert s.llm_gateway_http_timeout == 10.0
