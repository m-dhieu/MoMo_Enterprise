#!/bin/bash

#------------------------------------------------------------------------------
# Script Name: setup_project.sh
# Description: Creates the MoMo SMS Processing project directory and file structure.
# Author: Thierry Gabin & Santhiana Kaze
# Date:   2025-09-09
# Usage:  ./setup_project.sh
#------------------------------------------------------------------------------

set -euo pipefail

echo "Starting project directory and file structure creation..."

# Directories to create
dirs=(
  "web/assets/"
  "data/raw"
  "data/processed"
  "data/db"
  "data/logs/dead_letter"
  "etl"
  "api"
  "scripts"
  "tests"
)

# Create directories
for dir in "${dirs[@]}"; do
  if [[ ! -d "$dir" ]]; then
    mkdir -p "$dir"
    echo "Created directory: $dir"
  else
    echo "Directory already exists: $dir"
  fi
done

# Files to create (empty if not exist)
files=(
  ".env"
  "requirements.txt"
  "index.html"

  "web/styles.css"
  "web/chart_handler.js"

  "data/raw/momo.xml"
  "data/processed/dashboard.json"
  "data/logs/etl.log"

  "etl/__init__.py"
  "etl/config.py"
  "etl/parse_xml.py"
  "etl/clean_normalize.py"
  "etl/categorize.py"
  "etl/load_db.py"
  "etl/run.py"

  "api/__init__.py"
  "api/app.py"
  "api/db.py"
  "api/schemas.py"

  "scripts/run_etl.sh"
  "scripts/export_json.sh"
  "scripts/serve_frontend.sh"

  "tests/test_parse_xml.py"
  "tests/test_clean_normalize.py"
  "tests/test_categorize.py"
)

# Function to add inline comment content for specific files
function add_file_comment() {
  local file=$1
  local content=$2
  # Only add content if file empty or missing
  if [[ ! -f "$file" || ! -s "$file" ]]; then
    echo -e "$content" > "$file"
    echo "Initialized file with comment: $file"
  else
    echo "File already exists and not empty: $file"
  fi
}

# Create files
for file in "${files[@]}"; do
  if [[ ! -f "$file" ]]; then
    touch "$file"
    echo "Created file: $file"
  else
    echo "File already exists: $file"
  fi
done

# Add comments to files
add_file_comment "README.md" "# MoMo SMS Processing Application\n# Setup, run overview."
add_file_comment "CONTRIBUTING.md" "# Contribution Guidelines\n# PRs, branching, and issues guide."
add_file_comment "etl/config.py" "# Configuration file\n# File paths, thresholds, categories."
add_file_comment "etl/parse_xml.py" "# XML parsing module\n# Uses ElementTree/lxml."
add_file_comment "etl/clean_normalize.py" "# Data cleaning and normalization\n# Amounts, dates, phone normalization."
add_file_comment "etl/categorize.py" "# Transaction categorization logic\n# Rules for payment, withdrawal, transfer types."
add_file_comment "etl/load_db.py" "# Database load module\n# Creates tables and supports upserts into SQLite/PostgreSQL."
add_file_comment "etl/run.py" "# Main ETL run script\n# Parses, cleans, categorizes, loads data and exports JSON."
add_file_comment "api/app.py" "# FastAPI app\n# Exposes /transactions and /analytics endpoints."
add_file_comment "api/db.py" "# SQLite connection and helpers."
add_file_comment "api/schemas.py" "# Pydantic models for API response schemas."
add_file_comment "scripts/run_etl.sh" "# Shell wrapper to run the ETL pipeline\npython etl/run.py --xml data/raw/momo.xml"
add_file_comment "scripts/export_json.sh" "# Export processed JSON for frontend dashboard."
add_file_comment "scripts/serve_frontend.sh" "# Serve static frontend via simple HTTP server or Flask."
add_file_comment "tests/test_parse_xml.py" "# Unit tests for XML parsing."
add_file_comment "tests/test_clean_normalize.py" "# Unit tests for data cleaning and normalization."
add_file_comment "tests/test_categorize.py" "# Unit tests for transaction categorization."

echo "Project structure setup complete."
