import os
import subprocess

REPO_URL = "https://github.com/ChatPRD/lennys-podcast-transcripts.git"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
TRANSCRIPTS_DIR = os.path.join(DATA_DIR, "lennys-podcast-transcripts")

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(TRANSCRIPTS_DIR):
        print(f"Cloning transcripts from {REPO_URL} into {TRANSCRIPTS_DIR}...")
        subprocess.run(["git", "clone", REPO_URL, TRANSCRIPTS_DIR], check=True)
        print("Clone successful.")
    else:
        print(f"Transcripts already exist at {TRANSCRIPTS_DIR}. Pulling latest...")
        subprocess.run(["git", "-C", TRANSCRIPTS_DIR, "pull"], check=True)
        print("Pull successful.")

if __name__ == "__main__":
    main()
