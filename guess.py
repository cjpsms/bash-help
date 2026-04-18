# guess.py — production
import sys
import os
import requests
import json

API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL   = "gemini-3.1-flash-lite-preview"
OS_INFO = os.popen("uname -a").read().strip()

def ask(command, full_input):
    prompt = f"""OS: {OS_INFO}
command not found: "{command}"
full input: "{full_input}"

assume the user has common tools installed but made a typo.
if the input contains a URL or media file, consider what command is commonly used to open it.
order suggestions by most likely first.

reply JSON only:
- typo: {{"type":"typo","suggestions":["x","y"]}}
- real command but not installed: {{"type":"not_installed","command":"x"}}"""

    res = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}",
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    return res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

def main():
    if not sys.argv[1:]:
        sys.exit(0)

    command    = sys.argv[1]
    full_input = " ".join(sys.argv[1:])
    raw        = ask(command, full_input)

    try:
        result = json.loads(raw.replace("```json","").replace("```","").strip())
        if result["type"] == "typo":
            suggestions = " ".join(f"{s}?" for s in result["suggestions"])
            print(f"did you mean: {suggestions}")
        elif result["type"] == "not_installed":
            print(f"{result['command']}: not installed")
    except:
        print(raw)

if __name__ == "__main__":
    main()
