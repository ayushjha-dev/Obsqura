import os
import datetime
import re
import json
from google import genai
from github import Github

# --- CONFIGURATION ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GH_TOKEN = os.getenv("GH_TOKEN")
REPO_NAME = "ayushjha-dev/Obsqura"
TOPICS_FILE = "topics.txt"
STATUS_FILE = "tools/status.json"

# Initialize the NEW Google GenAI client
client = genai.Client(api_key=GEMINI_API_KEY)

def get_next_topic():
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
    # Use stable gemini-1.5-pro for text generation
    prompt = f"""
    You are a MASTER STORYTELLER and professional cybersecurity writer for "Obsqura".
    TOPIC: {topic}
    DETAILS: {details}

    REQUIREMENTS:
    1. Output valid Jekyll Front Matter.
    2. Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S +0530')}
    3. Author: ayushjha
    4. Categories: [Tutorials, Industry Insights]
    5. Image path must be: /assets/img/posts/{datetime.datetime.now().strftime('%Y%m%d')}/1-hero-banner.png
    6. Use Chirpy callouts (e.g., {{: .prompt-tip}}).
    7. End with signature: **—Mr. Xploit** 🛡️
    
    Return ONLY the raw markdown content.
    """
    response = client.models.generate_content(
        model='gemini-1.5-pro',
        contents=prompt
    )
    return response.text

def generate_and_save_image(topic):
    # Use imagen-3 for actual image generation via the new SDK
    image_prompt = f"A futuristic, visually stunning cybersecurity banner for the topic: {topic}. Cinematic lighting, 4k, digital art style."
    
    img_date = datetime.datetime.now().strftime('%Y%m%d')
    img_dir = f"assets/img/posts/{img_date}"
    os.makedirs(img_dir, exist_ok=True)
    img_path = f"{img_dir}/1-hero-banner.png"
    
    try:
        # Generate the image
        response = client.models.generate_image(
            model='imagen-3',
            prompt=image_prompt
        )
        # Save the first generated image
        with open(img_path, 'wb') as f:
            f.write(response.generated_images[0].image_bytes)
        print(f"Successfully generated image: {img_path}")
    except Exception as e:
        print(f"Image generation failed (Quota/Access issue): {e}")
        # Create a tiny 1x1 empty file so the workflow doesn't crash
        with open(img_path, 'wb') as f: f.write(b"") 

    return img_path

def upload_to_github(md_filename, md_content, img_path):
    g = Github(GH_TOKEN)
    repo = g.get_repo(REPO_NAME)
    
    # Upload Image
    with open(img_path, 'rb') as f:
        img_data = f.read()
    if len(img_data) > 0:
        repo.create_file(img_path, f"Add image for {md_filename}", img_data, branch="main")
    
    # Upload Markdown Post
    repo_md_path = f"_posts/{md_filename}"
    repo.create_file(repo_md_path, f"Automated Post: {md_filename}", md_content, branch="main")

def main():
    day, topic, details = get_next_topic()
    if not topic:
        print("All topics completed or topics.txt is missing.")
        return

    print(f"Processing Day {day}: {topic}")
    
    md_content = generate_blog_content(topic, details)
    img_path = generate_and_save_image(topic)
    
    clean_title = re.sub(r'[^a-z0-9]', '-', topic.lower()).strip('-')
    md_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{clean_title}.md"
    
    upload_to_github(md_filename, md_content, img_path)
    
    with open(STATUS_FILE, 'w') as f:
        json.dump({"next_day": day + 1}, f)
    
    print(f"Successfully published Day {day}!")

if __name__ == "__main__":
    main()
