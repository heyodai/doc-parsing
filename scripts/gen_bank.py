import random, datetime as dt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

rng = random.Random(20260301)
start = dt.date(2026,3,1); end = dt.date(2026,3,31)
beginning = 4812.37
payees_debit = [("CARD PURCHASE EXAMPLE GROCERY #0421 ANYTOWN NY", 40, 180),
 ("CARD PURCHASE SAMPLE FUEL STATION ANYTOWN NY", 30, 75),
 ("CARD PURCHASE EXAMPLE CAFE ANYTOWN NY", 4, 22),
 ("ONLINE PAYMENT EXAMPLE ELECTRIC UTILITY", 110, 190),
 ("ONLINE PAYMENT SAMPLE WIRELESS CO", 85, 95),
 ("ACH DEBIT EXAMPLE MORTGAGE CO LOAN PMT", 2150, 2150),
 ("ACH DEBIT SAMPLE AUTO FINANCE PMT", 425, 425),
 ("ATM WITHDRAWAL 0001 MAIN ST ANYTOWN NY", 60, 200),
 ("CHECK #1041", 150, 900), ("CHECK #1042", 150, 900), ("CHECK #1043", 150, 900),
 ("CARD PURCHASE EXAMPLE PHARMACY ANYTOWN NY", 12, 60),
 ("ONLINE TRANSFER TO SAVINGS XXXXXX5678", 300, 500),
 ("CARD PURCHASE SAMPLE STREAMING SVC", 15, 16),
 ("ZELLE PAYMENT TO CASEY SAMPLE", 25, 120),
 ("CARD PURCHASE EXAMPLE HARDWARE ANYTOWN NY", 18, 140),
 ("MONTHLY SERVICE FEE", 12, 12)]
payees_credit = [("DIRECT DEPOSIT EXAMPLE SCHOOL DISTRICT PAYROLL", 2894.60, 2894.60),
 ("DIRECT DEPOSIT SAMPLE ENGINEERING INC PAYROLL", 3410.25, 3410.25),
 ("MOBILE CHECK DEPOSIT", 50, 400), ("ZELLE PAYMENT FROM ALEX SAMPLE", 20, 150),
 ("INTEREST PAID", 1.12, 1.12)]
tx=[]
d=start
while d<=end:
    n = rng.choice([1,2,2,3,3,4,5])
    for _ in range(n):
        p=rng.choice(payees_debit[:5]+payees_debit[7:8]+payees_debit[11:12]+payees_debit[13:16])
        amt=round(rng.uniform(p[1],p[2]),2)
        tx.append((d,p[0],-amt))
    d+=dt.timedelta(days=1)
# fixed items
tx.append((dt.date(2026,3,2),payees_debit[5][0],-2150.00))
tx.append((dt.date(2026,3,16),payees_debit[6][0],-425.00))
tx.append((dt.date(2026,3,6),payees_credit[0][0],2894.60)); tx.append((dt.date(2026,3,20),payees_credit[0][0],2894.60))
tx.append((dt.date(2026,3,13),payees_credit[1][0],3410.25)); tx.append((dt.date(2026,3,27),payees_credit[1][0],3410.25))
tx.append((dt.date(2026,3,9),payees_debit[8][0],-350.00)); tx.append((dt.date(2026,3,18),payees_debit[9][0],-725.00)); tx.append((dt.date(2026,3,25),payees_debit[10][0],-180.00))
tx.append((dt.date(2026,3,11),payees_credit[2][0],275.00)); tx.append((dt.date(2026,3,23),payees_credit[3][0],85.00))
tx.append((dt.date(2026,3,5),payees_debit[12][0],-400.00)); tx.append((dt.date(2026,3,19),payees_debit[12][0],-400.00))
tx.append((dt.date(2026,3,31),payees_credit[4][0],1.12)); tx.append((dt.date(2026,3,31),payees_debit[16][0],-12.00))
tx.sort(key=lambda t:(t[0], t[2]<0))
bal=beginning; rows=[]; deps=0; depn=0; wd=0; wdn=0
for d,desc,amt in tx:
    bal=round(bal+amt,2)
    if amt>0: deps+=amt; depn+=1
    else: wd+=-amt; wdn+=1
    rows.append((d.strftime('%m/%d'),desc, f"{-amt:,.2f}" if amt<0 else "", f"{amt:,.2f}" if amt>0 else "", f"{bal:,.2f}"))
deps=round(deps,2); wd=round(wd,2); ending=bal
minbal=min(float(r[4].replace(",","")) for r in rows); print("min balance", minbal); assert minbal>0
assert round(beginning+deps-wd,2)==ending
print(f"beginning={beginning:,.2f} deposits={deps:,.2f} ({depn}) withdrawals={wd:,.2f} ({wdn}) ending={ending:,.2f} ntx={len(rows)}")

ss=getSampleStyleSheet()
h=ParagraphStyle('h',parent=ss['Heading1'],fontSize=16,spaceAfter=2)
small=ParagraphStyle('s',parent=ss['Normal'],fontSize=8,leading=10)
norm=ParagraphStyle('n',parent=ss['Normal'],fontSize=9,leading=11)
def footer(canvas,doc):
    canvas.saveState(); canvas.setFont('Helvetica',7)
    canvas.drawString(0.6*inch,0.45*inch,"Example Bank, N.A.  |  Statement of Account  |  Account XXXXXX1234  |  03/01/2026 - 03/31/2026  |  SAMPLE DOCUMENT - fictitious data")
    canvas.drawRightString(7.9*inch,0.45*inch,f"Page {doc.page} of {TOTAL_PAGES}"); canvas.restoreState()
doc=SimpleDocTemplate('out/bank_statement_sample.pdf',pagesize=letter,leftMargin=0.6*inch,rightMargin=0.6*inch,topMargin=0.6*inch,bottomMargin=0.7*inch,
    title='Example Bank sample checking statement (fictitious)',author='synthetic')
el=[]
el.append(Paragraph("EXAMPLE BANK, N.A.",h))
el.append(Paragraph("1 Bank Plaza, Anytown, NY 12345 &nbsp;|&nbsp; Customer service 1-555-010-0000 &nbsp;|&nbsp; www.examplebank.example",small))
el.append(Spacer(1,10))
addr=Table([[Paragraph("<b>JANE Q SAMPLE</b><br/>JOHN A SAMPLE<br/>123 EXAMPLE ST APT 4B<br/>ANYTOWN NY 12345-6789",norm),
             Paragraph("<b>Everyday Checking</b><br/>Account number: XXXXXX1234<br/>Statement period: 03/01/2026 - 03/31/2026<br/>Statement date: 03/31/2026",norm)]],colWidths=[3.6*inch,3.6*inch])
el.append(addr); el.append(Spacer(1,12))
el.append(Paragraph("<b>Account Summary</b>",norm))
summ=Table([["Beginning balance on 03/01/2026","",f"${beginning:,.2f}"],
            ["Deposits and other credits",f"{depn}",f"{deps:,.2f}"],
            ["Withdrawals and other debits",f"{wdn}",f"-{wd:,.2f}"],
            ["Ending balance on 03/31/2026","",f"${ending:,.2f}"]],colWidths=[3.4*inch,0.8*inch,1.6*inch])
summ.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Helvetica',9),('FONT',(0,3),(-1,3),'Helvetica-Bold',9),('ALIGN',(1,0),(-1,-1),'RIGHT'),
    ('LINEABOVE',(0,3),(-1,3),0.75,colors.black),('BOTTOMPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),3)]))
el.append(summ); el.append(Spacer(1,14))
el.append(Paragraph("<b>Transaction Detail</b>",norm)); el.append(Spacer(1,4))
data=[["Date","Description","Withdrawals","Deposits","Balance"]]+[list(r) for r in rows]
data.append(["","Ending balance","","",f"{ending:,.2f}"])
t=Table(data,colWidths=[0.6*inch,3.9*inch,1.0*inch,1.0*inch,1.1*inch],repeatRows=1)
t.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Helvetica',8),('FONT',(0,0),(-1,0),'Helvetica-Bold',8),('FONT',(0,-1),(-1,-1),'Helvetica-Bold',8),
    ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DDE3EA')),('ALIGN',(2,0),(-1,-1),'RIGHT'),('LINEBELOW',(0,0),(-1,0),0.75,colors.black),
    ('LINEABOVE',(0,-1),(-1,-1),0.75,colors.black),('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor('#F4F6F8')]),
    ('BOTTOMPADDING',(0,0),(-1,-1),2.5),('TOPPADDING',(0,0),(-1,-1),2.5)]))
el.append(t)
el.append(Spacer(1,16))
el.append(Paragraph("<b>Important information</b>",norm))
el.append(Paragraph("This is a synthetic sample statement created for software testing. Example Bank, N.A. is not a real institution; all names, addresses, account numbers and transactions are fictitious. In case of errors or questions about electronic transfers, a real statement would direct you to contact the bank within 60 days.",small))
el.append(Spacer(1,14)); el.append(Paragraph("<b>Daily Ending Balance</b>",norm)); el.append(Spacer(1,4))
daily={}
for r in rows: daily[r[0]]=r[4]
items=list(daily.items()); cols=3; per=(len(items)+cols-1)//cols
grid=[]
for i in range(per):
    row=[]
    for c in range(cols):
        j=i+c*per
        row+= [items[j][0], items[j][1]] if j<len(items) else ['','']
    grid.append(row)
dt_=Table([["Date","Balance","Date","Balance","Date","Balance"]]+grid,colWidths=[0.7*inch,1.1*inch]*3)
dt_.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Helvetica',8),('FONT',(0,0),(-1,0),'Helvetica-Bold',8),('ALIGN',(1,0),(-1,-1),'RIGHT'),('LINEBELOW',(0,0),(-1,0),0.5,colors.black)]))
el.append(dt_)
import copy
TOTAL_PAGES=0
tmp=SimpleDocTemplate('out/_tmp_bank.pdf',pagesize=letter,leftMargin=0.6*inch,rightMargin=0.6*inch,topMargin=0.6*inch,bottomMargin=0.7*inch)
tmp.build(copy.deepcopy(el),onFirstPage=footer,onLaterPages=footer); TOTAL_PAGES=tmp.page
doc.build(el,onFirstPage=footer,onLaterPages=footer)
import pymupdf; d=pymupdf.open('out/bank_statement_sample.pdf'); print('pages',len(d))
for i,p in enumerate(d): p.get_pixmap(dpi=80).save(f'out/check_bank_p{i+1}.png')
# print a few GT rows
for r in rows:
    if 'MORTGAGE' in r[1] or 'CHECK #1042' in r[1] or 'INTEREST' in r[1] or 'SERVICE FEE' in r[1]: print(r)
print('row count', len(rows), 'first', rows[0], 'last', rows[-1])
