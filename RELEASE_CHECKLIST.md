# ARIA Framework Release Checklist

## Version 0.1.1-alpha

### Pre-Release Checks

- [x] Update version number in setup.py
- [x] Update version number in pyproject.toml
- [x] Update version number in README.md
- [x] Update CHANGELOG.md with release date and version
- [x] Create RELEASE_NOTES.md
- [x] Create release branch (release/0.1.1-alpha)
- [x] Commit all changes
- [x] Create git tag (v0.1.1-alpha)

### Release Steps

- [x] Merge release branch to main
- [x] Push changes to GitHub
- [x] Push tag to GitHub
- [x] Prepare GitHub Release notes (GITHUB_RELEASE.md)
- [x] Create GitHub Release with release notes
- [x] Build distribution packages
- [x] Verify package with twine check
- [ ] Upload package to PyPI

### Post-Release

- [ ] Verify package installation from PyPI
- [ ] Update documentation site
- [ ] Announce release on appropriate channels
- [ ] Create new development branch for next version

## Notes

This is an alpha release focusing on documentation improvements and IDE integration. The next release will focus on improving policy enforcement mechanisms and expanding IDE support.

## Release Manager

Antenore Gatta
