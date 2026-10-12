import pymupdf
P1='topmostSubform[0].Page1[0].'; P2='topmostSubform[0].Page2[0].'
text = {
 P1+'f1_14[0]':'Jane Q', P1+'f1_15[0]':'Sample', P1+'f1_16[0]':'123456789',
 P1+'f1_17[0]':'John A', P1+'f1_18[0]':'Sample', P1+'f1_19[0]':'987654321',
 P1+'Address_ReadOrder[0].f1_20[0]':'123 Example St', P1+'Address_ReadOrder[0].f1_21[0]':'4B',
 P1+'Address_ReadOrder[0].f1_22[0]':'Anytown', P1+'Address_ReadOrder[0].f1_23[0]':'NY', P1+'Address_ReadOrder[0].f1_24[0]':'12345',
 # dependents
 P1+'Table_Dependents[0].Row1[0].f1_31[0]':'Alex', P1+'Table_Dependents[0].Row2[0].f1_35[0]':'Sample',
 P1+'Table_Dependents[0].Row3[0].f1_39[0]':'111223333', P1+'Table_Dependents[0].Row4[0].f1_43[0]':'Son',
 P1+'Table_Dependents[0].Row1[0].f1_32[0]':'Casey', P1+'Table_Dependents[0].Row2[0].f1_36[0]':'Sample',
 P1+'Table_Dependents[0].Row3[0].f1_40[0]':'444556666', P1+'Table_Dependents[0].Row4[0].f1_44[0]':'Daughter',
 # income
 P1+'f1_47[0]':'96,400', P1+'f1_57[0]':'96,400',
 P1+'f1_59[0]':'1,215', P1+'f1_60[0]':'1,900', P1+'f1_61[0]':'2,380',
 P1+'f1_70[0]':'3,150', P1+'f1_73[0]':'103,145', P1+'f1_74[0]':'4,500', P1+'f1_75[0]':'98,645',
 # page 2
 P2+'f2_01[0]':'98,645', P2+'f2_02[0]':'31,500', P2+'f2_05[0]':'31,500', P2+'f2_06[0]':'67,145',
 P2+'f2_08[0]':'7,580', P2+'f2_10[0]':'7,580', P2+'f2_11[0]':'4,400', P2+'f2_13[0]':'4,400',
 P2+'f2_14[0]':'3,180', P2+'f2_16[0]':'3,180',
 P2+'f2_17[0]':'6,912', P2+'f2_20[0]':'6,912', P2+'f2_29[0]':'6,912',
 P2+'f2_30[0]':'3,732', P2+'f2_31[0]':'3,732',
 P2+'RoutingNo[0].f2_32[0]':'123456789', P2+'AccountNo[0].f2_33[0]':'000123456789',
 P2+'f2_40[0]':'Teacher', P2+'f2_42[0]':'Engineer', P2+'f2_44[0]':'(555) 010-0199', P2+'f2_45[0]':'jane@example.com',
}
checks = {
 P1+'Checkbox_ReadOrder[0].c1_8[1]',   # Married filing jointly
 P1+'c1_6[0]',                        # Presidential campaign - You
 P1+'c1_10[1]',                       # Digital assets - No
 P1+'Table_Dependents[0].Row5[0].Dependent1[0].c1_12[0]', P1+'Table_Dependents[0].Row5[0].Dependent1[0].c1_13[0]',
 P1+'Table_Dependents[0].Row5[0].Dependent2[0].c1_14[0]', P1+'Table_Dependents[0].Row5[0].Dependent2[0].c1_15[0]',
 P1+'Table_Dependents[0].Row7[0].Dependent1[0].c1_28[0]', P1+'Table_Dependents[0].Row7[0].Dependent2[0].c1_29[0]',  # child tax credit
 P1+'c1_44[0]',                       # 7b: includes child's capital gain? no -> use Schedule D not required = c1_43
 P2+'c2_16[0]',                       # Checking
 P2+'c2_17[1]',                       # Third party designee: No
}
checks.discard(P1+'c1_44[0]'); checks.add(P1+'c1_43[0]')
doc=pymupdf.open('src/f1040.pdf')
seen=set(); done_t=set(); done_c=set()
for page in doc:
    for w in page.widgets():
        fn=w.field_name; seen.add(fn)
        if fn in text:
            w.field_value=text[fn]; w.update(); done_t.add(fn)
        elif fn in checks:
            w.field_value=w.on_state(); w.update(); done_c.add(fn)
print('missing text', set(text)-done_t); print('missing checks', checks-done_c)
doc.bake(annots=True, widgets=True)
doc.set_metadata({'title':'Form 1040 (2025) - sample filled with fictitious data','author':'synthetic'})
doc.save('out/irs_form_1040_2025_sample_filled.pdf', garbage=3, deflate=True)
d2=pymupdf.open('out/irs_form_1040_2025_sample_filled.pdf')
print('widgets left', sum(1 for p in d2 for _ in p.widgets()))
for i,p in enumerate(d2): p.get_pixmap(dpi=110).save(f'out/check_1040_p{i+1}.png')
t=d2[0].get_text(); print('98,645' in t, 'Jane Q' in t, '96,400' in t)
