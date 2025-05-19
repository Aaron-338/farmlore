"""
Script to check for potato-related information in the Prolog knowledge base
"""
import os
import re
from pathlib import Path

def check_potato_info():
    """Check for potato-related information in the Prolog knowledge base"""
    # Get the base directory of the project
    base_dir = Path(__file__).resolve().parent
    prolog_dir = base_dir / "pest-management-chatbot" / "farmlore-project" / "prolog_integration"
    
    print("\n===== POTATO INFORMATION CHECK =====\n")
    
    # Check if the directory exists
    if not prolog_dir.exists():
        print(f"ERROR: Prolog integration directory not found: {prolog_dir}")
        return
    
    # Files to check
    files_to_check = [
        "crop_updates.pl",
        "knowledgebase.pl",
        "control_methods.pl",
        "advanced_queries.pl"
    ]
    
    total_potato_mentions = 0
    total_potato_frames = 0
    
    for filename in files_to_check:
        file_path = prolog_dir / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count potato mentions
            potato_mentions = content.lower().count("potato")
            
            # Count potato frames
            potato_frames = len(re.findall(r'frame\([^,]+,\s*\[\s*name:\s*potato', content, re.IGNORECASE))
            potato_frames += len(re.findall(r'frame\([^,]+,\s*\[\s*name:\s*[^,]*potato[^,]*', content, re.IGNORECASE))
            
            print(f"File: {filename}")
            print(f"  - Potato mentions: {potato_mentions}")
            print(f"  - Potato frames: {potato_frames}")
            
            # Extract potato-related frames
            potato_frame_matches = re.findall(r'frame\([^,]+,\s*\[\s*name:\s*[^,]*potato[^,]*.*?\]\)', content, re.IGNORECASE | re.DOTALL)
            if potato_frame_matches:
                print(f"  - Found {len(potato_frame_matches)} potato-related frames:")
                for i, frame in enumerate(potato_frame_matches[:3]):
                    # Get just the first line of the frame
                    frame_first_line = frame.split('\n')[0] + " ..."
                    print(f"    {i+1}. {frame_first_line}")
                if len(potato_frame_matches) > 3:
                    print(f"    ... and {len(potato_frame_matches) - 3} more")
            
            # Look for potato in controls
            potato_controls = re.findall(r'controls:\s*\[[^\]]*potato[^\]]*\]', content, re.IGNORECASE)
            if potato_controls:
                print(f"  - Found {len(potato_controls)} entries with potato in controls")
            
            print()
            
            total_potato_mentions += potato_mentions
            total_potato_frames += potato_frames
    
    print(f"Total potato mentions across all files: {total_potato_mentions}")
    print(f"Total potato frames across all files: {total_potato_frames}")
    
    # Check if we have enough potato information
    if total_potato_frames > 0:
        print("\nVERIFICATION PASSED: Potato information found in the knowledge base")
    else:
        print("\nVERIFICATION FAILED: No potato frames found in the knowledge base")
    
    print("\n===== CHECK COMPLETED =====\n")

if __name__ == "__main__":
    check_potato_info() 