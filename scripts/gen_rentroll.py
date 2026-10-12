import random, datetime as dt
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
rng=random.Random(4130)
types={'1BR/1BA':(650,1450),'2BR/1BA':(850,1750),'2BR/2BA':(950,1925),'3BR/2BA':(1150,2350),'Studio':(480,1195)}
tenants=['Jane Sample','John Sample','Alex Example','Casey Example','Pat Placeholder','Sam Specimen','Jordan Dummy','Taylor Testcase','Morgan Mockup','Riley Fictional','Avery Nobody','Quinn Anyone']
units=[]
n=0
for bld in ('A','B'):
    for fl in (1,2,3):
        for k in range(1,9):
            n+=1
            typ=rng.choice(list(types)); sf,mkt=types[typ]
            sf=sf+rng.choice([0,0,10,20,35])
            unit=f"{bld}-{fl}{k:02d}"
            r=rng.random()
            if r<0.10:
                units.append((unit,typ,sf,'VACANT','','',0,'Vacant',0,mkt))
            else:
                rent=mkt-rng.choice([0,25,50,75,100,150])
                start=dt.date(2024+rng.choice([0,0,1,1,1,2]),rng.randint(1,12),1)
                endd=dt.date(start.year+1,start.month,1)-dt.timedelta(days=1)
                status='Current'
                if rng.random()<0.08: status='Delinquent'
                if endd<dt.date(2026,4,1): status='MTM'
                units.append((unit,typ,sf,rng.choice(tenants),start.strftime('%m/%d/%Y'),endd.strftime('%m/%d/%Y'),rent,status,rent if rng.random()<0.9 else round(rent*1.5),mkt))
tot_sf=sum(u[2] for u in units); occ=[u for u in units if u[6]>0]; vac=[u for u in units if u[6]==0]
tot_rent=sum(u[6] for u in units); tot_mkt=sum(u[9] for u in units); tot_dep=sum(u[8] for u in units)
annual_gpr=tot_mkt*12; in_place_annual=tot_rent*12
print(f"units={len(units)} occupied={len(occ)} vacant={len(vac)} total_sf={tot_sf:,} monthly_rent={tot_rent:,} market={tot_mkt:,} deposits={tot_dep:,} annual_in_place={in_place_annual:,} annual_gpr={annual_gpr:,}")
delinq=[u for u in units if u[7]=='Delinquent']; print('delinquent', [(u[0],u[3],u[6]) for u in delinq])
print('vacant', [(u[0],u[1],u[9]) for u in vac])
ss=getSampleStyleSheet()
norm=ParagraphStyle('n',parent=ss['Normal'],fontSize=9,leading=11); small=ParagraphStyle('s',parent=ss['Normal'],fontSize=7.5,leading=9)
h=ParagraphStyle('h',parent=ss['Heading1'],fontSize=14,spaceAfter=2)
def footer(c,d):
    c.saveState(); c.setFont('Helvetica',7)
    c.drawString(0.5*inch,0.4*inch,"Example Gardens Apartments - Rent Roll as of 03/31/2026 - SAMPLE DOCUMENT, fictitious data"); c.drawRightString(10.5*inch,0.4*inch,f"Page {d.page}"); c.restoreState()
doc=SimpleDocTemplate('out/rent_roll_operating_statement_sample.pdf',pagesize=landscape(letter),leftMargin=0.5*inch,rightMargin=0.5*inch,topMargin=0.5*inch,bottomMargin=0.6*inch,
    title='Example Gardens Apartments - rent roll and T-12 operating statement (fictitious)',author='synthetic')
el=[Paragraph("Example Gardens Apartments &mdash; Rent Roll",h),
    Paragraph("123 Example St, Anytown, NY 12345 &nbsp;|&nbsp; Owner: Example Gardens Holdings LLC &nbsp;|&nbsp; As of: 03/31/2026 &nbsp;|&nbsp; 48 units, 2 buildings",norm),Spacer(1,8)]
hdr=["Unit","Type","Sq Ft","Tenant","Lease Start","Lease End","Monthly Rent","Market Rent","Deposit","Status"]
data=[hdr]
for u in units:
    data.append([u[0],u[1],f"{u[2]:,}",u[3],u[4],u[5],f"{u[6]:,.2f}" if u[6] else "0.00",f"{u[9]:,.2f}",f"{u[8]:,.2f}" if u[8] else "0.00",u[7]])
data.append(["Totals","",f"{tot_sf:,}",f"{len(occ)} occupied / {len(vac)} vacant","","",f"{tot_rent:,.2f}",f"{tot_mkt:,.2f}",f"{tot_dep:,.2f}",f"{len(occ)/len(units):.1%} occ."])
cw=[0.6,0.8,0.6,1.5,0.9,0.9,1.0,1.0,0.9,0.9]
t=Table(data,colWidths=[c*inch for c in cw],repeatRows=1)
t.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Helvetica',8),('FONT',(0,0),(-1,0),'Helvetica-Bold',8),('FONT',(0,-1),(-1,-1),'Helvetica-Bold',8),
  ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#D9E2EC')),('GRID',(0,0),(-1,-1),0.25,colors.grey),('ALIGN',(2,1),(2,-1),'RIGHT'),('ALIGN',(6,1),(8,-1),'RIGHT'),
  ('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor('#F5F7FA')]),('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#EEF2F6')),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
el.append(t)
el.append(Spacer(1,6)); el.append(Paragraph("Status key: Current = paid through 03/31/2026; MTM = month-to-month holdover; Delinquent = 30+ days past due. Market rent per 03/2026 survey.",small))
el.append(PageBreak())
# ---- T-12 operating statement
vac_loss=round(sum(u[9] for u in vac)*12)  # vacancy at market
loss_to_lease=annual_gpr-in_place_annual-vac_loss
bad_debt=round(sum(u[6] for u in delinq)*2)
other_income=round(len(units)*35*12)+round(len(units)*0.6*45*12)
egi=annual_gpr-vac_loss-loss_to_lease-bad_debt+other_income
exp=[("Real estate taxes",118400),("Insurance",41250),("Utilities (owner-paid water/sewer/common electric)",52780),("Repairs and maintenance",61940),
     ("Contract services (landscaping, pest, trash)",23600),("Payroll and benefits",98500),("Management fee (4.0% of EGI)",round(egi*0.04)),
     ("General and administrative",14320),("Marketing and leasing",9875),("Replacement reserves ($300/unit)",len(units)*300)]
tot_exp=sum(e[1] for e in exp); noi=egi-tot_exp
print(f"GPR={annual_gpr:,} vacancy={vac_loss:,} LTL={loss_to_lease:,} bad_debt={bad_debt:,} other={other_income:,} EGI={egi:,} opex={tot_exp:,} NOI={noi:,} mgmt={exp[6][1]:,} expense_ratio={tot_exp/egi:.1%}")
el.append(Paragraph("Example Gardens Apartments &mdash; Operating Statement (Trailing 12 Months)",h))
el.append(Paragraph("Period: 04/01/2025 - 03/31/2026 &nbsp;|&nbsp; Basis: cash &nbsp;|&nbsp; Prepared 04/08/2026 by Example Property Management LLC (fictitious)",norm)); el.append(Spacer(1,8))
def money(v): return f"({abs(v):,.0f})" if v<0 else f"{v:,.0f}"
os_rows=[["","T-12 Total","Per Unit","% of EGI"],
 ["INCOME","","",""],
 ["Gross potential rent (market)",money(annual_gpr),money(round(annual_gpr/48)),f"{annual_gpr/egi:.1%}"],
 ["Less: vacancy loss",money(-vac_loss),money(-round(vac_loss/48)),f"({vac_loss/egi:.1%})"],
 ["Less: loss to lease",money(-loss_to_lease),money(-round(loss_to_lease/48)),f"({loss_to_lease/egi:.1%})"],
 ["Less: bad debt / concessions",money(-bad_debt),money(-round(bad_debt/48)),f"({bad_debt/egi:.1%})"],
 ["Other income (fees, parking, laundry)",money(other_income),money(round(other_income/48)),f"{other_income/egi:.1%}"],
 ["EFFECTIVE GROSS INCOME",money(egi),money(round(egi/48)),"100.0%"],
 ["OPERATING EXPENSES","","",""]]
for name,v in exp: os_rows.append([name,money(v),money(round(v/48)),f"{v/egi:.1%}"])
os_rows.append(["TOTAL OPERATING EXPENSES",money(tot_exp),money(round(tot_exp/48)),f"{tot_exp/egi:.1%}"])
os_rows.append(["NET OPERATING INCOME",money(noi),money(round(noi/48)),f"{noi/egi:.1%}"])
t2=Table(os_rows,colWidths=[4.6*inch,1.4*inch,1.1*inch,1.0*inch])
bold_rows=[1,7,8,len(os_rows)-2,len(os_rows)-1]
st=[('FONT',(0,0),(-1,-1),'Helvetica',9),('FONT',(0,0),(-1,0),'Helvetica-Bold',9),('ALIGN',(1,0),(-1,-1),'RIGHT'),('LINEBELOW',(0,0),(-1,0),0.75,colors.black),
    ('LINEABOVE',(0,7),(-1,7),0.5,colors.black),('LINEABOVE',(0,len(os_rows)-2),(-1,len(os_rows)-2),0.5,colors.black),('LINEABOVE',(0,len(os_rows)-1),(-1,len(os_rows)-1),1,colors.black),('LINEBELOW',(0,len(os_rows)-1),(-1,len(os_rows)-1),1,colors.black),
    ('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5)]
for r in bold_rows: st.append(('FONT',(0,r),(-1,r),'Helvetica-Bold',9))
t2.setStyle(TableStyle(st)); el.append(t2)
el.append(Spacer(1,8)); el.append(Paragraph("Notes: (1) Negative amounts shown in parentheses. (2) Management fee calculated at 4.0% of effective gross income. (3) Replacement reserves are an underwriting adjustment, not a cash expense. (4) All figures are fictitious and generated for parser testing.",small))
doc.build(el,onFirstPage=footer,onLaterPages=footer)
import pymupdf; d=pymupdf.open('out/rent_roll_operating_statement_sample.pdf'); print('pages',len(d))
for i,p in enumerate(d): p.get_pixmap(dpi=80).save(f'out/check_rr_p{i+1}.png')
# which units on page 2
t1=d[0].get_text(); t2_=d[1].get_text()
print('last unit p1:', [u[0] for u in units if u[0] in t1][-1], '| first unit p2:', [u[0] for u in units if u[0] in t2_][0])
for u in units[:3]+units[-3:]: print(u)
