import fitz  # PyMuPDF
import json
import os
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def extract_pdf_content(pdf_path, output_dir="extracted_images"):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize the PDF document
    doc = fitz.open(pdf_path)
    content = {"pages": []}

    # Regex pattern for parsing questions 
    question_pattern = re.compile(r'^\d+\.\s*(.*?)(?=\n\d+\.|\n\[A\]|\Z)', re.MULTILINE | re.DOTALL)

    for page_num in range(len(doc)):
        page = doc[page_num]
        # Extract text
        text = page.get_text("text").strip()

        # Extract images, skipping the first one (watermark)
        image_list = page.get_images(full=True)
        image_paths = []
        for img_index, img in enumerate(image_list[1:], start=1):  # Skip first image
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"page{page_num + 1}_image{img_index}.{image_ext}"
            image_path = os.path.join(output_dir, image_filename)
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
            image_paths.append(image_path)

        # Parse questions from text
        questions = []
        question_matches = question_pattern.finditer(text)
        for q_match in question_matches:
            question_text = q_match.group(1).strip()
            if question_text:  # Only include non-empty questions
                questions.append(question_text)

        # Append page content to JSON structure
        content["pages"].append({
            "page_number": page_num + 1,
            "text": text,
            "questions": questions,
            "images": image_paths
        })

    doc.close()

    # Save content to JSON file
    json_output_path = os.path.join(output_dir, "extracted_content.json")
    with open(json_output_path, "w", encoding="utf-8") as json_file:
        json.dump(content, json_file, indent=4, ensure_ascii=False)

    return json_output_path

def select_pdf_file():
 
    root = Tk()
    root.withdraw()  
    file_path = askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF files", "*.pdf")]
    )
    return file_path

def process_pdf():
   
    pdf_path = select_pdf_file()
    if not pdf_path:
        print("No file selected. Exiting...")
        return None
    json_path = extract_pdf_content(pdf_path)
    print(f"Content extracted and saved to {json_path}")
    return json_path

process_pdf()