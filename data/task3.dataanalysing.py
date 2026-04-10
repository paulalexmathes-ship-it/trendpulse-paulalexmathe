# Task 3 — Data Analysis with Pandas & NumPy
# This script loads the cleaned CSV from Task 2, explores the
# data, computes statistics using NumPy, adds new columns,
# and saves the result for Task 4.

import pandas as pd
import numpy as np
from pathlib import Path

# TASK 1 — Load and Explore (4 marks)

# Load the cleaned CSV file into a DataFrame

file_path = Path("C:/Users/mathepm/Documents/trendpulse/data/trends_clean.csv")
df = pd.read_csv(file_path)


# Print the shape of the DataFrame (rows, columns)
print(f"Loaded data with shape: {df.shape}")

# Print the first 5 rows for a quick visual check
print("First 5 rows:")
print(df.head())

# Calculate and print the average score and average num_comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"Average score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

#TASK 2 — Basic Analysis with NumPy
# Convert score and num_comments columns to NumPy arrays
# (ensures we are explicitly using NumPy for calculations

scores_array = np.array(df["score"])
comments_array = np.array(df["num_comments"])

# --- Statistical measures using NumPy ---
mean_score = np.mean(scores_array)
median_score = np.median(scores_array)
std_score = np.std(scores_array)
max_score = np.max(scores_array)
min_score = np.min(scores_array)

#which category has the most number of stories

category_counts=df["category"].value_counts()
top_category=category_counts.idxmax()
top_stories=category_counts.max()

print(f"Most stories in: {top_category} {top_stories} stories")


# --- Which story has the most comments? ---
# Find the index of the row with the maximum num_comments using NumPy
max_comments_idx = np.argmax(comments_array)

# Retrieve the title and comment count for that row

most_commented_title = df.iloc[max_comments_idx]["title"]
most_commented_count = comments_array[max_comments_idx]

print(f'Most commented story: "{most_commented_title}" — {most_commented_count:,} comments')

# TASK 3 — Add New Columns 
# --- engagement column ---
# Formula: num_comments / (score + 1)
# The +1 avoids division by zero and measures discussion per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# --- is_popular column ---

# True if the story's score is above the overall average score, else False
df["is_popular"] = df["score"] > avg_score

# Quick verification: print the new columns for the first 5 rows

print("New columns preview (first 5 rows):")
print(df.head())

# TASK 4 — Save the Result 
# Define the output file path
output_path = "data/trends_analysed.csv"

# Save the updated DataFrame (with new columns) to CSV, no index
df.to_csv(output_path, index=False)

# Print confirmation message
print(f"Saved to {output_path}")
print(f"Total rows: {len(df)} | Total columns: {len(df.columns)}")


