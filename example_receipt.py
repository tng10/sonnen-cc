import pytest
from model_objects import (
    Bundle,
    BundleOfferType,
    Offer,
    Product,
    ProductUnit,
    SpecialOfferType,
)
from shopping_cart import ShoppingCart, ShoppingCartItem
from teller import Teller
from receipt_printer import Context
from receipt_printer_text import TextReceiptPrinter
from receipt_printer_html import HtmlReceiptPrinter
from tests.fake_catalog import FakeCatalog


catalog = FakeCatalog()
toothbrush = Product("toothbrush", ProductUnit.EACH)
toothpaste = Product("toothpaste", ProductUnit.EACH)
apples = Product("apples", ProductUnit.KILO)

toothbrush_price = 0.99
catalog.add_product(toothbrush, toothbrush_price)

toothpaste_price = 1.79
catalog.add_product(toothpaste, toothpaste_price)

apples_price = 1.99
catalog.add_product(apples, apples_price)

total_price_tooth_bundle = toothbrush_price + toothpaste_price
total_price = total_price_tooth_bundle + apples_price
total_price_with_discount = ((total_price_tooth_bundle * 0.9) * 2) + apples_price * 0.9

toothbrush_and_toothpaste_bundle = Bundle(
    BundleOfferType.TEN_PERCENT_DISCOUNT, [toothbrush, toothpaste]
)
apples_offer = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)

teller = Teller(catalog)
teller.add_special_bundle(toothbrush_and_toothpaste_bundle)
teller.add_special_offer(apples_offer)

cart = ShoppingCart()
toothbrush_cart_item = ShoppingCartItem(toothbrush, 1)
toothpaste_cart_item = ShoppingCartItem(toothpaste, 1)
apples_cart_item = ShoppingCartItem(apples, 1)
cart.add_item(toothbrush_cart_item)
cart.add_item(toothbrush_cart_item)
cart.add_item(toothpaste_cart_item)
cart.add_item(toothpaste_cart_item)
cart.add_item(apples_cart_item)

receipt = teller.checks_out_articles_from(cart)

assert total_price_with_discount == pytest.approx(receipt.total_price, 0.01)

assert 3 == len(receipt.discounts)
assert 3 == len(receipt.items)
assert 5 == sum([item.quantity for item in receipt.items])

assert toothbrush in [item.product for item in receipt.items]
assert toothpaste in [item.product for item in receipt.items]
assert apples in [item.product for item in receipt.items]

toothbrush_item = next(
    (item for item in receipt.items if item.product == toothbrush), None
)
toothpaste_item = next(
    (item for item in receipt.items if item.product == toothpaste), None
)
apples_item = next((item for item in receipt.items if item.product == apples), None)

assert toothbrush_item is not None
assert toothpaste_item is not None
assert apples_item is not None

assert 2 == toothbrush_item.quantity
assert 2 == toothpaste_item.quantity
assert 1 == apples_item.quantity


# text strategy
context = Context(TextReceiptPrinter())
output1: str = context.output(receipt)
print(output1)

# html strategy
context.strategy = HtmlReceiptPrinter()
output2: str = context.output(receipt)
print(output2)
