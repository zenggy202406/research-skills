#!/bin/bash
# Run this script from the research-skills directory on your local machine.
# Prerequisites: git installed, GitHub account ready, GitHub CLI (gh) or SSH key configured.

set -e

echo "=== Step 1: Clean up nested .git from paper-mentor ==="
rm -rf plugins/paper-pipeline/skills/paper-mentor/.git
echo "Done."

echo ""
echo "=== Step 2: Initialize git repo ==="
git init
git add .
git commit -m "feat: initial commit — 3 plugin marketplaces, 15 skills"
echo "Done."

echo ""
echo "=== Step 3: Create GitHub repo and push ==="
echo "Choose one of the following:"
echo ""
echo "Option A — GitHub CLI (recommended):"
echo "  gh repo create research-skills --private --source=. --push"
echo ""
echo "Option B — Manual:"
echo "  1. Create a private repo named 'research-skills' on github.com"
echo "  2. Run:"
echo "     git remote add origin git@github.com:YOUR_USERNAME/research-skills.git"
echo "     git branch -M main"
echo "     git push -u origin main"
echo ""
echo "=== Done! ==="
