# Obsqura Content & Image Structure Standards

## Image Path Convention

All blog post images should be stored in:
```
/assets/img/posts/YYYYMMDD/
```

**Example:**
- For a post dated January 15, 2024, images go in: `/assets/img/posts/20240115/`
- For a post dated December 29, 2025, images go in: `/assets/img/posts/20251229/`

## Standard Front Matter Template

Every new post MUST include the following YAML front matter:

```yaml
---
title: "Your Post Title Here"
date: YYYY-MM-DD HH:MM:SS +0530
categories: [Category1, Category2]
tags: [tag1, tag2, tag3]
image:
  path: /assets/img/posts/YYYYMMDD/featured-image.jpg
  alt: "Alternative text for the image"
author: ayushjha
---
```

## Categories for Cybersecurity Blog

Recommended primary categories:
- **Ethical Hacking** - Penetration testing, vulnerability exploitation
- **Network Security** - Firewalls, IDS/IPS, network protocols
- **Web Security** - OWASP, XSS, SQL injection, web app vulnerabilities
- **Malware Analysis** - Reverse engineering, malware detection
- **CTF Writeups** - Capture The Flag challenge solutions
- **Tools & Resources** - Security tools, frameworks, utilities
- **Tutorials** - Step-by-step guides and how-tos
- **Industry Insights** - News, trends, best practices

## Tags Best Practices

Use specific, searchable tags:
- Tool names: `burpsuite`, `nmap`, `wireshark`, `metasploit`
- Techniques: `sql-injection`, `xss`, `privilege-escalation`
- Platforms: `tryhackme`, `hackthebox`, `vulnhub`
- Technologies: `linux`, `windows`, `python`, `bash`

## Example Post Front Matter

```yaml
---
title: "SQL Injection Tutorial: From Basics to Advanced"
date: 2025-12-29 21:00:00 +0530
categories: [Web Security, Tutorials]
tags: [sql-injection, web-security, owasp, burpsuite]
image:
  path: /assets/img/posts/20251229/sql-injection-banner.jpg
  alt: "SQL Injection attack demonstration"
author: ayushjha
---
```

## Directory Creation

Before uploading a post with images, ensure the directory exists:

```bash
mkdir -p assets/img/posts/YYYYMMDD
```

## Image Naming Convention

Use descriptive, kebab-case names:
- ✅ `network-topology-diagram.png`
- ✅ `burpsuite-intercept-request.jpg` - ✅ `xss-payload-execution.gif`
- ❌ `IMG_1234.jpg`
- ❌ `Screenshot 2025-12-29.png`
