#!/usr/bin/env python3
"""
Unified training script for SMS spam classifier
Runs all training steps in sequence
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    
    result = subprocess.run(
        command,
        shell=True,
        capture_output=False,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error: {description} failed")
        sys.exit(1)
    
    print(f"✓ {description} completed successfully")

def main():
    """Run all training steps"""
    print("Starting SMS spam classifier training pipeline...")
    
    os.makedirs('output', exist_ok=True)
    print("✓ Output directory ready")
    
    run_command(
        "python src/read_data.py",
        "Step 1: Reading data"
    )
    
    run_command(
        "python src/text_preprocessing.py",
        "Step 2: Preprocessing text"
    )
    
    run_command(
        "python src/text_classification.py",
        "Step 3: Training classifier"
    )
    
    print("\n" + "="*60)
    print("✓ Training pipeline completed successfully!")
    print("="*60)
    
    required_files = ['output/model.joblib', 'output/preprocessor.joblib']
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✓ {file} ({size} bytes)")
        else:
            print(f"⚠ Warning: {file} not found")

if __name__ == "__main__":
    main()