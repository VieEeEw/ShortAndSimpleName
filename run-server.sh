#!/usr/bin/env bash

# Set environment variables
export FLASK_APP=server
export FLASK_ENV=development

FILE="server/google_backend.key"
if ! test -f "$FILE"; then
    echo "$FILE does not exist."
    echo "Please enter the backend Google Maps API key:"
    read -r MAPS_KEY
    echo "$MAPS_KEY" > "$FILE"
fi

# Start flask server
flask run &
