import os
import datetime
import re
import json
import sys
import requests
from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types
from github import Github

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

def generate_blog_content(topic, details):
    """Generate blog post content using Gemini AI with enhanced visual appeal."""
    # Use latest stable gemini-2.5-flash for text generation (faster and more cost-effective)
    # Alternative: gemini-2.5-pro for more complex reasoning tasks
    prompt = f"""
    You are a MASTER STORYTELLER and professional cybersecurity writer for "Obsqura" blog.
    Research and include the LATEST information, trends, and developments about this topic.
    
    TOPIC: {topic}
    DETAILS: {details}

    STRICT REQUIREMENTS:
    1. Output valid Jekyll Front Matter with these exact fields:
       - title: (engaging, SEO-optimized)
       - date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0530')}
       - author: ayushjha
       - categories: [Tutorials, Industry Insights]
       - tags: (5-7 relevant tags)
       - image:
           path: /assets/img/posts/{datetime.datetime.now().strftime('%Y%m%d')}/1-hero-banner.png
           alt: (descriptive alt text)
       - description: (compelling 150-160 char meta description)
    
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
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def validate_and_clean_content(content):
    """Remove broken internal blog links from generated content."""
    import re
    
    # Pattern to find internal blog links (links starting with /blog/ or /posts/)
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

def get_unsplash_image(topic):
    """Fetch image from Unsplash as fallback."""
    # Check if Unsplash API key is available
    if not UNSPLASH_ACCESS_KEY:
        print(f"  ⚠️  Unsplash API key not configured, skipping...")
        return None, None
    
    try:
        # Search for relevant image
        search_query = topic.lower().replace('post-quantum', 'quantum').replace('readiness for', '')
        print(f"  📸 Searching Unsplash for: '{search_query}'")
        
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query": search_query,
                "per_page": 1,
                "orientation": "landscape",
                "client_id": UNSPLASH_ACCESS_KEY
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                photo = data['results'][0]
                image_url = photo['urls']['regular']
                photographer = photo['user']['name']
                
                print(f"  ✅ Found image by {photographer}")
                
                # Download image
                img_response = requests.get(image_url, timeout=15)
                if img_response.status_code == 200:
                    img = Image.open(BytesIO(img_response.content))
                    print(f"  ✅ Downloaded image ({img.size[0]}x{img.size[1]}px)")
                    return img, photographer
        
        print(f"  ⚠️  No suitable images found on Unsplash")
        return None, None
        
    except Exception as e:
        print(f"  ❌ Unsplash error: {e}")
        return None, None

def generate_and_save_image(topic):
    """Generate hero banner image using multiple fallback strategies."""
    # Using gemini-2.5-flash-image for image generation
    # Fallback chain: Gemini → Unsplash → Placeholder
    image_prompt = f"""Create a professional, high-quality cybersecurity hero banner for the topic: {topic}.
    
    Style: Modern digital art with a futuristic tech aesthetic
    Composition: Wide 16:9 banner format suitable for blog header
    Elements: Include abstract representations of cybersecurity concepts (shields, locks, network nodes, code, digital security)
    Color scheme: Deep blues, cyans, and purples with accent highlights
    Mood: Professional, secure, cutting-edge technology
    Lighting: Dramatic cinematic lighting with depth
    Quality: Sharp, high-resolution, suitable for web use
    
    Make it visually striking and engaging while maintaining professional credibility."""
    
    img_date = datetime.datetime.now().strftime('%Y%m%d')
    img_dir = f"assets/img/posts/{img_date}"
    os.makedirs(img_dir, exist_ok=True)
    img_path = f"{img_dir}/1-hero-banner.png"
    
    # Strategy 1: Try Gemini AI image generation
    try:
        print("  🎨 Trying Gemini AI image generation...")
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=[image_prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(aspect_ratio='16:9')
            )
        )
        
        # Extract and save the image
        for part in response.parts:
            if part.inline_data is not None and part.inline_data.mime_type.startswith('image/'):
                with open(img_path, 'wb') as f:
                    f.write(part.inline_data.data)
                print(f"  ✅ Gemini generated image successfully!")
                return img_path
        
        raise Exception("No image data in Gemini response")
            
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            print(f"  ⚠️  Gemini quota exceeded, trying Unsplash...")
        else:
            print(f"  ⚠️  Gemini failed ({error_msg[:50]}...), trying Unsplash...")
    
    # Strategy 2: Try Unsplash stock photos
    try:
        img, photographer = get_unsplash_image(topic)
        if img:
            img.save(img_path)
            print(f"  ✅ Using Unsplash image by {photographer}")
            print(f"  💡 Tip: You can add attribution in the blog post if desired")
            return img_path
    except Exception as e:
        print(f"  ⚠️  Unsplash fallback failed: {e}")
    
    # Strategy 3: Create placeholder
    print(f"  ⚠️  All image sources exhausted, creating placeholder...")
    placeholder_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    with open(img_path, 'wb') as f:
        f.write(placeholder_png)
    print(f"  ✅ Placeholder created (you can replace it manually later)")

    return img_path

def upload_to_github(md_filename, md_content, img_path):
    """Upload markdown post and image to GitHub repository."""
    try:
        from github import Auth
        auth = Auth.Token(GH_TOKEN)
        g = Github(auth=auth)
        repo = g.get_repo(REPO_NAME)
        
        # Upload Image (if it's not empty)
        with open(img_path, 'rb') as f:
            img_data = f.read()
        
        if len(img_data) > 100:  # Only upload if it's a real image (not just placeholder)
            try:
                repo.create_file(img_path, f"Add image for {md_filename}", img_data, branch="main")
                print(f"✓ Uploaded image to GitHub: {img_path}")
            except Exception as e:
                print(f"⚠ Image upload failed: {e}")
                print(f"  You may need to upload the image manually")
        else:
            print(f"⚠ Skipping empty placeholder image upload")
        
        # Upload Markdown Post
        repo_md_path = f"_posts/{md_filename}"
        repo.create_file(repo_md_path, f"Automated Post: {md_filename}", md_content, branch="main")
        print(f"✓ Uploaded post to GitHub: {repo_md_path}")
        
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
        md_content = generate_blog_content(topic, details)
        print(f"   ✓ Content generated ({len(md_content)} characters)")
        
        # Step 1.5: Validate and clean content
        print("\n1️⃣.5️⃣  Validating content...")
        md_content = validate_and_clean_content(md_content)
        print(f"   ✓ Content validated")
        
        # Step 2: Generate hero image
        print("\n2️⃣  Generating hero banner image...")
        img_path = generate_and_save_image(topic)
        
        # Step 3: Save locally
        clean_title = re.sub(r'[^a-z0-9]', '-', topic.lower()).strip('-')
        md_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{clean_title}.md"
        
        local_post_path = f"_posts/{md_filename}"
        os.makedirs("_posts", exist_ok=True)
        with open(local_post_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"\n3️⃣  Saved locally: {local_post_path}")
        
        # Step 4: Upload to GitHub
        print("\n4️⃣  Uploading to GitHub...")
        upload_to_github(md_filename, md_content, img_path)
        
        # Step 5: Update status
        with open(STATUS_FILE, 'w') as f:
            json.dump({"next_day": day + 1, "last_processed": topic}, f, indent=2)
        print(f"\n5️⃣  Status updated: Next run will process Day {day + 1}")
        
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
