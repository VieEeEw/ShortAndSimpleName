#!/usr/bin/env bash 

# Check for dotenv file (create if not found)
if [ ! -f frontend/.env ]; then
    $MAPS_KEY
    echo "Environment variables are not set. Please provide them."
    printf "Google Maps API Key: "
    read -r MAPS_KEY
    echo "GRIDSOME_GOOGLE_MAPS_KEY=$MAPS_KEY" > frontend/.env    
fi

pushd frontend > /dev/null
yarn # Install dependencies
yarn develop # Run the development server
popd > /dev/null
