import math
from typing import Dict, TypedDict

from model_objects import Bundle, Offer, Discount
from catalog import SupermarketCatalog, SupermarketCatalogItem
from receipt import Receipt
from shopping_cart_item import ShoppingCartItem


class OfferCartItemCatalogItem(TypedDict):
    offer: Offer
    cart_item: ShoppingCartItem
    catalog_item: SupermarketCatalogItem | None


class BundleCartItemCatalogItem(TypedDict):
    bundle: Bundle
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

    # def get_bundle_cart_item_catalog_item_set(
    #     self, bundles: Dict[str, Bundle], catalog: SupermarketCatalog
    # ) -> list[BundleCartItemCatalogItem]:
    #     return [
    #         {
    #             "bundle": bundles[],
    #             "cart_item": cart_item,
    #             "catalog_item": catalog.find_item_by_product(cart_item.product),
    #         }
    #         for cart_item in self.items
    #         if cart_item.product.name in bundles
    #     ]

    def find_offer_discount(
        self,
        offer: Offer,
        cart_item: ShoppingCartItem,
        catalog_item: SupermarketCatalogItem | None,
    ) -> Discount | None:

        if not catalog_item:
            return None

        amount: float | None = None
        discount = None

        amount = Discount.calculate_offer_amount(
            offer, catalog_item.price, cart_item.quantity
        )
        description = Discount.get_offer_description(offer)
        if amount and description:
            discount = Discount([offer.product], description, amount)

        return discount

    def find_bundle_discount(
        self,
        bundle: Bundle,
        cart_items: list[ShoppingCartItem],
        catalog_items: list[SupermarketCatalogItem],
    ) -> Discount | None:

        amount: float | None = None
        discount = None

        base_price = sum([catalog_item.price for catalog_item in catalog_items])
        amount = Discount.calculate_bundle_amount(bundle, base_price)

        description = Discount.get_bundle_description(bundle)
        if amount and description:
            discount = Discount(bundle.products, description, amount)

        return discount

    def calculate_discounts(
        self,
        offers: Dict[str, Offer],
        bundles: Dict[str, Bundle],
        catalog: SupermarketCatalog,
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

            discount = self.find_offer_discount(offer, cart_item, catalog_item)
            if discount is not None:
                discounts.append(discount)

        for bundle_name, bundle in bundles.items():

            filtered_cart_items: list[ShoppingCartItem] = [
                cart_item
                for cart_item in self.items
                if cart_item.product in bundle.products
            ]

            cart_products_set = set(
                [cart_item.product for cart_item in filtered_cart_items]
            )
            bundle_products_set = set(bundle.products)

            catalog_set = set()
            for product in bundle.products:
                catalog_item: SupermarketCatalogItem | None = catalog.find_item_by_product(product)  # type: ignore
                if catalog_item:
                    catalog_set.add(catalog_item)

            catalog_product_set = set(
                [catalog_item.product for catalog_item in catalog_set if catalog_item]
            )

            if cart_products_set == bundle_products_set == catalog_product_set:
                min_quantity = math.floor(
                    min([cart_item.quantity for cart_item in filtered_cart_items])
                )
                min_quantity_in_all = all(
                    [
                        cart_item.quantity >= min_quantity
                        for cart_item in filtered_cart_items
                    ]
                )

                if min_quantity > 0 and min_quantity_in_all:
                    for i in range(0, min_quantity):
                        discount = self.find_bundle_discount(
                            bundle,
                            list(filtered_cart_items),
                            list(catalog_set),
                        )
                        if discount:
                            discounts.append(discount)

        return discounts
