# 🛡️ Obsqura - Cybersecurity Blog

> **Learn, Practice & Master Cybersecurity Skills**

A professional Jekyll-based cybersecurity blog powered by the Chirpy theme, featuring automated content publishing and AI integration.

---

## 📚 Table of Contents

- [About](#about)
- [Features](#features)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Content Publishing](#content-publishing)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Support](#support)

---

## 🎯 About

**Obsqura** is a cybersecurity learning platform created by **Ayush Kumar Jha**, a B.Tech CSE Cybersecurity student. The blog focuses on:

- 🔓 Ethical Hacking & Penetration Testing
- 🌐 Network & Web Security
- 🎯 CTF Writeups & Challenges
- 🔧 Security Tools & Tutorials
- 📊 Industry Insights & Best Practices

**Live Site:** [https://ayushjha-dev.github.io/Obsqura](https://ayushjha-dev.github.io/Obsqura)

---

## ✨ Features

### Core Features
- ✅ **Dark Theme** - Default dark mode for cybersecurity aesthetic
- ✅ **Responsive Design** - Mobile-first, works on all devices
- ✅ **SEO Optimized** - Built-in SEO best practices
- ✅ **PWA Enabled** - Installable as web app
- ✅ **Fast Loading** - Optimized performance
- ✅ **Syntax Highlighting** - Beautiful code blocks

### Custom Features
- 🤖 **AI Integration** - Generate content with ChatGPT/Claude
- 📤 **Auto Uploader** - Publish without Git commands
- 📁 **Organized Structure** - Date-based image organization
- 🏷️ **Smart Tagging** - Cybersecurity-focused categories
- 📱 **Social Integration** - LinkedIn, TryHackMe, YouTube, Instagram

---

## 🚀 Quick Start

### For Local Development

```bash
# Install dependencies
bundle install

# Run local server
bundle exec jekyll serve

# View at http://localhost:4000
```

### For Publishing Content

**Option 1: Use the Uploader Tool** (Recommended)
1. Open `uploader.html` in your browser
2. Generate content with AI
3. Upload and publish instantly

**Option 2: Traditional Git**
```bash
# Add new post to _posts/
git add .
git commit -m "Add new post"
git push origin main
```

---

## 📖 Documentation

All documentation is included in this repository:

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[FINAL-REVIEW.md](FINAL-REVIEW.md)** | Configuration checklist | Before first deployment |
| **[DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md)** | Deployment instructions | Setting up GitHub Pages |
| **[UPLOADER-GUIDE.md](UPLOADER-GUIDE.md)** | Uploader tool tutorial | Publishing new content |
| **[CONTENT-STRUCTURE.md](CONTENT-STRUCTURE.md)** | Content standards | Writing posts |
| **[QUICK-REFERENCE.md](QUICK-REFERENCE.md)** | Command reference | Daily operations |
| **[IMPLEMENTATION-SUMMARY.md](IMPLEMENTATION-SUMMARY.md)** | Project overview | Understanding setup |

### Quick Links
- 📘 **First Time?** Start with [FINAL-REVIEW.md](FINAL-REVIEW.md)
- 🚀 **Ready to Deploy?** Read [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md)
- ✍️ **Publishing Content?** Use [UPLOADER-GUIDE.md](UPLOADER-GUIDE.md)
- 🔍 **Need Quick Help?** Check [QUICK-REFERENCE.md](QUICK-REFERENCE.md)

---

## 📝 Content Publishing

### Method 1: AI-Powered Uploader (Easiest)

1. **Generate Content**
   - Open `uploader.html`
   - Copy the master prompt
   - Paste into ChatGPT/Claude/Gemini
   - Get a complete blog post

2. **Upload**
   - Save AI output as `.md` file
   - Select file in uploader
   - Add images if needed
   - Click "Publish to GitHub"

3. **Done!**
   - Post goes live in 3-5 minutes
   - No Git commands needed
   - No terminal required

### Method 2: Manual Creation

1. **Create Post File**
   ```bash
   _posts/YYYY-MM-DD-title-slug.md
   ```

2. **Add Front Matter**
   ```yaml
   ---
   title: "Your Post Title"
   date: 2025-12-29 21:00:00 +0530
   categories: [Ethical Hacking, Tutorials]
   tags: [pentesting, nmap, security]
   image:
     path: /assets/img/posts/20251229/featured.jpg
     alt: "Image description"
   author: ayushjha
   ---
   ```

3. **Write Content**
   - Use Markdown formatting
   - Add code blocks
   - Include images

4. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add new post: title"
   git push origin main
   ```

---

## ⚙️ Configuration

### Site Settings (_config.yml)

```yaml
title: Obsqura
tagline: "Learn, Practice & Master Cybersecurity Skills"
url: "https://ayushjha-dev.github.io/Obsqura"
timezone: Asia/Kolkata
theme_mode: dark
```

### Author Information

```yaml
social:
  name: Ayush Kumar Jha
  email: ayushjha.dev@gmail.com
  links:
    - https://github.com/ayushjha-dev
    - https://www.linkedin.com/in/ayush-kumar-jha-058b64323/
```

### Social Links (_data/contact.yml)

- GitHub: [ayushjha-dev](https://github.com/ayushjha-dev)
- LinkedIn: [Profile](https://www.linkedin.com/in/ayush-kumar-jha-058b64323/)
- TryHackMe: [Mr.Xploit](https://tryhackme.com/p/Mr.Xploit)
- YouTube: [Obsqura](https://www.youtube.com/@Obsqura-e1v)
- Instagram: [@_ayush_jha_43](https://www.instagram.com/_ayush_jha_43/)

---

## 🌐 Deployment

### Prerequisites
- GitHub account
- Repository: `ayushjha-dev.github.io/Obsqura`
- GitHub Personal Access Token (for uploader)

### Deploy to GitHub Pages

1. **Enable GitHub Pages**
   - Go to repository Settings
   - Navigate to Pages
   - Source: GitHub Actions

2. **Push Code**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Obsqura blog"
   git remote add origin https://github.com/ayushjha-dev/Obsqura/Obsqura.git
   git push -u origin main
   ```

3. **Monitor Build**
   - Check Actions tab
   - Wait for green checkmark (3-5 minutes)
   - Visit `https://ayushjha-dev.github.io/Obsqura`

**Detailed Instructions:** See [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md)

---

## 📂 Project Structure

```
chirpy-starter-main/
├── _config.yml                # Main configuration
├── _data/
│   ├── contact.yml           # Social links
│   └── share.yml             # Share buttons
├── _posts/                    # Blog posts
│   └── YYYY-MM-DD-title.md
├── _tabs/                     # Main pages
│   ├── about.md              # About page
│   ├── archives.md           # Post archives
│   ├── categories.md         # Categories page
│   └── tags.md               # Tags page
├── assets/
│   └── img/
│       └── posts/
│           └── YYYYMMDD/     # Post images
├── uploader.html             # Content uploader tool
├── OBSQURA-README.md         # This file
├── DEPLOYMENT-GUIDE.md       # Deployment instructions
├── UPLOADER-GUIDE.md         # Uploader tutorial
├── CONTENT-STRUCTURE.md      # Content guidelines
├── QUICK-REFERENCE.md        # Quick reference
├── FINAL-REVIEW.md           # Configuration checklist
└── IMPLEMENTATION-SUMMARY.md # Project summary
```

---

## 🎯 Content Categories

### Predefined Categories
1. **Ethical Hacking** - Penetration testing, exploitation
2. **Network Security** - Protocols, firewalls, IDS/IPS
3. **Web Security** - OWASP, web vulnerabilities
4. **Malware Analysis** - Reverse engineering
5. **CTF Writeups** - Challenge solutions
6. **Tools & Resources** - Security tools
7. **Tutorials** - How-to guides
8. **Industry Insights** - News, trends

### Common Tags
`nmap`, `burpsuite`, `metasploit`, `sql-injection`, `xss`, `tryhackme`, `hackthebox`, `linux`, `python`, `bash`

---

## 🛠️ Technologies Used

- **Static Site Generator:** Jekyll 4.x
- **Theme:** Chirpy
- **Hosting:** GitHub Pages
- **CI/CD:** GitHub Actions
- **Analytics:** (Optional) GoatCounter, Google Analytics
- **Comments:** (Optional) Giscus, Utterances

---

## 🔒 Security

### Best Practices Implemented
- ✅ PAT never committed to repository
- ✅ Minimal permissions (repo scope only)
- ✅ Token rotation recommended every 90 days
- ✅ HTTPS enforced on GitHub Pages
- ✅ No tracking or analytics by default

### Ethical Hacking Commitment
All content promotes:
- ✅ Responsible disclosure
- ✅ Authorized testing only
- ✅ Educational purposes
- ❌ No malicious activities
- ❌ No unauthorized access

---

## 📊 Performance

- **Build Time:** 30-60 seconds
- **Deployment Time:** 3-5 minutes
- **Page Load Speed:** < 2 seconds
- **Lighthouse Score:** 90+ (Performance, SEO, Accessibility)

---

## 🤝 Contributing

This is a personal blog, but suggestions are welcome!

- 🐛 **Found a bug?** Open an issue
- 💡 **Have an idea?** Share it
- 📝 **Want to contribute?** Fork and PR

---

## 📞 Support & Contact

### Creator
**Ayush Kumar Jha**  
B.Tech CSE Cyber Security, 2nd Year  
Lamrin Tech Skills University, Punjab

### Connect
- 🐙 GitHub: [@ayushjha-dev](https://github.com/ayushjha-dev)
- 💼 LinkedIn: [Ayush Kumar Jha](https://www.linkedin.com/in/ayush-kumar-jha-058b64323/)
- 🎯 TryHackMe: [Mr.Xploit](https://tryhackme.com/p/Mr.Xploit)
- 📺 YouTube: [Obsqura](https://www.youtube.com/@Obsqura-e1v)
- 📸 Instagram: [@_ayush_jha_43](https://www.instagram.com/_ayush_jha_43/)

### Resources
- Jekyll Documentation: [jekyllrb.com](https://jekyllrb.com)
- Chirpy Theme: [github.com/cotes2020/jekyll-theme-chirpy](https://github.com/cotes2020/jekyll-theme-chirpy)
- GitHub Pages: [docs.github.com/pages](https://docs.github.com/en/pages)

---

## 📝 License

This blog uses the [MIT License](LICENSE) from the Chirpy theme.

Content (blog posts, images) © 2025 Ayush Kumar Jha. All rights reserved.

---

## 🎉 Acknowledgments

- **Chirpy Theme** by [@cotes2020](https://github.com/cotes2020)
- **Jekyll** static site generator
- **GitHub Pages** for free hosting
- **Cybersecurity Community** for inspiration

---

## 🚀 Version History

- **v1.0** (Dec 2025) - Initial setup
  - Personalized configuration
  - AI uploader tool
  - Comprehensive documentation
  - Sample content

---

## 💡 Tips for Success

1. **Consistency** - Publish regularly
2. **Quality** - Focus on practical, hands-on content
3. **Engagement** - Respond to comments and feedback
4. **SEO** - Use proper titles, meta descriptions
5. **Images** - Always include visuals
6. **Code** - Provide working examples
7. **Ethics** - Promote responsible hacking

---

## 🎯 Goals

- 📚 Share knowledge with the cybersecurity community
- 💪 Document personal learning journey
- 🎓 Help beginners get started in cybersecurity
- 🔐 Promote ethical hacking practices
- 🌟 Build a portfolio of technical skills

---

**Ready to start your cybersecurity blogging journey?**

1. Read [FINAL-REVIEW.md](FINAL-REVIEW.md) for configuration
2. Follow [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) to deploy
3. Use [UPLOADER-GUIDE.md](UPLOADER-GUIDE.md) to publish content

**Stay curious. Stay secure.** 🛡️

---

*Last Updated: December 29, 2025*  
*Maintained by: Ayush Kumar Jha*  
*Website: https://ayushjha-dev.github.io/Obsqura*

