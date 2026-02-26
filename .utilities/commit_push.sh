#!/usr/bin/env bash
set -e

MESSAGE="${1:-Saved}"

# Check for changes
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit."
    exit 0
fi

git add -A

# Check if anything is actually staged
if git diff --cached --quiet; then
    echo "No staged changes to commit."
    exit 0
fi

git commit -m "$MESSAGE"

# Push, setting upstream if needed
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if git rev-parse --abbrev-ref --symbolic-full-name "@{u}" >/dev/null 2>&1; then
    git push
else
    git push -u origin "$BRANCH"
fi
