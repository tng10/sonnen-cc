import pytest

from model_objects import Offer, Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from shopping_cart_item import ShoppingCartItem
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_ten_percent_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)
    offer = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
    teller.add_special_offer(offer)

    cart = ShoppingCart()
    cart_item = ShoppingCartItem(apples, 2.5)
    cart.add_item(cart_item)

    # receipt = teller.checks_out_articles_from(cart)

    # assert 4.975 == pytest.approx(receipt.total_price, 0.01)
    # assert [] == receipt.discounts
    # assert 1 == len(receipt.items)
    # receipt_item = receipt.items[0]
    # assert apples == receipt_item.product
    # assert 1.99 == receipt_item.price
    # assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    # assert 2.5 == receipt_item.quantity
