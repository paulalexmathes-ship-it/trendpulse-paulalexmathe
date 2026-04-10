from numpy import dtype
from pathlib import Path
import pandas as pd


# Load the raw JSON file from the data/ folder into a DataFrame
file_path = Path("C:/Users/mathepm/Documents/trendpulse/data/trends_20260409.json")
df = pd.read_json(file_path)

# Print how many rows were loaded
print(f"Loaded {len(df)} rows from data/trends_20260409.json")


# Store the initial count for comparison later
rows_before = len(df)

# Step 1: Remove duplicate rows based on 'post_id'
df = df.drop_duplicates(subset='post_id',keep='first')
print(f"After removing duplicates:       {len(df)} rows")

# Step 2: Drop rows where post_id, title, or score is missing
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After dropping missing values:   {len(df)} rows")

# Step 3: Fix data types — score and num_comments as integers
# Fill any remaining NaN in num_comments with 0 before converting
df["num_comments"] = df["num_comments"].fillna(0)

# Use pd.to_numeric to safely coerce any non-numeric values, then convert to int
df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

print(f"After fixing data types:         {len(df)} rows")

# Step 4: Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low quality:      {len(df)} rows")

# Step 5: Strip extra whitespace from the 'title' column
df["title"] = df["title"].str.strip()
print(f"After stripping whitespace:      {len(df)} rows")

# Print final summary of cleaning
rows_after = len(df)
rows_removed = rows_before - rows_after
print("-" * 50)
print(f"Cleaning complete — {rows_after} rows remaining ({rows_removed} rows removed)")
print("-" * 50)

# TASK 3 — Save as CSV (6 marks)
# Define the output file path
output_path = "data/trends_clean.csv"

# Save the cleaned DataFrame to CSV (without the default index column)
df.to_csv(output_path, index=False)

# Print confirmation message with row count
print(f"Saved {len(df)} clean rows to '{output_path}'")
print("-" * 50)

# Print a quick summary — number of stories per category
category_counts = df["category"].value_counts()
for category, count in category_counts.items():
    print(f"  {category:<20} → {count} stories")

print("=" * 35)
print(f"  {'TOTAL':<20} → {len(df)} stories")