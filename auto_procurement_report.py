
from pathlib import Path
from datetime import date
import pandas as pd

BASE = Path(__file__).resolve().parent
DATA = BASE / "sample_data"
OUT_XLSX = BASE / f"Procurement_Report_{date.today().isoformat()}.xlsx"

def load():
    quotes   = pd.read_csv(DATA/"supplier_quotes.csv")
    fx       = pd.read_csv(DATA/"fx_rates.csv")
    tariffs  = pd.read_csv(DATA/"tariff_table.csv")
    shipping = pd.read_csv(DATA/"shipping_rates.csv")
    demand   = pd.read_csv(DATA/"demand_plan.csv")
    return quotes, fx, tariffs, shipping, demand

def compute():
    quotes, fx, tariffs, shipping, demand = load()
    df = quotes.merge(fx, on="currency", how="left").merge(tariffs, on="sku", how="left")
    df = df.merge(demand, on="sku", how="left")
    ship = shipping.rename(columns={"days":"ship_days"})
    df = df.merge(ship, left_on=["origin","preferred_mode"], right_on=["origin","mode"], how="left")

    df["unit_price_CAD"] = df["unit_price"] * df["to_CAD"]
    df["total_weight_kg"] = df["qty_needed"] * df["avg_weight_kg_per_unit"]
    df["freight_cost"] = (df["per_kg"] * df["total_weight_kg"]).clip(lower=df["min_charge"].fillna(0))
    df["freight_per_unit"] = df["freight_cost"] / df["qty_needed"]
    df["tariff_cost"] = df["tariff_rate"].fillna(0) * (df["unit_price_CAD"] * df["qty_needed"])
    df["tariff_per_unit"] = df["tariff_cost"] / df["qty_needed"]
    df["landed_per_unit_CAD"] = df["unit_price_CAD"] + df["freight_per_unit"] + df["tariff_per_unit"]
    df["total_landed_CAD"] = df["landed_per_unit_CAD"] * df["qty_needed"]
    df["sla_days"] = df["lead_time_days"] + df["ship_days"]
    return df

def export(df):
    try:
        with pd.ExcelWriter(OUT_XLSX) as writer:
            total_spend = float(df["total_landed_CAD"].sum())
            avg_sla = float(df["sla_days"].mean())
            sku_count = int(df["sku"].nunique())
            kpi = pd.DataFrame([{"total_spend_CAD": round(total_spend,2), "avg_sla_days": round(avg_sla,1), "sku_count": sku_count}])
            kpi.to_excel(writer, index=False, sheet_name="KPI_Summary")

            best = (df.sort_values(["sku","landed_per_unit_CAD","sla_days"])
                      .groupby("sku", as_index=False)
                      .first())
            best_cols = ["sku","desc","supplier","currency","unit_price","unit_price_CAD",
                         "freight_per_unit","tariff_per_unit","landed_per_unit_CAD",
                         "qty_needed","total_landed_CAD","sla_days","moq"]
            best[best_cols].to_excel(writer, index=False, sheet_name="Best_By_SKU")

            comp = (df.sort_values(["sku","landed_per_unit_CAD"]).groupby("sku").head(5))
            comp_cols = ["sku","desc","supplier","currency","unit_price","unit_price_CAD",
                         "freight_per_unit","tariff_per_unit","landed_per_unit_CAD","sla_days","valid_until"]
            comp[comp_cols].to_excel(writer, index=False, sheet_name="Supplier_Compare")
        print(f"✅ Report created: {OUT_XLSX}")
    except Exception as e:
        print(f"⚠️ Excel engine not available ({e}). Writing CSV instead...")
        df.to_csv(BASE/'report_full.csv', index=False)
        print(f"✅ CSV created: {BASE/'report_full.csv'}")

def main():
    df = compute()
    export(df)

if __name__ == "__main__":
    main()
