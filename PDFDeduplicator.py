#program to remove duplicate pages from pdf file
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import ocrmypdf
import pdfplumber

class PDFDeduplication:
    def __init__(self, filepath):
        self.filepath = filepath


    def make_pdf_readable(self):
        try:
            results = ocrmypdf.ocr(self.filepath, self.filepath, deskew=True, skip_text = True)
        except Exception as e:
            print(e)
            pass
        print("OCR Complete")
    
    def get_pages_text_from_pypdf2(self):
        pages = {}
        for i in range(self.pdf_reader.numPages):
            page = self.pdf_reader.getPage(i)
            pages[i] = page.extractText()
        
        return pages

    def get_pages_text_from_pdfplumber(self):
        pages = {}
        with pdfplumber.open(self.filepath) as pdf:
            for i, page in enumerate(pdf.pages):
                pages[i] = page.extract_text()
        return pages

    def get_duplicate_pages(self, pages_text_dictionary):
        temp = []
        results = []
        for key, value in pages_text_dictionary.items():
            if value not in temp:
                results.append(key)
                temp.append(value)
            else:
                pass
        return results

    def remove_duplicate_pages(self, pdf_reader_type = 'pdfplumber'):
        self.pdf_reader = PdfFileReader(open(self.filepath, 'rb'))
        self.pdf_writer = PdfFileWriter()
        self.make_pdf_readable()
        if pdf_reader_type == 'pdfplumber':
            pages_text_dictionary = self.get_pages_text_from_pdfplumber()
        elif pdf_reader_type =='pypdf2':
            pages_text_dictionary = self.get_pages_text_from_pypdf2()
        else:
            raise Exception("No PDF library selected")
        duplicate_pages = self.get_duplicate_pages(pages_text_dictionary)

        for page in duplicate_pages:
            p = self.pdf_reader.getPage(page)
            self.pdf_writer.addPage(p)

        with open('testfile.pdf', 'wb') as f:
            self.pdf_writer.write(f)
        print("Duplicate pages removed")

if __name__ == '__main__':
    filepath = os.path.join(os.getcwd(), "test.pdf")
    deduplicator = PDFDeduplication(filepath)
    deduplicator.remove_duplicate_pages('pdfplumber')