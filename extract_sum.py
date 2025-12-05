# !/usr/bin/env python3
"""
Extract and aggregate all sources from somef_analysis_results.json
Creates a JSON file with total counts for each source across all metadata fields.
"""

import json
from pathlib import Path
from collections import defaultdict


def extract_sources(input_file, output_file):
    """
    Extract all sources from somef_analysis_results.json and calculate totals.

    Args:
        input_file: Path to somef_analysis_results.json
        output_file: Path to output JSON file
    """
    # Load the input data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Dictionary to store aggregated source counts
    source_totals = defaultdict(int)

    # Iterate through all metadata fields
    for field_name, field_data in data.items():
        if 'sources' in field_data:
            # Add each source count to the total
            for source, count in field_data['sources'].items():
                source_totals[source] += count

    # Sort sources by count (descending)
    sorted_sources = dict(sorted(
        source_totals.items(),
        key=lambda x: x[1],
        reverse=True
    ))

    # Calculate grand total
    grand_total = sum(source_totals.values())

    # Create output structure
    output_data = {
        "total_sources": len(sorted_sources),
        "grand_total": grand_total,
        "sources": sorted_sources,
        "sources_summary": {
            "top_5_sources": dict(list(sorted_sources.items())[:5]),
            "total_occurrences": grand_total
        }
    }

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)

    # Print summary
    print(f"Source extraction complete!")
    print(f"Total unique sources: {len(sorted_sources)}")
    print(f"Grand total of all source occurrences: {grand_total:,}")
    print(f"\nResults saved to: {output_file}")


def main():
    # Define file paths
    script_dir = Path(__file__).parent
    input_file = script_dir / 'data' / 'somef_analysis_results.json'
    output_file = script_dir / 'data' / 'sources_total.json'

    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        return

    # Extract sources
    extract_sources(input_file, output_file)


if __name__ == '__main__':
    main()