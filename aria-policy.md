version: 1.0
model: ASSISTANT

defaults:
  allow: []
  require:
    - human_review
    - tests
    - documentation

paths:
  'src/templates/**':
    allow: 
      - generate
      - modify
      - suggest
    require:
      - template_validation
      - documentation

  'src/validators/**':
    allow:
      - suggest
      - review
    require:
      - human_implementation
      - test_coverage

  'tests/**':
    allow:
      - generate
      - modify
      - suggest
    require:
      - test_coverage
      - human_review

  'docs/**':
    allow:
      - generate
      - modify
      - suggest
    require:
      - human_review

  'aria.yaml':
    allow: []  # Explicitly deny any AI modifications to ARIA's own policy