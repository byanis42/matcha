-- Initialize Matcha database
-- This script is run when the PostgreSQL container starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database user if not exists
-- (This is handled by POSTGRES_USER env var, but kept for reference)

-- Set timezone
SET timezone = 'UTC';

-- Create initial schema (will be managed by Alembic)
-- This is just for initial setup