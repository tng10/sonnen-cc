from catalog import SupermarketCatalog, SupermarketCatalogItem
from model_objects import Product


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        super()
        self._items: list[SupermarketCatalogItem] = list()

    def add_product(self, product: Product, price: float) -> None:
        item: SupermarketCatalogItem | None = self.find_item_by_product(product)
        if item:
            self._items[self._items.index(item)].price = price
        else:
            self._items.append(SupermarketCatalogItem(product, price))

    def unit_price(self, product: Product) -> float | None:
        item: SupermarketCatalogItem | None = self.find_item_by_product(product)
        return item.price if item else None
