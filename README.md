# 📄 PDF Content Extractor (Text + Images)

This Python script allows you to extract **all textual content and images** (excluding watermarks) from a selected PDF file using a simple GUI (`tkinter`). The output is structured page-wise and saved in a JSON file for easy consumption.

---

## ✅ Features

- 📝 Extracts all **text** from each page
- 📷 Extracts all **images**
- ❓ Detects **questions** using smart regex (e.g., `1. What is...`)
- 🗂️ Saves all content in a **JSON structure**, organized page-wise

---

## 📦 Output Structure

The script creates an `extracted_images/` folder that contains:

- Individual images: `pageX_imageY.png`
- A JSON file: `extracted_content.json`

### Sample JSON:
```json
{
  "pages": [
    {
      "page_number": 1,
      "text": "Full text from page 1...",
      "questions": [
        "What is the next figure?",
        "How many apples are there?"
      ],
      "images": [
        "extracted_images/page1_image2.png",
        "extracted_images/page1_image3.png"
      ]
    },
    ...
  ]
}

