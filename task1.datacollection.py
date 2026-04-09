"""
TrendPulse Task 1 — Fetch Data from HackerNews API
====================================================
This script fetches the top 500 trending stories from HackerNews,
categorizes them by keywords found in their titles, and saves the
results as a JSON file in the data/ folder.

Author: <Your Name>
Date: <Today's Date>
"""

import requests   # For making HTTP API calls
import json       # For reading/writing JSON data
import os         # For file system operations (creating folders)
import time       # For adding delays between category loops
from datetime import datetime  # For timestamps

# ──────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────

# Base URLs for the HackerNews API (no auth required)
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required header to identify our application to the API
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# How many top story IDs to fetch from the list
MAX_STORY_IDS = 500

# Maximum stories to collect per category
MAX_PER_CATEGORY = 25

# Category-to-keywords mapping (all matching is case-insensitive)
# Each category has a list of keywords; if ANY keyword appears in the
# story title, that story belongs to that category.
CATEGORIES = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
         "war", "government", "country", "president", "election",
        "climate", "attack", "global","US","Iran","Israel"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship","cup","trophy"
    ],
    "science": [
       "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome","lab","paper"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game", "book",
        "show", "award", "streaming"
    ],
}

# ──────────────────────────────────────────────
# STEP 1 — Fetch the list of top story IDs
# ──────────────────────────────────────────────

def fetch_top_story_ids():
    """
    Fetches the top story IDs from HackerNews.
    The API returns a JSON array of up to ~500 integer IDs,
    sorted by popularity. We take the first 500.
    Returns a list of story IDs, or an empty list on failure.
    """
    print("Fetching top story IDs from HackerNews...")
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        story_ids = response.json()  # Parse the JSON array of IDs

        # Take only the first 500 IDs (as required by the task)
        story_ids = story_ids[:MAX_STORY_IDS]
        print(f"Successfully fetched {len(story_ids)} story IDs.")
        return story_ids

    except requests.exceptions.RequestException as e:
        # Handle any network/HTTP errors gracefully — don't crash
        print(f"[ERROR] Failed to fetch top story IDs: {e}")
        return []

# ──────────────────────────────────────────────
# STEP 2 — Fetch each story's details
# ──────────────────────────────────────────────

def fetch_story_details(story_id):
    """
    Fetches the full details of a single story by its ID.
    Returns the story dict if successful, or None on failure.
    Each story object contains fields like: id, title, score,
    descendants (comment count), by (author), url, etc.
    """
    try:
        url = ITEM_URL.format(story_id)
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        story = response.json()

        # Some items might be deleted or None — handle that
        if story is None:
            print(f"  [WARN] Story {story_id} returned None (may be deleted). Skipping.")
            return None

        return story

    except requests.exceptions.RequestException as e:
        # Print a message and skip this story — don't crash the script
        print(f"  [ERROR] Failed to fetch story {story_id}: {e}")
        return None

def fetch_all_stories(story_ids):
    """
    Fetches details for ALL story IDs in the list.
    Returns a list of story dicts (excluding any that failed).
    This is done BEFORE categorization so we only hit the API once
    per story, regardless of how many categories we check.
    """
    print(f"\nFetching details for {len(story_ids)} stories...")
    all_stories = []

    for index, story_id in enumerate(story_ids):
        story = fetch_story_details(story_id)

        if story is not None:
            all_stories.append(story)

        # Print progress every 50 stories so the user knows it's working
        if (index + 1) % 50 == 0:
            print(f"  Progress: {index + 1}/{len(story_ids)} stories fetched...")

    print(f"Successfully fetched {len(all_stories)} story details out of {len(story_ids)}.")
    return all_stories

# ──────────────────────────────────────────────
# STEP 3 — Categorize stories and extract fields
# ──────────────────────────────────────────────

def matches_category(title, keywords):
    """
    Checks if a story title contains ANY of the given keywords.
    Matching is case-insensitive. We convert the title to lowercase
    and check each keyword (also lowered) against it.
    Returns True if at least one keyword is found in the title.
    """
    title_lower = title.lower()
    for keyword in keywords:
        # Check if the keyword appears anywhere in the title
        if keyword.lower() in title_lower:
            return True
    return False

def extract_story_fields(story, category):
    """
    Extracts the required fields from a raw HackerNews story object
    and returns a clean dict with the exact keys needed for output.
    Uses .get() with defaults to handle missing fields gracefully.
    """
    return {
        "post_id": story.get("id", None),                  # Unique story ID
        "title": story.get("title", "Untitled"),            # Story title
        "category": category,                                # Our assigned category
        "score": story.get("score", 0),                     # Number of upvotes
        "num_comments": story.get("descendants", 0),        # Number of comments
        "author": story.get("by", "unknown"),                # Username of the poster
        "collected_at": datetime.now().isoformat(),          # Current timestamp (ISO format)
    }

def categorize_stories(all_stories):
    """
    Loops through each category and its keywords, then checks every
    fetched story to see if its title matches. Collects up to 25
    stories per category. A story is only assigned to the FIRST
    matching category (tracked via a set of seen IDs to avoid duplicates).

    Uses time.sleep(2) between each category loop as required.
    """
    collected_stories = []       # Final list of categorized story dicts
    seen_ids = set()             # Track which story IDs are already categorized

    print("\nCategorizing stories...\n")

    for category_index, (category, keywords) in enumerate(CATEGORIES.items()):
        # Add a 2-second delay between categories (not before the first one)
        if category_index > 0:
            print("  Waiting 2 seconds before next category...")
            time.sleep(2)

        print(f"Processing category: '{category}' (keywords: {keywords})")
        count = 0  # Track how many stories we've collected for this category

        for story in all_stories:
            # Stop once we have 25 stories for this category
            if count >= MAX_PER_CATEGORY:
                break

            story_id = story.get("id")
            title = story.get("title", "")

            # Skip stories that are already assigned to a previous category
            if story_id in seen_ids:
                continue

            # Skip stories with no title (can't categorize them)
            if not title:
                continue

            # Check if the title matches any keyword for this category
            if matches_category(title, keywords):
                # Extract the required fields and add to our collection
                extracted = extract_story_fields(story, category)
                collected_stories.append(extracted)
                seen_ids.add(story_id)  # Mark this story as used
                count += 1

        print(f"  → Collected {count} stories for '{category}'")

    print(f"\nTotal stories categorized: {len(collected_stories)}")
    return collected_stories

# ──────────────────────────────────────────────
# STEP 4 — Save results to a JSON file
# ──────────────────────────────────────────────

def save_to_json(stories):
    """
    Saves the collected stories to a JSON file inside the data/ folder.
    The filename includes today's date in YYYYMMDD format.
    Creates the data/ folder if it doesn't already exist.
    """
    # Create the data/ directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Build the filename with today's date (e.g., trends_20260409.json)
    today_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{today_str}.json"

    # Write the list of story dicts to the JSON file with nice formatting
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)

    # Print the summary message (matches expected output format)
    print(f"\nCollected {len(stories)} stories. Saved to {filename}")

    return filename

# ──────────────────────────────────────────────
# MAIN — Orchestrate the full pipeline
# ──────────────────────────────────────────────

def main():
    """
    Main function that runs the full Task 1 pipeline:
    1. Fetch top 500 story IDs from HackerNews
    2. Fetch details for each story
    3. Categorize stories by title keywords (up to 25 per category)
    4. Save the results to a JSON file in data/
    """
    print("=" * 60)
    print("  TrendPulse Task 1 — Data Collection")
    print("=" * 60)

    # Step 1: Get the top story IDs
    story_ids = fetch_top_story_ids()
    if not story_ids:
        print("No story IDs fetched. Exiting.")
        return

    # Step 2: Fetch full details for each story
    all_stories = fetch_all_stories(story_ids)
    if not all_stories:
        print("No story details fetched. Exiting.")
        return

    # Step 3: Categorize stories and extract required fields
    categorized = categorize_stories(all_stories)

    # Step 4: Save to JSON file
    if categorized:
        save_to_json(categorized)
    else:
        print("No stories matched any category. Nothing to save.")

    print("\nDone!")

# Entry point — only runs when the script is executed directly
if __name__ == "__main__":
    main()