import pandas as pd

def loadData(filepath):
    """Load transaction data from a CSV file."""
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df

def cleanData(dataFile):
    """Drop rows with missing values in 'date', 'category', or 'value', ensure correct types"""
    dataFile = dataFile.dropna(subset=["date", "category", "value"])
    dataFile["value"] = dataFile["value"].astype(float)
    return dataFile

def summaryByCategory(dataFile):
    """Summarize total value by category."""
    summary = dataFile.groupby("category")["value"].sum().sort_values(ascending=False)
    return summary

def summaryByMonth(dataFile):
    """Summarize total value by month."""
    dataFile["month"] = dataFile["date"].dt.to_period("M")
    summary = dataFile.groupby("month")["value"].sum()
    return summary

def topTransactions(dataFile, n=5):
    """Returns the largest individual transactions."""
    toptransactions = dataFile.sort_values("value", ascending=False).head(n)
    return toptransactions

def CompareMonths(dataFile, month1, month2):
    """Compare total values between two specified months."""
    dataFile["month"] = dataFile["date"].dt.to_period("M").astype(str)
    month1Data = dataFile[dataFile["month"] == month1]
    month2Data = dataFile[dataFile["month"] == month2]
    
    totalMonth1 = month1Data["value"].sum()
    totalMonth2 = month2Data["value"].sum()
    
    difference = totalMonth2 - totalMonth1

    if difference > 0:
        print(f"You spent ${difference:.2f} MORE in {month2} than in {month1}.")
    elif difference < 0:
        print(f"You spent ${-difference:.2f} LESS in {month2} than in {month1}.")
    else:
        print(f"You spent the same amount in {month1} and {month2}.")

    month1CategorySummary = month1Data.groupby("category")["value"].sum()
    month2CategorySummary = month2Data.groupby("category")["value"].sum()

    allCategories = set(month1CategorySummary.index) | set(month2CategorySummary.index)
    print("\n Category-wise Comparison:")
    for category in sorted(allCategories):
        value1 = month1CategorySummary.get(category, 0)
        value2 = month2CategorySummary.get(category, 0)
        change = value2 - value1
        if change > 0:
            print(f"  {category}: ${change:.2f} more in {month2}")
        elif change < 0:
            print(f"  {category}: ${-change:.2f} less in {month2}")
        else:
            print(f"  {category}: Same amount in both months")


if __name__ == "__main__":
    # Example usage
    data = loadData("transactions.csv")
    cleanedData = cleanData(data)
    
    categorySummary = summaryByCategory(cleanedData)
    print("Summary by Category:")
    print(categorySummary)
    
    monthSummary = summaryByMonth(cleanedData)
    print("\nSummary by Month:")
    print(monthSummary)

    topTransactions = topTransactions(cleanedData)
    print("\nTop Transactions:")
    print(topTransactions)

    CompareMonths(cleanedData, "2026-01", "2026-02")
