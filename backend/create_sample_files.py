import os
import pandas as pd
import numpy as np
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_data")
os.makedirs(SAMPLE_DIR, exist_ok=True)

def create_dirty_sales_csv():
    data = [
        # Date, Product, Region, Revenue, Units, Customer_Type
        ["2024-01-01", "iPhone 15", "North", "$1,200", 2, "Retail"],
        ["2024-01-02", "iphone 15", "North", "$1,200", 2, "Retail"], # Duplicate variation
        ["2024-01-03", "IPHONE 15", "North", "₹1,00,000", 2, "Retail"],
        ["01/04/2024", "MacBook Pro", "West", "$2,499", 1, "Corporate"],
        ["2024-01-05", "MacBook Pro", "West", "$2,499", 1, "Corporate"],
        ["2024-01-06", "iPad Air", "South", "650", None, "Retail"], # Missing units
        ["2024-01-07", "ipad air", "South", "$650", 3, "Retail"],
        ["01-08-2024", "Apple Watch", "East", "$399", 4, "Online"],
        ["2024-01-09", "Apple Watch", "East", "399.00", 4, "Online"],
        ["2024-01-10", "AirPods Pro", "North", "$249", 10, "Retail"],
        ["2024-01-11", "iPhone 15", "East", "$2,400", 4, "Retail"],
        ["2024-01-12", "MacBook Pro", "North", "$7,497", 3, "Corporate"],
        ["2024-01-13", "iPad Air", "West", "$1,300", 2, "Retail"],
        ["2024-01-14", "AirPods Pro", "South", "$498", 2, "Online"],
        ["2024-01-15", "iPhone 15", "West", "$85,000", 50, "Corporate"], # Statistical Anomaly / Outlier
        ["2024-01-16", "iPhone 15", "North", "$1,200", 2, "Retail"], # Duplicate row
        ["2024-01-16", "iPhone 15", "North", "$1,200", 2, "Retail"], # Duplicate row
    ]
    df = pd.DataFrame(data, columns=["Order_Date", "Product", "Region", "Revenue", "Units_Sold", "Customer_Type"])
    file_path = os.path.join(SAMPLE_DIR, "sales_dirty.csv")
    df.to_csv(file_path, index=False)
    print(f"Created: {file_path}")

def create_financial_xlsx():
    df_q1 = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar"],
        "Revenue": [120000, 135000, 150000],
        "Operating_Cost": [80000, 85000, 92000],
        "Net_Profit": [40000, 50000, 58000]
    })
    df_q2 = pd.DataFrame({
        "Month": ["Apr", "May", "Jun"],
        "Revenue": [160000, 175000, 190000],
        "Operating_Cost": [95000, 102000, 110000],
        "Net_Profit": [65000, 73000, 80000]
    })
    file_path = os.path.join(SAMPLE_DIR, "financial_report.xlsx")
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        df_q1.to_excel(writer, sheet_name="Q1_Performance", index=False)
        df_q2.to_excel(writer, sheet_name="Q2_Performance", index=False)
    print(f"Created: {file_path}")

def create_sample_docx():
    doc = Document()
    doc.add_heading("Quarterly Performance Review", level=0)
    doc.add_paragraph("This document outlines the performance metrics for Q3 operations across all global business units.")
    doc.add_heading("Operational Highlights", level=1)
    
    table = doc.add_table(rows=1, cols=4)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Department"
    hdr_cells[1].text = "Budget"
    hdr_cells[2].text = "Spend"
    hdr_cells[3].text = "Efficiency"

    data = [
        ["Engineering", "$500,000", "$480,000", "96%"],
        ["Marketing", "$300,000", "$295,000", "98%"],
        ["Sales", "$450,000", "$440,000", "97%"],
        ["Customer Success", "$150,000", "$140,000", "93%"]
    ]
    for row in data:
        row_cells = table.add_row().cells
        for i, val in enumerate(row):
            row_cells[i].text = val

    file_path = os.path.join(SAMPLE_DIR, "project_summary.docx")
    doc.save(file_path)
    print(f"Created: {file_path}")

def create_sample_pdf():
    file_path = os.path.join(SAMPLE_DIR, "quarterly_report.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Executive Sales & Analytics Report", styles["Heading1"]),
        Paragraph("Comprehensive multi-channel sales performance and customer acquisition metrics.", styles["Normal"]),
        Spacer(1, 15)
    ]
    data = [
        ["Category", "Q1 Sales", "Q2 Sales", "Growth"],
        ["Electronics", "$120,000", "$145,000", "+20.8%"],
        ["Apparel", "$85,000", "$92,000", "+8.2%"],
        ["Home Goods", "$64,000", "$71,000", "+10.9%"],
        ["Accessories", "$42,000", "$49,000", "+16.7%"]
    ]
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1'))
    ]))
    story.append(t)
    doc.build(story)
    print(f"Created: {file_path}")

if __name__ == "__main__":
    create_dirty_sales_csv()
    create_financial_xlsx()
    create_sample_docx()
    create_sample_pdf()
    print("All sample files generated successfully.")
