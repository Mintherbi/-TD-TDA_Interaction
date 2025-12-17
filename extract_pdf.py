import pdfplumber

pdf_path = "Presentation/Propose Review Presentation.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, 1):
        print(f"\n{'='*60}")
        print(f"PAGE {i}")
        print(f"{'='*60}")
        text = page.extract_text()
        if text:
            print(text)
        else:
            print("[No text extracted - likely image-only slide]")
