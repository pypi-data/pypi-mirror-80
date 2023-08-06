git checkout release
git merge master
bumpversion --tag --commit patch
git push
git checkout master
git merge release
git push