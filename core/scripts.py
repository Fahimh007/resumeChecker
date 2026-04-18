# import pdfplumber
# import spacy

# def extract_text_from_pdf(file_path):
#     with pdfplumber.open(file_path) as pdf:
#         text = ''
#         for page in pdf.pages:
#             text += page.extract_text() + '\n'
#     return text.strip()

# ans = extract_text_from_pdf('./zaddel.pdf')
# print(ans)