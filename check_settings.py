#!/usr/bin/env python3
"""Check settings loading"""

import sys
import os

# Add backend to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.config.settings import get_settings

settings = get_settings()
print(f"DATABASE_URL: {settings.DATABASE_URL}")
print(f"DEBUG: {settings.DEBUG}")
print(f"PROJECT_NAME: {settings.PROJECT_NAME}")