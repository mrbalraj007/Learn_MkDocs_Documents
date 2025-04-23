import os
import requests
import json

HASHNODE_API_TOKEN = os.environ.get("HASHNODE_API_TOKEN")
HASHNODE_BLOG_ID = os.environ.get("HASHNODE_BLOG_ID")
HASHNODE_API_URL = "https://api.hashnode.com"

def publish_article(title, content):
    print(f"Attempting to publish: '{title[:50]}...'")
    query = """
    mutation CreateStory($input: CreateStoryInput!) {
      createPublicationStory(input: $input, publicationId: "%s") {
        post {
          slug
          url
        }
      }
    }
    """ % HASHNODE_BLOG_ID

    payload = {
        "query": query,
        "variables": {
            "input": {
                "title": title,
                "contentMarkdown": content,
                "slug": title.lower().replace(" ", "-"), # Basic slug generation
                "tags": [] # Add relevant tags here
                # Add other relevant fields as per Hashnode API
            }
        }
    }

    headers = {
        "Authorization": HASHNODE_API_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(HASHNODE_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        if data.get("data") and data["data"].get("createPublicationStory") and data["data"]["createPublicationStory"].get("post"):
            slug = data["data"]["createPublicationStory"]["post"]["slug"]
            url = data["data"]["createPublicationStory"]["post"]["url"]
            print(f"Successfully published '{title}' to: {url}")
        elif data.get("errors"):
            print(f"Error publishing '{title}': {data['errors']}")
        else:
            print(f"Unexpected response publishing '{title}': {data}")

    except requests.exceptions.RequestException as e:
        print(f"Network error publishing '{title}': {e}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON response for '{title}'. Response text: {response.text}")

def process_markdown_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        # You'll need more robust logic to extract the title
        # Consider using regular expressions or a Markdown parsing library
        lines = content.splitlines()
        title_line = next((line for line in lines if line.startswith('# ')), None)
        title = title_line[2:].strip() if title_line else filepath.split('/')[-1].replace('.md', '').replace('-', ' ').title()
        publish_article(title, content)

if __name__ == "__main__":
    docs_directory = "docs"
    for filename in os.listdir(docs_directory):
        if filename.endswith(".md"):
            filepath = os.path.join(docs_directory, filename)
            process_markdown_file(filepath)

    print("Finished attempting to publish articles.")