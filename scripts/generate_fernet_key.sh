#!/bin/bash
set -e
ENV_FILE=".env"
FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
if grep -q "^AIRFLOW_FERNET_KEY=" "$ENV_FILE"; then
    sed -i "s/^AIRFLOW_FERNET_KEY=.*/AIRFLOW_FERNET_KEY=$FERNET_KEY/" "$ENV_FILE"
else
    echo "AIRFLOW_FERNET_KEY=$FERNET_KEY" >> "$ENV_FILE"
fi
echo "AIRFLOW_FERNET_KEY has been generated."