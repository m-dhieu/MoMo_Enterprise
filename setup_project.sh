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
