FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Copy project
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Create non-root user
RUN useradd --create-home --shell /bin/bash matcha
RUN chown -R matcha:matcha /app
USER matcha

# Expose port
EXPOSE 8000

# Use start script that handles DB wait and migrations
CMD ["./start.sh"]