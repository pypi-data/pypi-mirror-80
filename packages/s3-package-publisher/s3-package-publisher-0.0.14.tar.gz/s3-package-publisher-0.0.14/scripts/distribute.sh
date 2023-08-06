pipenv run pipenv-setup sync
AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
AWS_DEFAULT_REGION="us-east-1" \
pipenv run s3pypi --bucket "${PACKAGE_REPOSITORY_BUCKET}" --verbose