"""Main module."""
import PyPDF2
import os
import tempfile
from uuid import uuid4
from PIL import Image
from pdf2image import convert_from_path
from pytesseract import image_to_string, TesseractError, image_to_osd, Output
import base64


class ImageProcessor:
    def __init__(self, language="eng"):
        self.set_language(language)
        self.TEMP_PATH = tempfile.gettempdir()
        self.PREVIEWFILE = ""
        self.PAGE_COUNT = 0

    def set_language(self, language):
        self.LANGUAGE = language

    def open_pdf(self, filename):
        try:
            pdfFileObject = open(filename, "rb")
            pdf_reader = PyPDF2.PdfFileReader(pdfFileObject, strict=False)
            self.PAGE_COUNT = pdf_reader.numPages
            return pdf_reader
        except PyPDF2.utils.PdfReadError:
            print("PDF not fully written - no EOF Marker")
            return None

    def pdf_valid(self, filename):
        if self.open_pdf(filename) is None:
            return False
        else:
            return True

    def pdf_page_to_image(self, path, page_num=0):
        pages = convert_from_path(path, 250)
        if page_num == 0:
            tempfile = f"{self.TEMP_PATH}/preview.png"
            self.PREVIEWFILE = tempfile
        else:
            tempfile = f"{self.TEMP_PATH}/{uuid4()}.png"
        pages[page_num].save(tempfile, "PNG")
        return tempfile

    def pdf_to_pngs(self, path):
        self.open_pdf(path)  # get page count
        filename, ext = os.path.splitext(path)
        pages = convert_from_path(path, 250)
        p = 0
        while p < self.PAGE_COUNT:
            print(p)
            pages[p].save(f"{filename}-page{p+1}", "PNG")
            p += 1
        return 0

    def extract_text_from_pdf(self, filename):
        pdfReader = self.open_pdf(filename)
        text = ""
        for i in range(self.PAGE_COUNT):
            text += f"\n\n***PAGE {i+1} of {self.PAGE_COUNT}*** \n\n"
            page = pdfReader.getPage(i)
            embedded_text = page.extractText()
            # if embedded PDF text is minimal or does not exist,
            # run OCR the images extracted from the PDF
            if len(embedded_text) >= 100:
                text += embedded_text
            else:
                extracted_image = self.pdf_page_to_image(filename, i)
                text += self.extract_text_from_image(extracted_image)
                if extracted_image != f"{self.TEMP_PATH}/preview.png":
                    os.remove(extracted_image)
        return text

    def extract_text_from_image(self, filename, autorotate=False):
        try:
            img = Image.open(filename)
            text = image_to_string(img, lang=self.LANGUAGE)
            rot_data = image_to_osd(img, output_type=Output.DICT)
            if autorotate:
                degrees_to_rotate = rot_data["orientation"]
                # rotate if text is extracted with reasonable confidence
                if degrees_to_rotate != 0 and rot_data["orientation_conf"] > 2:
                    self.rotate_image(filename, degrees_to_rotate)
                    # need to re-run the OCR after rotating
                    img = Image.open(filename)
                    text = image_to_string(img, lang=self.LANGUAGE)
                    print(f"Rotated image {degrees_to_rotate} degrees")

        except TesseractError as e:
            text = "\nCheck Tesseract OCR Configuration\n"
            text += e.message
        return text

    def encode_image(self, filename, datatype):
        encoded = base64.b64encode(open(filename, "rb").read())
        img = f"data:{datatype};base64,{encoded.decode()}"
        return img

    def rotate_image(self, filename, degrees_counterclockwise):
        im = Image.open(filename)
        angle = degrees_counterclockwise
        out = im.rotate(angle, expand=True)
        # overwrite the file
        out.save(filename)
