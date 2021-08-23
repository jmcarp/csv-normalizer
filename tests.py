import pytest

import normalize


def test_normalize_row():
    """Exercise `normalize_row` with a sample row."""
    input_row = {
        "Timestamp": "4/1/11 11:00:00 AM",
        "Address": "123 4th St, Anywhere, AA",
        "ZIP": "94121",
        "FullName": "Monkey Alberto",
        "FooDuration": "1:23:32.123",
        "BarDuration": "1:32:33.123",
        "TotalDuration": "zzsasdfa",
        "Notes": "I am the very model of a modern major general",
    }
    expected_row = {
        "Timestamp": "2011-04-01T11:00:00-07:00",
        "Address": "123 4th St, Anywhere, AA",
        "ZIP": "94121",
        "FullName": "MONKEY ALBERTO",
        "FooDuration": 5012.123,
        "BarDuration": 5553.123,
        "TotalDuration": 10565.246,
        "Notes": "I am the very model of a modern major general",
    }
    normalized_row = normalize.normalize_row(input_row)
    assert normalized_row == expected_row
    assert (
        normalized_row["TotalDuration"]
        == normalized_row["FooDuration"] + normalized_row["BarDuration"]
    )


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        # Standard time
        ("1/1/11 12:00:00 AM", "2011-01-01T00:00:00-08:00"),
        # Daylight savings time
        ("6/1/11 12:00:00 AM", "2011-06-01T00:00:00-07:00"),
    ],
)
def test_normalize_timestamp(value, expected):
    assert normalize.normalize_timestamp(value) == expected


@pytest.mark.parametrize(
    ["value", "expected", "exception_types"],
    [
        ("12345", "12345", ()),
        ("5", "00005", ()),
        ("zip", None, (ValueError,)),
        ("123456", None, (ValueError,)),
    ],
)
def test_normalize_zip(value, expected, exception_types):
    if exception_types:
        with pytest.raises(exception_types):
            normalize.normalize_zip(value)
    else:
        normalized = normalize.normalize_zip(value)


@pytest.mark.parametrize(
    ["value", "expected", "exception_types"],
    [
        # Valid input
        ("01:02:03.04", 3723.04, ()),
        # Invalid input: missing seconds
        ("01:02", None, (ValueError,)),
        # Invalid input: minutes >= 60
        ("01:60:00", None, (ValueError,)),
        # Invalid input: negative seconds
        ("01:00:-01", None, (ValueError,)),
        # Invalid input: seconds >= 60
        ("01:00:60", None, (ValueError,)),
    ],
)
def test_normalize_duration(value, expected, exception_types):
    if exception_types:
        with pytest.raises(exception_types):
            normalize.normalize_duration(value)
    else:
        normalized = normalize.normalize_duration(value)


def test_open_lenient(tmp_path):
    """Read a file descriptor with bad UTF-8 from the example."""
    bad_file = tmp_path.joinpath("bad.csv")
    with bad_file.open("wb") as fp:
        fp.write(
            b"This is some Unicode right h\xffxxx \xc3\xbc \xc2\xa1! \xf0\x9f\x98\x80"
        )
    with normalize.open_lenient(bad_file) as fp:
        normalized = fp.read()
    assert normalized == "This is some Unicode right h�xxx ü ¡! 😀"
