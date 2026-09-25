#!/bin/bash
# Deploy Evidence Room to Vercel

cd /tmp/madlanga-sync/evidence-room

echo "Installing dependencies..."
npm install

echo "Building..."
npm run build

echo "Deploying to Vercel..."
vercel --prod

echo "Done! Check Vercel dashboard for URL."