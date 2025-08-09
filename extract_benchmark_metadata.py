"""
Extract benchmark metadata for website generation.
"""

import os
import sys
import importlib.util
import json
from pathlib import Path

def extract_benchmark_metadata(benchmark_file_path):
    """Extract metadata from a benchmark file."""
    try:
        # Load the benchmark module
        spec = importlib.util.spec_from_file_location("benchmark", benchmark_file_path)
        benchmark_module = importlib.util.module_from_spec(spec)
        
        # Mock the solver import to avoid errors
        import types
        mock_solver = types.ModuleType('solver')
        mock_solver.solve_HJB = lambda *args, **kwargs: None
        sys.modules['solver'] = mock_solver
        
        # Execute the module
        spec.loader.exec_module(benchmark_module)
        
        # Extract metadata if function exists
        if hasattr(benchmark_module, 'get_benchmark_metadata'):
            return benchmark_module.get_benchmark_metadata()
        else:
            print(f"Warning: {benchmark_file_path} missing get_benchmark_metadata()")
            return None
            
    except Exception as e:
        print(f"Error extracting metadata from {benchmark_file_path}: {e}")
        return None

def scan_benchmarks_directory(benchmarks_dir):
    """Scan directory for benchmark files and extract metadata."""
    metadata_collection = {}
    
    benchmarks_path = Path(benchmarks_dir)
    
    # Find all benchmark files
    for benchmark_file in benchmarks_path.rglob("*_benchmark.py"):
        print(f"Processing: {benchmark_file}")
        
        # Extract relative path for categorization
        rel_path = benchmark_file.relative_to(benchmarks_path)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "uncategorized"
        
        # Extract metadata
        metadata = extract_benchmark_metadata(benchmark_file)
        
        if metadata:
            if category not in metadata_collection:
                metadata_collection[category] = []
            
            # Add file path information
            metadata['file_path'] = str(rel_path)
            metadata['download_url'] = f"/download/{rel_path}"
            
            metadata_collection[category].append(metadata)
    
    return metadata_collection

def generate_website_data(output_file="docs/benchmark_data.json"):
    """Generate JSON data file for website."""
    benchmarks_dir = "benchmarks"
    
    print("Scanning benchmarks directory...")
    metadata_collection = scan_benchmarks_directory(benchmarks_dir)
    
    # Add summary statistics
    website_data = {
        "last_updated": str(datetime.now().isoformat()),
        "summary": {
            "total_categories": len(metadata_collection),
            "total_benchmarks": sum(len(benchmarks) for benchmarks in metadata_collection.values()),
            "total_test_cases": sum(
                benchmark["total_cases"] 
                for benchmarks in metadata_collection.values() 
                for benchmark in benchmarks
            )
        },
        "categories": metadata_collection
    }
    
    # Save to JSON file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(website_data, f, indent=2)
    
    print(f"Generated website data: {output_file}")
    return website_data

if __name__ == "__main__":
    from datetime import datetime
    generate_website_data()