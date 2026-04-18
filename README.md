# bash-help

A terminal assistant that suggests what you meant when a command is not found.

## How it works
- Typo → `did you mean: pacman?`
- Real command but not installed → `mpv: not installed`

## Setup
1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com)
2. Add to `~/.bashrc`:
```bash
export GEMINI_API_KEY="your_key_here"
trap 'python /path/to/guess.py $BASH_COMMAND 2>/dev/null' ERR
```
3. Run `source ~/.bashrc`
