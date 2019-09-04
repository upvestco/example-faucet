#!/bin/sh

set -e

if [ -z "$UPVEST_OAUTH_CLIENT_ID" ] || [ -z "$UPVEST_OAUTH_CLIENT_SECRET" ]; then
  echo "
The OAuth ID and Secret for your Upvest application must be set as the environment variables:
    UPVEST_OAUTH_CLIENT_ID
    UPVEST_OAUTH_CLIENT_SECRET
See the README for how to configure this faucet: https://github.com/upvestco/demo-faucet/README.md
"
  exit 1
fi


if [ -z "$UPVEST_USERNAME" ] || [ -z "$UPVEST_PASSWORD" ] || [ -z "$UPVEST_WALLET_ID" ]; then
  echo "
The credentials for the user and the wallet to use must be set as environment variables:
   UPVEST_USERNAME
   UPVEST_PASSWORD
   UPVEST_WALLET_ID
See the README for how to configure this faucet: https://github.com/upvestco/demo-faucet/README.md
"
  exit 1
fi

set -x

echo "Migrating database"
python manage.py migrate --no-input

echo "Collecting static files"
python manage.py collectstatic --no-input

echo "Loading asset definitions"
python manage.py loaddata assets

gunicorn -c gunicorn.conf faucet.wsgi
