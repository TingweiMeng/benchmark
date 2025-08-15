"""
Extract benchmark metadata for website generation.
"""

import os
import sys
import importlib.util
import json
from pathlib import Path
from datetime import datetime

def extract_benchmark_metadata(benchmark_file_path):
    """Extract metadata from a benchmark file."""
    print(f"  Attempting to load: {benchmark_file_path}")
    
    try:
        # Add the benchmark directory and parent directories to Python path
        benchmark_dir = os.path.dirname(benchmark_file_path)
        benchmark_root = str(Path(benchmark_file_path).parent.parent.parent.parent)  # Go up to benchmark/
        
        if benchmark_dir not in sys.path:
            sys.path.insert(0, benchmark_dir)
        if benchmark_root not in sys.path:
            sys.path.insert(0, benchmark_root)
        
        # Mock imports that might fail
        import types
        
        # Mock solver
        mock_solver = types.ModuleType('solver')
        mock_solver.solve_HJB = lambda *args, **kwargs: None
        sys.modules['solver'] = mock_solver
        
        # Mock utils and template modules
        mock_utils = types.ModuleType('utils')
        sys.modules['utils'] = mock_utils
        
        # Create mock template and benchmark modules for relative imports
        mock_template = types.ModuleType('template')
        mock_template.utils = mock_utils
        sys.modules['template'] = mock_template
        sys.modules['template.utils'] = mock_utils
        
        # Mock the relative import structure
        mock_benchmark = types.ModuleType('benchmark')
        mock_benchmark.template = mock_template
        mock_benchmark.template.utils = mock_utils
        sys.modules['benchmark'] = mock_benchmark
        sys.modules['benchmark.template'] = mock_template
        sys.modules['benchmark.template.utils'] = mock_utils
        
        # Read the file and modify relative imports
        with open(benchmark_file_path, 'r') as f:
            content = f.read()
        
        # Replace problematic relative imports
        content = content.replace('from ...utils import *', '# from ...utils import *  # Mocked')
        content = content.replace('from ..template.utils import *', '# from ..template.utils import *  # Mocked')
        
        # Create a temporary module
        module_name = f"temp_benchmark_{os.path.basename(benchmark_file_path).replace('.py', '')}"
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        benchmark_module = importlib.util.module_from_spec(spec)
        
        print(f"  Executing module...")
        # Execute the modified content
        exec(content, benchmark_module.__dict__)
        
        print(f"  Checking for get_benchmark_metadata function...")
        # Extract metadata if function exists
        if hasattr(benchmark_module, 'get_benchmark_metadata'):
            print(f"  Found get_benchmark_metadata, calling it...")
            metadata = benchmark_module.get_benchmark_metadata()
            print(f"  Successfully extracted metadata: {metadata.get('name', 'Unknown')}")
            return metadata
        else:
            print(f"  WARNING: {benchmark_file_path} missing get_benchmark_metadata() function")
            # Try to extract basic info if possible
            if hasattr(benchmark_module, 'get_test_cases'):
                test_cases = benchmark_module.get_test_cases()
                problem_name = getattr(benchmark_module, 'YOUR_PROBLEM_NAME', 'Unknown Benchmark')
                return {
                    "name": problem_name.replace('_', ' '),
                    "category": "HJB",
                    "short_description": "Benchmark file found but missing metadata",
                    "equation": "Unknown",
                    "initial_condition": "Unknown", 
                    "file_path": os.path.basename(benchmark_file_path),
                    "quick_stats": {"total_cases": len(test_cases)},
                    "test_cases": [],
                    "parameter_variations": {},
                    "testing_aspects": {}
                }
            return None
            
    except Exception as e:
        print(f"  ERROR extracting metadata from {benchmark_file_path}: {e}")
        import traceback
        traceback.print_exc()
        return None

def scan_benchmarks_directory(benchmarks_dir="benchmarks"):
    """Scan directory for benchmark files and extract metadata."""
    metadata_collection = {}
    
    benchmarks_path = Path(benchmarks_dir)
    print(f"Scanning directory: {benchmarks_path.absolute()}")
    
    # Find all benchmark files
    benchmark_files = list(benchmarks_path.rglob("*_benchmark.py"))
    print(f"Found {len(benchmark_files)} benchmark files:")
    
    for benchmark_file in benchmark_files:
        print(f"\nProcessing: {benchmark_file}")
        
        # Extract relative path for categorization
        rel_path = benchmark_file.relative_to(benchmarks_path)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "uncategorized"
        
        print(f"  Category: {category}")
        
        # Extract metadata
        metadata = extract_benchmark_metadata(benchmark_file)
        
        if metadata:
            if category not in metadata_collection:
                metadata_collection[category] = []
            
            # Add file path information
            metadata['file_path'] = benchmark_file.name  # Just the filename, not the full path
            metadata['download_url'] = f"/download/{rel_path}"
            
            metadata_collection[category].append(metadata)
            print(f"  ✓ Successfully added {metadata['name']} to category {category}")
        else:
            print(f"  ✗ Failed to extract metadata")
    
    return metadata_collection

def generate_website_data(output_file="docs/benchmark_data.json"):
    """Generate JSON data file for website."""
    print("="*60)
    print("BENCHMARK METADATA EXTRACTION")
    print("="*60)
    
    metadata_collection = scan_benchmarks_directory()
    
    print(f"\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Categories found: {len(metadata_collection)}")
    for category, benchmarks in metadata_collection.items():
        print(f"  {category}: {len(benchmarks)} benchmarks")
    
    # Add summary statistics
    website_data = {
        "last_updated": datetime.now().isoformat(),
        "summary": {
            "total_categories": len(metadata_collection),
            "total_benchmarks": sum(len(benchmarks) for benchmarks in metadata_collection.values()),
            "total_test_cases": sum(
                benchmark.get("quick_stats", {}).get("total_cases", 0)
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
    
    print(f"\nGenerated website data: {output_file}")
    print(f"Total benchmarks: {website_data['summary']['total_benchmarks']}")
    print(f"Total test cases: {website_data['summary']['total_test_cases']}")
    return website_data

if __name__ == "__main__":
    generate_website_data()