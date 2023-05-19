import pytest
from datetime import datetime
from src.properties import Properties
from secrets import API_KEY

# Voy a suponer que la base de datos es estática

@pytest.mark.parametrize(
    "input_value, expected",
    [
        (1, 1),
        (2.1, 2),
        (4.5, 4),
        (20.7, 20),
        (100.9999, 100),
        (999.000001, 999),
    ]
)
def test_page_output(input_value, expected):
    app = Properties(api_key=API_KEY)
    listed_properties = app.list_all_properties(page=input_value)
    current_page = listed_properties["pagination"]["page"]
    assert current_page == expected


@pytest.mark.parametrize(
    "input_page, input_limit, expected",
    [
        (1, 1, 1),
        (3, 2.1, 2),
        (6, 4.9999, 4),
        (10, 5.000001, 5),
        (15, 100, 50),
        (18, 50, 34),
        (18, 25, 25),
        (900, 1, 0),
        (2, 0, "Bad request"),
        (1, -87, "Bad request")
    ]
)
def test_limit_length_output(input_page, input_limit, expected):
    app = Properties(api_key=API_KEY)
    listed_properties = app.list_all_properties(page=input_page, limit=input_limit)
    if "content" in listed_properties.keys():
        output = len(listed_properties["content"])
    elif "error" in listed_properties.keys():
        output = listed_properties["error"]
    else:
        output = listed_properties
    assert output == expected

@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("2023-01-01", True),
        ("2022-12-31", True),
        ("3000-01-01", False),
        ("1500-01-01", True),
    ]
)
def test_update_output(input_value, expected):
    app = Properties(api_key=API_KEY)
    options = app.create_options(updated_after=input_value)
    prop = app.list_all_properties(page=1, limit=1, options=options)["content"]
    if len(prop) == 0:
        return False
    updated_after_dt = datetime.strptime(input_value, "%Y-%m-%d")
    prop_updated_at = datetime.strptime(prop[0]['updated_at'].split("T")[0], "%Y-%m-%d")
    assert (prop_updated_at >= updated_after_dt) == expected
