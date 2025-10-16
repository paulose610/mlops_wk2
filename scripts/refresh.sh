#!/bin/bash

# This script will completely delete the Git history, remove all remote tags,
# delete all DVC-related files, create a fresh initial commit, and force-push
# to the remote repository.
#
# ⚠️ WARNING: THIS IS A DESTRUCTIVE OPERATION. ⚠️
# It will permanently overwrite the history on the remote repository.
# Ensure you have backed up any important information before proceeding.

# --- Configuration ---
REMOTE_URL="git@github.com:paulose610/mlops_wk2.git"

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Safety Check ---
read -p "Are you sure you want to permanently delete the Git history, DVC files, and all remote tags? (y/N) " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Operation cancelled."
    exit 1
fi

# --- Main Logic ---

echo "## 1️⃣ Listing current directory contents..."
ls -larth

echo "## 2️⃣ Deleting local Git history..."
rm -rf .git

echo "## 3️⃣ Deleting all DVC-related files..."
rm -rf .dvc          # DVC directory
rm -f .dvcignore     # DVC ignore file
rm -f *.dvc          # Any individual .dvc files (like data.dvc)

echo "## 4️⃣ Re-initializing Git repository..."
git init

echo "## 5️⃣ Staging all files..."
git add .

echo "## 6️⃣ Creating a new initial commit..."
git commit -m "Initial commit - fresh start"

echo "## 7️⃣ Renaming the local branch to 'main'..."
git branch -M main

echo "## 8️⃣ Connecting to the remote repository..."
git remote add origin "$REMOTE_URL"

echo "## 9️⃣ Deleting all remote tags..."
git fetch --tags
for tag in $(git ls-remote --tags origin | awk '{print $2}' | sed 's#refs/tags/##'); do
    echo "Deleting remote tag: $tag"
    git push --delete origin "$tag"
done

echo "## 🔟 Force-pushing the main branch..."
git push -u --force origin main

echo "✅ Success! Git history, DVC files, and all remote tags have been reset."

