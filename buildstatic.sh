#!/bin/bash
echo -e "Checking for of static/vendor directory...\t\c"
if [ -d "static/vendor" ]; then
  echo "good"
else
  echo -n "Does not exist, creating..."
  mkdir static/vendor || (echo "Failed!" && exit 1)
  echo "done"
fi

declare -A repos=(
  ["semantic-ui"]="https://github.com/Semantic-Org/Semantic-UI-CSS"
)

for repo in "${!repos[@]}"; do
  echo -e "Checking $repo...\t\t\t\t\c"
  if [ -d "static/vendor/$repo" ]; then
    git -C static/vendor/$repo pull
  else
    echo "Cloning!"
    git clone ${repos["$repo"]} static/vendor/$repo
  fi
done
