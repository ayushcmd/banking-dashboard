import io
from fpdf import FPDF

class BankingPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(11, 35, 84)
        self.cell(0, 10, "Bharat Banking Pulse — FY 2020-2024", align="C")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(148, 163, 184)
        self.ln(6)
        self.cell(0, 6, "Ayush Raj | IIT Patna | Source: RBI Annual Reports", align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(kpi_f, selected_year, ai_insight=""):
    pdf = BankingPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # KPI Section
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(11, 35, 84)
    pdf.cell(0, 8, f"Key Metrics — FY {selected_year}", ln=True)
    pdf.ln(2)

    metrics = [
        ("Best Net Profit", f"Rs {kpi_f['Net_Profit_Crore'].max():,.0f} Cr"),
        ("Lowest NPA", f"{kpi_f['Gross_NPA_Pct'].min():.2f}%"),
        ("Best ROE", f"{kpi_f['Return_On_Equity_Pct'].max():.1f}%"),
        ("Avg CAR (Private)", f"{kpi_f[kpi_f['Bank_Type']=='Private']['Capital_Adequacy_Ratio_Pct'].mean():.1f}%"),
    ]

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(30, 30, 30)
    for label, val in metrics:
        pdf.cell(80, 7, label, border="B")
        pdf.cell(0, 7, val, border="B", ln=True)

    pdf.ln(8)

    # Bank Table
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(11, 35, 84)
    pdf.cell(0, 8, "Bank-wise Performance", ln=True)
    pdf.ln(2)

    headers = ["Bank", "Type", "Net Profit (Cr)", "NPA%", "ROE%", "NIM%"]
    widths  = [45, 20, 35, 20, 20, 20]

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(11, 35, 84)
    pdf.set_text_color(255, 255, 255)
    for h, w in zip(headers, widths):
        pdf.cell(w, 7, h, border=1, fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for i, (_, row) in enumerate(kpi_f.iterrows()):
        pdf.set_fill_color(240, 244, 248) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(45, 6, str(row["Bank"]), border=1, fill=True)
        pdf.cell(20, 6, str(row["Bank_Type"]), border=1, fill=True)
        pdf.cell(35, 6, f"{row['Net_Profit_Crore']:,.0f}", border=1, fill=True)
        pdf.cell(20, 6, f"{row['Gross_NPA_Pct']:.2f}%", border=1, fill=True)
        pdf.cell(20, 6, f"{row['Return_On_Equity_Pct']:.1f}%", border=1, fill=True)
        pdf.cell(20, 6, f"{row['Net_Interest_Margin_Pct']:.1f}%", border=1, fill=True)
        pdf.ln()

    # AI Insight
    if ai_insight:
        pdf.ln(8)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(11, 35, 84)
        pdf.cell(0, 8, "AI Sector Insight", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 6, ai_insight)

    buf = io.BytesIO()
    pdf.output(buf)
    return buf.getvalue()
