bump_version() {
  git reset --hard HEAD
  git config --global user.email "bumpversion@email.com"
  git config --global user.name "bumpversion"
  echo "Bumping version"
  pipenv run bumpversion \
    --current-version "$(pipenv run python setup.py --version)" \
    --verbose --commit --tag \
    --message "Bump version: {current_version} → {new_version} [skip ci]" \
    patch setup.py
  echo "Pushing"
  git push
}

distribute() {
  pipenv run pipenv-setup sync
  rm -rf dist
  pipenv run python setup.py sdist bdist_wheel
  pipenv run python -m twine upload -r pypi -u "${PYPI_USERNAME}" -p "${PYPI_PASSWORD}" --verbose dist/*
}

(
  distribute
) || (
  bump_version
  distribute
)
