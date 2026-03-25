import csv
import base64
import os
import requests
import re
from io import StringIO

SHEET_ID = "1intC0cjTfHtRoSXj2FdH2To8CNy7uT-uhtoUqs0pzE8"
GID = "1919361331"

CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

OUTPUT_DIR = "./"
os.makedirs(OUTPUT_DIR, exist_ok=True)

response = requests.get(CSV_URL)
response.raise_for_status()

csv_data = StringIO(response.text)
reader = csv.reader(csv_data)

rows = list(reader)

data_rows = rows[1:]

BASE64_COL = 1
TITLE_COL = 2
CREATOR_COL = 3
DIFFICULTY_COL = 4
COLOR_COL = 5

output_csv_path = os.path.join(OUTPUT_DIR, "index.csv")

with open(output_csv_path, "w", newline='', encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["id", "title", "creator", "difficulty", "color"])

    for i, row in enumerate(data_rows, start=1):
        try:
            base64_string = row[BASE64_COL]
            title = row[TITLE_COL]
            creator = row[CREATOR_COL]
            difficulty = row[DIFFICULTY_COL]
            color = row[COLOR_COL]

            if color.startswith("#"):
                color = color[1:]

            if "," in base64_string:
                base64_string = base64_string.split(",", 1)[1]

            base64_string = re.sub(r"\s+", "", base64_string)

            missing_padding = len(base64_string) % 4
            if missing_padding:
                base64_string += "=" * (4 - missing_padding)

            decoded = base64.b64decode(base64_string)
            with open(os.path.join(OUTPUT_DIR, f"{i}.scn"), "wb") as f:
                f.write(decoded)

            writer.writerow([i, title, creator, difficulty.lower().replace(' ', '_'), color])

            print(f"Saved {i}.scn")

        except Exception as e:
            print(f"Error on row {i}: {e}")

print("DONE. Files saved locally.")