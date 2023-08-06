clean=$(git status --porcelain --untracked-files=no | wc -l)
if [$clean < 1]; then
	if [[ $# == 1 && ($1 == "patch" || $1 == "minor" || $1 == "major") ]]; then
		echo "good work"
	else
		echo "bad"
	fi
else
	echo working directory is not clean!
	git status --porcelain --untracked-files=no 
fi