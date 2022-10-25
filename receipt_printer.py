from receipt import Receipt
from abc import ABC, abstractmethod


class ReceiptPrinterStrategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def output(self, receipt: Receipt) -> str:
        pass


class Context:
    def __init__(self, strategy: ReceiptPrinterStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> ReceiptPrinterStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ReceiptPrinterStrategy) -> None:
        self._strategy = strategy

    def output(self, receipt: Receipt) -> str:
        return self._strategy.output(receipt)
