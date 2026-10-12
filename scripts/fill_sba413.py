import pymupdf
text = {
 'Name':'John A. Sample', 'Business Phone xxx-xxx-xxxx':'555-010-0100', 'Home Address':'123 Example St, Apt 4B',
 'Home Phone xxx-xxx-xxxx':'555-010-0199', 'City, State, & Zip Code':'Anytown, NY 12345',
 'Business Name of Applicant/Borrower':'Example Widgets LLC', 'Business Address (if different than home address)':'456 Sample Ave, Suite 200, Anytown, NY 12345',
 'This information is current as of month/day/year':'03/31/2026',
 'Cash on Hand & in banks':'18,500', 'Savings Accounts':'42,000', 'IRA or Other Retirement Account':'125,000',
 'Accounts and Notes Receivable':'0', 'Life Insurance - Cash Surrender Value Only':'7,500', 'Stocks and Bonds':'36,250',
 'Real Estate':'450,000', 'Automobiles':'28,000', 'Other Personal Property':'15,000', 'Other Assets':'0',
 'Accounts Payable':'2,300', 'Notes Payable to Banks and Others':'12,000', 'Installment Account (Auto)':'14,200',
 'Installment Account - Monthly Payments (Auto)':'425', 'Installment Account (Other)':'0', 'Installment Account - Monthly Payments (Other)':'0',
 'Loan(s) Against Life Insurance':'0', 'Mortgages on Real Estate':'298,400', 'Unpaid Taxes':'0', 'Other Liabilities':'0',
 'TotalLiabilities':'326,900', 'Net Worth':'395,350',
 'Salary':'112,000', 'Net Investment Income':'2,900', 'Real Estate Income':'0', 'Other Income':'0',
 'As Endorser or Co-Maker':'0', 'Legal Claims and Judgements':'0', 'Provision for Federal Income Tax':'9,800', 'Other Special Debt':'0',
 'Names and Addresses of NoteholdersRow1':'Example Bank, N.A., Anytown NY',
 'Original BalanceRow1':'20,000', 'Current BalanceRow1':'12,000', 'Payment AmountRow1':'450', 'Frequency monthly etcRow1':'Monthly',
 'How Secured or Endorsed Type of CollateralRow1':'Unsecured',
 'Names and Addresses of NoteholdersRow2':'Sample Auto Finance, Anytown NY',
 'Original BalanceRow2':'24,500', 'Current BalanceRow2':'14,200', 'Payment AmountRow2':'425', 'Frequency monthly etcRow2':'Monthly',
 'How Secured or Endorsed Type of CollateralRow2':'2023 Example Sedan',
 'Number of SharesRow1':'250', 'Name of SecuritiesRow1':'Example Corp common', 'CostRow1':'20,000',
 'Market Value QuotationExchangeRow1':'145.00', 'Date of QuotationExchangeRow1':'03/31/2026', 'Total ValueRow1':'36,250',
 'Property AType of Real Estate eg Primary Residence Other Residence Rental Property Land etc':'Primary Residence',
 'Property AAddress':'123 Example St, Anytown, NY 12345', 'Property ADate Purchased_es_:date':'06/15/2015',
 'Property AOriginal Cost':'385,000', 'Property APresent Market Value':'450,000',
 'Property AName  Address of Mortgage Holder':'Example Mortgage Co., PO Box 100, Anytown, NY 12345',
 'Property AMortgage Account Number':'0000-SAMPLE-01', 'Property AMortgage Balance':'298,400',
 'Property AAmount of Payment per MonthYear':'2,150 / month', 'Property AStatus of Mortgage':'Current',
 'Section 5  Other Personal Property and Other Assets: Describe and if any is pledged as security state name and address of lien holder amount of lien terms of payment and if delinquent describe delinquencyRow1':
   'Household furnishings and electronics, est. $15,000. None pledged as security.',
 'Section 6 Unpaid Taxes Describe in detail as to type to whom payable when due amount and to what property if any a tax lien attachesRow1':'None.',
 'Section 7 Other Liabilities Describe in detailRow1':'None.',
 'Section 8 Life Insurance Held Give face amount and cash surrender value of policies  name of insurance company and BeneficiariesRow1':
   'Example Life Insurance Co. whole life policy, face amount $250,000, cash surrender value $7,500. Beneficiary: Jane Q. Sample (spouse).',
 'Date':'04/01/2026', 'Print Name':'John A. Sample', 'Social Security No':'123-45-6789',
}
checks = {'7(a) loan/04 loan/Surety Bonds', 'Business Type: LLC'}
doc=pymupdf.open('src/SBAForm413.pdf')
done_t=set(); done_c=set()
for page in doc:
    for w in page.widgets():
        fn=w.field_name
        if fn=='TotalAssets':
            w.field_value='722,250'; w.update(); done_t.add(fn)
        elif fn in text:
            w.field_value=text[fn]; w.update(); done_t.add(fn)
        elif fn in checks:
            w.field_value=w.on_state(); w.update(); done_c.add(fn)
print('missing text', set(text)-done_t); print('missing checks', checks-done_c)
doc.bake(annots=True, widgets=True)
doc.set_metadata({'title':'SBA Form 413 - sample filled with fictitious data','author':'synthetic'})
doc.save('out/sba_form_413_sample_filled.pdf', garbage=3, deflate=True)
d2=pymupdf.open('out/sba_form_413_sample_filled.pdf')
print('pages', len(d2), 'widgets left', sum(1 for p in d2 for _ in p.widgets()))
for i in (0,1,2,3): d2[i].get_pixmap(dpi=100).save(f'out/check_sba_p{i+1}.png')
t=d2[1].get_text(); print('722,250' in t, '395,350' in t)
