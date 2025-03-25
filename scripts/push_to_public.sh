#!/bin/bash

CURRENT_BRANCH=$(git symbolic-ref --short HEAD)
TEMP_BRANCH="temp-public-push-$(date +%s)"
PUBLIC_REMOTE="public"
LAST_COMMIT_MSG=$(git log -1 --pretty=%B)

git stash push --include-untracked --quiet
git checkout -b $TEMP_BRANCH

PRIVATE_FILES=$(git ls-files "*.private.py")

if [ -n "$PRIVATE_FILES" ]; then
    for file in $PRIVATE_FILES; do
        git rm --cached "$file"
    done
    git commit -m "$LAST_COMMIT_MSG"
fi

git push -f $PUBLIC_REMOTE $TEMP_BRANCH:$CURRENT_BRANCH
git checkout $CURRENT_BRANCH
git stash pop --quiet
git branch -D $TEMP_BRANCH 2>/dev/null || echo "Note: Could not delete temporary branch. This is OK."