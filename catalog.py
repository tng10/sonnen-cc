from model_objects import Product


class SupermarketCatalogItem:
    def __init__(self, product: Product, price: float) -> None:
        self.product: Product = product
        self.price: float = price


class SupermarketCatalog:
    def __init__(self):
        self._items: list[SupermarketCatalogItem] = list()

    @property
    def items(self) -> list[SupermarketCatalogItem]:
        return self._items

    def add_product(self, product, price):
        raise Exception("cannot be called from a unit test - it accesses the database")

    def unit_price(self, product):
        raise Exception("cannot be called from a unit test - it accesses the database")

    def find_item_by_product(self, product: Product) -> SupermarketCatalogItem | None:
        return next((item for item in self._items if item.product == product), None)
