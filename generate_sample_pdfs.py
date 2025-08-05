import os
from fpdf import FPDF

# Create bios folder if not exists
os.makedirs('data/bios', exist_ok=True)

# Sample bios content by user_id
bios = {
    "u001": "Raj Purohith is a Data Scientist at OpenAI specializing in AI and ML.",
    "u002": "Alice Smith is a Software Engineer at Google with 5 years of experience.",
    "u003": "Bob Lee works as a Product Manager at Meta focusing on social media products.",
}

class PDF(FPDF):
    def add_bio(self, text):
        self.add_page()
        self.set_font("Arial", size=12)
        self.multi_cell(0, 10, text)

def generate_pdfs():
    for user_id, bio_text in bios.items():
        pdf = PDF()
        pdf.add_bio(bio_text)
        pdf.output(f"data/bios/{user_id}.pdf")
    print(f"Created {len(bios)} sample PDF bios in data/bios/")

if __name__ == "__main__":
    generate_pdfs()
