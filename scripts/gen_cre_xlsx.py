import openpyxl, random
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
rng=random.Random(777)
wb=openpyxl.Workbook()
bold=Font(bold=True); money='#,##0;(#,##0)'; money2='#,##0.00;(#,##0.00)'; pct='0.00%'
hdrfill=PatternFill('solid',fgColor='D9E2EC')
# --- Assumptions
a=wb.active; a.title='Assumptions'
rows=[('Property','Example Gardens Apartments (fictitious)'),('Address','123 Example St, Anytown, NY 12345'),('Units',48),
('Purchase Price',6850000),('Loan Amount',4452500),('Interest Rate',0.0625),('Amortization (years)',30),('Loan Term (years)',10),
('Vacancy & Credit Loss',0.06),('Management Fee (% of EGI)',0.04),('Other Income per Unit per Month',62),('Replacement Reserve per Unit',300),('Exit Cap Rate',0.0575)]
a['A1']='Underwriting Assumptions'; a['A1'].font=Font(bold=True,size=13)
for i,(k,v) in enumerate(rows,start=3):
    a.cell(i,1,k).font=bold; a.cell(i,2,v)
a['B6'].number_format=money; a['B7'].number_format=money; a['B8'].number_format=pct; a['B11'].number_format=pct; a['B12'].number_format=pct; a['B15'].number_format=pct
a.column_dimensions['A'].width=34; a.column_dimensions['B'].width=38
# --- Rent Roll
r=wb.create_sheet('Rent Roll')
r['A1']='Rent Roll as of 3/31/2026'; r['A1'].font=Font(bold=True,size=13)
r.merge_cells('A1:H1')
hdr=['Unit','Type','Sq Ft','Tenant','Lease End','Monthly Rent','Annual Rent','Status']
for j,hh in enumerate(hdr,1):
    c=r.cell(3,j,hh); c.font=bold; c.fill=hdrfill
types={'1BR/1BA':(650,1450),'2BR/1BA':(850,1750),'2BR/2BA':(950,1925),'3BR/2BA':(1150,2350),'Studio':(480,1195)}
names=['Jane Sample','John Sample','Alex Example','Casey Example','Pat Placeholder','Sam Specimen','Jordan Dummy','Taylor Testcase']
row=4
for b in 'AB':
    for f in (1,2,3):
        for k in range(1,9):
            typ=rng.choice(list(types)); sf,mkt=types[typ]
            vac=rng.random()<0.08
            rent=0 if vac else mkt-rng.choice([0,25,50,75,100])
            r.cell(row,1,f'{b}-{f}{k:02d}'); r.cell(row,2,typ); r.cell(row,3,sf); r.cell(row,4,'VACANT' if vac else rng.choice(names))
            r.cell(row,5,None if vac else f'{rng.randint(1,12):02d}/{rng.choice([28,30,31])}/{rng.choice([2026,2027])}')
            r.cell(row,6,rent).number_format=money; r.cell(row,7,f'=F{row}*12').number_format=money; r.cell(row,8,'Vacant' if vac else 'Current')
            row+=1
last=row-1
r.cell(row,1,'Total').font=bold; r.cell(row,3,f'=SUM(C4:C{last})'); r.cell(row,6,f'=SUM(F4:F{last})').number_format=money; r.cell(row,7,f'=SUM(G4:G{last})').number_format=money
r.cell(row,8,f'=COUNTIF(H4:H{last},"Current")&" occupied / "&COUNTIF(H4:H{last},"Vacant")&" vacant"')
for j,w in enumerate([8,10,8,18,12,13,13,24],1): r.column_dimensions[get_column_letter(j)].width=w
r.freeze_panes='A4'
TOT=row
# --- Operating Statement
o=wb.create_sheet('Operating Statement')
o['A1']='Pro Forma Operating Statement (Year 1)'; o['A1'].font=Font(bold=True,size=13)
lines=[('Gross Potential Rent (in-place, annualized)',f"='Rent Roll'!G{TOT}"),
('Less: Vacancy & Credit Loss','=-B3*Assumptions!B11'),
('Other Income','=Assumptions!B5*Assumptions!B13*12'),
('Effective Gross Income','=SUM(B3:B5)'),
('',None),
('Real Estate Taxes',118400),('Insurance',41250),('Utilities',52780),('Repairs & Maintenance',61940),('Contract Services',23600),('Payroll',98500),
('Management Fee','=B6*Assumptions!B12'),('General & Administrative',14320),('Marketing',9875),('Replacement Reserves','=Assumptions!B5*Assumptions!B14'),
('Total Operating Expenses','=SUM(B8:B17)'),
('Net Operating Income','=B6-B18'),
('Expense Ratio','=B18/B6')]
for i,(k,v) in enumerate(lines,start=3):
    o.cell(i,1,k); 
    if v is not None: o.cell(i,2,v).number_format=money
for rr in (6,18,19): o.cell(rr,1).font=bold; o.cell(rr,2).font=bold
o['B20'].number_format=pct; o.column_dimensions['A'].width=44; o.column_dimensions['B'].width=16
# --- Debt Service
d=wb.create_sheet('Debt Service')
d['A1']='Debt Service & Returns'; d['A1'].font=Font(bold=True,size=13)
dl=[('Loan Amount','=Assumptions!B7'),('Interest Rate','=Assumptions!B8'),('Amortization (months)','=Assumptions!B9*12'),
('Monthly Payment','=-PMT(B4/12,B5,B3)'),('Annual Debt Service','=B6*12'),('Net Operating Income',"='Operating Statement'!B19"),
('DSCR','=B8/B7'),('LTV','=B3/Assumptions!B6'),('Going-in Cap Rate','=B8/Assumptions!B6'),('Debt Yield','=B8/B3'),('Cash Flow After Debt Service','=B8-B7')]
for i,(k,v) in enumerate(dl,start=3):
    d.cell(i,1,k); d.cell(i,2,v)
for rr,f in ((3,money),(4,pct),(6,money2),(7,money2),(8,money),(9,'0.00"x"'),(10,pct),(11,pct),(12,pct),(13,money)): d.cell(rr,2).number_format=f
d.column_dimensions['A'].width=30; d.column_dimensions['B'].width=16
# --- Summary
s=wb.create_sheet('Summary',0)
s['A1']='Underwriting Summary'; s['A1'].font=Font(bold=True,size=14); s.merge_cells('A1:C1')
s['A2']='All values flow from the other sheets via cross-sheet formulas. Fictitious data for parser testing.'; s.merge_cells('A2:C2')
sl=[('Property','=Assumptions!B3'),('Units','=Assumptions!B5'),('Occupied Units',"=COUNTIF('Rent Roll'!H4:H51,\"Current\")"),
('Physical Occupancy','=B6/B5'),('In-Place Monthly Rent',"='Rent Roll'!F52"),('Effective Gross Income',"='Operating Statement'!B6"),
('Total Operating Expenses',"='Operating Statement'!B18"),('Net Operating Income',"='Operating Statement'!B19"),
('Annual Debt Service',"='Debt Service'!B7"),('DSCR',"='Debt Service'!B9"),('LTV',"='Debt Service'!B10"),('Going-in Cap Rate',"='Debt Service'!B11")]
for i,(k,v) in enumerate(sl,start=4):
    s.cell(i,1,k).font=bold; s.cell(i,2,v)
for rr,f in ((7,pct),(8,money),(9,money),(10,money),(11,money),(12,money),(13,'0.00"x"'),(14,pct),(15,pct)): s.cell(rr,2).number_format=f
s.column_dimensions['A'].width=28; s.column_dimensions['B'].width=22
assert TOT==52, TOT
wb.save('out/cre_underwriting_model_raw.xlsx'); print('saved; rent roll total row', TOT)
