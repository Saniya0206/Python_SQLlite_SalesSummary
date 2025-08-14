import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect("sales_data.db")

# Make sure the sales table exists (optional safety for a fresh DB)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    sale_date TEXT NOT NULL
);
""")

# Example seed (only if table is empty)
cur.execute("SELECT COUNT(*) FROM sales;")
if cur.fetchone()[0] == 0:
    cur.executemany(
        "INSERT INTO sales (product, quantity, price, sale_date) VALUES (?, ?, ?, ?);",
        [
            ("Shampoo", 10, 120.0, "2025-08-01"),
            ("Shampoo", 7, 120.0, "2025-08-02"),
            ("Conditioner", 5, 150.0, "2025-08-02"),
            ("Conditioner", 9, 150.0, "2025-08-03"),
            ("FaceWash", 12, 90.0, "2025-08-01"),
            ("FaceWash", 4, 90.0, "2025-08-03"),
            ("Serum", 6, 300.0, "2025-08-02"),
            ("Serum", 3, 300.0, "2025-08-03"),
            ("HairOil", 8, 200.0, "2025-08-01"),
            ("HairOil", 5, 200.0, "2025-08-03"),
        ]
    )
    conn.commit()

# Core SQL summary
query = """
SELECT 
    product,
    SUM(quantity) AS total_qty,
    ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC;
"""

df = pd.read_sql_query(query, conn)
print("\n=== Sales Summary by Product ===")
print(df)

# Save summary and charts
df.to_csv("sales_summary_by_product.csv", index=False)

plt.figure()
plt.bar(df["product"], df["total_qty"])
plt.title("Quantity by Product")
plt.xlabel("Product")
plt.ylabel("Total Quantity")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("quantity_by_product.png")

plt.figure()
plt.bar(df["product"], df["revenue"])
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("revenue_by_product.png")

print("\nFiles saved:")
print("- sales_summary_by_product.csv")
print("- quantity_by_product.png")
print("- revenue_by_product.png")
