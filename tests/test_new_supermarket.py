from model_objects import Offer, Product, ProductUnit, SpecialOfferType
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
