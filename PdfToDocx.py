import os
import sys
from pdf2image import convert_from_path
from docx import Document
import pytesseract

# Step 1: Get PDF Files from User Input
pdf_paths = input("📌 Write PDF paths (separate multiple paths with space): ").split()
pdf_paths = [path.strip() for path in pdf_paths if os.path.exists(path)]

if not pdf_paths:
    print("❌ No valid file paths provided. Exiting...")
    sys.exit()

for pdf_path in pdf_paths:
    print(f"📌 Processing: {pdf_path}")
    
    print("📌 Converting PDF to images...")
    images = convert_from_path(pdf_path, dpi=300)
    
    print(f"✅ Converted {len(images)} pages to images.")

    # Step 2: Perform OCR on Each Image
    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # Adjust if needed

    if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
        raise FileNotFoundError("Tesseract not found. Check your installation path.")

    ocr_texts = []

    print("📌 Running OCR on images...")
    for i, img in enumerate(images):
        print(f"🔍 Processing page {i+1}/{len(images)}...")
        text = pytesseract.image_to_string(img, lang="eng", config="--psm 6")
        ocr_texts.append(text)
    print("✅ OCR completed.")

    # Step 3: Save Extracted Text to a DOCX File
    docx_path = os.path.join(os.path.expanduser("~/Downloads"), os.path.splitext(os.path.basename(pdf_path))[0] + ".docx")
    doc = Document()

    for text in ocr_texts:
        doc.add_paragraph(text)

    doc.save(docx_path)

    print(f"🎉 Conversion complete! Saved as: {docx_path}")

