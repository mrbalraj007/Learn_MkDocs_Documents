import os
import requests
import json

HASHNODE_API_TOKEN = os.environ.get("HASHNODE_API_TOKEN")
# HASHNODE_BLOG_ID = os.environ.get("HASHNODE_BLOG_ID") # You won't need this for the test query
HASHNODE_API_URL = "https://api.hashnode.com"

# --- Temporarily comment out or remove these ---
# def publish_article(title, content):
#     # ... your original publish_article code ...
#     pass

# def process_markdown_file(filepath):
#     # ... your original process_markdown_file code ...
#     pass
# --- End of temporary commenting/removal ---

# --- Test Query ---
query_test = """
query {
  publication(host: "%s") {
    id
    title
  }
}
""" % "balrajsingh-dev.hashnode.dev"  # Replace with your actual subdomain

payload_test = {"query": query_test}

headers = {
    "Authorization": HASHNODE_API_TOKEN,
    "Content-Type": "application/json"
}

try:
    response_test = requests.post(HASHNODE_API_URL, headers=headers, data=json.dumps(payload_test))
    response_test.raise_for_status()
    data_test = response_test.json()
    print("Test Query Response:", data_test)
except requests.exceptions.RequestException as e:
    print("Test Query Error:", e)
except json.JSONDecodeError:
    print("Test Query JSON Decode Error:", response_test.text)

# --- If you want to keep the original functions, you can leave this at the end ---
# if __name__ == "__main__":
#     docs_directory = "docs"
#     for filename in os.listdir(docs_directory):
#         if filename.endswith(".md"):
#             filepath = os.path.join(docs_directory, filename)
#             process_markdown_file(filepath)
#
#     print("Finished attempting to publish articles.")