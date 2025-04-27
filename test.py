import requests
import subprocess
import webbrowser
import json
import os

GITHUB_USERNAME = ""
GITHUB_TOKEN = ""
PROJECT_PATH = ""
OLLAMA_MODEL = "mistral:latest"

def Model(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {
        "content-type": "application/json"
    }
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"Error: ", e)
        return None


def main():
    folder_name = os.path.basename(os.path.normpath(PROJECT_PATH))
    print(f"📂 Detected Project Folder: {folder_name}")

    project_description_detail = input("📝 Describe your project briefly: ")

    prompt = f"give me the name of the project and a description of the short project just make the {project_description_detail}"
    response = Model(prompt)

    if response:
        lines = response.strip().split("\n")
        project_name = ""
        project_description = ""
        for line in lines:
            if "Project Name:" in line:
                project_name = line.split(":", 1)[1].strip()
            elif "Description:" in line:
                project_description = line.split(":", 1)[1].strip()

        if not project_name or not project_description:
            print("Parsing Failed: Fallback to manual input.")
            project_name = input("📦 Enter project name manually: ")
            project_description = input("📝 Enter project description manually: ")

    else:
        print("Model Ollama unreachable. Fallback to manual input.")
        project_name = input("📦 Enter project name manually: ")
        project_description = input("📝 Enter project description manually: ")


    print(f"\n📦 Project Name: {project_name}")
    print(f"📝 Description: {project_description}")

    visibility = input("Do you want to make a private repository? (y/n): ").lower()
    private = True if visibility == "y" else False

    # repository_url = create_repo(project_name, project_description, private)
    # init_and_push(repository_url, project_name)

    open_web = input("Do you want to open your new repository? (y/n) : ")
    if open_web == "y":
        # webbrowser.open(repository_url)
        pass

if __name__ == "__main__":
    main()