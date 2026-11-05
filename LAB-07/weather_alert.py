
import math


def parse_reading(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    if text.count('/') != 1:
        raise ValueError("Use temperature/humidity format")

    temp, humidity = text.split('/')

    try:
        temp = float(temp)
        humidity = int(humidity)
    except (ValueError, TypeError, OverflowError):
        raise ValueError("Invalid temperature or humidity")

    if not math.isfinite(temp):
        raise ValueError("Temperature must be finite")

    return temp, humidity


def wind_category(speed_text):
    if not isinstance(speed_text, str) or not speed_text.strip():
        raise ValueError("Wind speed must be a valid integer")

    try:
        speed = int(speed_text)
    except (ValueError, TypeError, OverflowError):
        raise ValueError("Wind speed must be an integer")

    if speed < 0:
        raise ValueError("Wind speed cannot be negative")

    if speed >= 89:
        return 'warning'
    if speed >= 39:
        return 'advisory'
    return 'none'


def rainfall_spread(readings_csv):
    if not isinstance(readings_csv, str) or not readings_csv.strip():
        raise ValueError("Rainfall readings cannot be empty")

    try:
        readings = [
            float(value.strip())
            for value in readings_csv.split(',')
        ]
    except (ValueError, TypeError, OverflowError):
        raise ValueError("Invalid rainfall readings")

    if not readings:
        raise ValueError("At least one reading is required")

    if not all(math.isfinite(value) and value >= 0 for value in readings):
        raise ValueError("Rainfall must be finite and non-negative")

    return max(readings) - min(readings)


def main():
    print("==== Running parse_reading ====")
    try:
        user_input = input("Enter temperature/humidity (e.g. 35.5/80): ")
        print("Temperature and Humidity:", parse_reading(user_input))
    except ValueError as e:
        print("Input error:", e)

    print("\n==== Running wind_category ====")
    try:
        user_input = input("Enter a wind speed in km/h (e.g. 45): ")
        print("Wind Category:", wind_category(user_input))
    except ValueError as e:
        print("Input error:", e)

    print("\n==== Running rainfall_spread ====")
    try:
        user_input = input("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): ")
        print("Rainfall Spread:", rainfall_spread(user_input))
    except ValueError as e:
        print("Input error:", e)


if __name__ == "__main__":
    main()
