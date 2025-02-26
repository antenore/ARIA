# ARIA Framework Changelog

All notable changes to the ARIA project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation structure in `/docs` directory
  - API reference documentation
  - User guides and tutorials
  - Example policies and templates
  - Technical documentation
  - CI/CD integration guides
- Example policy files demonstrating inheritance and template usage
- Detailed API documentation for all core modules
- CI/CD integration guides for GitHub Actions, GitLab CI, and Jenkins
- Technical architecture documentation for templates and validation
- New documentation sections:
  - Getting Started guide
  - Policy inheritance guide
  - Template usage guide
  - Configuration guide
  - Policy validation guide with dual-format support
  - Integration guide for external systems
- Documentation dependencies in setup.py extras_require
- Expanded policy models in CLI to include 'guardian', 'observer', 'collaborator', and 'partner' options
- Enhanced enum handling in templates with proper validation and case-insensitive matching
- Improved type safety across template and policy management
- GitHub Actions CI workflow for automated testing
- Test status badge in README.md
- Enhanced policy validator to support both capability-based policies (for testing) and model-based policies (for production)
- Added validation for capability descriptions, conditions format, and restrictions
- Added ValidationResult class with comprehensive feedback and error details
- Added support for strict validation mode with detailed warnings
- Added policy format examples demonstrating both capability-based and model-based formats
- Added integration guide with examples for various AI frameworks and CI/CD systems
- IDE integration support:
  - Policy to IDE rules converter tool (`aria.tools.policy_to_iderules`)
  - Support for Windsurf (`.windsurfrules`) and Cursor (`.cursorrules`)
  - Documentation for IDE integration options
  - Example policy files for IDE rule generation
  - Framework for future IDE plugin development
  - IDE ignore file generation (`.codeiumignore`, `.cursorignore`)
  - Enhanced protection for policy files and sensitive paths
- Added disclaimer to generated ignore files about current enforcement limitations
- Added explicit protection for main policy file (aria_policy.yml) in ignore files
- Added documentation about IDE integration limitations and future improvements

### Changed
- Reorganized documentation structure for better navigation
- Updated all cross-references to use correct relative paths
- Improved main documentation index for easier navigation
- Enhanced example policies with detailed comments
- Standardized documentation format across all files
- Renamed policy validation methods for better clarity
- Added proper type hints throughout the codebase
- Refactored template processing for better error handling and validation
- Enhanced YAML serialization with proper enum value handling
- Improved path handling consistency using os.path
- Better error messages and logging in template processing
- Updated CLI to handle policy model display more robustly
- Improved type handling in template creation with explicit PolicyModel conversion
- Updated policy evaluation to better match AWS IAM behavior:
  - Path-specific policies now have highest precedence
  - Global statements follow "last match wins" principle
  - Model defaults act as baseline when no explicit policies match
- Improved test coverage for policy inheritance and evaluation
- Updated policy validator to provide more specific error messages for different validation scenarios
- Updated inheritance documentation to support both capability-based and model-based policies
- Enhanced CLI documentation with format-specific options and examples
- Updated template documentation to reflect dual-format support
- Improved example files to demonstrate both policy formats
- Enhanced index.md with comprehensive feature descriptions for both policy formats
- Renamed CLI command from `aria` to `ariacli` to avoid name conflicts
- Updated entry points in setup.py and pyproject.toml
- Enhanced installation documentation with PATH troubleshooting guidance
- Updated self-testing documentation with IDE rules integration

### Fixed
- Broken documentation links and references
- Inconsistent documentation structure
- Missing API documentation sections
- Outdated installation instructions
- Documentation build failures due to missing mkdocs-minify-plugin
- Type checking errors in policy and template modules
- CLI validation command compatibility with new validation methods
- Consistent path handling across the codebase using `os.path` instead of mixed Path/string operations
- YAML serialization in policy and template management
- Type annotations and error handling in core modules
- Tests for policy and template management
- CLI output formatting and error messages
- Template processing now properly handles case-insensitive enum values
- Fixed temporary template creation in Template.from_dict
- Improved error handling in policy statement processing
- Policy inheritance now correctly handles path-specific overrides
- Global statement evaluation now respects statement order
- Documentation inconsistencies between capability-based and model-based approaches
- Example policy files now correctly demonstrate both formats
- Fixed inheritance examples to show proper format-specific inheritance rules
- Command name conflict by renaming from `aria` to `ariacli`
- Policy model validation to use lowercase model names
- Self-testing documentation to reflect new command name

## [1.0.0] - 2025-02-21

### Added
- Comprehensive logging system
  * Logger module
  * Configurable log levels and formats
  * Logging in CLI commands and core modules

- CLI Improvements
  * Progress indicators for long-running operations
  * Command aliases for common operations
  * Shorter option names (-t, -m, -o)
  * Better error messages and handling

- Testing Infrastructure
  * Improved test coverage
  * Fixed test environment setup
  * Added error case tests
  * Consolidated test structure

### Changed
- Simplified error handling in CLI
- Consolidated model usage (removed AICapability in favor of AIAction)
- Made command structure more consistent
- Improved type hints and docstrings
- Enhanced YAML serialization/deserialization
- Updated validation system
- Simplified policy YAML handling with consistent methods
- Improved error messages and validation in template operations
- Streamlined policy manager interface

### Removed
- Legacy test files
- Deprecated AICapability model
- Redundant command aliases

### Technical Details
- Python 3.8+ compatibility
- Extensive use of Pydantic for model validation
- Enum-based policy models
- YAML serialization with custom representers

### Security
- Enhanced type checking
- Improved enum validation
- Consistent policy model enforcement

## [0.9.0] - Initial Release

- Basic policy management
- Template system
- CLI interface
- Core validation

## [0.1.0] - 2025-01-26

### Added
- Initial release of ARIA
- Basic policy management
- Template system
- CLI interface