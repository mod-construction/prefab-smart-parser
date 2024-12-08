import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        all_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            all_text += page_text if page_text else ""
    
    return all_text

pdf_file_path = "assets/Datenblatt_20Jansen_20Paneele.pdf"
pdf_text = extract_text_from_pdf(pdf_file_path)
print(pdf_text)

def split_into_sentences(text):
    # Use regex to split text at sentence-ending punctuation marks followed by a space
    sentence_list = re.split(r'(?<=[.!?]) +', text)
    return sentence_list

sentences_list = split_into_sentences(pdf_text)

for index, sentence in enumerate(sentences_list):
    print(f"Sentence {index}: {sentence}")

def create_overlapping_chunks(sentences, chunk_size=10, overlap_size=3):
    chunks = []
    for i in range(0, len(sentences), chunk_size - overlap_size):
        chunk = sentences[i:i + chunk_size]
        chunks.append(chunk)
        if len(chunk) < chunk_size:
            break
    return chunks

chunks = create_overlapping_chunks(sentences_list)
for index, chunk in enumerate(chunks):
    print(f"Chunk {index}: {chunk}")

