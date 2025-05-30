#!/bin/bash

set -e  # Exit on any error

echo "📁 Ensuring ./databases directory exists..."
mkdir -p ./databases

echo "🧠 Running Alembic migrations..."
alembic upgrade head

echo "✅ Database is ready!"

PYTHONPATH=. python3 api/ai_core/init_blogposts_collection.py