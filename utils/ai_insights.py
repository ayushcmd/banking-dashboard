import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_insight(bank_name, year, npa, roe, profit, nim, car):
    prompt = f"""
You are a senior Indian banking analyst. Give a 3-line sharp insight about this bank's performance.
Be specific, data-driven, no fluff.

Bank: {bank_name}
Year: FY{year}
Gross NPA: {npa}%
Return on Equity: {roe}%
Net Profit: ₹{profit:,.0f} Crore
Net Interest Margin: {nim}%
Capital Adequacy Ratio: {car}%

Give exactly 3 bullet points. Each bullet max 15 words. Start each with •
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.4
    )
    return response.choices[0].message.content.strip()


def get_sector_insight(avg_npa, avg_roe, total_assets, year):
    prompt = f"""
You are a senior RBI banking sector analyst. Give a sharp 3-point sector summary.

FY{year} Indian Banking Sector:
Average Gross NPA: {avg_npa:.2f}%
Average ROE: {avg_roe:.1f}%
Total Assets (all banks): ₹{total_assets/100000:.1f}L Crore

3 bullet points only. Each max 15 words. Start each with •
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.4
    )
    return response.choices[0].message.content.strip()