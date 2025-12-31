# 🚀 Obsqura AI-to-Blog Uploader - User Guide

## Overview
The **Obsqura AI-to-Blog Uploader** is a standalone HTML tool that allows you to publish blog posts and images directly to your GitHub repository without using Git commands.

---

## 🎯 Quick Start (3 Steps)

### Step 1: Generate Content with AI
1. Double-click `uploader.html` to open in your browser
2. Click "📋 Copy Master Prompt to Clipboard"
3. Paste into ChatGPT, Claude, or Gemini
4. Ask AI: "Generate a blog post about [topic]"
5. Save AI output as a `.md` file

### Step 2: Configure GitHub
Enter your GitHub details (pre-filled):
- **PAT:** Your Personal Access Token
- **Owner:** ayushjha-dev
- **Repo:** ayushjha-dev.github.io
- **Branch:** main

### Step 3: Upload & Publish
1. Select your `.md` file
2. Select images (optional, multiple supported)
3. Click "🚀 Publish to GitHub"
4. Wait for success message!

---

## 📋 Master Prompt Details

The tool generates this prompt for AI:

```
You are a professional cybersecurity content writer for "Obsqura".

Generate a complete Jekyll Chirpy blog post with:
- Proper YAML front matter (title, date, categories, tags, image, author)
- Asia/Kolkata timezone
- Cybersecurity-focused categories
- Markdown formatting
- Code examples
- Image suggestions (3-5 filenames)
- SEO optimization
```

---

## 🔐 GitHub PAT Setup

### Creating a Personal Access Token

1. **Go to GitHub Settings**
   - Click your profile → Settings
   - Scroll to "Developer settings"
   - Click "Personal access tokens" → "Tokens (classic)"

2. **Generate New Token**
   - Click "Generate new token (classic)"
   - Name: "Obsqura Blog Uploader"
   - Expiration: 90 days (or custom)
   - **Scopes:** Check ONLY `repo` (full control of private repositories)

3. **Copy Token**
   - Copy the generated token (starts with `ghp_`)
   - **SAVE IT SECURELY** - You won't see it again!

4. **Use in Uploader**
   - Paste into "GitHub Personal Access Token" field
   - Token is NOT saved in browser
   - Re-enter each time you use the tool (for security)

### Security Best Practices
- ✅ Never commit PAT to repository
- ✅ Use minimal permissions (`repo` only)
- ✅ Set expiration date (90 days recommended)
- ✅ Rotate regularly
- ✅ Revoke if compromised

---

## 📁 How File Upload Works

### Markdown File Processing
1. Tool reads your `.md` file
2. Extracts date from front matter (e.g., `2025-12-29`)
3. Extracts title and creates slug (e.g., `sql-injection-tutorial`)
4. Creates filename: `2025-12-29-sql-injection-tutorial.md`
5. Uploads to: `_posts/2025-12-29-sql-injection-tutorial.md`

### Image Processing
1. Reads date from markdown front matter
2. Creates directory: `/assets/img/posts/YYYYMMDD/`
3. Uploads each image with original filename
4. Examples:
   - `burpsuite-scan.png` → `/assets/img/posts/20251229/burpsuite-scan.png`
   - `nmap-results.jpg` → `/assets/img/posts/20251229/nmap-results.jpg`

### Automatic Actions
- ✅ Creates directories if they don't exist
- ✅ Generates commit messages
- ✅ Pushes directly to main branch
- ✅ Triggers GitHub Actions build

---

## 🎨 UI Features

### Progress Bar
- Shows upload progress (0% → 100%)
- Updates in real-time
- Indicates current task

### Status Messages
- **🟢 Success:** Green background, upload complete
- **🔴 Error:** Red background, shows error details
- **🔵 Info:** Blue background, processing updates

### File Preview
- Shows selected markdown file name
- Lists all selected images
- Preview before upload

---

## ✅ Example Workflow

### Scenario: Publishing "Nmap Tutorial"

#### 1. Generate Content
```
You (to ChatGPT): "Generate a comprehensive blog post about Nmap 
scanning techniques for Obsqura cybersecurity blog. Include basic 
to advanced examples."

ChatGPT: [Generates complete markdown with front matter]

You: Save as "nmap-tutorial.md"
```

#### 2. Prepare Images
Create/capture screenshots:
- `nmap-basic-scan.png`
- `nmap-service-detection.png`
- `nmap-output-analysis.png`

#### 3. Upload
1. Open `uploader.html`
2. Copy master prompt (optionally, for next time)
3. Enter GitHub PAT
4. Select `nmap-tutorial.md`
5. Select 3 images
6. Click "🚀 Publish to GitHub"

#### 4. Result
Files uploaded:
```
_posts/2025-12-29-nmap-tutorial.md
assets/img/posts/20251229/nmap-basic-scan.png
assets/img/posts/20251229/nmap-service-detection.png
assets/img/posts/20251229/nmap-output-analysis.png
```

#### 5. Go Live
- GitHub Actions builds site (3-5 minutes)
- Post appears at: `https://ayushjha-dev.github.io/posts/nmap-tutorial/`

---

## 🔧 Troubleshooting

### Error: "401 Unauthorized"
**Cause:** Invalid or expired PAT  
**Solution:**
1. Verify PAT is correct (copy-paste carefully)
2. Check PAT hasn't expired
3. Ensure PAT has `repo` permission
4. Generate new PAT if needed

### Error: "404 Not Found"
**Cause:** Incorrect repository name/owner  
**Solution:**
1. Verify owner: `ayushjha-dev`
2. Verify repo: `ayushjha-dev.github.io`
3. Check repository exists and is accessible
4. Ensure you have write access

### Error: "422 Validation Failed"
**Cause:** File already exists or invalid content  
**Solution:**
1. Change post filename (different date/title)
2. Check markdown front matter is valid YAML
3. Ensure date format is correct
4. Try with a new post

### Images Not Uploading
**Cause:** File too large or invalid format  
**Solution:**
1. Compress images (keep under 2MB each)
2. Use common formats: JPG, PNG, GIF, WebP
3. Remove special characters from filenames
4. Try uploading images individually

### "No Date Found" Error
**Cause:** Invalid front matter in markdown  
**Solution:**
1. Ensure front matter starts with `---`
2. Include valid date line: `date: 2025-12-29 21:00:00 +0530`
3. Check YAML syntax is correct
4. No tabs, only spaces for indentation

---

## 💡 Pro Tips

### Optimize Your Workflow
1. **Save PAT Securely:** Use a password manager
2. **Batch Process:** Upload multiple posts in succession
3. **Image Names:** Use descriptive, SEO-friendly names
4. **Preview Locally:** Test markdown before uploading
5. **Incremental Posts:** Don't wait to perfect everything

### Image Best Practices
- **Size:** 800-1200px wide for featured images
- **Format:** JPG for photos, PNG for screenshots
- **Compression:** Use tinypng.com before upload
- **Alt Text:** Always include in front matter

### Content Tips
- **Front Matter:** Copy from existing post as template
- **Categories:** Use 1-2 max, from predefined list
- **Tags:** 3-5 specific tags
- **Featured Image:** Always include for better social sharing

---

## 🎯 What Happens After Upload?

### Immediate
1. Files pushed to GitHub repository
2. Commit visible in repository history
3. GitHub Actions workflow triggered

### Within 3-5 Minutes
1. Jekyll builds your site
2. New post processed and rendered
3. Site deployed to GitHub Pages
4. Post accessible via URL

### Verification Steps
1. Check GitHub Actions tab - look for green checkmark ✅
2. Visit site: `https://ayushjha-dev.github.io`
3. Navigate to new post
4. Verify images display correctly
5. Test on mobile

---

## 📊 Feature Comparison

| Feature | Uploader Tool | Manual Git | Github.com UI |
|---------|---------------|------------|----------------|
| **No Git Knowledge** | ✅ | ❌ | ✅ |
| **Batch Image Upload** | ✅ | ❌ | ❌ |
| **AI Integration** | ✅ | ❌ | ❌ |
| **Auto Path Detection** | ✅ | ❌ | ❌ |
| **Progress Feedback** | ✅ | ⚠️ | ⚠️ |
| **Local File Access** | ✅ | ✅ | ❌ |
| **Speed** | ⚡ Fast | ⚡ Fast | 🐢 Slow |

---

## 🔒 Security & Privacy

### What Gets Sent to GitHub?
- ✅ Markdown file content
- ✅ Image files (base64 encoded)
- ✅ Commit messages

### What Stays Local?
- ✅ Your PAT (enter each time)
- ✅ Original files (not deleted)
- ✅ Browser data (no tracking)

### No Data Collection
- ❌ No analytics
- ❌ No external requests (except GitHub API)
- ❌ No cookies
- ❌ No tracking

---

## 📈 Advanced Usage

### Custom Commit Messages
Currently auto-generated. To customize:
1. Edit `uploader.html`
2. Find message in JavaScript
3. Modify template

### Different Branch
Change branch field from `main` to:
- `develop` - For staging
- `feature-xyz` - For testing

### Multiple Repositories
You can use the same tool for different repos:
1. Change owner/repo fields
2. Upload to different blog
3. No code changes needed

---

## 🆘 Support

### Common Issues
- **Tool not opening?** Double-click HTML file (don't right-click open)
- **PAT not working?** Regenerate with `repo` scope only
- **Upload stuck?** Check internet connection
- **Images missing?** Verify paths in markdown match uploads

### Getting Help
1. Check `DEPLOYMENT-GUIDE.md` for troubleshooting
2. Review GitHub Actions logs for build errors
3. Verify file structure in repository
4. Test with sample post first

---

## 🎉 Enjoy Hassle-Free Publishing!

The Obsqura uploader eliminates the complexity of Git, allowing you to focus on creating great cybersecurity content!

**Happy Blogging! 🛡️**

---

*Tool Version: 1.0*  
*Created: December 29, 2025*  
*Compatible with: Any modern browser (Chrome, Firefox, Edge, Safari)*
