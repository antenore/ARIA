# GitHub Pages Setup Instructions

To ensure the documentation is properly deployed to GitHub Pages, follow these steps:

## 1. Set up a Deploy Key for GitHub Actions

The GitHub Actions workflow needs permission to push to your repository. Here's how to set up a deploy key:

1. Generate a new SSH key pair on your local machine (do not use your personal SSH key):
   ```bash
   ssh-keygen -t ed25519 -C "github-actions-deploy@github.com" -f gh-pages-deploy
   ```
   This will create two files: `gh-pages-deploy` (private key) and `gh-pages-deploy.pub` (public key)

2. Add the public key to your repository:
   - Go to your GitHub repository
   - Click on "Settings" > "Deploy keys" > "Add deploy key"
   - Title: "GitHub Actions Deploy Key"
   - Key: Paste the contents of `gh-pages-deploy.pub`
   - Check "Allow write access"
   - Click "Add key"

3. Add the private key as a repository secret:
   - Go to your GitHub repository
   - Click on "Settings" > "Secrets and variables" > "Actions"
   - Click "New repository secret"
   - Name: `ACTIONS_DEPLOY_KEY`
   - Value: Paste the contents of the `gh-pages-deploy` file (the private key)
   - Click "Add secret"

4. Delete the key files from your local machine after adding them to GitHub:
   ```bash
   rm gh-pages-deploy gh-pages-deploy.pub
   ```

## 2. Configure GitHub Pages

After setting up the deploy key and pushing the updated workflow:

1. Commit and push the updated CI workflow to your repository
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
- The deploy key is specific to this repository and cannot be used elsewhere

## Troubleshooting

If the documentation is not updating:

1. Check the GitHub Actions workflow runs to ensure the deployment step completed successfully
2. Verify that the GitHub Pages settings are configured to use the `gh-pages` branch
3. Clear your browser cache or try viewing the site in an incognito/private window
4. Check if there are any GitHub Pages build errors in the repository settings
5. Ensure the deploy key has been properly set up with write access

## Manual Deployment

If needed, you can manually deploy the documentation:

```bash
# Install MkDocs and plugins
pip install mkdocs mkdocs-material mkdocs-minify-plugin mkdocs-exclude

# Build the documentation
mkdocs build

# Deploy to GitHub Pages (this will create the gh-pages branch if it doesn't exist)
mkdocs gh-deploy --force
