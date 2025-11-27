#!/usr/bin/env python3
"""Add length_minutes field to all episodes in episodes.json."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / 'metadata' / 'episodes.json'

def main():
    # Read the episodes
    data = json.loads(META.read_text())
    
    # Add length_minutes field to each episode if it doesn't exist
    modified = False
    for episode in data:
        if 'length_minutes' not in episode:
            episode['length_minutes'] = 0
            modified = True
    
    if modified:
        # Write back with nice formatting
        META.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"Added length_minutes field to episodes in {META}")
    else:
        print("All episodes already have length_minutes field")

if __name__ == '__main__':
    main()
