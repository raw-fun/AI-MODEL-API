# AI Model Information Extraction

This directory contains tools to extract AI model information from the source data file and convert it to YAML format.

## Files

- `AI MODEL DATA.txt` - Source file containing AI model information in markdown table format
- `extract_model_info.py` - Python script to parse and extract model information
- `ai_model_info.yaml` - Generated YAML file with structured model data

## Usage

To extract model information and generate the YAML file:

```bash
python3 extract_model_info.py
```

This will:
1. Read `AI MODEL DATA.txt`
2. Extract model name, token limit, and model link for each AI model
3. Generate `ai_model_info.yaml` with the structured data

## Output Format

The generated YAML file contains a list of AI models with the following structure:

```yaml
- AI_model: <model_name>
  Token_limit: <limit>
  Model_link: <link>
- AI_model: <model_name_2>
  Token_limit: <limit_2>
  Model_link: <link_2>
```

## Requirements

- Python 3.6+
- PyYAML library

Install requirements:
```bash
pip install pyyaml
```

## Notes

- Only text models with valid numeric token limits are included
- Some models may have multiple identifiers/aliases listed in a single entry
- Placeholder values (-, _-_, –, _Coming Soon_) are replaced with API reference links
- Token limits are converted to integers where possible
