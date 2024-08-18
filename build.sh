#!/bin/bash

# Print message indicating the start of the build process
echo "Starting custom build process..."

# Install Python dependencies (assuming you're using pip)
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la

# Print installed packages
echo "Installed Python packages:"
pip freeze

# Print message indicating the end of the build process
echo "Build process completed."
