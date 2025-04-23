import os
import requests
import json
import sys
import frontmatter  # For extracting frontmatter

HASHNODE_API_URL = "https://api.hashnode.com/"
HASHNODE_API_TOKEN = os.environ.get("HASHNODE_API_TOKEN")
HASHNODE_BLOG_ID = os.environ.get("HASHNODE_BLOG_ID")
MKDOCS_SITE_DIR = "site"
DOCS_SOURCE_DIR = "docs"  # Define the source directory for Markdown files

if not HASHNODE_API_TOKEN or not HASHNODE_BLOG_ID:
    print("Error: HASHNODE_API_TOKEN and HASHNODE_BLOG_ID environment variables must be set.")
    sys.exit(1)

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
        response.raise_for_status()

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
    """Processes a single Markdown file and publishes it to Hashnode using frontmatter."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        title = post.get('title')
        slug = post.get('slug')
        tags = post.get('tags') if post.get('tags') else []
        cover_image_url = post.get('cover_image')

        if not title or not slug:
            print(f"Warning: Missing 'title' or 'slug' in frontmatter of '{filepath}'. Skipping.")
            return

        publish_to_hashnode(title, post.content, slug, tags=tags, cover_image_url=cover_image_url)

    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    docs_path = os.path.join(os.getcwd(), DOCS_SOURCE_DIR)
    markdown_files = []

    for root, _, files in os.walk(docs_path):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                markdown_files.append(filepath)

    if not markdown_files:
        print(f"No Markdown files found in the '{DOCS_SOURCE_DIR}' directory to publish.")
    else:
        print(f"Found {len(markdown_files)} Markdown files in '{DOCS_SOURCE_DIR}' to publish...")
        for md_file in markdown_files:
            print(f"Processing: {md_file}")
            process_markdown_file(md_file)

        print("Publishing to Hashnode completed.")