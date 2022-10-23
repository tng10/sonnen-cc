import math
from typing import Dict

from model_objects import Product, ProductQuantity, SpecialOfferType, Discount


class ShoppingCartItem:
    def __init__(self, product: Product, quantity: float = 1.0):
        self.product = product
        self.quantity = quantity

    def __add__(self, other: object) -> "ShoppingCartItem":

        if not hasattr(other, "product") or self.product != other.product or not isinstance(other.quantity, (int, float)):  # type: ignore
            raise Exception(f"Cannot calculate with this object: {other}")

        return ShoppingCartItem(self.product, self.quantity + other.quantity)  # type: ignore


class NewShoppingCart:
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


class ShoppingCart:
    def __init__(self):
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        return self._items

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] = (
                self._product_quantities[product] + quantity
            )
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt, offers, catalog):
        for p in self._product_quantities.keys():
            quantity = self._product_quantities[p]
            if p in offers.keys():
                offer = offers[p]
                unit_price = catalog.unit_price(p)
                quantity_as_int = int(quantity)
                discount = None
                x = 1
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                    x = 3

                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    x = 2
                    if quantity_as_int >= 2:
                        total = (
                            offer.argument * (quantity_as_int / x)
                            + quantity_as_int % 2 * unit_price
                        )
                        discount_n = unit_price * quantity - total
                        discount = Discount(
                            p, "2 for " + str(offer.argument), -discount_n
                        )

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                    x = 5

                number_of_x = math.floor(quantity_as_int / x)
                if (
                    offer.offer_type == SpecialOfferType.THREE_FOR_TWO
                    and quantity_as_int > 2
                ):
                    discount_amount = quantity * unit_price - (
                        (number_of_x * 2 * unit_price)
                        + quantity_as_int % 3 * unit_price
                    )
                    discount = Discount(p, "3 for 2", -discount_amount)

                if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount = Discount(
                        p,
                        str(offer.argument) + "% off",
                        -quantity * unit_price * offer.argument / 100.0,
                    )

                if (
                    offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT
                    and quantity_as_int >= 5
                ):
                    discount_total = unit_price * quantity - (
                        offer.argument * number_of_x + quantity_as_int % 5 * unit_price
                    )
                    discount = Discount(
                        p, str(x) + " for " + str(offer.argument), -discount_total
                    )

                if discount:
                    receipt.add_discount(discount)
