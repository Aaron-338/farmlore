"""
Simple script to verify the Prolog files exist and contain expected content
"""
import os
from pathlib import Path

def verify_prolog_files():
    """Verify the Prolog files exist and contain expected content"""
    # Get the base directory of the project
    base_dir = Path(__file__).resolve().parent
    prolog_dir = base_dir / "pest-management-chatbot" / "farmlore-project" / "prolog_integration"
    
    print("\n===== PROLOG FILES VERIFICATION =====\n")
    print(f"Looking for Prolog files in: {prolog_dir}\n")
    
    # Check if the directory exists
    if not prolog_dir.exists():
        print(f"ERROR: Prolog integration directory not found: {prolog_dir}")
        return
    
    # Files to check
    files_to_check = [
        "load_all.pl",
        "advanced_queries.pl",
        "pea_updates.pl",
        "crop_updates.pl"
    ]
    
    for filename in files_to_check:
        file_path = prolog_dir / filename
        if file_path.exists():
            file_size = os.path.getsize(file_path) / 1024  # Size in KB
            print(f"✓ {filename} exists - Size: {file_size:.2f} KB")
            
            # Print first few lines of each file
            print(f"\nFirst 10 lines of {filename}:")
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:10]):
                    print(f"  {i+1}: {line.strip()}")
            print("  ...")
            
            # Print some statistics
            content = "".join(lines)
            print(f"\n  - Total lines: {len(lines)}")
            print(f"  - Frame definitions: {content.count('frame(')}")
            print(f"  - Contains 'pea': {content.lower().count('pea')}")
            print(f"  - Contains 'potato': {content.lower().count('potato')}")
            print(f"  - Contains 'aphid': {content.lower().count('aphid')}")
            print("\n" + "-"*50 + "\n")
        else:
            print(f"✗ {filename} does not exist")
    
    print("\n===== VERIFICATION COMPLETED =====\n")

if __name__ == "__main__":
    verify_prolog_files() 