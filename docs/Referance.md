[Emojis Documents](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/)

```powershell
 "editor.fontSize": 10,
    "window.zoomLevel": 2,
    "extensions.ignoreRecommendations": true,
    "terminal.integrated.defaultProfile.osx": "zsh",
    "redhat.telemetry.enabled": true,
    "yaml.schemas": {
        "https://squidfunk.github.io/mkdocs-material/schema.json": "mkdocs.yml"
    },
    "yaml.customTags": [
        "!ENV scalar",
        "!ENV sequence",
        "!relative scalar",
        "tag:yaml.org,2002:python/name:material.extensions.emoji.to_svg",
        "tag:yaml.org,2002:python/name:material.extensions.emoji.twemoji",
        "tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format"
    ]
```

# To Enable venv for MkDocs 
✅ For Git Bash terminal in VS Code:
Open the terminal in VS Code (select Git Bash from the dropdown if it’s not default).

Run this command:
```bash
source venv/Scripts/activate
```
✅ This should change your prompt to show (venv) — indicating the virtual environment is active.


Steps to activate:
Open Command Prompt (cmd) or PowerShell.

Navigate to your project directory:

```sh
cd c:\Z_Test_Repo\RND
```
Then activate the virtual environment:

If using Command Prompt:
```sh
venv\Scripts\activate.bat
```

If using PowerShell:
```sh
.\venv\Scripts\Activate.ps1
```
🛑 PowerShell Execution Policy Gotcha
If you get an error like:

execution of scripts is disabled on this system

You need to temporarily allow script execution:

```sh
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
Then try activating again:

```sh
.\venv\Scripts\Activate.ps1
``````
