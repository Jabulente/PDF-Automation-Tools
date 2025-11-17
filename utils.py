from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF

def pdf_to_images(pdf_path: str, output_base_dir: str, dpi: int = 300) -> None:
    pdf_file = Path(pdf_path)
    out_dir = Path(output_base_dir)  # All images go into this single folder
    out_dir.mkdir(parents=True, exist_ok=True)

    with fitz.open(pdf_file) as doc:
        for page_num, page in enumerate(doc, start=1):
            zoom = dpi / 72  # 72 is the default PDF resolution
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            
            # Save image directly in the output folder
            img_path = out_dir / f"{pdf_file.stem}0{page_num}.png"
            pix.save(img_path)
            
            log_success(str(img_path))  # Log each image generated

from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_log_header(total_length=100):
    header = f"| {'Timestamp':^19} | {'Filename':^40} | {'Status':^30} |"
    print(f"{Colors.HEADER}{Colors.BOLD}{header}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'-'*total_length}{Colors.ENDC}")

def log_success(filename: str) -> None:
    total_length = 100
    save_message = f"{Colors.OKGREEN}{Colors.BOLD}✔ Invoice Generated Successfully{Colors.ENDC}"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    display_filename = filename
    if len(display_filename) > 40:
        display_filename = display_filename[:37] + "..."
    
    row = f"| {Colors.OKCYAN}{current_time}{Colors.ENDC} | " \
          f"{Colors.OKBLUE}{Colors.BOLD}{display_filename:<40}{Colors.ENDC} | " \
          f"{save_message:<30} |"
    
    print(row)