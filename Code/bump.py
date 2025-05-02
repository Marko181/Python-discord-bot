import sys
import subprocess
from pathlib import Path

# map keyword → semver level
KEYWORDS = {
    'major': 'major',   # big API/feature/backwards-incompatible changes
    'feature': 'minor', # smaller additions & enhancements
    'fix': 'patch',     # bug fixes
}

def bump(version, level):
    major, minor, patch = version
    if level == 'major':
        return [major + 1, 0, 0]
    elif level == 'minor':
        return [major, minor + 1, 0]
    else:  # patch
        return [major, minor, patch + 1]

def read_version(path):
    text = path.read_text().strip()
    if text.startswith('v'):
        text = text[1:]
    return list(map(int, text.split('.')))

def write_version(path, nums):
    path.write_text("{}.{}.{}\n".format(*nums))

def run_git(cmd):
    """Run a git subcommand (list of args), abort on failure."""
    subprocess.run(['git'] + cmd, check=True)

def main():
    # usage check
    if len(sys.argv) < 3:
        print(f"Usage: python {Path(__file__).name} <{'|'.join(KEYWORDS)}> <commit message>")
        sys.exit(1)

    key = sys.argv[1].lower()
    if key not in KEYWORDS:
        print(f"Unknown keyword: {key!r}.  Use one of: {', '.join(KEYWORDS)}")
        sys.exit(1)

    commit_msg = " ".join(sys.argv[2:])
    level = KEYWORDS[key]

    # bump version.txt
    ver_file = Path(__file__).parent / "version.txt"
    old_version  = read_version(ver_file)
    new_version = bump(old_version , level)
    
    write_version(ver_file, new_version)
    version_str = f"{new_version[0]}.{new_version[1]}.{new_version[2]}"
    print(f"Bumped to version {version_str}")

    # git workflow
    try:
        run_git(['add', '.'])
        run_git(['commit', '-m', commit_msg])
        run_git(['push'])
        print("Git add/commit/push complete.")
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        print("Rolling back version change...")
        write_version(ver_file, old_version)
        print(f"Version restored to {old_version[0]}.{old_version[1]}.{old_version[2]}")
        sys.exit(1)

if __name__ == "__main__":
    main()
