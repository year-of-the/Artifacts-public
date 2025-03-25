#!/bin/bash

CURRENT_BRANCH=$(git symbolic-ref --short HEAD)
TEMP_BRANCH="temp-public-push"
PUBLIC_REMOTE="public"

git branch -D $TEMP_BRANCH 2>/dev/null || true

git checkout -b $TEMP_BRANCH

PRIVATE_FILES=$(git ls-files "*.private.py")

if [ -n "$PRIVATE_FILES" ]; then
    for file in $PRIVATE_FILES; do
        git rm --cached "$file"
    done
    git commit -m "Temporary commit to remove private files for public push"
fi

git push -f public $TEMP_BRANCH:$CURRENT_BRANCH

git checkout $CURRENT_BRANCH

git branch -D $TEMP_BRANCH