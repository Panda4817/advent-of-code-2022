#!/bin/bash

# Ensure a valid year is passed as an argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <year>"
  exit 1
fi

YEAR=$1

# Loop through all the days (1 to 25)
for DAY in $(seq 1 25); do
  # Ensure that the day is two digits (e.g., 01, 02, ..., 25)
  DAY_FORMATTED=$(printf "%02d" $DAY)

  # Run the Python command for the given year and day
  # Change python command if needed for your setup
  echo "Running: python3.12 main.py -y $YEAR -d $DAY_FORMATTED"
  python3.12 main.py -y $YEAR -d $DAY_FORMATTED

  # Check if the command was successful
  if [ $? -eq 0 ]; then
    echo "Successfully ran for year $YEAR, day $DAY_FORMATTED."
  else
    echo "Failed to run for year $YEAR, day $DAY_FORMATTED."
  fi
done
