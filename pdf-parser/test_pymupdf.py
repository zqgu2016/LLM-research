import pymupdf4llm
import pathlib

md_text = pymupdf4llm.to_markdown("/Users/evilkylin/Downloads/2410.09871v1.pdf")
pathlib.Path("2410.09871v1-pymupdf.md").write_bytes(md_text.encode())