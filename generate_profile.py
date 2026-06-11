import json
import os
from datetime import datetime

def generate_profile_readme():
    # Load template
    with open("README_TEMPLATE.md", "r") as f:
        template = f.read()

    # Load AI-generated bio and design recommendations
    with open("ai_bio_results.txt", "r") as f:
        ai_results = f.read()
    
    user_bio_hook = ""
    user_about_me = ""
    for line in ai_results.splitlines():
        if line.startswith("HOOK:"):
            user_bio_hook = line.replace("HOOK:", "").strip()
        elif line.startswith("ABOUT:"): 
            user_about_me = line.replace("ABOUT:", "").strip()

    # Load GitHub repository data
    with open("repos_data.json", "r") as f:
        repos_data = json.load(f)

    # Process GitHub data
    languages = {}
    projects = []
    for repo in repos_data:
        if repo["primaryLanguage"] and repo["primaryLanguage"]["name"]:
            lang = repo["primaryLanguage"]["name"]
            languages[lang] = languages.get(lang, 0) + 1
        
        # Collect project details for CURRENT_PROJECTS
        if repo["description"] and repo["name"] != "johnnietse": # Exclude profile repo itself
            projects.append({
                "name": repo["name"],
                "description": repo["description"],
                "updatedAt": repo["updatedAt"],
                "stargazerCount": repo["stargazerCount"]
            })
    
    # Define high-impact projects to prioritize based on latest profile data
    high_impact_repos = [
        "llm-d-epp-Energy-Aware-Endpoint-Picker-Plugin-",
        "lws",
        "RISC_V_CPU",
        "strawberry-farm",
        "elec-498-group-30-2025-2026-proxy-app",
        "L4-autonomous-vehicle-object-detection-model-training"
    ]
    
    # Sort projects: prioritized first, then by stars, then by date
    projects.sort(key=lambda x: (
        x["name"] in high_impact_repos,
        x["stargazerCount"],
        x["updatedAt"]
    ), reverse=True)
    
    top_projects_markdown = ""
    for project in projects[:4]: # Top 4 high-impact projects
        top_projects_markdown += f"""
#### 🚀 [{project['name']}](https://github.com/johnnietse/{project['name']})
> {project['description']}
"""

    # Generate tech stack badges using skillicons.dev
    tech_stack_icons = ",".join([lang.lower().replace(" ", "") for lang in languages.keys()])
    tech_stack_badges = f"<img src=\"https://skillicons.dev/icons?i={tech_stack_icons}&theme=dark\" />"

    # Current date for LAST_UPDATED
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Populate template
    final_readme = template.replace("{{USER_BIO_HOOK}}", user_bio_hook)
    final_readme = final_readme.replace("{{USER_ABOUT_ME}}", user_about_me)
    final_readme = final_readme.replace("{{TECH_STACK_BADGES}}", tech_stack_badges)
    final_readme = final_readme.replace("{{CURRENT_PROJECTS}}", top_projects_markdown)
    final_readme = final_readme.replace("{{LAST_UPDATED}}", last_updated)

    # Write final README.md
    with open("README.md", "w") as f:
        f.write(final_readme)

if __name__ == "__main__":
    generate_profile_readme()
