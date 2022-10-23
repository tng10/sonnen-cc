from model_objects import Product, ProductUnit
from shopping_cart import NewShoppingCart, ShoppingCartItem


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
