import pandas as pd
from generator import generate_restaurant_receipt
from utils import pdf_to_images, print_log_header, log_success

def main():
    df = pd.read_csv("Datasets/Vertex Restuarant Bills.csv")
    bills = df['bill_id'].unique()
    pdf_files = []           # List to store all generated PDF paths
    print_log_header()       # Print table header once

    for bill in bills:
        order = df[df['bill_id'] == bill]
        output_path = f"./Outputs/{bill}.pdf"
        generate_restaurant_receipt(order_df=order, output_path=output_path)       # Generate the PDF
        pdf_files.append(output_path)                                              # Add the PDF path to the list
        log_success(output_path)                                                   # Log success

    # Convert PDFs to images, all images in one folder
    for pdf_file in pdf_files:
        pdf_to_images(pdf_file, output_base_dir="../Images")
        
if __name__ == "__main__":
    main()

