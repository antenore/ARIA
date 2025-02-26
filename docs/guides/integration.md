# Integrating ARIA with External Systems

This guide explains how to integrate ARIA with various external systems, supporting both capability-based and model-based policy formats.

## Overview

ARIA can be integrated with:

- AI/ML frameworks
- CI/CD pipelines
- Governance systems
- Monitoring tools
- Custom applications

## Integration Methods

### Python API Integration

The most direct method is to use ARIA's Python API:

```python
from aria import Policy, Validator, Template

# Load a policy (auto-detects format)
policy = Policy.from_file("policy.yml")

# Validate against a specific model or capability request
validator = Validator(policy)
result = validator.validate(request_data)

if result.is_valid:
    # Proceed with AI operation
    print(f"Request approved: {result.message}")
else:
    # Handle validation failure
    print(f"Request denied: {result.message}")
    print(f"Errors: {result.errors}")
```

### REST API Integration

For non-Python systems, use the REST API:

```bash
# Start the ARIA API server
aria server start --port 8000

# In another terminal or system
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "policy_path": "policy.yml",
    "request": {
      "operation": "text_generation",
      "parameters": {
        "prompt": "Write a story about..."
      }
    }
  }'
```

### CLI Integration

For CI/CD pipelines or shell scripts:

```bash
# Validate a request against a policy
aria validate policy.yml --request request.json

# Exit code indicates success (0) or failure (1)
if [ $? -eq 0 ]; then
  echo "Request approved"
else
  echo "Request denied"
fi
```

## Format-Specific Integration

### Capability-Based Integration

When working with capability-based policies:

```python
from aria import Policy, Validator

# Load a capability-based policy
policy = Policy.from_file("policy.yml", format="capability")

# Create a capability request
request = {
    "capability": "text_generation",
    "parameters": {
        "prompt": "Generate a story about...",
        "max_tokens": 500
    },
    "context": {
        "user_id": "user123",
        "session_id": "session456"
    }
}

# Validate the request
validator = Validator(policy)
result = validator.validate(request)

if result.is_valid:
    # Proceed with capability
    pass
```

### Model-Based Integration

When working with model-based policies:

```python
from aria import Policy, Validator

# Load a model-based policy
policy = Policy.from_file("policy.yml", format="model")

# Create a model request
request = {
    "action": "generate",
    "resource": "src/main.py",
    "parameters": {
        "prompt": "Add error handling to...",
        "context": "function implementation"
    }
}

# Validate the request
validator = Validator(policy)
result = validator.validate(request)

if result.is_valid:
    # Proceed with model action
    pass
```

## Integration with AI Frameworks

### OpenAI Integration

```python
import openai
from aria import Policy, Validator

# Load policy
policy = Policy.from_file("policy.yml")
validator = Validator(policy)

# Prepare OpenAI request
openai_request = {
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write code to..."}
    ]
}

# Convert to ARIA request format
aria_request = {
    "capability": "code_generation" if policy.format == "capability" else None,
    "action": "generate" if policy.format == "model" else None,
    "resource": "code",
    "parameters": openai_request
}

# Validate
result = validator.validate(aria_request)

if result.is_valid:
    # Proceed with OpenAI call
    response = openai.ChatCompletion.create(**openai_request)
    print(response.choices[0].message.content)
else:
    print(f"Policy violation: {result.message}")
```

### Hugging Face Integration

```python
from transformers import pipeline
from aria import Policy, Validator

# Load policy
policy = Policy.from_file("policy.yml")
validator = Validator(policy)

# Prepare Hugging Face request
hf_request = {
    "model": "gpt2",
    "prompt": "Write a story about...",
    "max_length": 100
}

# Convert to ARIA request format
aria_request = {
    "capability": "text_generation" if policy.format == "capability" else None,
    "action": "generate" if policy.format == "model" else None,
    "resource": "text",
    "parameters": hf_request
}

# Validate
result = validator.validate(aria_request)

if result.is_valid:
    # Proceed with Hugging Face call
    generator = pipeline('text-generation', model=hf_request["model"])
    output = generator(hf_request["prompt"], max_length=hf_request["max_length"])
    print(output[0]["generated_text"])
else:
    print(f"Policy violation: {result.message}")
```

## CI/CD Integration

### GitHub Actions Integration

```yaml
# .github/workflows/aria-validation.yml
name: ARIA Policy Validation

on:
  pull_request:
    paths:
      - '**.py'
      - '**.js'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
          
      - name: Install ARIA
        run: pip install aria-policy
        
      - name: Validate AI operations
        run: |
          # Get changed files
          FILES=$(git diff --name-only ${{ github.event.before }} ${{ github.event.after }})
          
          # Validate each file against policy
          for FILE in $FILES; do
            aria validate policy.yml --resource "$FILE" --action modify
            if [ $? -ne 0 ]; then
              echo "Policy violation in $FILE"
              exit 1
            fi
          done
```

### Jenkins Pipeline Integration

```groovy
pipeline {
    agent any
    
    stages {
        stage('ARIA Policy Validation') {
            steps {
                sh '''
                    # Install ARIA
                    pip install aria-policy
                    
                    # Get changed files
                    FILES=$(git diff --name-only HEAD~1 HEAD)
                    
                    # Validate each file against policy
                    for FILE in $FILES; do
                        aria validate policy.yml --resource "$FILE" --action modify
                        if [ $? -ne 0 ]; then
                            echo "Policy violation in $FILE"
                            exit 1
                        fi
                    done
                '''
            }
        }
    }
}
```

## Best Practices

1. **Autodetect Policy Format**: Use `Policy.from_file()` without specifying format to auto-detect.
2. **Validate Early**: Integrate validation as early as possible in your workflow.
3. **Detailed Requests**: Provide comprehensive information in requests for better validation.
4. **Handle Validation Failures**: Always handle validation failures gracefully.
5. **Log Validation Results**: Log all validation results for audit purposes.
6. **Use Strict Mode**: Enable strict validation in production environments.
7. **Regular Updates**: Keep policies updated as requirements change.
8. **Version Control**: Store policies in version control alongside code.

## Troubleshooting

### Common Issues

1. **Format Detection Failures**
   - Ensure your policy file follows the correct schema
   - Explicitly specify format if auto-detection fails

2. **Validation Errors**
   - Check validation result errors for details
   - Ensure request format matches policy format
   - Verify all required fields are present

3. **Integration Issues**
   - Confirm ARIA version compatibility
   - Check API endpoint configuration
   - Verify authentication if required

## See Also

- [Policy Validation Guide](policy-validation.md)
- [Templates Guide](templates.md)
- [Policy API](../api/policy.md)
- [CLI Reference](cli.md)
- [Policy Format Examples](../examples/policy-formats.yml)
