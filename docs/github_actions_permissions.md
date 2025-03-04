# GitHub Actions Permissions Configuration

This document explains the permissions configuration used in the ARIA project's GitHub Actions workflows.

## Principle of Least Privilege

The ARIA project follows the principle of least privilege for GitHub Actions workflows. This means that workflows are granted only the permissions they need to function, and no more. This helps to minimize the potential impact of a compromised workflow.

## CI Workflow Permissions

The main CI workflow has the following permissions:

| Permission | Level | Justification |
|------------|-------|---------------|
| `contents` | read | Needed to checkout the repository |
| `pull-requests` | read | Needed to read PR information |
| `checks` | write | Needed to create check runs for test results |
| `actions` | read | Needed to read workflow run information |
| `issues` | read | Needed to read issue information |

### Documentation Job Permissions

The documentation job has the following permissions:

| Permission | Level | Justification |
|------------|-------|---------------|
| `contents` | write | Needed to push to the gh-pages branch |

### Security Job Permissions

The security job has the following permissions:

| Permission | Level | Justification |
|------------|-------|---------------|
| `security-events` | write | Needed to upload security analysis results |
| `contents` | read | Needed to checkout the repository |
| `actions` | read | Needed to read workflow run information |

## Best Practices

1. **Always specify permissions explicitly**: Even if you're using the default permissions, it's good practice to specify them explicitly in the workflow file.

2. **Use job-level permissions when possible**: If different jobs need different permissions, specify them at the job level rather than the workflow level.

3. **Regularly review permissions**: As the project evolves, regularly review the permissions to ensure they're still appropriate.

4. **Use GITHUB_TOKEN instead of personal access tokens**: The GITHUB_TOKEN is automatically created for each workflow run and is scoped to the repository, making it more secure than personal access tokens.

5. **Avoid using the `write-all` permission**: This permission grants write access to all scopes, which is rarely necessary and increases the risk of a compromised workflow.

## References

- [GitHub Actions: Permissions for the GITHUB_TOKEN](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token)
- [GitHub Actions: Permissions syntax](https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs)
