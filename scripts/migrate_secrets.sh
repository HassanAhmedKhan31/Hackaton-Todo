#!/bin/bash

# migrate_secrets.sh
# Usage: ./migrate_secrets.sh <release_name>

RELEASE_NAME=$1

if [ -z "$RELEASE_NAME" ]; then
  echo "Usage: ./migrate_secrets.sh <release_name>"
  exit 1
fi

echo "Migrating secrets for release: $RELEASE_NAME"

# Prompt for secrets if not set in environment
if [ -z "$DATABASE_URL" ]; then
  read -sp "Enter DATABASE_URL: " DATABASE_URL
  echo
fi

if [ -z "$OPENAI_API_KEY" ]; then
  read -sp "Enter OPENAI_API_KEY: " OPENAI_API_KEY
  echo
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
  read -sp "Enter OPENROUTER_API_KEY: " OPENROUTER_API_KEY
  echo
fi

# Create Kubernetes Secret
kubectl create secret generic ${RELEASE_NAME}-secrets \
  --from-literal=DATABASE_URL="$DATABASE_URL" \
  --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" \
  --from-literal=OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "Secrets updated successfully."
