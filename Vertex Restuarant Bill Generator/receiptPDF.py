from fpdf import FPDF, XPos, YPos
from datetime import datetime
from pathlib import Path
import qrcode

class RestaurantBill(FPDF):
    def __init__(self, restaurant_name="VERTEX RESTAURANT",
                 restaurant_address="123 Main St, Dar es Salaam",
                 restaurant_tel="+255 123 456 789",
                 bill_number=None,
                 waiter="Waiter",
                 order_type="Dine-In",
                 customer_info=None,
                 items=None,
                 tax_rate=0.18,
                 service_charge_rate=0.05,
                 footer_note="Thank you for dining with us!",
                 qr_data=None):

        self.customer_info = customer_info or {}
        self.items = items or []
        self.tax_rate = tax_rate
        self.service_charge_rate = service_charge_rate
        self.footer_note = footer_note
        self.qr_data = qr_data
        self.waiter = waiter
        self.order_type = order_type

        header_h = 40
        customer_h = 0
        items_h = 7 * max(len(self.items), 1)
        totals_h = 30
        payment_h = 15
        qr_h = 50 if qr_data else 0
        footer_h = 20
        page_height = max(200, header_h + customer_h + items_h + totals_h + payment_h + qr_h + footer_h)

        super().__init__(orientation="P", unit="mm", format=(80, page_height))
        self.set_auto_page_break(auto=False)
        self.set_margins(4, 5, 4)

        today = datetime.today()
        self.restaurant_name = restaurant_name
        self.restaurant_address = restaurant_address
        self.restaurant_tel = restaurant_tel
        self.bill_number = bill_number or f"BILL-{today.strftime('%Y%m%d%H%M')}"
        self.date = today.strftime("%d %b %Y  %I:%M %p")

        self.subtotal = 0
        self.tax_amount = 0
        self.service_charge = 0
        self.total_amount = 0

    def _mono(self, size=10, style=""):
        self.set_font("Courier", style, size)

    def separator(self, thickness=0.2):
        self.set_line_width(thickness)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)

    def add_header(self):
        self._mono(12, "B")
        self.cell(0, 6, self.restaurant_name, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self._mono(9)
        self.cell(0, 5, self.restaurant_address, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.cell(0, 5, f"Tel: {self.restaurant_tel}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.separator()

        info_lines = [
            ("Bill #:", self.bill_number),
            ("Date:", self.date),
            ("Table:", self.customer_info.get('table_number', '-')),
            ("Waiter:", self.waiter),
            ("Order Type:", self.order_type)
        ]

        for label, value in info_lines:
            lw = self.get_string_width(label) + 2
            vw = self.w - self.l_margin - self.r_margin - lw
            self.cell(lw, 5, label)
            self.cell(vw, 5, str(value), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.separator()

    def add_items(self):
        self._mono(9, "B")
        table_header = f"{'ITEM':<14}{'QTY':^6}{'PRICE':>6}{'TOTAL':>11}"
        self.cell(0, 5, table_header, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.separator()
        self._mono(9)

        subtotal = 0
        total_discount = 0

        for row in self.items:
            name = row["description"][:14].ljust(14)
            qty = row["quantity"]
            price = float(row["unit_price"])

            discount_percent = row.get("discount", 0)
            discount_val = qty * price * (discount_percent / 100)
            total_discount += discount_val

            total_amt = (qty * price) - discount_val
            subtotal += total_amt

            qty_str = str(qty).center(6)
            price_str = f"{price:,.0f}".rjust(6)
            total_str = f"{total_amt:,.2f}".rjust(11)
            row = f"{name}{qty_str}{price_str}{total_str}"
            self.cell(0, 5, row, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.separator()
        self.subtotal = subtotal
        self.total_discount = total_discount

    def add_totals(self):
        self._mono(9)
        tax_amt = self.subtotal * self.tax_rate
        service = self.subtotal * self.service_charge_rate
        total = self.subtotal + tax_amt + service
        self.tax_amount = tax_amt
        self.service_charge = service
        self.total_amount = total

        totals = [
            ("Subtotal:", f"{self.subtotal:,.2f}"),
            ("Discount:", f"-{self.total_discount:,.2f}") if self.total_discount > 0 else None,
            (f"Tax ({int(self.tax_rate*100)}%):", f"{tax_amt:,.2f}"),
            (f"Service Charge ({int(self.service_charge_rate*100)}%):", f"{service:,.2f}"),
            ("TOTAL:", f"{total:,.2f}")
        ]

        for entry in totals:
            if entry is None:
                continue
            label, value = entry
            lw = self.get_string_width(label) + 2
            vw = self.w - self.l_margin - self.r_margin - lw
            self._mono(9, "B")
            self.cell(lw, 5, label)
            self.cell(vw, 5, value, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.separator()

    def add_payment(self, method="Cash"):
        self._mono(9)

        lines = [
            ("Payment Method:", method),
            ("Amount Paid:", f"{self.total_amount:,.2f}"),
            ("Change:", "0.00")
        ]

        for label, value in lines:
            lw = self.get_string_width(label) + 2
            vw = self.w - self.l_margin - self.r_margin - lw
            self.cell(lw, 5, label)
            self.cell(vw, 5, value, align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.separator()

    def add_footer(self):
        self.set_y(self.h - 20)
        self.separator()
        self._mono(9, "I")
        self.cell(0, 5, self.footer_note, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.cell(0, 5, "Powered by Vertex Systems", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    def add_qr_code(self, qr_width=40):
        if not self.qr_data:
            return

        qr = qrcode.QRCode(box_size=2, border=1)
        qr.add_data(self.qr_data)
        qr.make(fit=True)
        temp = "temp_qr.png"
        qr.make_image().save(temp)
        self.set_y(self.h - 60)
        x_center = (self.w - qr_width) / 2
        self.image(temp, x=x_center, w=qr_width)
        Path(temp).unlink(missing_ok=True)