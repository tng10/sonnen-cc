from email.mime import base
from enum import Enum
import math


class Product:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit


class ProductQuantity:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4


class Offer:
    def __init__(self, offer_type: SpecialOfferType, product: Product, argument: float):
        self.offer_type: SpecialOfferType = offer_type
        self.product: Product = product
        self.argument: float = argument


class Discount:
    QUANTITY_BASIS = {
        SpecialOfferType.TWO_FOR_AMOUNT: 2,
        SpecialOfferType.FIVE_FOR_AMOUNT: 5,
        SpecialOfferType.THREE_FOR_TWO: 3,
    }

    def __init__(self, product: Product, description: str, discount_amount: float):
        self.product: Product = product
        self.description: str = description
        self.discount_amount: float = discount_amount

    @staticmethod
    def calculate_amount(
        offer: Offer, unit_price: float, quantity: float
    ) -> float | None:
        quantity_as_int = math.floor(quantity)

        base_value = unit_price * quantity

        if offer.offer_type in [
            SpecialOfferType.TWO_FOR_AMOUNT,
            SpecialOfferType.FIVE_FOR_AMOUNT,
            SpecialOfferType.THREE_FOR_TWO,
        ]:
            if quantity_as_int < Discount.QUANTITY_BASIS[offer.offer_type]:
                return None

            # defaults to *_FOR_AMOUNT
            factor_1 = offer.argument
            if offer.offer_type in [SpecialOfferType.THREE_FOR_TWO]:
                factor_1 = unit_price * Discount.QUANTITY_BASIS[offer.offer_type]

            # apply floor operation
            factor_2 = quantity_as_int / Discount.QUANTITY_BASIS[offer.offer_type]
            if offer.offer_type in [
                SpecialOfferType.FIVE_FOR_AMOUNT,
                SpecialOfferType.THREE_FOR_TWO,
            ]:
                factor_2 = math.floor(factor_2)

            total = (
                factor_1 * factor_2
                + quantity_as_int
                % Discount.QUANTITY_BASIS[offer.offer_type]
                * unit_price
            )
            base_value -= total
        elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
            base_value *= offer.argument / 100

        return base_value * -1

    @staticmethod
    def get_description(offer: Offer) -> str | None:
        if offer.offer_type in [
            SpecialOfferType.TWO_FOR_AMOUNT,
            SpecialOfferType.FIVE_FOR_AMOUNT,
        ]:
            return f"{str(Discount.QUANTITY_BASIS[offer.offer_type])} for {str(offer.argument)}"
        elif offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
            return f"{str(Discount.QUANTITY_BASIS[offer.offer_type])} for 2"
        elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
            return f"{str(offer.argument)} % off"
        return None
