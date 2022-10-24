from catalog import SupermarketCatalog
from typing import Dict, Any
from model_objects import Offer, Product
from receipt import Receipt, ReceiptItem
from shopping_cart import ShoppingCart


class Teller:
    def __init__(self, catalog: SupermarketCatalog):
        self._catalog: SupermarketCatalog = catalog
        self._offers: Dict[str, Offer] = {}

    @property
    def offers(self):
        return self._offers

    @property
    def catalog(self):
        return self._catalog

    def add_special_offer(self, offer: Offer) -> None:
        self._offers.setdefault(offer.product.name, offer)

    def checks_out_articles_from(self, cart: ShoppingCart) -> Receipt:

        receipt: Receipt = Receipt()
        for cart_item in cart.items:

            catalog_item = self._catalog.find_item_by_product(cart_item.product)
            if catalog_item:
                receipt_item: ReceiptItem = ReceiptItem(cart_item, catalog_item.price)
                receipt.add_item(receipt_item)
            else:
                raise ValueError("Not possible to calculate the price")

        cart.handle_offers(receipt, self._offers, self._catalog)

        return receipt
