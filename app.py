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

# --- 2. TEXT PODMÍNEK (30 BODŮ) ---
FULL_TERMS = """1. Basic Provisions The Carrier undertakes to transport the goods from the place of dispatch to the place of destination according to the instructions of the Principal (The Mitrans s.r.o.) with due professional care and within the time limit stipulated by the Principal.
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
16. Maturity (Due Date) The due date of the invoice shall be 60 days after its receipt together with all requisites and documents.
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

# --- 4. STREAMLIT ROZHRANÍ ---
st.set_page_config(page_title="Mitrans Order System", page_icon="🚛", layout="centered")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("Login")
    pw = st.text_input("Heslo", type="password")
    if st.button("Vstoupit"):
        if pw == "mitrans2026":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Spatne heslo!")
    st.stop()

st.title("🚛 The Mitrans s.r.o. - Order System")
df_carriers = load_data()

# --- SEKCE 1: DOPRAVCE ---
st.subheader("1. Carrier Selection")
carrier_names = ["-- New Carrier --"] + sorted(df_carriers['nazev'].tolist())
selected_carrier = st.selectbox("Choose from directory", carrier_names, key="sel_carrier")

if selected_carrier != "-- New Carrier --":
    row = df_carriers[df_carriers['nazev'] == selected_carrier].iloc[0]
    st.session_state['c_name'] = str(row['nazev'])
    st.session_state['c_ico'] = str(row['ico'])
    st.session_state['c_tel'] = str(row['tel'])
    st.session_state['c_email'] = str(row['email'])
    st.session_state['c_addr'] = str(row['adresa'])

col1, col2 = st.columns(2)
with col1:
    c_name = st.text_input("Carrier Name", key="c_name")
    c_ico = st.text_input("VAT ID / ID", key="c_ico")
    c_tel = st.text_input("Phone", key="c_tel")
with col2:
    c_email = st.text_input("Email", key="c_email")
    c_addr = st.text_area("Full Address", key="c_addr")

if st.button("💾 Save/Update Carrier"):
    if c_name:
        new_row = {'nazev': c_name, 'adresa': c_addr, 'ico': c_ico, 'tel': c_tel, 'email': c_email}
        df_carriers = df_carriers[df_carriers['nazev'] != c_name]
        df_carriers = pd.concat([df_carriers, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df_carriers)
        st.success("Ulozeno.")
        st.rerun()

st.divider()

# --- SEKCE 2: LOGISTIKA ---
st.subheader("2. Transport Logistics")
col_o1, col_o2 = st.columns(2)
with col_o1:
    ord_num = st.text_input("ORDER NUMBER", key="ord_num")
with col_o2:
    truck_id = st.text_input("Truck ID / Plate (SPZ)", key="truck_id") # <--- NOVÉ POLE

col_l, col_u = st.columns(2)
with col_l:
    d_load = st.text_input("Loading Date", key="d_load")
    a_load = st.text_area("Loading Address", key="a_load")
with col_u:
    d_unload = st.text_input("Unloading Date", key="d_unload")
    a_unload = st.text_area("Unloading Address", key="a_unload")

st.divider()

# --- SEKCE 3: NÁKLAD ---
st.subheader("3. Cargo & Price")
c_qty, c_price = st.columns([1, 1])
qty = c_qty.text_input("Quantity (LF)", key="qty")
price = c_price.text_input("Price (EUR)", key="price")
desc = st.text_area("Description / VIN", key="desc")

st.divider()

# --- SEKCE 4: TLAČÍTKA ---
c_btn1, c_btn2 = st.columns(2)
with c_btn1:
    st.button("🆕 NEW ORDER / CLEAR", use_container_width=True, on_click=reset_form)

with c_btn2:
    if st.button("📄 PREPARE PDF", type="primary", use_container_width=True):
        if not ord_num or not c_name:
            st.error("Chybi cislo objednavky!")
        else:
            pdf = FPDF()
            pdf.add_page()
            
            try:
                if os.path.exists('logo.png'):
                    pdf.image('logo.png', 10, 8, 45)
                    pdf.ln(20)
                else:
                    pdf.ln(5)
            except:
                pdf.ln(5)

            pdf.set_font('helvetica', 'B', 14)
            pdf.cell(0, 10, f"ORDER NUMBER: {clean_text(ord_num)}", ln=1, align='R')
            pdf.ln(5)
            
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(95, 7, "PRINCIPAL (The Mitrans s.r.o.):", ln=0)
            pdf.cell(95, 7, "CARRIER:", ln=1)
            
            pdf.set_font('helvetica', '', 9)
            pdf.cell(95, 5, clean_text(MOJE_FIRMA["nazev"]), ln=0)
            pdf.cell(95, 5, clean_text(c_name), ln=1)
            pdf.cell(95, 5, clean_text(MOJE_FIRMA["adresa"]), ln=0)
            pdf.cell(95, 5, clean_text(c_addr), ln=1)
            pdf.cell(95, 5, f"VAT: {MOJE_FIRMA['dic']}", ln=0)
            pdf.cell(95, 5, f"VAT/ID: {clean_text(c_ico)}", ln=1)
            pdf.cell(95, 5, f"Tel: {MOJE_FIRMA['tel']}", ln=0)
            pdf.cell(95, 5, f"Tel: {clean_text(c_tel)}", ln=1)
            pdf.cell(95, 5, f"Email: {MOJE_FIRMA['email']}", ln=0)
            pdf.cell(95, 5, f"Email: {clean_text(c_email)}", ln=1)
            
            pdf.ln(10)
            # --- ZOBRAZENÍ SPZ V PDF ---
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(0, 7, f"TRUCK PLATE: {clean_text(truck_id)}", ln=1)
            pdf.ln(2)

            pdf.cell(95, 7, f"LOADING: {clean_text(d_load)}", ln=0)
            pdf.cell(95, 7, f"UNLOADING: {clean_text(d_unload)}", ln=1)
            
            pdf.set_font('helvetica', '', 9)
            y_log = pdf.get_y()
            pdf.multi_cell(90, 5, clean_text(a_load), border=1)
            y_l = pdf.get_y()
            pdf.set_xy(105, y_log)
            pdf.multi_cell(95, 5, clean_text(a_unload), border=1)
            y_u = pdf.get_y()
            pdf.set_y(max(y_l, y_u) + 10)
            
            pdf.set_fill_color(230, 230, 230)
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(35, 10, "Quantity", border=1, fill=True, align='C')
            pdf.cell(105, 10, "Description / VIN", border=1, fill=True, align='C')
            pdf.cell(50, 10, "Price", border=1, fill=True, ln=1, align='C')
            
            pdf.set_font('helvetica', '', 9)
            y_t = pdf.get_y()
            pdf.set_xy(45, y_t)
            pdf.multi_cell(105, 5, clean_text(desc), border=1)
            h = max(15, pdf.get_y() - y_t)
            pdf.set_xy(10, y_t); pdf.cell(35, h, f"LF{clean_text(qty)}", border=1, align='C')
            pdf.set_xy(150, y_t); pdf.cell(50, h, f"{clean_text(price)} EUR", border=1, ln=1, align='C')
            
            pdf.ln(10)
            pdf.set_font('helvetica', 'B', 11)
            pdf.cell(0, 10, "TERMS AND CONDITIONS", ln=1)
            pdf.set_font('helvetica', '', 7)
            pdf.multi_cell(0, 4, clean_text(FULL_TERMS))
            
            try:
                final_pdf = pdf.output()
                st.download_button(
                    label="📥 DOWNLOAD PDF",
                    data=bytes(final_pdf),
                    file_name=f"Order_{ord_num}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error: {e}")
