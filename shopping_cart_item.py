from model_objects import Product


class ShoppingCartItem:
    def __init__(self, product: Product, quantity: float = 1.0):
        self.product = product
        self.quantity = quantity

    def __add__(self, other: object) -> "ShoppingCartItem":

        if not hasattr(other, "product") or self.product != other.product or not isinstance(other.quantity, (int, float)):  # type: ignore
            raise Exception(f"Cannot calculate with this object: {other}")

        return ShoppingCartItem(self.product, self.quantity + other.quantity)  # type: ignore
