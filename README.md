# Clothing Procurement Report

This project is a **Python tool** that generates procurement reports for clothing SKUs.  
It calculates **landed cost, tariffs, freight, and SLA (lead time + shipping)**, then exports an Excel file with three sheets:

- **KPI_Summary** → Total spend, average SLA, SKU count  
- **Best_By_SKU** → Best supplier per SKU (lowest landed cost & SLA)  
- **Supplier_Compare** → Top 5 suppliers per SKU for comparison  

---

## 📂 Project Structure
clothing-procurement-report/
├─ sample_data/
│ ├─ supplier_quotes.csv
│ ├─ fx_rates.csv
│ ├─ tariff_table.csv
│ ├─ shipping_rates.csv
│ └─ demand_plan.csv
├─ auto_procurement_report.py # Main script
├─ README.md
└─ .gitignore

---

## ⚙️ Requirements
- Python 3.8+
- pandas
- openpyxl (for Excel export)

Install dependencies:
pip install pandas openpyxl

---

## 🚀 How to Run

1. **Clone this repository**
git clone https://github.com/Angela0602/clothing-procurement-report.git

cd clothing-procurement-report

2. **Install required packages**
pip install pandas openpyxl
3. **Run the script**
python auto_procurement_report.py
4. **Check the output**  
The script will generate an Excel report in the project root:
Procurement_Report_YYYY-MM-DD.xlsxIt contains three sheets:
- **KPI_Summary** → Total spend, average SLA, SKU count  
- **Best_By_SKU** → Best supplier per SKU (lowest landed cost & SLA)  
- **Supplier_Compare** → Top 5 suppliers per SKU for comparison  

---

## 📊 Example Output
You can preview a sample report here:  
👉 [Procurement_Report_sample.xlsx](Procurement_Report_sample.xlsx)

---

## 📝 Notes
- Tariff rates in the sample data are based on **Canada Customs Tariff (MFN rates, 2025)**.  
- Real imports may apply **preferential tariff rates (CUSMA, CPTPP, etc.)**, so adjust as needed.  
- The output `.xlsx` file is ignored in `.gitignore` to keep the repo clean.  

---

## 📌 License
MIT License
