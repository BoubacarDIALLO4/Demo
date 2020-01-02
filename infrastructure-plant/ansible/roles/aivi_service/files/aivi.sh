#!/usr/bin/env bash
# Start AIVI
sudo systemctl start aivi.service
# Open Firefox on target web page
echo "Starting AIVI..."
sleep 30
sudo systemctl restart firefox.service
sleep 10
