import sys, openpyxl
for p in sys.argv[1:]:
    try:
        wb = openpyxl.load_workbook(p)  # formulas as text
    except Exception as e:
        print(p, 'LOAD FAIL', e); continue
    print('=====', p, 'sheets:', wb.sheetnames)
    for ws in wb.worksheets:
        hidden_rows = [r for r,d in ws.row_dimensions.items() if d.hidden]
        hidden_cols = [c for c,d in ws.column_dimensions.items() if d.hidden]
        merged = list(ws.merged_cells.ranges)
        formulas = 0; cross = 0; ex = []
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith('='):
                    formulas += 1
                    if '!' in c.value:
                        cross += 1
                        if len(ex) < 3: ex.append((c.coordinate, c.value))
        print(f"  [{ws.title}] state={ws.sheet_state} dims={ws.dimensions} merged={len(merged)} hidden_rows={len(hidden_rows)} hidden_cols={len(hidden_cols)} formulas={formulas} cross_sheet={cross} {ex}")
        if merged[:3]: print('    merged e.g.', [str(m) for m in merged[:3]])
        if hidden_rows[:5]: print('    hidden rows e.g.', hidden_rows[:5])
        if hidden_cols[:5]: print('    hidden cols e.g.', hidden_cols[:5])
