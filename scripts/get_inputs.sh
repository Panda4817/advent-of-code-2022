#!/bin/bash

# Ensure valid arguments (year and session cookie) are passed
if [ $# -ne 2 ]; then
  echo "Usage: $0 <year> <session_cookie>"
  exit 1
fi

YEAR=$1
COOKIE=$2

# Loop through all the days (1 to 25)
for DAY in $(seq 1 25); do
  # Ensure that the day is two digits (e.g., 01, 02, ..., 25)
  DAY_FORMATTED=$(printf "%02d" $DAY)

  # The file path for the day's input
  FILE_PATH="year${YEAR}/${DAY_FORMATTED}/${DAY_FORMATTED}.txt"

  # URL for the input data
  URL="https://adventofcode.com/${YEAR}/day/${DAY}/input"

  # Fetch the input data using curl (overwrite the file if it exists)
  curl -s -b "session=$COOKIE" $URL -o "$FILE_PATH"

  # Check if the file was successfully created
  if [ -f "$FILE_PATH" ]; then
    # Post-process the file: remove the trailing newline if it exists
    # Use the `truncate` command to remove the newline at the end of the file
    if [ -s "$FILE_PATH" ]; then
      # Strip the last newline if it exists
      truncate -s -1 "$FILE_PATH"
      echo " (Removed trailing newline)"
    fi
    echo " Input data saved to $FILE_PATH"
  else
    echo " Failed to retrieve input data for day ${DAY_FORMATTED}."
  fi
done
