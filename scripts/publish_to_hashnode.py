import os
import requests
import json
import sys

HASHNODE_API_URL = "https://api.hashnode.com/"  # Make sure this is the *correct* base URL
HASHNODE_API_TOKEN = os.environ.get("HASHNODE_API_TOKEN")
HASHNODE_BLOG_ID = os.environ.get("HASHNODE_BLOG_ID")
MKDOCS_SITE_DIR = "site"  # Default MkDocs output directory

if not HASHNODE_API_TOKEN or not HASHNODE_BLOG_ID:
    print("Error: HASHNODE_API_TOKEN and HASHNODE_BLOG_ID environment variables must be set.")
    sys.exit(1)

def extract_frontmatter(markdown_content):
    """Extracts frontmatter (if any) from the Markdown content."""
    lines = markdown_content.splitlines()
    if len(lines) >= 3 and lines[0] == "---" and lines[2] == "---":
        frontmatter_str = "\n".join(lines[1:2])
        try:
            frontmatter = json.loads(frontmatter_str)
            content = "\n".join(lines[3:])
            return frontmatter, content
        except json.JSONDecodeError:
            return {}, markdown_content
    return {}, markdown_content

def publish_to_hashnode(title, content_markdown, slug, tags=None, cover_image_url=None):
    """Publishes a story to Hashnode."""
    mutation = """
    mutation CreateStory($publicationId: String!, $input: CreateStoryInput!) {
      createPublicationStory(publicationId: $publicationId, input: $input) {
        post {
          id
          slug
          url
        }
      }
    }
    """

    payload = {
        "query": mutation,
        "variables": {
            "publicationId": HASHNODE_BLOG_ID,
            "input": {
                "title": title,
                "contentMarkdown": content_markdown,
                "slug": slug,
                "tags": tags if tags else [],
                "coverImageURL": cover_image_url,
                "isPartOfPublication": True,
                "isAnonymous": False
            }
        }
    }

    headers = {
        "Authorization": HASHNODE_API_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(HASHNODE_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        if data.get("errors"):
            print(f"Hashnode API Error: {data['errors']}")
        elif data.get("data") and data["data"].get("createPublicationStory") and data["data"]["createPublicationStory"].get("post"):
            post_url = data["data"]["createPublicationStory"]["post"]["url"]
            print(f"Successfully published '{title}' to Hashnode: {post_url}")
        else:
            print(f"Unexpected response from Hashnode API: {data}")

    except requests.exceptions.RequestException as e:
        print(f"Error publishing to Hashnode: {e}")
    except json.JSONDecodeError:
        print("Error decoding Hashnode API response.")

def process_markdown_file(filepath):
    """Processes a single Markdown file and publishes it to Hashnode."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # You might need more sophisticated logic to extract title, slug, tags, etc.
        # This is a basic example assuming the filename can be used as a base for the slug
        filename = os.path.splitext(os.path.basename(filepath))[0]
        title = filename.replace('-', ' ').title()
        slug = filename.lower()

        # Basic tag extraction (you might want to improve this)
        # For example, look for a specific section or frontmatter
        tags = [tag.strip() for tag in title.lower().split()[:3]] # Basic: first 3 words of title as tags

        # You might want to add logic to extract a cover image URL if present in your Markdown

        publish_to_hashnode(title, markdown_content, slug, tags=tags)

    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    site_path = os.path.join(os.getcwd(), MKDOCS_SITE_DIR)
    markdown_files = []

    for root, _, files in os.walk(site_path):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                # Ensure we are only processing source Markdown files, not the HTML output
                if MKDOCS_SITE_DIR not in filepath:
                    markdown_files.append(filepath)

    if not markdown_files:
        print(f"No Markdown files found outside the '{MKDOCS_SITE_DIR}' directory to publish.")
    else:
        print(f"Found {len(markdown_files)} Markdown files to publish...")
        for md_file in markdown_files:
            print(f"Processing: {md_file}")
            process_markdown_file(md_file)

        print("Publishing to Hashnode completed.")