
import pytest

from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert


def test_wind_alert_all_levels():
    assert wind_alert(10) == "none"
    assert wind_alert(39) == "advisory"
    assert wind_alert(62) == "watch"
    assert wind_alert(89) == "warning"


def test_rain_alert_all_levels():
    assert rain_alert(5, False) == "none"
    assert rain_alert(10, False) == "advisory"
    assert rain_alert(10, True) == "watch"
    assert rain_alert(50, False) == "watch"
    assert rain_alert(50, True) == "warning"


def test_heat_alert_all_levels():
    assert heat_alert(25, 40) == "none"
    assert heat_alert(35, 40) == "advisory"
    assert heat_alert(40, 40) == "watch"
    assert heat_alert(45, 40) == "warning"


def test_heat_alert_humidity_adjustment():
    assert heat_alert(34, 50) == "advisory"
    assert heat_alert(39, 60) == "watch"
    assert heat_alert(44, 60) == "warning"


def test_overall_alert_severity():
    assert overall_alert(["none", "advisory"]) == "advisory"
    assert overall_alert(["watch", "warning", "none"]) == "warning"
    assert overall_alert(["warning", "watch"]) == "warning"


def test_overall_alert_unknown_value():
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["storm"])
