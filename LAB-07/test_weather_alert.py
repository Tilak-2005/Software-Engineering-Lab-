import math
import pytest
from hypothesis import given, strategies as st

from weather_alert import parse_reading, wind_category, rainfall_spread


# 1. Fuzz testing: parse_reading
@given(st.one_of(
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.text()
))
def test_parse_reading_rejects_or_handles_arbitrary_input(s):
    try:
        result = parse_reading(s)
    except ValueError:
        return

    assert isinstance(result, tuple) and len(result) == 2
    assert math.isfinite(result[0])
    assert isinstance(result[1], int)


# 2. Fuzz testing: wind_category
@given(st.one_of(
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.text()
))
def test_wind_category_rejects_or_handles_arbitrary_input(s):
    try:
        result = wind_category(s)
    except ValueError:
        return

    assert result in {"warning", "advisory", "none"}


# 3. Fuzz testing: rainfall_spread
@given(st.one_of(
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.text()
))
def test_rainfall_spread_rejects_or_handles_arbitrary_input(s):
    try:
        result = rainfall_spread(s)
    except ValueError:
        return

    assert isinstance(result, float)
    assert math.isfinite(result)
    assert result >= 0


# 4. Valid temperature and humidity inputs
@given(
    st.floats(allow_nan=False, allow_infinity=False),
    st.integers()
)
def test_parse_reading_valid_values(temp, humidity):
    result = parse_reading(f"{temp}/{humidity}")
    assert result == (temp, humidity)


# 5–7. Wind category boundary tests
@given(st.integers(min_value=0, max_value=38))
def test_wind_category_none_range(speed):
    assert wind_category(str(speed)) == "none"


@given(st.integers(min_value=39, max_value=88))
def test_wind_category_advisory_range(speed):
    assert wind_category(str(speed)) == "advisory"


@given(st.integers(min_value=89, max_value=100000))
def test_wind_category_warning_range(speed):
    assert wind_category(str(speed)) == "warning"


# 8. Rainfall spread property test
@given(
    st.lists(
        st.floats(
            min_value=0,
            max_value=1000000,
            allow_nan=False,
            allow_infinity=False
        ),
        min_size=1,
        max_size=30
    )
)
def test_rainfall_spread_matches_max_minus_min(readings):
    csv = ",".join(str(value) for value in readings)

    assert math.isclose(
        rainfall_spread(csv),
        max(readings) - min(readings),
        rel_tol=1e-12,
        abs_tol=1e-12
    )


# 9–16. Invalid temperature/humidity inputs
@pytest.mark.parametrize("bad", [
    None,
    "",
    "25",
    "25/70/90",
    "abc/70",
    "25/abc",
    "nan/70",
    "inf/70"
])
def test_parse_reading_invalid_examples(bad):
    with pytest.raises(ValueError):
        parse_reading(bad)


# 17–21. Invalid wind inputs
@pytest.mark.parametrize("bad", [
    None,
    "",
    "abc",
    "12.5",
    "-1"
])
def test_wind_category_invalid_examples(bad):
    with pytest.raises(ValueError):
        wind_category(bad)


# 22–28. Invalid rainfall inputs
@pytest.mark.parametrize("bad", [
    None,
    "",
    "1,,3",
    "one,two",
    "nan,1",
    "inf,2",
    "-1,2"
])
def test_rainfall_spread_invalid_examples(bad):
    with pytest.raises(ValueError):
        rainfall_spread(bad)