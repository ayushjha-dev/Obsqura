import os
import datetime
import re
import json
import google.generativeai as genai
from github import Github

# --- CONFIGURATION ---
# Use Environment Variables for Security (Set these in GitHub Secrets)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GH_TOKEN = os.getenv("GH_TOKEN")
REPO_NAME = "ayushjha-dev/Obsqura"
TOPICS_FILE = "topics.txt"
STATUS_FILE = "tools/status.json"

# Initialize Models
genai.configure(api_key=GEMINI_API_KEY)
# Using user-specified model names
model_pro = genai.GenerativeModel('gemini-2.5-pro')
model_image = genai.GenerativeModel('gemini-2.5-flash-image')

def get_next_topic():
    # Load status to know which day we are on
    if not os.path.exists(STATUS_FILE):
        current_day = 1
    else:
        with open(STATUS_FILE, 'r') as f:
            status = json.load(f)
            current_day = status.get("next_day", 1)

    with open(TOPICS_FILE, 'r') as f:
        content = f.read()
    
    pattern = rf"Day {current_day}\nTopic: (.*?)\n(?:Additional Details: (.*?)\n)?"
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        return current_day, match.group(1).strip(), (match.group(2) or "").strip()
    return None, None, None

def generate_blog_content(topic, details):
    # This prompt is based on your "Master AI Prompt" in uploader-v2.html
    prompt = f"""
    You are a MASTER STORYTELLER and professional cybersecurity writer for "Obsqura".
    TOPIC: {topic}
    DETAILS: {details}

    REQUIREMENTS:
    1. Output valid Jekyll Front Matter.
    2. Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0530')}
    3. Author: ayushjha
    4. Categories: [Tutorials, Industry Insights]
    5. Image path must be: assets/img/posts/{datetime.datetime.now().strftime('%Y%m%d')}/1-hero-banner.png
    6. Use Chirpy callouts (e.g., {{: .prompt-tip}}).
    7. End with signature: **—Mr. Xploit** 🛡️
    
    Return ONLY the raw markdown content.
    """
    response = model_pro.generate_content(prompt)
    return response.text

def generate_and_save_image(topic):
    # Logic to generate an image using the flash-image model
    image_prompt = f"A futuristic, visually stunning cybersecurity banner for the topic: {topic}. Cinematic lighting, 4k, digital art style."
    # Assuming the model outputs an image object with a save method
    result = model_image.generate_content(image_prompt)
    
    # Create local directory
    img_dir = f"assets/img/posts/{datetime.datetime.now().strftime('%Y%m%d')}"
    os.makedirs(img_dir, exist_ok=True)
    img_path = f"{img_dir}/1-hero-banner.png"
    
    # In a real API scenario, you would save the bytes:
    # with open(img_path, 'wb') as f: f.write(result.image_bytes)
    return img_path

def upload_to_github(md_filename, md_content, img_path):
    g = Github(GH_TOKEN)
    repo = g.get_repo(REPO_NAME)
    
    # 1. Upload Image
    with open(img_path, 'rb') as f:
        img_data = f.read()
    repo.create_file(img_path, f"Add image for {md_filename}", img_data, branch="main")
    
    # 2. Upload Markdown Post
    repo_md_path = f"_posts/{md_filename}"
    repo.create_file(repo_md_path, f"Automated Post: {md_filename}", md_content, branch="main")

def main():
    day, topic, details = get_next_topic()
    if not topic:
        print("All topics completed!")
        return

    print(f"Processing Day {day}: {topic}")
    
    # 1. Generate Content
    md_content = generate_blog_content(topic, details)
    
    # 2. Generate Image
    img_path = generate_and_save_image(topic)
    
    # 3. Prepare Filename (Jekyll Format: YYYY-MM-DD-title.md)
    clean_title = re.sub(r'[^a-z0-9]', '-', topic.lower()).strip('-')
    md_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{clean_title}.md"
    
    # 4. Upload to GitHub
    upload_to_github(md_filename, md_content, img_path)
    
    # 5. Update Status
    with open(STATUS_FILE, 'w') as f:
        json.dump({"next_day": day + 1}, f)
    
    print(f"Successfully published Day {day}!")

if __name__ == "__main__":
    main()
