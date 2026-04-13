import streamlit as st
from fpdf import FPDF
import pandas as pd
import os
import unicodedata

# --- 1. KONFIGURACE TVÉ FIRMY ---
MOJE_FIRMA = {
    "nazev": "The Mitrans s.r.o.",
    "adresa": "Roudniky 95, 403 17 Chabarovice",
    "ico": "19971605",
    "dic": "CZ19971605",
    "tel": "+420 606 058 265",
    "email": "info@themitrans.cz"
}

# --- 2. TEXTY PODMÍNEK (CZ a EN) ---
TERMS_EN = """1. Basic Provisions The Carrier undertakes to transport the goods from the place of dispatch to the place of destination according to the instructions of the Principal (The Mitrans s.r.o.) with due professional care and within the time limit stipulated by the Principal.
2. Liability The Carrier shall be liable for any damage to the goods occurring from the moment the goods are taken over by the Carrier until the moment they are taken over by the consignee.
3. Compensation for Damage In the event of loss or destruction of the consignment, the Carrier shall be obliged to compensate the damage in full.
4. Insurance For the cases referred to in the preceding paragraphs, the Carrier declares that it is insured in such a manner that any potential damage can be fully covered.
5. Documents The Carrier shall be obliged to submit delivery notes and dispatch notes confirmed by the consignee to the consignor (or, as the case may be, to the Principal) immediately after the carriage has been performed.
6. Route The Carrier undertakes to adhere to optimal transport routes.
7. Insurance Policy The Carrier shall be obliged and undertakes to have in place liability insurance for damage caused in the course of carriage, with an insurance indemnity limit at such level as to cover any damage that may be incurred by the Carrier, the Principal, the Consignee or third parties as a result of damage, destruction or deterioration of the goods. Without such insurance in place, the Carrier must not perform the carriage. The Carrier shall be obliged to submit, prior to the performance of the first carriage and at any time thereafter upon the Principal's request, a valid insurance policy for inspection, evidencing fulfilment of this condition.
8. Prohibition of Subcontracting Without the prior written consent of the Principal, the Carrier shall not be entitled to perform the carriage under the Cooperation Agreement, or any part thereof, through another carrier.
9. Parking The Carrier shall be obliged to ensure that parking and leaving vehicles loaded with goods during the transport at night, at weekends, during mandatory breaks or on public holidays takes place exclusively on fenced and secured parking areas.
10. Parking Security All loaded vehicles may be parked only on secured premises, guarded parking lots, places otherwise supervised, or on designated areas (fuel stations with designated truck parking, truck parking areas, customs areas, etc.).
11. Times (Time Slots) The Carrier undertakes to comply with the so-called "pick up time" - the time of cargo collection. The dispatcher shall inform the Carrier in advance whether it is a so-called spot load, where the pick-up time shall be no later than 12 hours from notification. The Carrier further undertakes to comply with the so-called "transit time" - the time of delivery. The standard delivery time is 48 hours from loading, but no later than 84 hours from loading, unless otherwise agreed.
12. Duty to Inform The Carrier shall be obliged to duly, timely and without undue delay inform the Principal of all material facts affecting the carriage (loss events, vehicle locations). In the event of a defect of the vehicle which may affect the delivery deadline, the Carrier shall be obliged to notify this fact within 30 minutes of its discovery. Delays at loading/unloading must be notified in writing to the relevant dispatcher. Should the Carrier fail to do so, it shall be deemed that the information has not been provided.
13. Contractual Penalties for Delay: 
- Delay up to 12 hours: contractual penalty in the amount of 25% of the freight price. 
- Delay exceeding 12 hours: contractual penalty in the amount of 50% of the freight price (if not reported in due time and in writing). 
- Delay exceeding 48 hours: contractual penalty in the amount of 100% of the freight price and a reason for immediate termination of cooperation.
14. Failure to Meet the Loading Time In case the Carrier fails to meet the deadline for cargo collection, the Principal shall be entitled to cancel the order and assign it to another carrier. The Principal may claim a contractual penalty of up to 10% of the freight price.
15. Prohibition of Resale The load must not, without the consent of The Mitrans s.r.o., be further resold (assigned to another forwarding agent). In the event of a breach of this obligation, the carriage shall not be paid.
16. Maturity (Due Date) and Payment Conditions: The due date of the invoice shall be 60 days from the day the Principal receives the original hard copies of the following documents: the freight invoice, the CMR consignment note, and the delivery note (confirmed by the consignee). In the event of any damage to, destruction of, or loss of the cargo, the maturity of the freight invoice shall be automatically suspended. In such a case, the freight invoice shall only become due and payable after the exact amount of the damage has been fully quantified and resolved. The Principal reserves the right to unilaterally set off any quantified damage claims against the Carrier's freight invoice.
17. Dispute Resolution The Principal and the Carrier undertake to resolve disputes primarily by mutual agreement. If no agreement is reached, disputes shall be resolved by the court of subject-matter and local jurisdiction in the Czech Republic according to the registered office of the Principal.
18. Assignment of Receivables The Carrier shall not be entitled to assign its receivables from the Principal to third parties without the Principal's prior written consent.
19. Quality Standards and Penalties The Carrier confirms that it has been acquainted with the quality requirements. Penalties for Breach: 
- EUR 100: insufficient securing of cargo (lashing straps, chocks, anti-slip mats). 
- EUR 150: insufficient quality of the vehicle (dirty loading compartment, oil leakage, technical condition). 
- EUR 100: inappropriate clothing/behaviour of the driver (occupational health and safety, gloves). 
- EUR 50: administrative error in connection with damage. 
- EUR 50: failure to submit transport documents (electronically or by post) within 48 hours. 
The maximum aggregate amount of these penalties per one carriage shall be EUR 450.
20. Receivables Management The Carrier acknowledges that accounting and claims matters may be handled for the Principal by an authorised third party. The Carrier shall be obliged to provide cooperation.
21. Photographic Documentation The Mitrans s.r.o. shall not be obliged, in the event of a loss event, to provide its own photographic documentation of the damage (it relies on the record in the CMR and the documentation of the consignee/carrier).
22. Reporting of Damage The Carrier shall be obliged to report to The Mitrans s.r.o. all loss events and their causes immediately after their occurrence.
23. Discrepancies at Loading In the event of any discrepancy at loading (quality of goods, packaging), the Carrier shall be obliged to inform The Mitrans s.r.o. at the e-mail address info@themitrans.cz prior to loading. Later complaints shall not be taken into consideration.
24. Discrepancies at Unloading In the event of any discrepancy at unloading, the Carrier shall be obliged to inform The Mitrans s.r.o. at the e-mail address info@themitrans.cz prior to departure from the place of unloading.
25. Recourse (Right of Recourse) The Carrier shall reimburse The Mitrans s.r.o. for all payments (penalties, compensations) which the company had to pay to its customers due to the Carrier's fault, within 10 days from receipt of the relevant request.
26. VW/Skoda/Seat/Audi Clause In the event of carriage for the VW Group, the Carrier shall be obliged to ensure that the CMR and the delivery note bear the original stamp: "PREPRAVNE BUDE ZAPLACENO JEN PO PREDLOZENI TETO KOPIE / FREIGHT PAYMENTS ONLY WITH THIS DOCUMENT ACCOMPANYING THE FREIGHT INVOICE". Without this document, the invoice shall not be due.
27. TESLA Clause In the case of carriage for TESLA, it is necessary to use the TESLA application (confirmation of loading/unloading). The penalty for failure to use the application or failure to comply with the time limit shall be EUR 500.
28. Extended Liability The Carrier undertakes to pay compensation for all damage to the cargo in full, even beyond the limitation pursuant to the CMR Convention, including damage not recorded in the CMR, provided that such damage occurred during the carriage.
29. Failure to comply with Toyota cost conditions resulting in the subsequent blocking or suspension of the driver shall be subject to a contractual penalty of EUR 500.
30. In the case of loads for Skoda Auto, a.s., failure to load the cargo on the date specified in the order shall result in a contractual penalty of EUR 500.

By accepting this order, the Carrier expressly agrees to cover all damages to the transported cargo, even if such damages are not recorded in the CMR consignment note or in the delivery note."""

TERMS_CZ = """1. Zakladni ustanoveni: Dopravce se zavazuje prepravit zbozi z mista odeslani do mista urceni podle pokynu objednatele (The Mitrans s.r.o.) s odbornou peci a ve lhute stanovene objednatelem.
2. Odpovednost: Dopravce odpovida za skodu na zbozi vzniklou od okamziku prevzeti zbozi dopravcem az do okamziku jeho predani prijemci.
3. Nahrady skody: V pripade ztraty nebo zniceni zasilky je dopravce povinen nahradit skodu v plne vysi.
4. Pojisteni: Pro pripady uvedene v predchozich odstavcich dopravce prohlasuje, ze je pojisten takovym zpusobem, aby pripadna skoda mohla byt plne kryta.
5. Dokumenty: Dopravce je povinen ihned po provedeni prepravy predat odesilateli (pripadne objednateli) dodaci a nakladni listy potvrzene prijemcem.
6. Trasa: Dopravce se zavazuje dodrzovat optimalni prepravni trasy.
7. Pojistna smlouva: Dopravce je povinen mit uzavreno pojisteni odpovednosti za skodu zpusobenou pri preprave s limitem kryti dostatecnym pro vsechny vznikle skody. Bez tohoto pojisteni nesmi dopravce prepravu provest. Platnou pojistku musi predlozit na vyzadani.
8. Zakaz dalsiho podnajmu: Bez predchoziho pisemneho souhlasu objednatele neni dopravce opravnen provest prepravu prostrednictvim jineho dopravce.
9. Parkovani: Dopravce je povinen zajistit, aby parkovani nalozenych vozidel behem noci, vikendu nebo prestavek probihalo vyhradne na oplocenych a hlidanych parkovistich.
10. Zabezpeceni parkovani: Vozidla smi parkovat pouze na zabezpecenych prostorech, hlidanych parkovistich nebo cerpacich stanicich s vyhrazenym stanim pro kamiony.
11. Casy (Time Slots): Dopravce se zavazuje dodrzet cas nakladky. Standardni doba dodani je 48 hodin od nakladky, nejpozdeji vsak 84 hodin, neni-li dohodnuto jinak.
12. Informacni povinnost: Dopravce je povinen neprodlene (do 30 min) informovat objednatele o vsech skutecnostech majicich vliv na prepravu (skody, zpozdeni, poruchy).
13. Smluvni pokuty za zpozdeni:
- Zpozdeni do 12 hod: smluvni pokuta ve vysi 25% z ceny prepravneho.
- Zpozdeni nad 12 hod: smluvni pokuta ve vysi 50% z ceny prepravneho.
- Zpozdeni nad 48 hod: smluvni pokuta ve vysi 100% z ceny prepravneho a duvod k ukonceni spoluprace.
14. Nedodrzeni casu nakladky: Pokud dopravce nedodrzi termin nakladky, objednatel muze objednavku zrusit a uctovat pokutu do 10% z ceny prepravneho.
15. Zakaz dalsiho prodeje: Naklad nesmi byt bez souhlasu The Mitrans s.r.o. dale prodan (predan jine spedici). V pripade poruseni nebude preprava zaplacena.
16. Splatnost a platebni podminky: Splatnost faktury je 60 dni ode dne, kdy objednatel obdrzi originaly nasledujicich dokumentu: fakturu za prepravu, nakladni list CMR a dodaci list (potvrzeny prijemcem). V pripade jakehokoli poskozeni, zniceni nebo ztraty nakladu se splatnost faktury automaticky pozastavuje. V takovem pripade se faktura stane splatnou az pote, co bude presna vyse skody plne vycisleny a vyreseny. Objednatel si vyhrazuje pravo jednostranne zapocist jakekoli vycislene naroky na nahradu skody proti fakture dopravce.
17. Reseni sporu: Sporne zalezitosti budou reseny prednostne dohodou, jinak u vecne a mistne prislusneho soudu v Ceske republice dle sidla objednatele.
18. Postoupeni pohledavek: Dopravce neni opravnen postoupit sve pohledavky vuci objednateli tretim osobam bez jeho pisemneho souhlasu.
19. Standardy kvality a sankce: Pokuty za poruseni:
- 100 EUR: nedostatecne zajisteni nakladu (pasy, podlozky).
- 150 EUR: spatny stav vozidla (necistota, unik oleje).
- 100 EUR: nevhodne obleceni/chovani ridice (OOPP).
- 50 EUR: administrativni chyba u skody.
- 50 EUR: nedodani dokumentu do 48 hod.
Maximalni souhrnna pokuta na jednu prepravu je 450 EUR.
20. Sprava pohledavek: Dopravce bere na vedomi, ze ucetni a reklamacni zalezitosti muze pro objednatele resit poverena treti strana.
21. Fotodokumentace: The Mitrans s.r.o. neni povinna zajistovat vlastni fotodokumentaci skody (poleha na zaznam v CMR a dokumentaci prijemce).
22. Hlaseni skod: Vsechny skodni udalosti musi byt nahlaseny neprodlene po jejich vzniku.
23. Nesrovnalosti pri nakladce: Jakoukoli nesrovnalost (kvalita, baleni) musi dopravce nahlasit na info@themitrans.cz jeste pred nakladkou. Pozdejsi reklamace nebudou uznany.
24. Nesrovnalosti pri vykladce: Jakoukoli nesrovnalost pri vykladce musi dopravce nahlasit na info@themitrans.cz pred odjezdem z mista vykladky.
25. Regres: Dopravce uhradi objednateli vsechny naklady (pokuty, nahrady), ktere musel objednatel vyplatit zakaznikum vinou dopravce, a to do 10 dni.
26. VW/Skoda/Seat/Audi klauzule: U preprav pro VW Group musi CMR a dodaci list obsahovat razitko: "PREPRAVNE BUDE ZAPLACENO JEN PO PREDLOZENI TETO KOPIE". Bez tohoto dokumentu neni faktura splatna.
27. TESLA klauzule: U preprav pro TESLA je nutne pouzivat aplikaci TESLA. Pokuta za nepouziti nebo nedodrzeni casu je 500 EUR.
28. Rozsirena odpovednost: Dopravce se zavazuje uhradit skodu na nakladu v plne vysi i nad ramec omezeni Umluvy CMR.
29. Toyota klauzule: Nedodrzeni podminek vedouci k blokaci ridice je trestano pokutou 500 EUR.
30. Skoda Auto klauzule: Nepristaveni vozidla k nakladce v dany den je trestano pokutou 500 EUR.

Prijetim teto objednavky dopravce vyslovne souhlasi s uhradou vsech skod na prepravovanem nakladu, i kdyz nejsou zapsany v CMR."""

# --- 3. POMOCNÉ FUNKCE ---
def clean_text(text):
    if text is None: return ""
    text = str(text)
    normalized = "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return normalized.encode('ascii', 'ignore').decode('ascii')

def load_data():
    if os.path.exists('carriers.csv'):
        return pd.read_csv('carriers.csv')
    return pd.DataFrame(columns=['nazev', 'adresa', 'ico', 'tel', 'email'])

def save_data(df):
    df.to_csv('carriers.csv', index=False)

def reset_form():
    for key in list(st.session_state.keys()):
        if key != "authenticated":
            del st.session_state[key]

def update_carrier_fields():
    """Funkce, která se spustí při změně v adresáři"""
    df = load_data()
    sel = st.session_state.sel_carrier
    if sel != "-- New / Novy --":
        row = df[df['nazev'] == sel].iloc[0]
        st.session_state['c_name'] = str(row['nazev'])
        st.session_state['c_ico'] = str(row['ico'])
        st.session_state['c_tel'] = str(row['tel'])
        st.session_state['c_email'] = str(row['email'])
        st.session_state['c_addr'] = str(row['adresa'])

# --- 4. STREAMLIT KONFIGURACE ---
st.set_page_config(page_title="Mitrans Order System", page_icon="🚛", layout="centered")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("Login")
    pw = st.text_input("Heslo / Password", type="password")
    if st.button("Vstoupit / Login"):
        if pw == "mitrans2026":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Spatne heslo / Wrong password!")
    st.stop()

lang = st.radio("Jazyk / Language", ("EN", "CZ"), horizontal=True)

T = {
    "CZ": {
        "title": "Objednavka prepravy", "sec1": "1. Vyber dopravce", "dir": "Adresar",
        "name": "Jmeno dopravce", "vat": "ICO / DIC", "tel": "Telefon", "mail": "Email", "addr": "Adresa",
        "save": "Ulozit dopravce", "sec2": "2. Logistika", "ord_n": "CISLO OBJEDNAVKY", "truck": "SPZ vozidla",
        "l_date": "Datum nakladky", "l_addr": "Misto nakladky", "u_date": "Datum vykladky", "u_addr": "Misto vykladky",
        "sec3": "3. Naklad a Cena", "qty": "Mnozstvi (LF)", "price": "Cena (EUR)", "desc": "Popis / VIN",
        "new": "NOVA OBJEDNAVKA", "prep": "PRIPRAVIT PDF", "principal": "OBJEDNATEL", "carrier": "DOPRAVCE", "terms_label": "SMLUVNI PODMINKY"
    },
    "EN": {
        "title": "Transport Order", "sec1": "1. Carrier Selection", "dir": "Directory",
        "name": "Carrier Name", "vat": "VAT / ID", "tel": "Phone", "mail": "Email", "addr": "Address",
        "save": "Save Carrier", "sec2": "2. Logistics", "ord_n": "ORDER NUMBER", "truck": "Truck Plate",
        "l_date": "Loading Date", "l_addr": "Loading Address", "u_date": "Unloading Date", "u_addr": "Unloading Address",
        "sec3": "3. Cargo & Price", "qty": "Quantity (LF)", "price": "Price (EUR)", "desc": "Description / VIN",
        "new": "NEW ORDER / CLEAR", "prep": "PREPARE PDF", "principal": "PRINCIPAL", "carrier": "CARRIER", "terms_label": "TERMS AND CONDITIONS"
    }
}[lang]

st.title(f"🚛 {T['title']}")
df_carriers = load_data()

# 1. Dopravce
st.subheader(T["sec1"])
carrier_names = ["-- New / Novy --"] + sorted(df_carriers['nazev'].tolist())
# ZDE JE OPRAVA: on_change zavolá funkci pro vyplnění polí
st.selectbox(T["dir"], carrier_names, key="sel_carrier", on_change=update_carrier_fields)

col1, col2 = st.columns(2)
with col1:
    st.text_input(T["name"], key="c_name")
    st.text_input(T["vat"], key="c_ico")
    st.text_input(T["tel"], key="c_tel")
with col2:
    st.text_input(T["mail"], key="c_email")
    st.text_area(T["addr"], key="c_addr")

if st.button(T["save"]):
    if st.session_state.get('c_name'):
        new_row = {'nazev': st.session_state.c_name, 'adresa': st.session_state.c_addr, 'ico': st.session_state.c_ico, 'tel': st.session_state.c_tel, 'email': st.session_state.c_email}
        df_carriers = df_carriers[df_carriers['nazev'] != st.session_state.c_name]
        df_carriers = pd.concat([df_carriers, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df_carriers)
        st.success("OK")
        st.rerun()

st.divider()

# 2. Logistika
st.subheader(T["sec2"])
c_o1, c_o2 = st.columns(2)
with c_o1: st.text_input(T["ord_n"], key="ord_num")
with c_o2: st.text_input(T["truck"], key="truck_id")

col_l, col_u = st.columns(2)
with col_l:
    st.text_input(T["l_date"], key="d_load")
    st.text_area(T["l_addr"], key="a_load")
with col_u:
    st.text_input(T["u_date"], key="d_unload")
    st.text_area(T["u_addr"], key="a_unload")

st.divider()

# 3. Naklad
st.subheader(T["sec3"])
c_qty, c_price = st.columns(2)
with c_qty: st.text_input(T["qty"], key="qty")
with c_price: st.text_input(T["price"], key="price")
st.text_area(T["desc"], key="desc")

st.divider()

# 4. Akce
b1, b2 = st.columns(2)
with b1: st.button(T["new"], use_container_width=True, on_click=reset_form)
with b2:
    if st.button(T["prep"], type="primary", use_container_width=True):
        if not st.session_state.get('ord_num') or not st.session_state.get('c_name'):
            st.error("Missing data!")
        else:
            pdf = FPDF()
            pdf.add_page()
            try:
                if os.path.exists('logo.png'):
                    pdf.image('logo.png', 10, 8, 45)
                    pdf.ln(20)
                else: pdf.ln(5)
            except: pdf.ln(5)

            pdf.set_font('helvetica', 'B', 14)
            pdf.cell(0, 10, f"{T['ord_n']}: {clean_text(st.session_state.ord_num)}", ln=1, align='R')
            pdf.ln(5)
            
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(95, 7, f"{T['principal']} (The Mitrans s.r.o.):", ln=0)
            pdf.cell(95, 7, f"{T['carrier']}:", ln=1)
            
            pdf.set_font('helvetica', '', 9)
            pdf.cell(95, 5, clean_text(MOJE_FIRMA["nazev"]), ln=0)
            pdf.cell(95, 5, clean_text(st.session_state.c_name), ln=1)
            pdf.cell(95, 5, clean_text(MOJE_FIRMA["adresa"]), ln=0)
            pdf.cell(95, 5, clean_text(st.session_state.c_addr), ln=1)
            pdf.cell(95, 5, f"VAT: {MOJE_FIRMA['dic']}", ln=0)
            pdf.cell(95, 5, f"VAT/ID: {clean_text(st.session_state.c_ico)}", ln=1)
            pdf.cell(95, 5, f"Tel: {MOJE_FIRMA['tel']}", ln=0)
            pdf.cell(95, 5, f"Tel: {clean_text(st.session_state.c_tel)}", ln=1)
            pdf.cell(95, 5, f"Email: {MOJE_FIRMA['email']}", ln=0)
            pdf.cell(95, 5, f"Email: {clean_text(st.session_state.c_email)}", ln=1)
            
            pdf.ln(10)
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(0, 7, f"{T['truck']}: {clean_text(st.session_state.truck_id)}", ln=1)
            pdf.ln(2)
            pdf.cell(95, 7, f"{T['l_date']}: {clean_text(st.session_state.d_load)}", ln=0)
            pdf.cell(95, 7, f"{T['u_date']}: {clean_text(st.session_state.d_unload)}", ln=1)
            
            pdf.set_font('helvetica', '', 9)
            y_log = pdf.get_y()
            pdf.multi_cell(90, 5, clean_text(st.session_state.a_load), border=1)
            y_l = pdf.get_y()
            pdf.set_xy(105, y_log)
            pdf.multi_cell(95, 5, clean_text(st.session_state.a_unload), border=1)
            pdf.set_y(max(y_l, pdf.get_y()) + 10)
            
            pdf.set_fill_color(230, 230, 230)
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(35, 10, T["qty"], border=1, fill=True, align='C')
            pdf.cell(105, 10, T["desc"], border=1, fill=True, align='C')
            pdf.cell(50, 10, T["price"], border=1, fill=True, ln=1, align='C')
            
            pdf.set_font('helvetica', '', 9)
            y_t = pdf.get_y()
            pdf.set_xy(45, y_t)
            pdf.multi_cell(105, 5, clean_text(st.session_state.desc), border=1)
            h = max(15, pdf.get_y() - y_t)
            pdf.set_xy(10, y_t); pdf.cell(35, h, f"LF{clean_text(st.session_state.qty)}", border=1, align='C')
            pdf.set_xy(150, y_t); pdf.cell(50, h, f"{clean_text(st.session_state.price)} EUR", border=1, ln=1, align='C')
            
            pdf.ln(10)
            pdf.set_font('helvetica', 'B', 11)
            pdf.cell(0, 10, T["terms_label"], ln=1)
            pdf.set_font('helvetica', '', 7)
            current_terms = TERMS_CZ if lang == "CZ" else TERMS_EN
            pdf.multi_cell(0, 4, clean_text(current_terms))
            
            final_pdf = pdf.output()
            st.download_button(label=f"DOWNLOAD {lang} PDF", data=bytes(final_pdf), file_name=f"Order_{st.session_state.ord_num}.pdf", mime="application/pdf", use_container_width=True)
