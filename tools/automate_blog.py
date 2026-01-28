import os
import datetime
import re
import json
import sys
import random
import requests
from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types
from github import Github
from datetime import timezone, timedelta

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("⚠️  PyYAML not installed. YAML validation will be limited.")
    print("   Install with: pip install PyYAML")

# --- CONFIGURATION ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GH_TOKEN = os.getenv("GH_TOKEN")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
REPO_NAME = "ayushjha-dev/Obsqura"
TOPICS_FILE = "topics.txt"
STATUS_FILE = "tools/status.json"

# Validate required environment variables
if not GEMINI_API_KEY:
    print("❌ ERROR: GEMINI_API_KEY environment variable is not set!")
    print("   Please set it with: export GEMINI_API_KEY='your-api-key-here'")
    sys.exit(1)

if not GH_TOKEN:
    print("❌ ERROR: GH_TOKEN environment variable is not set!")
    print("   Please set it with: export GH_TOKEN='your-github-token-here'")
    sys.exit(1)

# Note: UNSPLASH_ACCESS_KEY is optional - will skip Unsplash fallback if not set
if not UNSPLASH_ACCESS_KEY:
    print("⚠️  Warning: UNSPLASH_ACCESS_KEY not set. Image generation will skip Unsplash fallback.")

# Initialize the NEW Google GenAI client
client = genai.Client(api_key=GEMINI_API_KEY)

def get_ist_time():
    """Get current time in IST (India Standard Time) timezone."""
    # IST is UTC+5:30
    ist_offset = timedelta(hours=5, minutes=30)
    ist_tz = timezone(ist_offset)
    return datetime.datetime.now(ist_tz)

def get_next_topic():
    """Get the next unprocessed topic from topics.txt."""
    if not os.path.exists(STATUS_FILE):
        current_day = 1
    else:
        with open(STATUS_FILE, 'r') as f:
            status = json.load(f)
            current_day = status.get("next_day", 1)

    if not os.path.exists(TOPICS_FILE):
        return None, None, None

    with open(TOPICS_FILE, 'r') as f:
        content = f.read()
    
    pattern = rf"Day {current_day}\nTopic: (.*?)\n(?:Additional Details: (.*?)\n)?"
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        return current_day, match.group(1).strip(), (match.group(2) or "").strip()
    return None, None, None

def generate_blog_content(topic, details, day):
    """Generate blog post content using Gemini AI with enhanced visual appeal."""
    # Use latest stable gemini-2.5-flash for text generation (faster and more cost-effective)
    # Alternative: gemini-2.5-pro for more complex reasoning tasks
    prompt = f"""
    You are a MASTER STORYTELLER and professional cybersecurity writer for "Obsqura" blog.
    Research and include the LATEST information, trends, and developments about this topic.
    
    TOPIC: {topic}
    DETAILS: {details}

    CRITICAL YAML FORMATTING RULES:
    - The title field MUST be enclosed in double quotes
    - Each YAML field must be on its own line with proper spacing
    - Ensure proper indentation (2 spaces) for nested fields
    - Do NOT use colons or special characters in unquoted strings
    - Example of proper YAML front matter:
    ---
    title: "Your Blog Title Here"
    date: 2026-01-09 10:00:00 +0530
    author: ayushjha
    categories: [Tutorials, Industry Insights]
    tags: [Tag1, Tag2, Tag3]
    image:
      path: /assets/img/posts/day-1/1-hero-banner.png
      alt: Description of the image
    description: Brief description of the post
    ---

    STRICT REQUIREMENTS:
    1. Output valid Jekyll Front Matter with these exact fields:
       - title: "YOUR TITLE HERE" (MUST be quoted, engaging, SEO-optimized)
       - date: {get_ist_time().strftime('%Y-%m-%d %H:%M:%S %z')}
       - author: ayushjha
       - categories: [Tutorials, Industry Insights]
       - tags: (5-7 relevant tags in an array)
       - image:
           path: /assets/img/posts/day-{day}/1-hero-banner.png
           alt: (descriptive alt text - keep it short and descriptive)
       - description: (compelling 150-160 char meta description - keep it concise)
    
    2. VISUAL APPEAL - Make it look like a professional blog:
       - Start with an engaging hook (1-2 sentences that grab attention)
       - Use emojis strategically (🔐 🛡️ ⚡ 💡 🚀 ⚠️ ✅ 📊) for visual breaks
       - Add visual separators like "---" between major sections
       - Use blockquotes (> ) for key takeaways or important quotes
       - Include tables for comparisons or data when relevant
       - Use numbered lists for steps/processes
       - Use bullet points for features/benefits
       - Add code blocks with syntax highlighting when showing examples
    
    3. CONTENT STRUCTURE:
       ## Introduction
       - Hook the reader immediately
       - State what they'll learn
       - Why this matters NOW (use latest info/trends)
       
       ## Main Content (3-5 sections with H2 headings)
       - Each section should be 2-3 paragraphs
       - Include PRACTICAL examples from real-world scenarios
       - Use Chirpy callouts for emphasis:
         {{: .prompt-tip}} for helpful tips
         {{: .prompt-info}} for additional information
         {{: .prompt-warning}} for security warnings
         {{: .prompt-danger}} for critical security issues
       - Add code snippets where relevant (properly formatted)
       - Include recent statistics or data (2024-2026)
       
       ## Key Takeaways
       - Summarize 3-5 main points as bullet list
       - Make them actionable
       
       ## Conclusion
       - Reinforce main message
       - Call to action
       - End with signature: **—Mr. Xploit** 🛡️
    
    4. TONE & STYLE:
       - Professional yet conversational
       - Educational but engaging (like teaching a friend)
       - Use analogies to explain complex concepts
       - Vary sentence length for better flow
       - Include questions to engage readers
       - Reference CURRENT events or recent breaches when relevant
    
    5. SEO & ENGAGEMENT:
       - Use keywords naturally throughout
       - Add external reference links to authoritative sources (e.g., NIST, CISA, academic papers)
       - Front-load important information
       - Use descriptive anchor text for all external links
    
    6. LENGTH: Aim for 1000-1500 words (comprehensive but readable)
    
    Return ONLY the raw markdown content with complete front matter and body.
    DO NOT add any explanations or comments outside the markdown.
    DO NOT wrap the output in markdown code blocks (no ```markdown or ``` tags).
    """
    
    # Add retry logic and error handling for Gemini API
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"  ⚠️  Gemini API attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                import time
                wait_time = (attempt + 1) * 2  # Exponential backoff: 2s, 4s, 6s
                print(f"  ⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print(f"  ❌ All Gemini API attempts failed!")
                raise Exception(f"Gemini API failed after {max_retries} attempts: {e}")

def validate_and_clean_content(content):
    """Remove broken internal blog links, markdown code block wrappers, and fix YAML formatting."""
    import re
    
    # Step 1: Remove markdown code block wrappers (```markdown ... ``` or ```md ... ```)
    # This handles cases where Gemini wraps the entire response in code blocks
    code_block_pattern = r'^```(?:markdown|md)?\s*\n(.*?)\n```\s*$'
    match = re.match(code_block_pattern, content.strip(), re.DOTALL)
    if match:
        content = match.group(1)
        print(f"  ✓ Removed markdown code block wrapper")
    
    # Step 2: Fix YAML front matter formatting issues
    # Extract the YAML front matter
    yaml_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    yaml_match = re.match(yaml_pattern, content, re.DOTALL)
    
    if yaml_match:
        yaml_content = yaml_match.group(1)
        body_content = yaml_match.group(2)
        
        # Fix common YAML issues:
        # 1. Ensure title is quoted if it contains colons or special characters
        title_match = re.search(r'^title:\s*(.+)$', yaml_content, re.MULTILINE)
        if title_match:
            title_value = title_match.group(1).strip()
            # Check if title is not already quoted and contains special chars
            if not (title_value.startswith('"') and title_value.endswith('"')):
                # Quote the title if it contains colons, emojis, or other special chars
                if ':' in title_value or any(ord(c) > 127 for c in title_value):
                    quoted_title = f'"{title_value}"'
                    yaml_content = re.sub(
                        r'^title:\s*.+$',
                        f'title: {quoted_title}',
                        yaml_content,
                        count=1,
                        flags=re.MULTILINE
                    )
                    print(f"  ✓ Fixed title quoting")
        
        # 2. Ensure proper newlines between fields (no fields concatenated)
        # This fixes issues like "date: 2026-01-09 15:27:18 +0530author: ayushjha"
        yaml_content = re.sub(r'(\+\d{4})([a-z])', r'\1\n\2', yaml_content)
        
        # 3. Validate YAML if PyYAML is available
        if YAML_AVAILABLE:
            try:
                yaml.safe_load(yaml_content)
                print(f"  ✓ YAML validation passed")
            except yaml.YAMLError as e:
                print(f"  ⚠️  YAML validation error: {e}")
                print(f"  Attempting auto-fix...")
                # Additional fixes can be added here based on common errors
        
        # Reconstruct the content
        content = f"---\n{yaml_content}\n---\n{body_content}"
        print(f"  ✓ YAML formatting verified")
    
    # Step 3: Pattern to find internal blog links (links starting with /blog/ or /posts/)
    internal_link_pattern = r'\[([^\]]+)\]\((/blog/[^\)]+|/posts/[^\)]+)\)'
    
    # Find all internal links
    matches = re.findall(internal_link_pattern, content)
    
    if matches:
        print(f"  ⚠️  Found {len(matches)} internal blog links - removing to prevent broken links:")
        for link_text, url in matches:
            print(f"     - '{link_text}' → {url}")
            # Replace the link with just the text (remove link but keep text)
            content = re.sub(
                rf'\[{re.escape(link_text)}\]\({re.escape(url)}\)',
                f'**{link_text}**',  # Make it bold instead
                content
            )
    
    return content

def generate_image_search_query(topic):
    """Generate a concise, effective Unsplash search query using AI."""
    prompt = f"""
    Generate a specific, highly effective search query for Unsplash to find a relevant and UNIQUE image for this blog topic.
    
    TOPIC: {topic}
    
    REQUIREMENTS:
    - Return 2-3 words that are SPECIFIC to this topic
    - Make the query unique enough to get different results than other topics
    - Must be visual terms that photographers commonly tag
    - Focus on the main concept + descriptive adjective/noun
    - Avoid being too generic (bad: "security", "technology")
    
    Examples:
    - "Zero Trust Architecture" → "zero trust network"
    - "Ransomware Evolution" → "ransomware cyber attack"
    - "Post-quantum cryptography" → "quantum encryption security"
    - "IoT Security" → "smart home security"
    - "Cloud Security" → "cloud security infrastructure"
    - "AI in Cyber Defense" → "artificial intelligence security"
    - "Social Engineering" → "phishing scam attack"
    
    Return ONLY the search query (2-3 words), nothing else.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        search_query = response.text.strip().lower()
        # Remove quotes if AI added them
        search_query = search_query.strip('"\'')
        return search_query
    except Exception as e:
        print(f"  ⚠️  AI query generation failed: {e}")
        # Fallback to simple extraction
        return topic.split(':')[0].split('-')[0].strip().lower()

def compress_image(img, max_size_kb=500):
    """Compress image to be under the specified size in KB."""
    from io import BytesIO
    
    # Start with quality 95
    quality = 95
    img_format = 'PNG'
    
    # Convert RGBA to RGB if needed for JPEG compression
    if img.mode == 'RGBA':
        # Create white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
        img = background
        img_format = 'JPEG'  # Use JPEG for better compression
    elif img.mode == 'RGB':
        img_format = 'JPEG'
    
    # Try to compress until we're under max_size_kb
    while quality > 20:
        buffer = BytesIO()
        img.save(buffer, format=img_format, quality=quality, optimize=True)
        size_kb = buffer.tell() / 1024
        
        if size_kb <= max_size_kb:
            print(f"  ✓ Compressed image to {size_kb:.1f}KB (quality: {quality})")
            buffer.seek(0)
            return Image.open(buffer), img_format
        
        # Reduce quality for next iteration
        quality -= 5
    
    # If still too large, resize the image
    print(f"  ⚠️  Image still large, resizing...")
    width, height = img.size
    img = img.resize((int(width * 0.8), int(height * 0.8)), Image.Resampling.LANCZOS)
    
    buffer = BytesIO()
    img.save(buffer, format=img_format, quality=75, optimize=True)
    size_kb = buffer.tell() / 1024
    print(f"  ✓ Resized and compressed to {size_kb:.1f}KB")
    buffer.seek(0)
    return Image.open(buffer), img_format

def get_unsplash_image(topic, used_images=None):
    """Fetch image from Unsplash with deduplication."""
    # Check if Unsplash API key is available
    if not UNSPLASH_ACCESS_KEY:
        print(f"  ⚠️  Unsplash API key not configured, skipping...")
        return None, None, None
    
    if used_images is None:
        used_images = []
    
    try:
        # Generate AI-powered search query (now returns 2-3 words)
        print(f"  🤖 Generating specific search query with AI...")
        search_query = generate_image_search_query(topic)
        print(f"  📸 Searching Unsplash for: '{search_query}'")
        
        # Fetch 10 images instead of just 1
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query": search_query,
                "per_page": 10,  # Get 10 results for variety
                "orientation": "landscape",
                "client_id": UNSPLASH_ACCESS_KEY
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                # Filter out already used images
                available_photos = [
                    photo for photo in data['results']
                    if photo['urls']['regular'] not in used_images
                ]
                
                if not available_photos:
                    print(f"  ⚠️  All images from this search have been used before")
                    # Try a broader fallback search
                    fallback_query = search_query.split()[0]  # Use first word only
                    print(f"  🔄 Trying fallback search: '{fallback_query}'")
                    response = requests.get(
                        "https://api.unsplash.com/search/photos",
                        params={
                            "query": fallback_query,
                            "per_page": 10,
                            "orientation": "landscape",
                            "client_id": UNSPLASH_ACCESS_KEY
                        },
                        timeout=10
                    )
                    if response.status_code == 200:
                        data = response.json()
                        available_photos = [
                            photo for photo in data.get('results', [])
                            if photo['urls']['regular'] not in used_images
                        ]
                
                if available_photos:
                    # Randomly select one of the available images
                    photo = random.choice(available_photos)
                    image_url = photo['urls']['regular']
                    photographer = photo['user']['name']
                    
                    print(f"  ✅ Selected image by {photographer} (from {len(available_photos)} options)")
                    
                    # Download image
                    img_response = requests.get(image_url, timeout=15)
                    if img_response.status_code == 200:
                        img = Image.open(BytesIO(img_response.content))
                        original_size = len(img_response.content) / 1024
                        print(f"  ✅ Downloaded image ({img.size[0]}x{img.size[1]}px, {original_size:.1f}KB)")
                        
                        # Compress if larger than 500KB
                        if original_size > 500:
                            print(f"  🗜️  Compressing image (original: {original_size:.1f}KB)...")
                            img, _ = compress_image(img, max_size_kb=500)
                        
                        # Return image, photographer, and URL for tracking
                        return img, photographer, image_url
        
        print(f"  ⚠️  No suitable images found on Unsplash")
        return None, None, None
        
    except Exception as e:
        print(f"  ❌ Unsplash error: {e}")
        return None, None, None

def generate_and_save_image(topic, day):
    """Download hero banner image from Unsplash and compress it."""
    img_dir = f"assets/img/posts/day-{day}"
    os.makedirs(img_dir, exist_ok=True)
    img_path = f"{img_dir}/1-hero-banner.png"
    
    # Load used images from status.json
    used_images = []
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                status = json.load(f)
                used_images = status.get('used_images', [])
                print(f"  📋 Loaded {len(used_images)} previously used images")
        except Exception as e:
            print(f"  ⚠️  Could not load used images: {e}")
    
    # Check if Unsplash API key is available
    if not UNSPLASH_ACCESS_KEY:
        print(f"  ⚠️  Unsplash API key not configured!")
        print(f"  Creating placeholder image...")
        placeholder_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        with open(img_path, 'wb') as f:
            f.write(placeholder_png)
        return img_path, None
    
    # Get image from Unsplash (with deduplication)
    try:
        img, photographer, image_url = get_unsplash_image(topic, used_images)
        if img:
            # Determine format based on compression result
            # Save with optimization
            img.save(img_path, format='PNG', optimize=True)
            
            # Check final file size
            final_size = os.path.getsize(img_path) / 1024
            print(f"  ✅ Saved unique image by {photographer} ({final_size:.1f}KB)")
            return img_path, image_url
        else:
            raise Exception("No suitable images found on Unsplash")
    except Exception as e:
        print(f"  ⚠️  Unsplash failed: {e}")
        print(f"  Creating placeholder image...")
        placeholder_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        with open(img_path, 'wb') as f:
            f.write(placeholder_png)
        return img_path, None

def upload_to_github(md_filename, md_content, img_path, status_data=None):
    """Upload markdown post, image, and status.json to GitHub repository."""
    try:
        from github import Auth
        from github import GithubException
        auth = Auth.Token(GH_TOKEN)
        g = Github(auth=auth)
        repo = g.get_repo(REPO_NAME)
        
        # Upload Image (if it's not empty)
        with open(img_path, 'rb') as f:
            img_data = f.read()
        
        if len(img_data) > 100:  # Only upload if it's a real image (not just placeholder)
            try:
                # Check if image already exists
                try:
                    existing_img = repo.get_contents(img_path, ref="main")
                    print(f"⚠ Image already exists on GitHub: {img_path}")
                    print(f"  Skipping upload (file already present)")
                except GithubException as e:
                    if e.status == 404:
                        # File doesn't exist, safe to create
                        repo.create_file(img_path, f"Add image for {md_filename}", img_data, branch="main")
                        print(f"✓ Uploaded image to GitHub: {img_path}")
                    else:
                        raise
            except Exception as e:
                print(f"⚠ Image upload failed: {e}")
                print(f"  You may need to upload the image manually")
        else:
            print(f"⚠ Skipping empty placeholder image upload")
        
        # Upload Markdown Post
        repo_md_path = f"_posts/{md_filename}"
        try:
            # Check if post already exists
            existing_post = repo.get_contents(repo_md_path, ref="main")
            print(f"⚠ Post already exists on GitHub: {repo_md_path}")
            print(f"  Updating existing post...")
            repo.update_file(repo_md_path, f"Update Post: {md_filename}", md_content, existing_post.sha, branch="main")
            print(f"✓ Updated post on GitHub: {repo_md_path}")
        except GithubException as e:
            if e.status == 404:
                # File doesn't exist, safe to create
                repo.create_file(repo_md_path, f"Automated Post: {md_filename}", md_content, branch="main")
                print(f"✓ Uploaded post to GitHub: {repo_md_path}")
            else:
                raise
        
        # Upload status.json (update or create)
        if status_data:
            status_content = json.dumps(status_data, indent=2)
            try:
                # Try to get existing file first
                contents = repo.get_contents(STATUS_FILE, ref="main")
                repo.update_file(STATUS_FILE, f"Update status: Day {status_data['next_day']}", status_content, contents.sha, branch="main")
                print(f"✓ Updated status.json on GitHub: Next run will process Day {status_data['next_day']}")
            except GithubException as e:
                if e.status == 404:
                    # File doesn't exist, create it
                    repo.create_file(STATUS_FILE, f"Create status: Day {status_data['next_day']}", status_content, branch="main")
                    print(f"✓ Created status.json on GitHub: Next run will process Day {status_data['next_day']}")
                else:
                    raise
        
    except Exception as e:
        print(f"❌ GitHub upload failed: {e}")
        print(f"  The files have been generated locally. Please upload manually:")
        print(f"  - Post: _posts/{md_filename}")
        print(f"  - Image: {img_path}")
        raise

def main():
    """Main execution function for automated blog post generation."""
    print("="*60)
    print("🚀 Obsqura Blog Automation Tool")
    print("="*60)
    
    day, topic, details = get_next_topic()
    if not topic:
        print("\n✅ All topics completed or topics.txt is missing.")
        print("   Add more topics to topics.txt to continue automation.")
        return

    print(f"\n📝 Processing Day {day}: {topic}")
    print(f"   Details: {details or 'None'}")
    print("-"*60)
    
    try:
        # Step 1: Generate blog content
        print("\n1️⃣  Generating blog content with AI...")
        md_content = generate_blog_content(topic, details, day)
        print(f"   ✓ Content generated ({len(md_content)} characters)")
        
        # Step 1.5: Validate and clean content
        print("\n1️⃣.5️⃣  Validating content...")
        md_content = validate_and_clean_content(md_content)
        print(f"   ✓ Content validated")
        
        # Step 2: Generate hero image
        print("\n2️⃣  Generating hero banner image...")
        img_path, image_url = generate_and_save_image(topic, day)
        
        # Step 3: Save locally
        clean_title = re.sub(r'[^a-z0-9]', '-', topic.lower()).strip('-')
        md_filename = f"{get_ist_time().strftime('%Y-%m-%d')}-{clean_title}.md"
        
        local_post_path = f"_posts/{md_filename}"
        os.makedirs("_posts", exist_ok=True)
        with open(local_post_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"\n3️⃣  Saved locally: {local_post_path}")
        
        # Step 4: Prepare status update with image tracking
        # Load existing used images
        used_images = []
        if os.path.exists(STATUS_FILE):
            try:
                with open(STATUS_FILE, 'r') as f:
                    existing_status = json.load(f)
                    used_images = existing_status.get('used_images', [])
            except:
                pass
        
        # Add new image URL if available
        if image_url and image_url not in used_images:
            used_images.append(image_url)
            print(f"  📝 Tracking image URL (total tracked: {len(used_images)})")
        
        status_data = {
            "next_day": day + 1,
            "last_processed": topic,
            "used_images": used_images
        }
        
        # Save status locally first
        os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
        with open(STATUS_FILE, 'w') as f:
            json.dump(status_data, f, indent=2)
        
        # Step 5: Upload to GitHub (including status.json)
        print("\n4️⃣  Uploading to GitHub...")
        upload_to_github(md_filename, md_content, img_path, status_data)
        
        print("\n" + "="*60)
        print(f"✅ Successfully published Day {day}: {topic}")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"   Processing failed for Day {day}. Please check the error and try again.")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

