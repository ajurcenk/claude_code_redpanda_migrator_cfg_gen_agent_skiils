#!/usr/bin/env python3
"""
Validate Redpanda Migrator YAML configuration files.

Usage:
    python validate_config.py <config-file.yaml>
"""

import sys
import yaml
from typing import Dict, List, Any


def validate_required_fields(config: Dict[str, Any]) -> List[str]:
    """Validate that required fields are present."""
    errors = []
    
    # Check input.redpanda_migrator_bundle.redpanda_migrator.seed_brokers
    try:
        input_brokers = config['input']['redpanda_migrator_bundle']['redpanda_migrator']['seed_brokers']
        if not input_brokers or not isinstance(input_brokers, list):
            errors.append("input.redpanda_migrator_bundle.redpanda_migrator.seed_brokers must be a non-empty list")
    except KeyError:
        errors.append("Missing required field: input.redpanda_migrator_bundle.redpanda_migrator.seed_brokers")
    
    # Check output.redpanda_migrator_bundle.redpanda_migrator.seed_brokers
    try:
        output_brokers = config['output']['redpanda_migrator_bundle']['redpanda_migrator']['seed_brokers']
        if not output_brokers or not isinstance(output_brokers, list):
            errors.append("output.redpanda_migrator_bundle.redpanda_migrator.seed_brokers must be a non-empty list")
    except KeyError:
        errors.append("Missing required field: output.redpanda_migrator_bundle.redpanda_migrator.seed_brokers")
    
    # Check topics configuration
    try:
        topics = config['input']['redpanda_migrator_bundle']['redpanda_migrator'].get('topics')
        if not topics:
            errors.append("input.redpanda_migrator_bundle.redpanda_migrator.topics is required")
    except KeyError:
        errors.append("Missing required field: input.redpanda_migrator_bundle.redpanda_migrator.topics")
    
    return errors


def validate_schema_registry(config: Dict[str, Any]) -> List[str]:
    """Validate schema registry configuration if present."""
    errors = []
    
    # Check if schema registry is configured in input
    input_sr = config.get('input', {}).get('redpanda_migrator_bundle', {}).get('schema_registry')
    if input_sr:
        if 'url' not in input_sr:
            errors.append("input.redpanda_migrator_bundle.schema_registry.url is required when schema_registry is configured")
    
    # Check if schema registry is configured in output
    output_sr = config.get('output', {}).get('redpanda_migrator_bundle', {}).get('schema_registry')
    if output_sr:
        if 'url' not in output_sr:
            errors.append("output.redpanda_migrator_bundle.schema_registry.url is required when schema_registry is configured")
    
    # Warn if one is configured but not the other
    if input_sr and not output_sr:
        errors.append("WARNING: Schema registry configured for input but not output - schemas will not be migrated")
    if output_sr and not input_sr:
        errors.append("WARNING: Schema registry configured for output but not input - no schemas to migrate")
    
    return errors


def validate_consumer_groups(config: Dict[str, Any]) -> List[str]:
    """Validate consumer group offset translation settings."""
    warnings = []
    
    try:
        consumer_groups = config['output']['redpanda_migrator_bundle']['redpanda_migrator'].get('consumer_groups', False)
        if consumer_groups:
            warnings.append("NOTE: Consumer group offset translation requires identical partition counts between source and destination")
    except KeyError:
        pass
    
    return warnings


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_config.py <config-file.yaml>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {config_file}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML syntax: {e}")
        sys.exit(1)
    
    print(f"Validating {config_file}...\n")
    
    # Run validations
    all_errors = []
    all_errors.extend(validate_required_fields(config))
    all_errors.extend(validate_schema_registry(config))
    all_errors.extend(validate_consumer_groups(config))
    
    # Separate errors and warnings
    errors = [e for e in all_errors if not e.startswith('WARNING') and not e.startswith('SUGGESTION') and not e.startswith('NOTE')]
    warnings = [e for e in all_errors if e.startswith('WARNING') or e.startswith('SUGGESTION') or e.startswith('NOTE')]
    
    # Print results
    if errors:
        print("❌ ERRORS:")
        for error in errors:
            print(f"  - {error}")
        print()
    
    if warnings:
        print("⚠️  WARNINGS & SUGGESTIONS:")
        for warning in warnings:
            print(f"  - {warning}")
        print()
    
    if not errors and not warnings:
        print("✅ Configuration is valid!")
        sys.exit(0)
    elif errors:
        print("❌ Configuration has errors that must be fixed.")
        sys.exit(1)
    else:
        print("✅ Configuration is valid (with warnings)")
        sys.exit(0)


if __name__ == "__main__":
    main()
