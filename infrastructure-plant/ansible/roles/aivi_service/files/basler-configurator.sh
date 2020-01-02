#!/usr/bin/env bash
# Start Basler configurator
sudo systemctl start basler-configurator.service
# Open Firefox on target web page
echo "Starting Basler configurator..."
sleep 1
sudo systemctl restart firefox.service
