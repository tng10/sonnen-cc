from model_objects import Product


class SupermarketCatalogItem:
    def __init__(self, product: Product, price: float) -> None:
        self.product: Product = product
        self.price: float = price


class SupermarketCatalog:
    def add_product(self, product, price):
        raise Exception("cannot be called from a unit test - it accesses the database")

    def unit_price(self, product):
        raise Exception("cannot be called from a unit test - it accesses the database")
