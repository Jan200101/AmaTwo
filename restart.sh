#!/bin/bash/
echo "Restarting Amadeus..."
pkill -f run.py
python3 run.py
echo "Restart complete!"
