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
from tests.fake_catalog import FakeCatalog


def test_cart_add_same_item_twice():

    apples = Product("apples", ProductUnit.KILO)

    apples_quantity = 2.5

    cart: ShoppingCart = ShoppingCart()
    item: ShoppingCartItem = ShoppingCartItem(apples, apples_quantity)

    cart.add_item(item)
    cart.add_item(item)

    assert len(cart.items) == 1
    assert cart.items[0].product == item.product
    assert cart.items[0].quantity == apples_quantity * 2


def test_catalog_add_same_item_twice():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)

    toothbrush_price = 0.99
    catalog.add_product(toothbrush, toothbrush_price)

    toothbrush_new_price = 1.99
    catalog.add_product(toothbrush, toothbrush_new_price)

    assert len(catalog.items) == 1
    assert catalog.items[0].price == toothbrush_new_price


def test_catalog_add_differnt_items():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)

    toothbrush_price = 0.99
    catalog.add_product(toothbrush, toothbrush_price)

    apples_price = 1.99
    catalog.add_product(apples, apples_price)

    assert len(catalog.items) == 2

    catalog_toothbrush_item = catalog.find_item_by_product(toothbrush)

    assert catalog_toothbrush_item is not None
    assert catalog_toothbrush_item.product == toothbrush
    assert catalog_toothbrush_item.price == toothbrush_price

    catalog_apples_item = catalog.find_item_by_product(apples)

    assert catalog_apples_item is not None
    assert catalog_apples_item.product == apples
    assert catalog_apples_item.price == apples_price


def test_teller_add_same_special_offer_twice():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)

    toothbrush_price = 0.99
    catalog.add_product(toothbrush, toothbrush_price)

    offer = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    teller = Teller(catalog)
    teller.add_special_offer(offer)
    teller.add_special_offer(offer)

    assert len(teller.offers) == 1


def test_teller_add_different_special_offers():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)

    toothbrush_price = 0.99
    catalog.add_product(toothbrush, toothbrush_price)

    apples_price = 1.99
    catalog.add_product(apples, apples_price)

    toothbrush_offer = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
    apples_offer = Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)

    teller = Teller(catalog)
    teller.add_special_offer(toothbrush_offer)
    teller.add_special_offer(apples_offer)

    assert len(teller.offers) == 2


def test_teller_add_one_bundle():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    toothpaste = Product("toothpaste", ProductUnit.EACH)

    toothbrush_price = 0.99
    catalog.add_product(toothbrush, toothbrush_price)

    toothpaste_price = 1.79
    catalog.add_product(toothpaste, toothpaste_price)

    toothbrush_and_toothpaste_bundle = Bundle(
        BundleOfferType.TEN_PERCENT_DISCOUNT, [toothbrush, toothpaste]
    )

    teller = Teller(catalog)
    teller.add_special_bundle(toothbrush_and_toothpaste_bundle)

    assert len(teller.bundles) == 1


def test_teller_add_same_bundle_twice():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    toothpaste = Product("toothpaste", ProductUnit.EACH)

    toothbrush_price = 0.99
    catalog.add_product(toothbrush, toothbrush_price)

    toothpaste_price = 1.79
    catalog.add_product(toothpaste, toothpaste_price)

    toothbrush_and_toothpaste_bundle = Bundle(
        BundleOfferType.TEN_PERCENT_DISCOUNT, [toothbrush, toothpaste]
    )

    teller = Teller(catalog)
    teller.add_special_bundle(toothbrush_and_toothpaste_bundle)
    teller.add_special_bundle(toothbrush_and_toothpaste_bundle)

    assert len(teller.bundles) == 1


def test_ten_percent_discount_on_bundle():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    toothpaste = Product("toothpaste", ProductUnit.EACH)

    toothbrush_price = 0.99
    catalog.add_product(toothbrush, toothbrush_price)

    toothpaste_price = 1.79
    catalog.add_product(toothpaste, toothpaste_price)

    total_price = toothbrush_price + toothpaste_price
    total_price_with_discount = total_price * 0.9

    toothbrush_and_toothpaste_bundle = Bundle(
        BundleOfferType.TEN_PERCENT_DISCOUNT, [toothbrush, toothpaste]
    )

    teller = Teller(catalog)
    teller.add_special_bundle(toothbrush_and_toothpaste_bundle)

    cart = ShoppingCart()
    toothbrush_cart_item = ShoppingCartItem(toothbrush, 1)
    toothpaste_cart_item = ShoppingCartItem(toothpaste, 1)
    cart.add_item(toothbrush_cart_item)
    cart.add_item(toothpaste_cart_item)

    receipt = teller.checks_out_articles_from(cart)

    assert total_price_with_discount == pytest.approx(receipt.total_price, 0.01)

    assert 1 == len(receipt.discounts)
    assert 2 == len(receipt.items)

    assert toothbrush in [item.product for item in receipt.items]
    assert toothpaste in [item.product for item in receipt.items]

    toothbrush_item = next(
        (item for item in receipt.items if item.product == toothbrush), None
    )
    toothpaste_item = next(
        (item for item in receipt.items if item.product == toothpaste), None
    )

    assert toothbrush_item is not None
    assert toothpaste_item is not None

    assert 1 == toothbrush_item.quantity
    assert 1 == toothpaste_item.quantity


def test_ten_percent_discount_on_bundle_and_additional_product():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    toothpaste = Product("toothpaste", ProductUnit.EACH)

    toothbrush_price = 0.99
    catalog.add_product(toothbrush, toothbrush_price)

    toothpaste_price = 1.79
    catalog.add_product(toothpaste, toothpaste_price)

    total_price = toothbrush_price + toothpaste_price
    total_price_with_discount = (total_price * 0.9) + toothpaste_price

    toothbrush_and_toothpaste_bundle = Bundle(
        BundleOfferType.TEN_PERCENT_DISCOUNT, [toothbrush, toothpaste]
    )

    teller = Teller(catalog)
    teller.add_special_bundle(toothbrush_and_toothpaste_bundle)

    cart = ShoppingCart()
    toothbrush_cart_item = ShoppingCartItem(toothbrush, 1)
    toothpaste_cart_item = ShoppingCartItem(toothpaste, 1)
    cart.add_item(toothbrush_cart_item)
    cart.add_item(toothpaste_cart_item)
    cart.add_item(toothpaste_cart_item)

    receipt = teller.checks_out_articles_from(cart)

    assert total_price_with_discount == pytest.approx(receipt.total_price, 0.01)

    assert 1 == len(receipt.discounts)
    assert 2 == len(receipt.items)

    assert toothbrush in [item.product for item in receipt.items]
    assert toothpaste in [item.product for item in receipt.items]

    toothbrush_item = next(
        (item for item in receipt.items if item.product == toothbrush), None
    )
    toothpaste_item = next(
        (item for item in receipt.items if item.product == toothpaste), None
    )

    assert toothbrush_item is not None
    assert toothpaste_item is not None

    assert 1 == toothbrush_item.quantity
    assert 2 == toothpaste_item.quantity


def test_ten_percent_discount_on_bundle_twice():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    toothpaste = Product("toothpaste", ProductUnit.EACH)

    toothbrush_price = 0.99
    catalog.add_product(toothbrush, toothbrush_price)

    toothpaste_price = 1.79
    catalog.add_product(toothpaste, toothpaste_price)

    total_price = toothbrush_price + toothpaste_price
    total_price_with_discount = (total_price * 0.9) * 2

    toothbrush_and_toothpaste_bundle = Bundle(
        BundleOfferType.TEN_PERCENT_DISCOUNT, [toothbrush, toothpaste]
    )

    teller = Teller(catalog)
    teller.add_special_bundle(toothbrush_and_toothpaste_bundle)

    cart = ShoppingCart()
    toothbrush_cart_item = ShoppingCartItem(toothbrush, 1)
    toothpaste_cart_item = ShoppingCartItem(toothpaste, 1)
    cart.add_item(toothbrush_cart_item)
    cart.add_item(toothbrush_cart_item)
    cart.add_item(toothpaste_cart_item)
    cart.add_item(toothpaste_cart_item)

    receipt = teller.checks_out_articles_from(cart)

    assert total_price_with_discount == pytest.approx(receipt.total_price, 0.01)

    assert 2 == len(receipt.discounts)
    assert 2 == len(receipt.items)
    assert 4 == sum([item.quantity for item in receipt.items])

    assert toothbrush in [item.product for item in receipt.items]
    assert toothpaste in [item.product for item in receipt.items]

    toothbrush_item = next(
        (item for item in receipt.items if item.product == toothbrush), None
    )
    toothpaste_item = next(
        (item for item in receipt.items if item.product == toothpaste), None
    )

    assert toothbrush_item is not None
    assert toothpaste_item is not None

    assert 2 == toothbrush_item.quantity
    assert 2 == toothpaste_item.quantity


def test_ten_percent_discount_on_bundle_twice_and_special_offer():
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
    total_price_with_discount = (
        (total_price_tooth_bundle * 0.9) * 2
    ) + apples_price * 0.9

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
