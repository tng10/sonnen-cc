from catalog import SupermarketCatalog, SupermarketCatalogItem
from typing import Dict, TypedDict
from model_objects import Bundle, Discount, Offer
from receipt import Receipt, ReceiptItem
from shopping_cart import ShoppingCart
from shopping_cart_item import ShoppingCartItem


class CartItemCatalogItem(TypedDict):
    cart_item: ShoppingCartItem
    catalog_item: SupermarketCatalogItem


class Teller:
    def __init__(self, catalog: SupermarketCatalog):
        self._catalog: SupermarketCatalog = catalog
        self._offers: Dict[str, Offer] = {}
        self._bundles: Dict[str, Bundle] = {}

    @property
    def offers(self):
        return self._offers

    @property
    def bundles(self):
        return self._bundles

    @property
    def catalog(self):
        return self._catalog

    def add_special_offer(self, offer: Offer) -> None:
        self._offers.setdefault(offer.product.name, offer)

    def add_special_bundle(self, bundle: Bundle) -> None:
        self._bundles.setdefault("||".join([p.name for p in bundle.products]), bundle)

    def cart_item_catalog_item_set(
        self, items: list[ShoppingCartItem]
    ) -> list[CartItemCatalogItem]:
        return [
            {
                "cart_item": cart_item,
                "catalog_item": self._catalog.find_item_by_product(cart_item.product),  # type: ignore
            }
            for cart_item in items
            if self._catalog.find_item_by_product(cart_item.product)
        ]

    def checks_out_articles_from(self, cart: ShoppingCart) -> Receipt:
        receipt: Receipt = Receipt()

        cart_item_catalog_item_set: list[
            CartItemCatalogItem
        ] = self.cart_item_catalog_item_set(cart.items)

        for element in cart_item_catalog_item_set:
            receipt_item: ReceiptItem = ReceiptItem(
                element["cart_item"], element["catalog_item"]
            )
            receipt.add_item(receipt_item)

        discounts: list[Discount] = cart.calculate_discounts(
            self._offers, self.bundles, self._catalog
        )

        for discount in discounts:
            receipt.add_discount(discount)

        return receipt
