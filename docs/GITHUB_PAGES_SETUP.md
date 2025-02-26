# GitHub Pages Setup Instructions

To ensure the documentation is properly deployed to GitHub Pages, follow these steps:

1. First, commit and push the updated CI workflow to your repository
2. The GitHub Actions workflow will automatically create a `gh-pages` branch when it runs
3. After the workflow completes successfully, go to your GitHub repository settings
4. Navigate to "Pages" in the left sidebar
5. Under "Build and deployment" > "Source", select "Deploy from a branch"
6. Under "Branch", select "gh-pages" and "/ (root)"
7. Click "Save"

## Important Notes

- The CI workflow will automatically create the `gh-pages` branch on the first successful run
- You should no longer use the `docs` folder as the source for GitHub Pages
- The documentation will be automatically updated whenever changes are pushed to the main branch
- The deployment only happens after all tests pass

## Troubleshooting

If the documentation is not updating:

1. Check the GitHub Actions workflow runs to ensure the deployment step completed successfully
2. Verify that the GitHub Pages settings are configured to use the `gh-pages` branch
3. Clear your browser cache or try viewing the site in an incognito/private window
4. Check if there are any GitHub Pages build errors in the repository settings
5. Ensure the repository has the necessary permissions to create and update the `gh-pages` branch

## Manual Deployment

If needed, you can manually deploy the documentation:

```bash
# Install MkDocs and plugins
pip install mkdocs mkdocs-material mkdocs-minify-plugin mkdocs-exclude

# Build the documentation
mkdocs build

# Deploy to GitHub Pages (this will create the gh-pages branch if it doesn't exist)
mkdocs gh-deploy --force
