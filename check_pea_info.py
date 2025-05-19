"""
Script to check for pea-related information in the Prolog knowledge base
"""
import os
import re
from pathlib import Path

def check_pea_info():
    """Check for pea-related information in the Prolog knowledge base"""
    # Get the base directory of the project
    base_dir = Path(__file__).resolve().parent
    prolog_dir = base_dir / "pest-management-chatbot" / "farmlore-project" / "prolog_integration"
    
    print("\n===== PEA INFORMATION CHECK =====\n")
    
    # Check if the directory exists
    if not prolog_dir.exists():
        print(f"ERROR: Prolog integration directory not found: {prolog_dir}")
        return
    
    # Files to check
    files_to_check = [
        "pea_updates.pl",
        "crop_updates.pl",
        "knowledgebase.pl",
        "advanced_queries.pl"
    ]
    
    total_pea_mentions = 0
    total_pea_frames = 0
    
    for filename in files_to_check:
        file_path = prolog_dir / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count pea mentions
            pea_mentions = content.lower().count("pea")
            
            # Count pea frames
            pea_frames = len(re.findall(r'frame\([^,]+,\s*\[\s*name:\s*pea', content, re.IGNORECASE))
            pea_frames += len(re.findall(r'frame\([^,]+,\s*\[\s*name:\s*[^,]*pea[^,]*', content, re.IGNORECASE))
            
            print(f"File: {filename}")
            print(f"  - Pea mentions: {pea_mentions}")
            print(f"  - Pea frames: {pea_frames}")
            
            # Extract pea-related frames
            pea_frame_matches = re.findall(r'frame\([^,]+,\s*\[\s*name:\s*[^,]*pea[^,]*.*?\]\)', content, re.IGNORECASE | re.DOTALL)
            if pea_frame_matches:
                print(f"  - Found {len(pea_frame_matches)} pea-related frames:")
                for i, frame in enumerate(pea_frame_matches[:3]):
                    # Get just the first line of the frame
                    frame_first_line = frame.split('\n')[0] + " ..."
                    print(f"    {i+1}. {frame_first_line}")
                if len(pea_frame_matches) > 3:
                    print(f"    ... and {len(pea_frame_matches) - 3} more")
            
            # Look for pea in controls
            pea_controls = re.findall(r'controls:\s*\[[^\]]*pea[^\]]*\]', content, re.IGNORECASE)
            if pea_controls:
                print(f"  - Found {len(pea_controls)} entries with pea in controls")
            
            print()
            
            total_pea_mentions += pea_mentions
            total_pea_frames += pea_frames
    
    print(f"Total pea mentions across all files: {total_pea_mentions}")
    print(f"Total pea frames across all files: {total_pea_frames}")
    
    # Check if we have enough pea information
    if total_pea_frames > 0:
        print("\nVERIFICATION PASSED: Pea information found in the knowledge base")
    else:
        print("\nVERIFICATION FAILED: No pea frames found in the knowledge base")
    
    print("\n===== CHECK COMPLETED =====\n")

if __name__ == "__main__":
    check_pea_info() 