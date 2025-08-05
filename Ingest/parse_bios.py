import os
import json
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def parse_bios(input_folder='data/bios', output_file='ingest/parsed_bios.jsonl'):
    bios_data = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            user_id = os.path.splitext(filename)[0]  # e.g. 'u001'
            pdf_path = os.path.join(input_folder, filename)
            bio_text = extract_text_from_pdf(pdf_path)

            record = {
                "user_id": user_id,
                "bio": bio_text,
                "sources": [filename]
            }
            bios_data.append(record)

    # Write all records to JSONL
    with open(output_file, 'w', encoding='utf-8') as f:
        for rec in bios_data:
            f.write(json.dumps(rec) + "\n")

    print(f"[SUCCESS] Parsed {len(bios_data)} bios and saved to {output_file}")

if __name__ == "__main__":
    parse_bios()
