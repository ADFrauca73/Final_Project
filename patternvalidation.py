import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("vizzes", exist_ok=True)

# Load data
df = pd.read_csv("transactions.csv")

# Preprocessing
df["Start_date"] = pd.to_datetime(df["Start_date"], errors="coerce")
df["TransactionMonth"] = pd.to_datetime(df["TransactionMonth"], format="%Y-%m", errors="coerce")
df["Profit"] = df["Agency_fee"] - (df["Agency_hours"] * 30)

def get_region(dest):
    dest = str(dest)
    if any(x in dest for x in ["France", "Italy", "Spain", "Iceland"]):
        return "Europe"
    if any(x in dest for x in ["Thailand", "Japan", "Indonesia"]):
        return "Asia"
    if "Peru" in dest:
        return "Americas"
    if "South Africa" in dest:
        return "Africa"
    return "Other"

df["Region"] = df["Destination"].apply(get_region)

#------------------------------
# KPI CHECKS
#------------------------------
# Profit over time
profit_time = df.groupby(df["TransactionMonth"].dt.to_period("M"))["Profit"].mean()
plt.figure()
profit_time.plot()
plt.title("Average Profit Declines Over Time")
plt.xlabel("Month")
plt.ylabel("Average Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("vizzes/profit_over_time.png")
plt.show()

# Calculate and print total profit per year and over the entire period
df["Year"] = df["TransactionMonth"].dt.year
profit_per_year = df.groupby("Year")["Profit"].sum()
print("Total Profit Per Year:")
print(profit_per_year)
total_profit = df["Profit"].sum()
print(f"Total Profit Over Entire Period: {total_profit}")

# Number of transactions over time
txn_time = df.groupby(df["TransactionMonth"].dt.to_period("M")).size()
plt.figure()
txn_time.plot()
plt.title("Transaction Volume Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("vizzes/transaction_volume_over_time.png")
plt.show()

# Unique clients
unique_clients = df["Client_ID"].nunique()
print(f"Unique Clients: {unique_clients}")

# ---------------------------------------------
# VALIDATION CHECKS
# ---------------------------------------------
# 1. Popular destinations have lower fees
popularity_proxy = df.groupby("Destination")["Agency_fee"].mean().sort_values()
plt.figure()
popularity_proxy.plot(kind="bar")
plt.title("More Popular Destinations Should Have Lower Agency Fees")
plt.ylabel("Average Agency Fee")
plt.xticks(rotation=75)
plt.tight_layout()
plt.savefig("vizzes/popular_destinations_lower_fees.png")
plt.show()

# 2. Less popular destinations require more hours
hours_by_dest = df.groupby("Destination")["Agency_hours"].mean().sort_values(ascending=False)
plt.figure()
hours_by_dest.plot(kind="bar")
plt.title("Less Popular Destinations Require More Agency Hours")
plt.ylabel("Average Agency Hours")
plt.xticks(rotation=75)
plt.tight_layout()
plt.savefig("vizzes/less_popular_more_hours.png")
plt.show()

# 3. Younger clients pay higher fees
fees_by_age = df.groupby("Client_age_range")["Agency_fee"].mean()
plt.figure()
fees_by_age.plot(kind="bar")
plt.title("Younger Clients Should Be Charged Higher Agency Fees")
plt.ylabel("Average Agency Fee")
plt.tight_layout()
plt.savefig("vizzes/younger_clients_higher_fees.png")
plt.show()

# 4. Older clients require more hours
hours_by_age = df.groupby("Client_age_range")["Agency_hours"].mean()
plt.figure()
hours_by_age.plot(kind="bar")
plt.title("Older Clients Should Require More Agency Hours")
plt.ylabel("Average Agency Hours")
plt.tight_layout()
plt.savefig("vizzes/older_clients_more_hours.png")
plt.show()

# 5. Shift from Europe to Asia over time
region_time = df.groupby([df["TransactionMonth"].dt.to_period("M"), "Region"]).size().unstack(fill_value=0)
plt.figure()
region_time[["Europe", "Asia"]].plot()
plt.title("Travel Should Shift from Europe to Asia Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Trips")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("vizzes/region_shift_europe_asia.png")
plt.show()

# 6. Booking timing before peak season
lead_time = (df["Start_date"] - df["TransactionMonth"]).dt.days
plt.figure()
lead_time.hist(bins=30)
plt.title("Transactions Should Cluster Around ~3 Months Before Travel")
plt.xlabel("Lead Time (Days)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("vizzes/booking_lead_time.png")
plt.show()

# 7. Profitability trend
plt.figure()
df.groupby(df["TransactionMonth"].dt.to_period("M"))["Profit"].mean().plot()
plt.title("Transactions Are Becoming Less Profitable Over Time")
plt.xlabel("Month")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("vizzes/profitability_trend.png")
plt.show()

# 8. Travelers vs complaints proxy (group size)
plt.figure()
df.groupby("Number_of_travelers")["Agency_hours"].mean().plot()
plt.title("Larger Groups Should Require More Coordination (Proxy via Agency Hours)")
plt.xlabel("Number of Travelers")
plt.ylabel("Average Agency Hours")
plt.tight_layout()
plt.savefig("vizzes/group_size_vs_hours.png")
plt.show()


print("Visualization generation complete.")
