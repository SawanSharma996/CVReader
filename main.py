import zipfile
import os
import docx
import pdfplumber
import re
import pandas as pd
from io import BytesIO

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file):
    text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def find_email_and_phone(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b\d{3}[-.]?\d{2}\s?\d{2}[-.]?\d{3}\b'  
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    return emails, phones

def process_files_in_zip(zip_path):
    data = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        for file_info in z.infolist():
            if file_info.filename.endswith('.docx') or file_info.filename.endswith('.pdf'):
                with z.open(file_info) as file:
                    if file_info.filename.endswith('.docx'):
                        text = extract_text_from_docx(BytesIO(file.read()))
                    elif file_info.filename.endswith('.pdf'):
                        text = extract_text_from_pdf(BytesIO(file.read()))
                    emails, phones = find_email_and_phone(text)
                    data.append({
                        "Filename": file_info.filename,
                        "Emails": emails,
                        "Phones": phones,
                        
                    })
    return data

def save_to_excel(data):
    df = pd.DataFrame(data)
    df.to_excel('output.xlsx', index=False)


zip_path = '/Users/sawansharma/Desktop/code/CVReader/CVReader/input.zip'
data = process_files_in_zip(zip_path)
save_to_excel(data)

    
        