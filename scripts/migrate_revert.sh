#!/bin/bash
set -e
echo "Reverting last migration"
alembic downgrade -1