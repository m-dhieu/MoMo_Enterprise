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

# Create files
for file in "${files[@]}"; do
  if [[ ! -f "$file" ]]; then
    touch "$file"
    echo "Created file: $file"
  else
    echo "File already exists: $file"
  fi
done

# Populate files with comments
cat <<EOL > requirements.txt
# lxml/ElementTree, dateutil, FastAPI
EOL
cat <<EOL > index.html
# Dashboard entry (static)
EOL
cat <<EOL > etl/config.py 
# Configuration file\n# File paths, thresholds, categories.
EOL
cat <<EOL > etl/parse_xml.py 
# XML parsing module\n# Uses ElementTree/lxml.
EOL
cat <<EOL > etl/clean_normalize.py 
# Data cleaning and normalization\n# Amounts, dates, phone normalization.
EOL
cat <<EOL > etl/categorize.py 
# Transaction categorization logic\n# Rules for payment, withdrawal, transfer types.
EOL
cat <<EOL > etl/load_db.py 
# Database load module.
# Creates tables and supports upserts into SQLite/PostgreSQL.
EOL
cat <<EOL > etl/run.py 
# Main ETL run script\n# Parses, cleans, categorizes, loads data and exports JSON.
EOL
cat <<EOL > api/app.py
# FastAPI app\n# Exposes /transactions and /analytics endpoints.
EOL
cat <<EOL > api/db.py
# SQLite connection and helpers.
EOL
cat <<EOL > api/schemas.py
# Pydantic models for API response schemas.
EOL
cat <<EOL > scripts/run_etl.sh
# Shell wrapper to run the ETL pipeline\npython etl/run.py --xml data/raw/momo.xml
EOL
cat <<EOL > scripts/export_json.sh
# Export processed JSON for frontend dashboard.
EOL
cat <<EOL > scripts/serve_frontend.sh
# Serve static frontend via simple HTTP server or Flask.
EOL
cat <<EOL > tests/test_parse_xml.py
# Unit tests for XML parsing.
EOL
cat <<EOL > tests/test_clean_normalize.py
# Unit tests for data cleaning and normalization.
EOL
cat <<EOL > tests/test_categorize.py
# Unit tests for transaction categorization.
EOL

echo "Project structure setup complete."
