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
