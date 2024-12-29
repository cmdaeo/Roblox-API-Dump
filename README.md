# Automatic Roblox API Dumper

This repository contains an automated system for fetching and processing the Roblox API dump on a weekly basis. It uses GitHub Actions to run a Python script that retrieves the latest API information and stores it in a structured JSON format.

## Features

- Automatically fetches the latest Roblox API version hash
- Downloads and processes the API dump
- Extracts relevant data including Properties, DataTypes, Enums, and Class Hierarchy
- Runs weekly via GitHub Actions
- Stores results in version-specific JSON files

## How It Works

1. A GitHub Action is scheduled to run every Sunday at 00:00 UTC.
2. The action executes a Python script that:
   - Fetches the current Roblox API version hash
   - Downloads the corresponding API dump
   - Processes the dump to extract relevant information
   - Saves the processed data in a JSON file named with the version hash
3. If changes are detected, the action commits and pushes the new file to the repository

## Repository Structure

- `/.github/workflows/weekly_api_fetch.yml`: GitHub Actions workflow file
- `/script.py`: Python script for fetching and processing the API dump
- `/*.json`: Generated JSON files containing processed API data

## Usage

The data in this repository is automatically updated weekly. To use the latest data in your project:

1. Clone this repository or download the most recent JSON file
2. Parse the JSON file in your application to access the structured Roblox API data

## Contributing

Contributions to improve the script or extend the functionality are welcome. Please submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by Roblox Corporation. All Roblox-related trademarks and copyrights are the property of Roblox Corporation.
