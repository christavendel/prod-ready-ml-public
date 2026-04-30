from unittest import mock

# Uncomment this
from app import Item, app, items, update_items
from fastapi.testclient import TestClient


# Test the program logic
def test_update_items():
    item = Item(name="candy", description="nice chocolates", price=5, tax=1)

    res = update_items(item)
    assert res["price_with_tax"] == 6


# Test the endpoints
client = TestClient(app)


def test_get_item_endoint():
    items["foo"] = {"my": "fake item"}

    res = client.get("/item/foo")
    assert res.status_code == 200
    assert res.json() == {"my": "fake item"}


# Test a mocked-up endpoint
def test_get_item_mocked():
    with mock.patch("app.get_item", return_value={"my": "faked fake item"}):
        res = client.get("/item/foo")
        assert res.status_code == 200
        assert res.json() == {"my": "faked fake item"}
