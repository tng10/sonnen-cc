from catalog import SupermarketCatalog
from typing import Dict, Any
from model_objects import Offer
from receipt import Receipt


class NewTeller:
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

    def checks_out_articles_from(self, the_cart):
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self._catalog.unit_price(p)
            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        the_cart.handle_offers(receipt, self._offers, self._catalog)

        return receipt


class Teller:
    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}

    def add_special_offer(self, offer_type, product, argument):
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart):
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(p)
            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        the_cart.handle_offers(receipt, self.offers, self.catalog)

        return receipt
