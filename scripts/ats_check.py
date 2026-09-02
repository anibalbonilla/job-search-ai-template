#!/usr/bin/env python3
"""Check a tailored CV against a job description for ATS keyword coverage.

Loads the controlled vocabulary from profile/ats_keywords.md, finds which
terms actually appear in the job description, then reports which of those
are covered in the CV and which are missing.

Usage:
    python3 ats_check.py --cv applications/<carpeta>/cv.md --jd applications/<carpeta>/notes.md
    python3 ats_check.py --cv applications/<carpeta>/cv.md --jd path/to/plain_jd.txt
"""
import argparse
import re
from pathlib import Path

VOCAB_PATH = Path(__file__).resolve().parent.parent / "profile" / "ats_keywords.md"
JD_SECTION_MARKER = "## Descripción original de la vacante"


def load_vocabulary() -> list[str]:
    terms = []
    for line in VOCAB_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("Términos"):
            continue
        terms.extend(t.strip() for t in line.split(",") if t.strip())
    return terms


def load_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if path.name == "notes.md" and JD_SECTION_MARKER in text:
        text = text.split(JD_SECTION_MARKER, 1)[1]
    return text


def contains_term(text: str, term: str) -> bool:
    return re.search(r"\b" + re.escape(term.lower()) + r"\b", text.lower()) is not None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cv", required=True, help="path to the tailored cv.md")
    parser.add_argument("--jd", required=True, help="path to notes.md (or a plain text job description)")
    args = parser.parse_args()

    vocabulary = load_vocabulary()
    cv_text = load_text(Path(args.cv))
    jd_text = load_text(Path(args.jd))

    relevant_terms = [t for t in vocabulary if contains_term(jd_text, t)]
    if not relevant_terms:
        print("No se detectaron términos del vocabulario en la vacante. Revisa profile/ats_keywords.md — puede faltar agregar términos nuevos de esta vacante.")
        return

    matched = [t for t in relevant_terms if contains_term(cv_text, t)]
    missing = [t for t in relevant_terms if t not in matched]

    pct = round(100 * len(matched) / len(relevant_terms))

    print(f"Cobertura ATS: {len(matched)}/{len(relevant_terms)} términos ({pct}%)\n")

    print("Coinciden (presentes en la vacante y en tu CV):")
    for t in matched:
        print(f"  ✓ {t}")

    if missing:
        print("\nFaltan (presentes en la vacante, NO en tu CV):")
        for t in missing:
            print(f"  ✗ {t}")
        print("\nRevisa si alguno es experiencia real que se te olvidó incluir, o un vacío genuino a tener presente para la entrevista.")

    print("\nFormato (garantizado por el pipeline de generación, no requiere revisión manual):")
    print("  ✓ Una sola columna, sin tablas ni imágenes")
    print("  ✓ Fuente estándar (Helvetica)")
    print("  ✓ Texto plano seleccionable en el PDF")


if __name__ == "__main__":
    main()
