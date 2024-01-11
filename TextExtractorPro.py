import os
import logging
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Write text to a text file
def write(text, output_file):
    with open(output_file, "a") as file:
        file.write(text + "\n")

# Extract text from PDF or image files
def extract_text(file_path, file_type, output_file):
    try:
        if file_type == "pdf":
            # Convert PDF to images using pdf2image
            images = convert_from_path(file_path)
            length = len(images)
            logger.info(f"Total {length} pages found.")
        elif file_type == "img":
            images = [Image.open(file_path)]
            length = 1
        else:
            raise ValueError("Invalid File Type")
        # Iterate through images and perform OCR
        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img)
            write(text, output_file)
            logger.info(f"Processing page {i + 1} of {length}")

    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    try:
        pdf_path = input("Enter the path to File: ")
        output_text_file = input("Enter the path to the output text file: ")
        file_type = input("Enter the File Type (pdf or img): ")

        if not os.path.exists(pdf_path):
            logger.error("Invalid file path. Please provide a valid path.")
        else:
            extract_text(pdf_path, file_type, output_text_file)

    except KeyboardInterrupt:
        logger.warning("User interrupted the program.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
