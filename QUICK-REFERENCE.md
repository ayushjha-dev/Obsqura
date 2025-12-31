# Obsqura Quick Reference Guide

## 🚀 Quick Start Commands

### Local Development
```bash
# Install dependencies
bundle install

# Run local server
bundle exec jekyll serve

# Visit your site
# http://localhost:4000
```

### Git Workflow
```bash
# Add all changes
git add .

# Commit with message
git commit -m "Add new post: [topic]"

# Push to GitHub
git push origin main
```

---

## 📝 Creating New Posts

### File Naming Convention
```
_posts/YYYY-MM-DD-title-slug.md
```

**Example:**
```
_posts/2025-12-29-sql-injection-tutorial.md
```

### Front Matter Template
```yaml
---
title: "Your Post Title"
date: YYYY-MM-DD HH:MM:SS +0530
categories: [Category1, Category2]
tags: [tag1, tag2, tag3]
image:
  path: /assets/img/posts/YYYYMMDD/featured.jpg
  alt: "Image description"
author: ayushjha
---
```

---

## 📁 Directory Structure

```
chirpy-starter-main/
├── _config.yml                 # Main configuration
├── _data/
│   ├── contact.yml            # Social links
│   └── share.yml              # Share options
├── _posts/                     # Your blog posts
│   └── YYYY-MM-DD-title.md
├── _tabs/                      # Main pages
│   ├── about.md
│   ├── archives.md
│   ├── categories.md
│   └── tags.md
├── assets/
│   └── img/
│       └── posts/
│           └── YYYYMMDD/      # Post images
├── uploader.html              # Content uploader tool
├── CONTENT-STRUCTURE.md       # Content guidelines
└── DEPLOYMENT-GUIDE.md        # Deployment instructions
```

---

## 🎯 Recommended Categories

- **Ethical Hacking** - Pentesting, exploitation
- **Network Security** - Firewalls, protocols
- **Web Security** - OWASP, web vulnerabilities
- **Malware Analysis** - Reverse engineering
- **CTF Writeups** - Challenge solutions
- **Tools & Resources** - Tool guides
- **Tutorials** - How-to guides
- **Industry Insights** - News, trends

---

## 🏷️ Common Tags

### Tools
`nmap`, `burpsuite`, `metasploit`, `wireshark`, `john`, `hydra`, `sqlmap`

### Techniques
`sql-injection`, `xss`, `csrf`, `privilege-escalation`, `buffer-overflow`, `reverse-shell`

### Platforms
`tryhackme`, `hackthebox`, `vulnhub`, `picoctf`

### Technologies
`linux`, `windows`, `python`, `bash`, `powershell`, `php`

---

## 🖼️ Image Management

### Create Image Directory
```bash
mkdir -p assets/img/posts/20251229
```

### Reference in Post
```markdown
![Description](/assets/img/posts/20251229/image-name.jpg)
```

### Front Matter Image
```yaml
image:
  path: /assets/img/posts/20251229/featured.jpg
  alt: "Alternative text"
```

---

## 🔧 Uploader Tool Usage

1. **Open** `uploader.html` in browser
2. **Copy** master prompt
3. **Generate** content with AI
4. **Save** as `.md` file
5. **Upload** via tool interface

**GitHub PAT:** Keep secure, never commit to repo!

---

## ✅ Pre-Publish Checklist

- [ ] Front matter complete and correct
- [ ] Images in correct directory (`/assets/img/posts/YYYYMMDD/`)
- [ ] All image paths working
- [ ] Categories and tags appropriate
- [ ] Code blocks have syntax highlighting
- [ ] Spell check completed
- [ ] Preview locally before pushing

---

## 🌐 Deployment URLs

- **Production:** https://ayushjha-dev.github.io/Obsqura
- **Repository:** https://github.com/ayushjha-dev/Obsqura/Obsqura
- **GitHub Actions:** https://github.com/ayushjha-dev/Obsqura/Obsqura/actions

---

## 🐛 Troubleshooting

### Build Fails
```bash
# Check Jekyll version
bundle exec jekyll -v

# Update dependencies
bundle update

# Clear cache
bundle exec jekyll clean
```

### Site Not Updating
1. Check GitHub Actions status
2. Hard refresh (Ctrl+F5)
3. Clear browser cache
4. Wait 5-10 minutes

### Images Not Showing
1. Verify path: `/assets/img/posts/YYYYMMDD/filename.jpg`
2. Check file exists in repo
3. Use lowercase filenames
4. Avoid spaces in names

---

## 📚 Useful Markdown Syntax

### Code Blocks
````markdown
```python
def hello_world():
    print("Hello, Obsqura!")
```
````

### Alerts/Callouts
```markdown
> This is a tip
{: .prompt-tip }

> This is info
{: .prompt-info }

> This is a warning
{: .prompt-warning }

> This is danger
{: .prompt-danger }
```

### Tables
```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

### Links
```markdown
[Link Text](https://example.com)
[Link with Title](https://example.com "Tooltip text")
```

---

## 🔐 Security Best Practices

- ✅ Never commit PAT to repository
- ✅ Use environment variables for secrets
- ✅ Rotate tokens every 6 months
- ✅ Use minimal permissions
- ✅ Enable 2FA on GitHub

---

## 📞 Support & Resources

- **Jekyll Docs:** https://jekyllrb.com/docs/
- **Chirpy Theme:** https://github.com/cotes2020/jekyll-theme-chirpy
- **Markdown Guide:** https://www.markdownguide.org/
- **GitHub Pages:** https://docs.github.com/en/pages

---

## 💡 Pro Tips

1. **Use descriptive commit messages** - Makes tracking changes easier
2. **Write drafts offline** - Polish before publishing
3. **Test locally first** - Catch errors early
4. **Use categories wisely** - 2-3 max per post
5. **Tag specifically** - Helps with searchability
6. **Optimize images** - Keep file sizes under 500KB
7. **Internal linking** - Connect related posts
8. **SEO-friendly titles** - 50-60 characters optimal

---

**Last Updated:** December 29, 2025  
**Version:** 1.0  
**Maintained by:** Ayush Kumar Jha (@ayushjha-dev)

