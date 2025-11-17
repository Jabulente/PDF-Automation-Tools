from receiptPDF import RestaurantBill
import os


def customer_information(order_df):
    return {
        'name': order_df['customer_name'].iloc[0],
        'table_number': order_df['table_number'].iloc[0],
        'contact': order_df['customer_phone'].iloc[0]
    }

def generate_restaurant_receipt(order_df, output_path="./Outputs/RestaurantBill.pdf",
                                restaurant_name="VERTEX RESTAURANT",
                                restaurant_address="Plot 123, Mlimani St, Morogoro",
                                restaurant_tel="+255 754 123 456",
                                waiter="Jane Doe",
                                tax_rate=0.18,
                                service_charge_rate=0.05,
                                footer_note="Thank you for dining with us!",
                                order_type="Dine-In"):

    customer_info = customer_information(order_df)
    items = order_df[['description', 'quantity', 'unit_price', 'discount']].to_dict(orient='records')

    pdf = RestaurantBill(
        restaurant_name=restaurant_name,
        restaurant_address=restaurant_address,
        restaurant_tel=restaurant_tel,
        bill_number=order_df['bill_id'].iloc[0],
        waiter=waiter,
        order_type=order_type,
        customer_info=customer_info,
        items=items,
        tax_rate=tax_rate,
        service_charge_rate=service_charge_rate,
        footer_note=footer_note,
        qr_data=f"https://vertex.co/restaurant_bill/{order_df['bill_id'].iloc[0]}"
    )

    pdf.add_page()
    pdf.add_header()
    pdf.add_items()
    pdf.add_totals()
    pdf.add_payment(method="Mobile Money")
    pdf.add_qr_code()
    pdf.add_footer()
    pdf.output(output_path)

    return output_path
    
    

