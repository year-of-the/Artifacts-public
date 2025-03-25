#!/bin/bash

CURRENT_BRANCH=$(git symbolic-ref --short HEAD)
PUBLIC_REMOTE="public"
export GIT_INDEX_FILE=.git/index.public.tmp

echo "Pushing to $PUBLIC_REMOTE without *.private.py files..."

git read-tree HEAD
git ls-files "*.private.py" | xargs -r git update-index --force-remove --
TREE=$(git write-tree)
PARENT=$(git rev-parse HEAD)
COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT=$(git commit-tree $TREE -p $PARENT -m "$COMMIT_MSG")
git push $PUBLIC_REMOTE $COMMIT:refs/heads/$CURRENT_BRANCH
rm -f .git/index.public.tmp
unset GIT_INDEX_FILE

echo "Successfully pushed filtered commit to $PUBLIC_REMOTE/$CURRENT_BRANCH"