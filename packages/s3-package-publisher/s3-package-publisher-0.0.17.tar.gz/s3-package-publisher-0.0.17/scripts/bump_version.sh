git reset --hard HEAD
git config --global user.email "s3-package-publisher@email.com"
git config --global user.name "s3-package-publisher"
echo "Bumping version"
pipenv run bumpversion \
  --current-version "$(pipenv run python setup.py --version)" \
  --verbose --commit --tag \
  --message "Bump version: {current_version} → {new_version} [skip ci]" \
  patch setup.py
echo "Pushing"
git push