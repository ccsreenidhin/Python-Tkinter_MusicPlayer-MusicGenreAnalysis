#!/bin/sh

git init
git add .
read -p "Enter the commit date : " date
echo "commiting on, $date"
git commit -m "initial commit" --date $date
git log
read -p "Enter the remote repo : " repo
echo "pushing to repo, $repo"
git remote add origin $repo


