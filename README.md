# doc-parsing

Side-by-side comparison of document parsers on the hard cases in lender document intake.
Candidates: Docling, Azure Document Intelligence, LlamaParse, Mistral OCR, MarkItDown, Unstructured.

This branch contains **only the test dataset**. No parsers are installed or run yet.

## Layout

```
data/
  manifest.csv      one row per file: source, license, synthetic?, pages/sheets, what it tests, ground truth
  pdf/              6 PDFs
  xlsx/             3 workbooks
scripts/            generators and fillers used to build the synthetic files (as run; paths are relative to a scratch dir)
```

Every file is under 1 MB. Nothing comes from an employer or client repo. All people, addresses,
account numbers and amounts in the synthetic files are fictitious ("Jane Q Sample", "123 Example St").

## Files and what each one tests

| File | Origin | What it tests |
|---|---|---|
| `pdf/irs_form_1040_2025_sample_filled.pdf` | Official IRS blank form, filled with fake data and flattened | Form layout, checkboxes, SSN comb fields, filled numeric boxes, key-value extraction |
| `pdf/bank_statement_sample.pdf` | Synthetic (ReportLab) | 4-page transaction table with repeated header, running balance, blank debit/credit cells, summary reconciliation, daily-balance table in column pairs |
| `pdf/sec_10k_apple_fy2024_excerpt.pdf` | Apple FY2024 10-K from SEC EDGAR, pp. 23, 29, 47 | Dense financial tables, spanning "Years ended" header, parentheses negatives, `(x)%` change columns, footnote markers `(1)` with footnote text, `$` in separate cells |
| `pdf/scanned_skewed_1040_p1_no_text_layer.pdf` | Page 1 of the filled 1040, rasterized and degraded | Image-only PDF (no text layer), 1.6° skew, noise, low contrast, checkboxes under OCR, handwriting-style marginalia |
| `pdf/rent_roll_operating_statement_sample.pdf` | Synthetic (ReportLab), landscape | Table spanning two pages with repeated header, totals row, status codes, T-12 operating statement with parentheses negatives and per-unit / %-of-EGI columns |
| `pdf/sba_form_413_sample_filled.pdf` | Official SBA Form 413 (02/2025), filled with fake data and flattened | Two-column balance-sheet form with dot leaders, checkboxes, small multi-row tables, 3-column property grid, free-text boxes |
| `xlsx/cre_underwriting_model.xlsx` | Synthetic (openpyxl, recalculated with LibreOffice) | 5 sheets, 22 cross-sheet formulas, PMT, COUNTIF, merged title cells, frozen panes, cached values present |
| `xlsx/ocb_tools_bom_improved.xlsx` | Microsoft OfficeComprehensionBenchmark (`TOOLS_BOM_Improved.xlsx`) | 99 hidden rows, 2 hidden columns, hidden sheet, merged header groups, external-workbook formulas, header not on row 1, a malformed formula stored as text |
| `xlsx/ocb_ofm_facility_cost_template.xlsx` | Microsoft OfficeComprehensionBenchmark (`45b87400-...xlsx`), a Washington State OFM facility cost template | Messy real-world government workbook: instruction block in merged cells, two-row grouped header, data from row 8, totals mid-sheet, hidden lookup sheet, trailing space in a sheet name, 357 formulas incl. cross-sheet refs |

Full details, source URLs, license notes and 7–8 ground-truth values per file (with page or cell
locations) are in `data/manifest.csv`. Ground truth was read directly off each document and
re-checked programmatically against the final files.

## Licenses

- IRS Form 1040 and SBA Form 413: U.S. Government works, public domain (17 U.S.C. § 105). Filled values are synthetic.
- Apple 10-K excerpt: public SEC EDGAR filing (public record, freely accessible). Apple does not attach a license statement to the filing; three pages of 78 are included for testing.
- OfficeComprehensionBenchmark files: CDLA-Permissive-2.0 as published by Microsoft on Hugging Face. The two copies are byte-identical to the originals (renamed). The OFM workbook is also a Washington State public record. The dataset's URL manifest does not identify the original author of `TOOLS_BOM_Improved.xlsx`; it is a hosted reference file covered by the dataset license, and its content is anonymized (`Vendor_1`, `Tool_1`). If you want to be stricter, drop it and use the OFM workbook (which also has merged cells and a hidden sheet) for the merged/hidden case.
- Everything generated here (bank statement, rent roll, CRE model, scan, filled values, scripts): CC0.

## How the synthetic files were made

Scripts in `scripts/` were run from a scratch directory with `src/` (downloaded blanks) and `out/`
subfolders; they are kept as-is for provenance rather than as a reusable pipeline.

- `fill_1040.py`, `fill_sba413.py`: fill AcroForm fields with PyMuPDF, then `Document.bake()` to flatten so values live in the page content stream (parsers that ignore widget annotations still see them).
- `gen_bank.py`, `gen_rentroll.py`: ReportLab, seeded RNG, totals computed and asserted in code.
- `gen_cre_xlsx.py`: openpyxl, then `soffice --headless --convert-to xlsx` so cached formula values exist (openpyxl alone writes formulas with no cached results).
- `make_scan.py`: PyMuPDF raster → PIL noise/skew/blur → JPEG → image-only PDF. Handwriting uses the macOS "Bradley Hand" font rendered to pixels.
- `xfeat.py`: the openpyxl checker used to confirm merged cells, hidden rows/columns, hidden sheets and cross-sheet formulas in every candidate workbook.

## Gaps and caveats

- **No real handwriting.** The marginalia on the scanned page are font-rendered. A page with genuine handwriting (and a redistributable license, no personal data) was not found; this is the weakest case in the set.
- **The scan is synthetic.** It is a degraded render, not a physical scan, so it lacks real scanner artifacts (bleed-through, binding shadow, JPEG from a phone camera). A public-domain real scan with lender-relevant content was not located.
- **No real bank statement.** Banks' published samples carry bank branding and unclear reuse terms, so a synthetic one was used.
- **10-K is a browser render.** Apple files its 10-K as iXBRL HTML; the PDF was produced with headless Chrome from the EDGAR HTML, so fonts and line breaks differ from a native PDF filing. The numbers are the filed numbers.
- **No government workbook with hidden rows/columns.** The hidden-rows case is covered by an OCB file whose upstream author is not named. Several U.S. agency downloads (BLS, FDIC, OMB historical tables) returned HTML or empty responses to scripted requests and were skipped.
- **Form 1040 is the 2025 revision** (the current blank on irs.gov). Field labels differ slightly from 2023/2024 forms (e.g., line 11a/11b split, line 13b).
- **No native-PDF table with merged header cells generated by Word/Excel export**, which is a different renderer path from ReportLab and Chrome. Could be added later.
