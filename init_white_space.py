#!/usr/bin/env python3
import argparse
from pypdf import PdfReader, PdfWriter   # pip install pypdf


def parse_groups(spec: str) -> list[list[int]]:
    """
    Converte una stringa tipo "1-5,7,12-14" in una lista di gruppi di indici 0-based.
    Es.: "1-3,5" -> [[0,1,2], [4]]
    """
    groups: list[list[int]] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = map(int, part.split("-", 1))
            groups.append([i - 1 for i in range(start, end + 1)])  # end inclusivo
        else:
            groups.append([int(part) - 1])
    return groups


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estrai gruppi di pagine e separali con una pagina bianca."
    )
    parser.add_argument("input", help="PDF di origine")
    parser.add_argument("pages", help='Gruppi di pagine (es. "1-5,7,12-14")')
    parser.add_argument("output", help="PDF di destinazione")

    args = parser.parse_args()

    reader = PdfReader(args.input)
    writer = PdfWriter()

    groups = parse_groups(args.pages)
    max_page = len(reader.pages)

    for g_idx, group in enumerate(groups):
        # Aggiungi le pagine del gruppo
        for idx in group:
            if idx < 0 or idx >= max_page:
                raise ValueError(f"Pagina {idx + 1} fuori dal range (1–{max_page})")
            writer.add_page(reader.pages[idx])

        # Se non è l'ultimo gruppo, inserisci una pagina bianca di pari dimensioni
        if g_idx != len(groups) - 1:
            box = reader.pages[group[0]].mediabox  # usa il formato del primo del gruppo
            writer.add_blank_page(width=float(box.width), height=float(box.height))

    with open(args.output, "wb") as f_out:
        writer.write(f_out)

    tot_pag = sum(len(g) for g in groups)
    print(
        f"Creato {args.output} con {tot_pag} pagine + {len(groups)-1} pagine bianche."
    )


if __name__ == "__main__":
    main()

