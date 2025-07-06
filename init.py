#!/usr/bin/env python3
"""
Estrai da un PDF solo le pagine specificate e crea un nuovo PDF.

USO:
    python estrai_pagine.py input.pdf "1-5,7,12-14" output.pdf
"""

import argparse
from pypdf import PdfReader, PdfWriter   # pip install pypdf

def parse_pages(spec: str) -> list[int]:
    """
    Converte una stringa tipo "1-5,7,12-14" in una lista di indici zero-based.
    Esempio: "1-3,5" -> [0,1,2,4]
    """
    pages: list[int] = []
    for part in spec.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-', 1))
            pages.extend(range(start - 1, end))   # end inclusivo
        else:
            pages.append(int(part) - 1)
    return pages

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estrai pagine da un PDF e genera un nuovo file."
    )
    parser.add_argument("input",  help="PDF di origine")
    parser.add_argument("pages",  help='Pagine da estrarre (es. "1-5,7,12-14")')
    parser.add_argument("output", help="PDF di destinazione")

    args = parser.parse_args()

    reader = PdfReader(args.input)
    writer = PdfWriter()

    indices = parse_pages(args.pages)
    max_page = len(reader.pages)

    for idx in indices:
        if idx < 0 or idx >= max_page:
            raise ValueError(f"Pagina {idx + 1} fuori dal range (1–{max_page})")
        writer.add_page(reader.pages[idx])

    with open(args.output, "wb") as f_out:
        writer.write(f_out)

    print(f"Creato {args.output} con {len(indices)} pagine estratte.")

if __name__ == "__main__":
    main()

