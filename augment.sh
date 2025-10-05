#!/bin/bash

DATA_DIR="data"
# Get the first CSV file (alphabetically or numerically sorted)
first_csv=$(ls -v "$DATA_DIR"/*.csv | head -n 1)

# Loop over all CSVs except the first one
for csv_file in $(ls -v "$DATA_DIR"/*.csv | tail -n +2); do
    # Skip the header and append the rest to the first CSV
    tail -n +2 "$csv_file" >> "$first_csv"
    # Delete the processed file
    rm "$csv_file"
done

# Rename the merged first file to data.csv
mv "$first_csv" "$DATA_DIR/data.csv"

echo "All CSVs merged into $first_csv. Other CSVs deleted."

