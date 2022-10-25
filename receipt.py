from catalog import SupermarketCatalogItem
from model_objects import Discount, Product
from shopping_cart_item import ShoppingCartItem


class ReceiptItem:
    def __init__(
        self, cart_item: ShoppingCartItem, catalog_item: SupermarketCatalogItem
    ):
        self.product: Product = cart_item.product
        self.quantity: float = cart_item.quantity
        self.price: float = catalog_item.price

    @property
    def total_price(self):
        return self.price * self.quantity


class Receipt:
    def __init__(self):
        self._items: list[ReceiptItem] = []
        self._discounts: list[Discount] = []

    @property
    def total_price(self):
        total: float = sum([item.total_price for item in self.items]) + sum(
            [discount.discount_amount for discount in self._discounts]
        )
        return total

    def add_item(self, item: ReceiptItem) -> None:
        self._items.append(item)

    def add_discount(self, discount: Discount) -> None:
        self._discounts.append(discount)

    @property
    def items(self) -> list[ReceiptItem]:
        return self._items[:]

    @property
    def discounts(self) -> list[Discount]:
        return self._discounts[:]
