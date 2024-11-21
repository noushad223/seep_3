import PyPDF2
from PyPDF2 import PdfReader
from io import BytesIO
from PIL import Image

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_images_from_pdf(pdf_path):
    image_data_list = []
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        page = reader.pages[0]
        count = 0

        for image_file_object in page.images:
            # Convert the image to binary data
            image_data = image_file_object.data
            image_data_list.append(image_data)
            count += 1

    return image_data_list

def load_image_from_binary(binary_data):
    # Create a BytesIO stream from the binary data
    image_stream = BytesIO(binary_data)
    
    # Open the image with Pillow (PIL)
    image = Image.open(image_stream)
    
    # Optionally, display the image
    image.show()

    return image

# pdf_file = "src/Test.pdf"
# image_data_list = extract_images_from_pdf(pdf_file)
# print(extract_text_from_pdf(pdf_file))

# if image_data_list:
#     load_image_from_binary(image_data_list[0])