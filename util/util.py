import os

import pypdf
from pypdf import PdfReader, PdfWriter

class PDFEditor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.reader = PdfReader(file_path)
        self.writer = PdfWriter()

    def add_page(self, page_number: int):
        if page_number < 0 or page_number >= len(self.reader.pages):
            raise IndexError("Page number out of range")
        self.writer.add_page(self.reader.pages[page_number])

    def remove_after(self, page_number: int):
        if page_number < 0 or page_number >= len(self.reader.pages):
            raise IndexError("Page number out of range")
        for i in range(len(self.reader.pages)-1, page_number + 1, -1):
            self.reader.remove_page(self.reader.pages[i])

    def save(self, output_path: str):
        for page in self.reader.pages:
            self.writer.add_page(page)
        with open(output_path, 'wb') as out_file:
            self.writer.write(out_file)

# Example usage
cd = os.getcwd()
# Download from /Archive2/69/W1ER169/sources/W1ER169-I1ER1069/
editor = PDFEditor('I1ER1069.pdf')


editor.remove_after(3)  # Remove the second page
editor.save('Typical_BdrcPdf.pdf')