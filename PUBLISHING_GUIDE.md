# Publishing Guide

Step-by-step guide to publish Universal Claude Skills to GitHub.

## Current Status

✅ Repository created locally
✅ All files committed to git
✅ Ready to publish
❌ Not yet on GitHub

## Option 1: Using GitHub CLI (Recommended)

### Prerequisites
```bash
# Install GitHub CLI if not already installed
brew install gh  # macOS
# or visit: https://cli.github.com/

# Authenticate
gh auth login
```

### Publish Repository
```bash
# Navigate to repository
cd /Users/dmkang/Projects/claude-skills/claude-skills

# Create and publish in one command
gh repo create claude-skills \
  --public \
  --source=. \
  --remote=origin \
  --push

# This will:
# 1. Create repository on GitHub
# 2. Add remote origin
# 3. Push all commits
```

### Verify
```bash
# View on GitHub
gh repo view --web

# Check remote
git remote -v
```

---

## Option 2: Using GitHub Website

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Fill in details:
   - **Repository name**: `claude-skills`
   - **Description**: `Collection of universally useful Claude skills for development, project management, and workflow automation`
   - **Visibility**: Public (recommended) or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

### Step 2: Connect Local Repository

```bash
# Navigate to your repository
cd /Users/dmkang/Projects/claude-skills/claude-skills

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/claude-skills.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

### Step 3: Verify on GitHub

1. Visit: `https://github.com/YOUR_USERNAME/claude-skills`
2. You should see all your files and commits

---

## Option 3: Using SSH (More Secure)

### Step 1: Set Up SSH Key (if not already done)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add SSH key
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard
pbcopy < ~/.ssh/id_ed25519.pub
# or: cat ~/.ssh/id_ed25519.pub
```

### Step 2: Add SSH Key to GitHub

1. Go to GitHub → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste your public key
4. Click "Add SSH key"

### Step 3: Create Repository and Push

```bash
# Create repo with gh CLI
gh repo create claude-skills --public

# Add SSH remote
git remote add origin git@github.com:YOUR_USERNAME/claude-skills.git

# Push
git push -u origin main
```

---

## Post-Publishing Steps

### 1. Update Repository URLs

After publishing, update these files with your actual GitHub username:

```bash
# Update README.md
# Replace: yourusername/claude-skills
# With: YOUR_ACTUAL_USERNAME/claude-skills

# Update .claude-plugin/plugin.json
# Update repository and homepage URLs

# Update CONTRIBUTING.md
# Update repository URLs
```

### 2. Configure Repository Settings

On GitHub, go to Settings and configure:

**General:**
- ✅ Enable Issues
- ✅ Enable Discussions (optional)
- ✅ Enable Projects (optional)
- ✅ Set default branch to `main`

**Features:**
- ✅ Wikis (optional)
- ✅ Discussions (recommended)

**About:**
- Add description: "Universal Claude Skills for development and project management"
- Add topics: `claude`, `skills`, `ai`, `automation`, `project-management`, `linear`, `github`
- Add website (optional)

### 3. Add Repository Topics

Add these topics for discoverability:
- `claude`
- `claude-code`
- `skills`
- `ai-tools`
- `project-management`
- `task-decomposition`
- `issue-management`
- `linear`
- `github`
- `automation`
- `productivity`

### 4. Enable GitHub Pages (Optional)

To host documentation:
1. Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: / (root)
4. Save

Your docs will be at: `https://YOUR_USERNAME.github.io/claude-skills/`

### 5. Add Social Preview Image (Optional)

1. Settings → General → Social preview
2. Upload an image (1280x640px recommended)

---

## Sharing Your Repository

### 1. Create a Release

```bash
# Create a tag
git tag -a v1.0.0 -m "Initial release: Universal Claude Skills"

# Push tag
git push origin v1.0.0
```

Then on GitHub:
1. Go to Releases
2. Click "Create a new release"
3. Choose tag `v1.0.0`
4. Title: "v1.0.0 - Initial Release"
5. Description: Copy from CHANGELOG.md
6. Click "Publish release"

### 2. Share on Social Media

**Example Post:**
```
🚀 Just published Universal Claude Skills - a collection of
production-ready skills for Claude Code!

✨ Features:
- Task decomposition with rationale & risk assessment
- Multi-platform issue management (Linear/GitHub/Jira)
- Meta-skill for creating custom skills
- Comprehensive documentation & examples

🔗 https://github.com/YOUR_USERNAME/claude-skills

#AI #ClaudeCode #Productivity #OpenSource
```

### 3. Submit to Claude Marketplace (When Available)

Follow Claude Code plugin marketplace submission process.

### 4. List on Awesome Lists

Submit PRs to relevant awesome lists:
- awesome-claude
- awesome-ai-tools
- awesome-productivity

---

## Maintenance After Publishing

### Regular Updates

```bash
# Make changes
git add .
git commit -m "feat: Add new feature"
git push

# Create new release when significant changes
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

### Respond to Issues

- Triage new issues within 48 hours
- Label appropriately
- Respond to questions
- Accept good PRs

### Keep Documentation Updated

- Update CHANGELOG.md for each release
- Keep README.md current
- Add new examples as skills evolve
- Update version numbers

---

## Troubleshooting

### "Repository already exists"

```bash
# Remove remote and try again
git remote remove origin
gh repo create claude-skills --public --source=. --push
```

### "Permission denied (publickey)"

```bash
# Check SSH key is added
ssh -T git@github.com

# If fails, set up SSH key (see Option 3)
```

### "Failed to push"

```bash
# Check remote is correct
git remote -v

# Force push if needed (be careful!)
git push -f origin main
```

### "Branch main doesn't exist"

```bash
# Check current branch
git branch

# Rename if on 'master'
git branch -M main
git push -u origin main
```

---

## Quick Publishing Checklist

Before publishing:
- [ ] All files committed
- [ ] Repository tested locally
- [ ] Documentation reviewed
- [ ] No sensitive data in files
- [ ] LICENSE file included
- [ ] README is complete

After publishing:
- [ ] Repository is public/visible
- [ ] All files uploaded correctly
- [ ] GitHub Issues enabled
- [ ] Repository topics added
- [ ] Description added
- [ ] First release created
- [ ] URLs updated in files

---

## Success!

Once published, your repository will be available at:
```
https://github.com/YOUR_USERNAME/claude-skills
```

Share it and get feedback from the community! 🎉

---

**Questions?** See GitHub's documentation or open an issue.
