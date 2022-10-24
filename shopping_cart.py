import math
from typing import Dict

from model_objects import Offer, SpecialOfferType, Discount
from catalog import SupermarketCatalog, SupermarketCatalogItem
from receipt import Receipt
from shopping_cart_item import ShoppingCartItem


class ShoppingCart:
    def __init__(self):
        self._items: list[ShoppingCartItem] = []

    @property
    def items(self):
        group: Dict[str, list[ShoppingCartItem]] = {}
        for item in self._items:
            group.setdefault(item.product.name, []).append(item)

        computed_items: list[ShoppingCartItem] = []
        for _, items in group.items():
            if not items:
                continue
            initial = ShoppingCartItem(items[0].product, 0)
            for item in items:
                initial += item
            computed_items.append(initial)
        return computed_items

    def add_item(self, item: ShoppingCartItem) -> None:
        self._items.append(item)

    def find_discount(
        self,
        offer: Offer,
        cart_item: ShoppingCartItem,
        catalog_item: SupermarketCatalogItem | None,
    ) -> Discount | None:

        if not catalog_item:
            return None

        quantity = cart_item.quantity
        quantity_as_int = int(quantity)
        unit_price = catalog_item.price
        discount = None
        x: int = 1

        if offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
            x = 2
            if quantity_as_int >= 2:
                total = (
                    offer.argument * (quantity_as_int / x)
                    + quantity_as_int % 2 * unit_price
                )
                discount_n = unit_price * quantity - total
                discount = Discount(
                    offer.product, "2 for " + str(offer.argument), -discount_n
                )
        elif offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
            x = 3
            number_of_x: int = math.floor(quantity_as_int / x)
            discount_amount = quantity * unit_price - (
                (number_of_x * 2 * unit_price) + quantity_as_int % 3 * unit_price
            )
            discount = Discount(offer.product, "3 for 2", -discount_amount)
        elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
            discount = Discount(
                offer.product,
                str(offer.argument) + "% off",
                -quantity * unit_price * offer.argument / 100.0,
            )
        elif (
            offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT
            and quantity_as_int >= 5
        ):
            x = 5
            number_of_x = math.floor(quantity_as_int / x)
            discount_total = unit_price * quantity - (
                offer.argument * number_of_x + quantity_as_int % 5 * unit_price
            )
            discount = Discount(
                offer.product, str(x) + " for " + str(offer.argument), -discount_total
            )

        return discount

    def handle_offers(
        self, receipt: Receipt, offers: Dict[str, Offer], catalog: SupermarketCatalog
    ) -> None:
        for cart_item in self._items:
            offer = offers.get(cart_item.product.name)
            if offer:
                catalog_item = catalog.find_item_by_product(cart_item.product)
                discount = self.find_discount(offer, cart_item, catalog_item)
                if discount:
                    receipt.add_discount(discount)
