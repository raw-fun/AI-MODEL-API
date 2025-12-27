#!/usr/bin/env python3
"""
Script to extract AI model information from source text file and convert to YAML format.
Extracts: AI model name, Token limit, and Model link

Note: Some models may have multiple identifiers/aliases listed in a single entry.
These are preserved as-is from the source file.
"""

import re
import yaml

def parse_model_data(filename):
    """Parse the AI MODEL DATA.txt file and extract model information."""
    models = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for model ID pattern [model_id](api_reference_link)
        model_match = re.match(r'\[(.*?)\]\((.*?)\)', line)
        
        # Expected structure: model_id line, empty line, developer, empty line, token_limit, empty line, model_card
        # That's 7 lines total, but we check for 5 more lines ahead from current position
        if model_match and i + 5 < len(lines):
            model_id = model_match.group(1)
            api_reference = model_match.group(2)
            
            # Skip empty line
            i += 1
            if i >= len(lines):
                break
                
            i += 1  # Move to developer line
            if i >= len(lines):
                break
            developer = lines[i].strip()
            
            # Skip empty line
            i += 1
            if i >= len(lines):
                break
                
            i += 1  # Move to token limit line
            if i >= len(lines):
                break
            token_limit_str = lines[i].strip()
            
            # Parse token limit - remove commas and convert to int if possible
            token_limit = token_limit_str.replace(',', '')
            if token_limit.isdigit():
                token_limit = int(token_limit)
            else:
                token_limit = token_limit_str  # Keep as string if not a number
            
            # Skip empty line
            i += 1
            if i >= len(lines):
                break
                
            i += 1  # Move to model card line
            if i >= len(lines):
                break
            model_card_line = lines[i].strip()
            
            # Extract model card link
            model_card_match = re.match(r'\[(.*?)\]\((.*?)\)', model_card_line)
            if model_card_match:
                model_card_link = model_card_match.group(2)
            else:
                # Normalize placeholder values to None for consistency
                if model_card_line in ['-', '_-_', '–', '_Coming Soon_', '']:
                    model_card_link = None
                else:
                    model_card_link = model_card_line
            
            # Only add models with valid data
            if developer and token_limit and model_id:
                # Filter to only include models with numeric token limits (text models)
                # This excludes image/video/speech models which typically don't have token limits
                if isinstance(token_limit, int) or (isinstance(token_limit, str) and token_limit.replace(',', '').isdigit()):
                    model_info = {
                        'AI_model': model_id,
                        'Token_limit': token_limit,
                        'Model_link': model_card_link if model_card_link else api_reference
                    }
                    models.append(model_info)
        
        i += 1
    
    return models

def save_to_yaml(models, output_filename):
    """Save the extracted model information to YAML file."""
    with open(output_filename, 'w', encoding='utf-8') as f:
        yaml.dump(models, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

if __name__ == '__main__':
    # Input and output filenames
    input_file = 'AI MODEL DATA.txt'
    output_file = 'ai_model_info.yaml'
    
    print(f"Reading data from {input_file}...")
    models = parse_model_data(input_file)
    
    print(f"Extracted {len(models)} AI models")
    
    print(f"Saving to {output_file}...")
    save_to_yaml(models, output_file)
    
    print(f"Successfully created {output_file}")
    print(f"Total models: {len(models)}")
