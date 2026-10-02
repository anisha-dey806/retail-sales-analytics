from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "retail_sales.csv"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)


def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    required = {
        "order_id", "order_date", "customer_id", "product_name", "category",
        "region", "sales_channel", "quantity", "sales", "cost", "profit"
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    total_sales = df["sales"].sum()
    total_profit = df["profit"].sum()
    order_count = df["order_id"].nunique()
    customer_count = df["customer_id"].nunique()
    repeat_customers = df.groupby("customer_id")["order_id"].nunique().gt(1).sum()
    kpis = pd.DataFrame([{
        "total_revenue": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "profit_margin_pct": round(100 * total_profit / total_sales, 2) if total_sales else 0,
        "distinct_orders": int(order_count),
        "distinct_customers": int(customer_count),
        "repeat_customers": int(repeat_customers),
        "average_order_value": round(total_sales / order_count, 2) if order_count else 0,
    }])
    kpis.to_csv(REPORTS / "kpi_summary.csv", index=False)

    monthly = df.groupby("month", as_index=False).agg(
        revenue=("sales", "sum"), profit=("profit", "sum"),
        orders=("order_id", "nunique")
    )
    monthly.to_csv(REPORTS / "monthly_performance.csv", index=False)

    category = df.groupby("category", as_index=False).agg(
        revenue=("sales", "sum"), profit=("profit", "sum")
    )
    category["profit_margin_pct"] = (100 * category["profit"] / category["revenue"]).round(2)
    category = category.sort_values("revenue", ascending=False)
    category.to_csv(REPORTS / "category_performance.csv", index=False)

    region = df.groupby("region", as_index=False).agg(
        revenue=("sales", "sum"), profit=("profit", "sum"),
        orders=("order_id", "nunique")
    ).sort_values("revenue", ascending=False)
    region.to_csv(REPORTS / "regional_performance.csv", index=False)

    customers = df.groupby("customer_id", as_index=False).agg(
        orders=("order_id", "nunique"), total_spend=("sales", "sum")
    ).sort_values("total_spend", ascending=False)
    customers.head(20).to_csv(REPORTS / "top_20_customers.csv", index=False)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly["month"], monthly["revenue"], marker="o", label="Revenue")
    ax.plot(monthly["month"], monthly["profit"], marker="o", label="Profit")
    ax.set_title("Monthly Revenue and Profit (Synthetic Sample Data)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS / "monthly_revenue_profit.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=category, x="revenue", y="category", ax=ax)
    ax.set_title("Revenue by Product Category (Synthetic Sample Data)")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Category")
    fig.tight_layout()
    fig.savefig(REPORTS / "category_revenue.png", dpi=160)
    plt.close(fig)

    print("Analysis completed successfully.")
    print(f"Rows analyzed: {len(df):,}")
    print(f"Reports saved to: {REPORTS}")
    print(kpis.to_string(index=False))


if __name__ == "__main__":
    main()
