from locale import currency
from receipt import Receipt
from receipt_printer import ReceiptPrinterStrategy
from jinja2 import Environment, FileSystemLoader


environment = Environment(loader=FileSystemLoader("templates/"))
receipt_html_template = environment.get_template("receipt.html")
environment.filters["my_filter"] = lambda i: i * 100


class HtmlReceiptPrinter(ReceiptPrinterStrategy):
    def output(self, receipt: Receipt) -> str:

        content: str = receipt_html_template.render(
            items=receipt.items,
            discounts=receipt.discounts,
            total=receipt.total_price,
        )

        return content
