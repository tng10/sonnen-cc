from typing import Dict, TypedDict

from model_objects import Offer, Discount
from catalog import SupermarketCatalog, SupermarketCatalogItem
from receipt import Receipt
from shopping_cart_item import ShoppingCartItem


class OfferCartItemCatalogItem(TypedDict):
    offer: Offer
    cart_item: ShoppingCartItem
    catalog_item: SupermarketCatalogItem | None


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

    def get_offer_cart_item_catalog_item_set(
        self, offers: Dict[str, Offer], catalog: SupermarketCatalog
    ) -> list[OfferCartItemCatalogItem]:
        return [
            {
                "offer": offers[cart_item.product.name],
                "cart_item": cart_item,
                "catalog_item": catalog.find_item_by_product(cart_item.product),
            }
            for cart_item in self.items
            if cart_item.product.name in offers
        ]

    def find_discount(
        self,
        offer: Offer,
        cart_item: ShoppingCartItem,
        catalog_item: SupermarketCatalogItem | None,
    ) -> Discount | None:

        if not catalog_item:
            return None

        amount: float | None = None
        discount = None

        amount = Discount.calculate_amount(
            offer, catalog_item.price, cart_item.quantity
        )
        description = Discount.get_description(offer)
        if amount and description:
            discount = Discount(offer.product, description, amount)

        return discount

    def calculate_discounts(
        self, offers: Dict[str, Offer], catalog: SupermarketCatalog
    ) -> list[Discount]:
        discounts: list[Discount] = []
        offer_cart_item_catalog_item_set: list[
            OfferCartItemCatalogItem
        ] = self.get_offer_cart_item_catalog_item_set(offers, catalog)

        for element in offer_cart_item_catalog_item_set:
            offer, cart_item, catalog_item = (
                element["offer"],
                element["cart_item"],
                element["catalog_item"],
            )

            discount = self.find_discount(offer, cart_item, catalog_item)
            if discount is not None:
                discounts.append(discount)
        return discounts
