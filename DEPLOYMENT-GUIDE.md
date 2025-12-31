# Obsqura Deployment & Verification Guide

## Part 4: Deployment Instructions

### Prerequisites
- GitHub account: `ayushjha-dev`
- Repository: `ayushjha-dev.github.io/Obsqura`
- GitHub Personal Access Token (for uploader tool)

---

## Step 1: Enable GitHub Pages with GitHub Actions

### 1.1 Navigate to Repository Settings
1. Go to your repository: `https://github.com/ayushjha-dev/Obsqura/Obsqura`
2. Click on **Settings** tab
3. Scroll down to **Pages** in the left sidebar

### 1.2 Configure Build and Deployment
1. Under "Build and deployment"
2. **Source**: Select **GitHub Actions**
3. GitHub will automatically detect the Jekyll configuration

### 1.3 Verify Workflow File
Ensure `.github/workflows/pages-deploy.yml` exists (it should be included with Chirpy starter)

If missing, create `.github/workflows/pages-deploy.yml`:

```yaml
name: "Build and Deploy"
on:
  push:
    branches:
      - main
      - master
    paths-ignore:
      - .gitignore
      - README.md
      - LICENSE

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          submodules: true

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v4

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: 3.2
          bundler-cache: true

      - name: Build site
        run: bundle exec jekyll b -d "_site${{ steps.pages.outputs.base_path }}"
        env:
          JEKYLL_ENV: "production"

      - name: Test site
        run: |
          bundle exec htmlproofer _site \
            \-\-disable-external=true \
            \-\-ignore-urls "/^http:\/\/127.0.0.1/,/^http:\/\/0.0.0.0/,/^http:\/\/localhost/"

      - name: Upload site artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: "_site${{ steps.pages.outputs.base_path }}"

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## Step 2: Push Your Changes

### 2.1 Initialize Git (if not already done)
```bash
cd "c:\Users\Ns8pc\Videos\Screen Recordings\chirpy-starter-main"
git init
git add .
git commit -m "Initial setup: Personalized Obsqura blog"
```

### 2.2 Connect to GitHub Repository
```bash
git remote add origin https://github.com/ayushjha-dev/Obsqura/Obsqura.git
git branch -M main
```

### 2.3 Push to GitHub
```bash
git push -u origin main
```

**Alternative** (if you prefer HTTPS with token):
```bash
git remote set-url origin https://YOUR_PAT@github.com/ayushjha-dev/Obsqura.git
git push -u origin main
```

---

## Step 3: Monitor Build Status

### 3.1 Check GitHub Actions
1. Go to your repository
2. Click on **Actions** tab
3. Watch the "Build and Deploy" workflow
4. Wait for green checkmark ✅ (usually takes 2-5 minutes)

### 3.2 Common Build Issues

**Issue**: `Bundler::GemNotFound`
- **Solution**: Ensure `Gemfile` and `Gemfile.lock` are committed

**Issue**: `Page build failed`
- **Solution**: Check workflow logs for specific errors
- Verify `_config.yml` has no syntax errors

**Issue**: `404 Page Not Found`
- **Solution**: Wait 5-10 minutes after first deployment
- Clear browser cache
- Verify GitHub Pages is enabled

---

## Step 4: Verification Checklist

### 4.1 Site Accessibility
- [ ] Visit `https://ayushjha-dev.github.io/Obsqura`
- [ ] Confirm site loads without errors
- [ ] Check dark theme is active

### 4.2 Configuration Verification
- [ ] Title shows "Obsqura"
- [ ] Tagline: "Learn, Practice & Master Cybersecurity Skills"
- [ ] About page contains personal bio
- [ ] Social links work (LinkedIn, TryHackMe, Instagram, YouTube, GitHub)

### 4.3 Content Structure
- [ ] Create a test directory: `assets/img/posts/20251229/`
- [ ] Verify image paths work correctly
- [ ] Test post creation with standard front matter

### 4.4 Uploader Tool
- [ ] Open `uploader.html` in browser (local file)
- [ ] Copy master prompt successfully
- [ ] Test GitHub authentication with your PAT
- [ ] Upload a test post and image

---

## Step 5: Using the Uploader Tool

### 5.1 Generate Content with AI
1. Open `uploader.html` in your browser (double-click the file)
2. Click "📋 Copy Master Prompt to Clipboard"
3. Paste into ChatGPT/Claude/Gemini
4. Ask AI to generate a blog post on any cybersecurity topic
5. Save AI output as a `.md` file

### 5.2 Prepare Images
- Create images or screenshots for your post
- Name them descriptively (e.g., `nmap-scan-results.png`)

### 5.3 Upload to GitHub
1. In uploader tool, PAT is already pre-configured
2. Verify repository settings (already pre-filled)
3. Select your `.md` file
4. Select your images (multiple selection supported)
5. Click "🚀 Publish to GitHub"
6. Wait for success message

### 5.4 Verify Upload
1. Check GitHub repository for new files
2. Wait for GitHub Actions to rebuild (2-5 minutes)
3. Visit your blog to see the new post

---

## Step 6: Final Configuration Review

### Items to Check (Pre-deployment Verification):

#### PWA Settings
- **Status**: PWA is ENABLED in `_config.yml` (line 141)
- **Action Needed**: ✅ No changes needed (good default)

#### Avatar/Logo
- **Current**: No avatar set
- **Recommendation**: Add a cybersecurity-themed avatar
- **Path**: Place image in `/assets/img/avatar.jpg` or similar
- **Update** `_config.yml` line 101:
  ```yaml
  avatar: /assets/img/avatar.jpg
  ```

#### Social Preview Image
- **Current**: Not set
- **Recommendation**: Add for better social media sharing
- **Update** `_config.yml` line 105:
  ```yaml
  social_preview_image: /assets/img/social-preview.jpg
  ```

#### Comments System
- **Current**: Disabled
- **Options**: Disqus, Utterances, or Giscus
- **Action**: If you want comments, uncomment and configure in `_config.yml` (lines 110-130)

#### Analytics
- **Current**: None configured
- **Options**: Google Analytics, GoatCounter, Umami, etc.
- **Action**: If you want analytics, add ID in `_config.yml` (lines 60-74)

---

## Step 7: Post-Deployment Best Practices

### 7.1 Regular Backups
```bash
# Backup your repository regularly
git pull origin main
```

### 7.2 Content Workflow
1. Use uploader tool for quick publishing
2. Review posts in repository before they go live
3. Use descriptive commit messages

### 7.3 SEO Optimization
- Submit site to Google Search Console
- Create `robots.txt` if needed
- Monitor with analytics

### 7.4 Security
- **NEVER** commit your PAT to the repository
- Rotate PAT every 6 months
- Use minimal permissions (only `repo` scope)

---

## Troubleshooting

### Site Not Updating After Push
1. Check Actions tab for build status
2. Hard refresh browser (Ctrl+F5)
3. Clear browser cache
4. Wait 10 minutes and try again

### Images Not Displaying
1. Verify images are in correct directory: `/assets/img/posts/YYYYMMDD/`
2. Check Front Matter image path matches actual file location
3. Ensure image files were successfully pushed to GitHub

### Uploader Tool Errors
1. **401 Unauthorized**: Check PAT is correct and has `repo` permission
2. **404 Not Found**: Verify repository owner/name are correct
3. **403 Forbidden**: PAT may have expired, generate a new one

---

## Questions Before Finalizing

Please confirm or provide details for the following:

1. **Avatar Image**: Do you have a logo/avatar image for your blog? If yes, please provide it.

2. **Social Preview Image**: Do you have an image for social media previews (recommended 1200x630px)?

3. **Comments**: Do you want to enable comments? If yes, which system? (Giscus is recommended for GitHub users)

4. **Analytics**: Do you want visitor analytics? If yes, which service?

5. **Additional Categories**: Are the suggested cybersecurity categories sufficient, or do you want to add more?

6. **Custom Domain**: Do you plan to use a custom domain (e.g., `obsqura.com`) instead of `ayushjha-dev.github.io/Obsqura`?

---

## Summary

✅ **Completed**:
- Site personalized with Obsqura branding
- Configuration files updated
- Content structure defined
- Uploader tool created
- Deployment guide prepared

⏳ **Next Steps**:
1. Answer clarification questions above
2. Push repository to GitHub
3. Enable GitHub Pages with Actions
4. Test uploader tool with first post
5. Monitor initial deployment

---

**Support**: If you encounter any issues, check the troubleshooting section or review GitHub Actions logs for specific error messages.

**Happy Blogging!** 🛡️ Stay curious, stay secure!

