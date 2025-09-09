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

echo "Project structure setup complete."
