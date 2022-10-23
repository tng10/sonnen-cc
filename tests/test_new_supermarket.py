from model_objects import Product, ProductUnit
from shopping_cart import NewShoppingCart, ShoppingCartItem
from tests.fake_catalog import FakeCatalog


def test_cart_add_same_item_twice():

    apples = Product("apples", ProductUnit.KILO)

    apples_quantity = 2.5

    cart: NewShoppingCart = NewShoppingCart()
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
