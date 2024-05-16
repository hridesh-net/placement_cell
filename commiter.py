import os
import re
import random
from datetime import datetime

def generate_expertise_tag():
    # Generate expertise tag with a random color
    color = "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
    expertise_tag = f"<span style='background-color: {color};'>Python Expert</span>"
    return expertise_tag

def update_readme(repo_path):
    # Read the current content of the README file
    readme_path = os.path.join(repo_path, "README.md")
    with open(readme_path, "r") as readme_file:
        readme_content = readme_file.read()
    
    expertise_tag_regex = re.compile(r"<span style='background-color: #[0-9A-Fa-f]{6};'>Python Expert</span>")

    # Generate expertise tag with a new color
    expertise_tag = generate_expertise_tag()

    # Replace the placeholder with the new expertise tag
    updated_content = expertise_tag_regex.sub(expertise_tag, readme_content)

    # Write the updated content to the README file
    with open(readme_path, "w") as readme_file:
        readme_file.write(updated_content)

    # Commit and push changes
    os.system(f"cd {repo_path} && git fetch --all")
    os.system(f"cd {repo_path} && git pull")
    os.system(f"cd {repo_path} && git add README.md")
    os.system(f"cd {repo_path} && git commit -m 'Update expertise tag color'")
    os.system(f"cd {repo_path} && git push origin master")

def main():
    # Replace this path with the actual path to your local Git repository
    repo_path = r"D:\\Brudite\\dhruv-git\\placement_cell"
    update_readme(repo_path)

if __name__ == "__main__":
    main()