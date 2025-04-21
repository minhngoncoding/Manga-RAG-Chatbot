import os
import csv
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini"
INPUT_FILE = "data/raw/manga.csv"
OUTPUT_FILE = "data/processed/processed_manga.csv"
PROCESSED_DIR = "data/processed"

# Ensure the processed directory exists
if not os.path.exists(PROCESSED_DIR):
    os.makedirs(PROCESSED_DIR)

# Check API key
if not API_KEY:
    raise ValueError("Failed to load API key. Please check your .env file.")
openai.api_key = API_KEY

# Read and process the input file
processed_data = []
try:
    with open(INPUT_FILE, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            if idx >= 15:  # Limit to the first 100 rows
                break

            manga_info = f"Title: {row['Title']}"
            messages = [
                {"role": "system", "content": "You are a manga expert."},
                {
                    "role": "user",
                    "content": f"Provide a summary and analysis for the following manga:\n\n{manga_info}",
                },
            ]

            try:
                response = openai.chat.completions.create(
                    model=MODEL_NAME, messages=messages, max_tokens=500
                )
                summary = response.choices[0].message.content
                row["summary"] = summary
                processed_data.append(row)
            except Exception as e:
                print(f"Error processing row '{row['Title']}': {e}")

    # Save the processed data to a new CSV
    with open(OUTPUT_FILE, "w", newline="") as csvfile:
        fieldnames = list(processed_data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)

    print(f"Processed data saved to {OUTPUT_FILE}")

except FileNotFoundError:
    print(f"Input file '{INPUT_FILE}' not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
