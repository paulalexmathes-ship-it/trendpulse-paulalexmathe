# Task 4 — Data Visualization with Matplotlib

# This script loads the analysed CSV from Task 3, creates 3
# individual charts and a combined dashboard, then saves
# everything as PNG files in the outputs/ folder.

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

# Load the analysed CSV file into a DataFrame

file_path = Path("C:/Users/mathepm/Documents/trendpulse/data/trends_analysed.csv")
df = pd.read_csv(file_path)
print(f"Loaded data: {df.shape[0]} rows, {df.shape[1]} columns")

# Create the outputs/ folder if it doesn't already exist
os.makedirs("outputs", exist_ok=True)
print("outputs/ folder ready")


#TASK 2 — Chart 1: Top 10 Stories by Score

# Sort by score descending and take the top 10
top_10=df.nlargest(10, 'score').copy()

#Makes the title shorted to <50 Characters if it is more than 50 Characters

top_10["short_title"] = top_10["title"].apply(lambda t: t[:47]+"..." if len(str(t)) > 50 else t)
# Create the horizontal bar chart
fig1, ax1 = plt.subplots(figsize=(12, 7))

# Plot bars (reversed so highest score appears at the top)
bars = ax1.barh(
    top_10["short_title"].iloc[::-1],
    top_10["score"].iloc[::-1],
    color="#2196F3",
    edgecolor="white",
    height=0.6
)
# Add score labels at the end of each bar
for bar in bars:
    width = bar.get_width()
    ax1.text(
        width + max(top_10["score"]) * 0.01,
        bar.get_y() + bar.get_height() / 2,
        f"{int(width):,}",
        va="center",
        fontsize=9,
        fontweight="bold"
    )
# Title and axis labels
ax1.set_title("Top 10 Stories by Score", fontsize=16, fontweight="bold", pad=15)
ax1.set_xlabel("Score", fontsize=12)
ax1.set_ylabel("Story Title", fontsize=12)

# Clean up layout
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
plt.tight_layout()  


# IMPORTANT: savefig BEFORE show
plt.savefig("outputs/chart1_top_stories.png", dpi=150, bbox_inches="tight")
plt.show()

print("Saved: outputs/chart1_top_stories.png")

# TASK 3 — Chart 2: Stories per Category

# Count the number of stories in each category
category_counts = df["category"].value_counts()

# Define a distinct colour palette for each bar
colours = [
    "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
    "#9966FF", "#FF9F40", "#C9CBCF", "#7BC67E",
    "#E77C8E", "#55BFC7", "#FFB347", "#B39DDB"
]
# Slice to match the number of categories
bar_colours = colours[:len(category_counts)]

# Create the bar chart
fig2, ax2 = plt.subplots(figsize=(10, 6))

bars2 = ax2.bar(
    category_counts.index,
    category_counts.values,
    color=bar_colours,
    edgecolor="white",
    width=0.6
)
# Add count labels on top of each bar
for bar in bars2:
    height = bar.get_height()
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.3,
        str(int(height)),
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold"
    )
# Title and axis labels
ax2.set_title("Stories per Category", fontsize=16, fontweight="bold", pad=15)
ax2.set_xlabel("Category", fontsize=12)
ax2.set_ylabel("Number of Stories", fontsize=12)

# Rotate x-axis labels if they overlap
plt.xticks(rotation=30, ha="right")

# Clean up layout
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
plt.tight_layout()


plt.savefig("outputs/chart2_categories.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved: outputs/chart2_categories.png")

# TASK 4 — Chart 3: Score vs Comments Scatter Plot
# Separate popular and non-popular stories using the is_popular column
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

# Create the scatter plot
fig3, ax3 = plt.subplots(figsize=(10, 7))

# Plot non-popular stories first (background layer)
ax3.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    c="#90CAF9",
    label="Not Popular",
    alpha=0.6,
    edgecolors="white",
    s=60
)

# Plot popular stories on top (foreground layer)
ax3.scatter(
    popular["score"],
    popular["num_comments"],
    c="#E53935",
    label="Popular",
    alpha=0.8,
    edgecolors="white",
    s=80
)

ax3.set_title("Score vs Number of Comments", fontsize=16, fontweight="bold", pad=15)
ax3.set_xlabel("Score", fontsize=12)
ax3.set_ylabel("Number of Comments", fontsize=12)
ax3.legend(title="Story Status", fontsize=10, title_fontsize=11)

# Clean up layout
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
plt.tight_layout()

plt.savefig("outputs/chart3_scatter.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved: outputs/chart3_scatter.png")

# BONUS — Dashboard: All 3 Charts Combined (+3 marks)

# Create a figure with 1 row and 3 columns for the dashboard layout
fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(24, 7))

# Add an overall dashboard title
fig.suptitle("TrendPulse Dashboard", fontsize=22, fontweight="bold", y=1.02)

# --- Dashboard Panel 1: Top 10 Stories (horizontal bar chart) ---
top10_rev = top_10.iloc[::-1]
ax_a.barh(
    top10_rev["short_title"],
    top10_rev["score"],
    color="#2196F3",
    edgecolor="white",
    height=0.6
)

ax_a.set_title("Top 10 Stories by Score", fontsize=13, fontweight="bold")
ax_a.set_xlabel("Score", fontsize=10)
ax_a.spines["top"].set_visible(False)
ax_a.spines["right"].set_visible(False)

# --- Dashboard Panel 2: Stories per Category (bar chart) ---
ax_b.bar(
    category_counts.index,
    category_counts.values,
    color=bar_colours,
    edgecolor="white",
    width=0.6
)
ax_b.set_title("Stories per Category", fontsize=13, fontweight="bold")
ax_b.set_xlabel("Category", fontsize=10)
ax_b.set_ylabel("Count", fontsize=10)
ax_b.tick_params(axis="x", rotation=30)
ax_b.spines["top"].set_visible(False)
ax_b.spines["right"].set_visible(False)

# --- Dashboard Panel 3: Score vs Comments (scatter plot) ---

ax_c.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    c="#90CAF9",
    label="Not Popular",
    alpha=0.6,
    edgecolors="white",
    s=50
)
ax_c.scatter(
    popular["score"],
    popular["num_comments"],
    c="#E53935",
    label="Popular",
    alpha=0.8,
    edgecolors="white",
    s=60
)

ax_c.set_title("Score vs Comments", fontsize=13, fontweight="bold")
ax_c.set_xlabel("Score", fontsize=10)
ax_c.set_ylabel("Comments", fontsize=10)
ax_c.legend(fontsize=9)
ax_c.spines["top"].set_visible(False)
ax_c.spines["right"].set_visible(False)

# Adjust spacing between subplots
plt.tight_layout()

# IMPORTANT: savefig BEFORE show
plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved: outputs/dashboard.png")
# Final Summary

print("=" * 70)
print("All visualizations saved successfully!")
print("=" * 70)
print("  outputs/chart1_top_stories.png  — Top 10 bar chart")
print("  outputs/chart2_categories.png   — Category bar chart")
print("  outputs/chart3_scatter.png      — Score vs Comments scatter")
print("  outputs/dashboard.png           — Combined dashboard")
print("=" * 70)


