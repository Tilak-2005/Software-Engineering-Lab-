
import pytest

from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert


def test_wind_alert_boundaries():
    assert wind_alert(38) == "none"
    assert wind_alert(39) == "advisory"
    assert wind_alert(61) == "advisory"
    assert wind_alert(62) == "watch"
    assert wind_alert(88) == "watch"
    assert wind_alert(89) == "warning"


def test_rain_alert_branches():
    assert rain_alert(49, False) == "advisory"
    assert rain_alert(49, True) == "watch"
    assert rain_alert(50, False) == "watch"
    assert rain_alert(50, True) == "warning"
    assert rain_alert(9, False) == "none"
    assert rain_alert(9, True) == "none"


def test_heat_alert_branches():
    assert heat_alert(34, 40) == "none"
    assert heat_alert(35, 40) == "advisory"
    assert heat_alert(39, 40) == "advisory"
    assert heat_alert(40, 40) == "watch"
    assert heat_alert(44, 40) == "watch"
    assert heat_alert(45, 40) == "warning"


def test_heat_humidity_condition():
    assert heat_alert(35, 40) == "advisory"
    assert heat_alert(35, 41) == "advisory"
    assert heat_alert(34, 50) == "advisory"


def test_overall_alert_loop_and_validation():
    assert overall_alert([]) == "none"
    assert overall_alert(["none"]) == "none"
    assert overall_alert(["advisory", "watch"]) == "watch"
    assert overall_alert(["warning", "advisory"]) == "warning"

    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["invalid"])
