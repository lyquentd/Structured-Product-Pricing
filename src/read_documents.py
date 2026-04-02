"""
Document Reader for QUANT PM folder
Reads PDFs and XLS files and prints a summary of their contents.
"""

import os
import pymupdf  # PyMuPDF
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data", "raw")

# ─────────────────────────────
# PDF reader
# ─────────────────────────────
def summarise_pdf(path: str, max_chars: int = 3000) -> None:
    print(f"\n{'='*70}")
    print(f"📄  PDF: {os.path.basename(path)}")
    print(f"{'='*70}")
    doc = pymupdf.open(path)
    print(f"  Pages : {doc.page_count}")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    lines = [l.strip() for l in full_text.splitlines() if l.strip()]
    preview = "\n".join(lines[:80])          # first ~80 non-empty lines
    if len(preview) > max_chars:
        preview = preview[:max_chars] + "\n  … [truncated]"
    print(preview)
    doc.close()


# ─────────────────────────────
# Excel / XLS reader
# ─────────────────────────────
def summarise_excel(path: str) -> None:
    print(f"\n{'='*70}")
    print(f"📊  Excel: {os.path.basename(path)}")
    print(f"{'='*70}")
    engine = "xlrd" if path.endswith(".xls") else "openpyxl"
    xl = pd.ExcelFile(path, engine=engine)
    print(f"  Sheets : {xl.sheet_names}")
    for sheet in xl.sheet_names:
        df = xl.parse(sheet, header=None)
        print(f"\n  ── Sheet: '{sheet}'  ({df.shape[0]} rows × {df.shape[1]} cols) ──")
        # Print first 10 rows as a quick preview
        print(df.head(10).to_string(index=False, header=False))


# ─────────────────────────────
# Main
# ─────────────────────────────
def main():
    files = sorted(os.listdir(DATA_DIR))
    for fname in files:
        fpath = os.path.join(DATA_DIR, fname)
        if fname.lower().endswith(".pdf"):
            summarise_pdf(fpath)
        elif fname.lower().endswith((".xls", ".xlsx")):
            summarise_excel(fpath)

if __name__ == "__main__":
    main()
