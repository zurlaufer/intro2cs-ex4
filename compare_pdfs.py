import re
import argparse
import difflib
from pathlib import Path
from pypdf import PdfReader


def extract_pdf_text(pdf_path: Path) -> list[str]:
    reader = PdfReader(str(pdf_path))
    lines = []
    for page_index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        lines.append(f"===== PAGE {page_index} =====")
        lines.extend(text.splitlines())
    return lines


def normalize_line(line: str) -> str:
    # Reduce formatting noise to make diffs easier to read.
    line = line.replace("\u00a0", " ")
    line = re.sub(r"\s+", " ", line).strip()
    return line


def strip_llm_lines(lines: list[str]) -> list[str]:
    # Ignore lines that explicitly mention LLM/AI tooling.
    pattern = re.compile(
        r"(llm|ai|copilot|chatgpt|claude|gemini|gpt|בינה מלאכותית)",
        re.IGNORECASE,
    )
    return [line for line in lines if not pattern.search(line)]


def extract_submission_section(lines: list[str]) -> list[str]:
    """
    Extract "submission instructions" section.
    Starts at a line containing common submission keywords and continues
    until the next section heading matching "N." (or another page marker).
    """
    heading_pattern = re.compile(r"^\s*\d+\.\s")
    submission_keywords = (
        "נהלי הגשה",
        "הנחיות הגשה",
        "הגשה",
        "submission",
        "submit",
    )

    target_indexes = []
    preferred_indexes = []
    for i, line in enumerate(lines):
        normalized = line.lower()
        if any(keyword in normalized for keyword in submission_keywords):
            target_indexes.append(i)
            if "נהלי הגשה" in normalized or "submission" in normalized:
                preferred_indexes.append(i)

    if not target_indexes:
        return []

    start = preferred_indexes[0] if preferred_indexes else target_indexes[0]
    end = len(lines)

    for i in range(start + 1, len(lines)):
        if i - start > 3 and heading_pattern.match(lines[i]):
            end = i
            break
        if i - start > 20 and lines[i].startswith("===== PAGE"):
            end = i
            break
        if i - start > 220:
            end = i
            break

    return lines[start:end]


def make_diff(a_lines: list[str], b_lines: list[str], a_name: str, b_name: str) -> str:
    diff = difflib.unified_diff(
        a_lines,
        b_lines,
        fromfile=a_name,
        tofile=b_name,
        lineterm="",
    )
    return "\n".join(diff)


def prepare(lines: list[str], ignore_llm: bool) -> list[str]:
    out = [normalize_line(x) for x in lines]
    out = [x for x in out if x]
    if ignore_llm:
        out = strip_llm_lines(out)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare two exercise PDFs (full text or submission section only)."
    )
    parser.add_argument("pdf_a", type=Path, help="First PDF file")
    parser.add_argument("pdf_b", type=Path, help="Second PDF file")
    parser.add_argument(
        "--submission-only",
        action="store_true",
        help="Compare only the submission instructions section",
    )
    parser.add_argument(
        "--ignore-llm-lines",
        action="store_true",
        help="Ignore lines that contain AI/LLM-related keywords",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("pdf_diff_report.txt"),
        help="Output report path",
    )

    args = parser.parse_args()

    a_raw = extract_pdf_text(args.pdf_a)
    b_raw = extract_pdf_text(args.pdf_b)
    a_full = a_raw[:]
    b_full = b_raw[:]

    if args.submission_only:
        a_raw = extract_submission_section(a_raw)
        b_raw = extract_submission_section(b_raw)
        if not a_raw or not b_raw:
            print(
                "Warning: could not isolate submission section in one or both PDFs; "
                "falling back to full-text comparison."
            )
            a_raw = a_full
            b_raw = b_full

    a = prepare(a_raw, ignore_llm=args.ignore_llm_lines)
    b = prepare(b_raw, ignore_llm=args.ignore_llm_lines)

    report = make_diff(a, b, str(args.pdf_a), str(args.pdf_b))

    if not report.strip():
        report = "No differences found."

    args.out.write_text(report, encoding="utf-8")
    print(f"Done. Report written to: {args.out}")


if __name__ == "__main__":
    main()
