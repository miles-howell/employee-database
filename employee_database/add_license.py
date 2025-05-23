import os

LICENSE_TEXT = """Copyright (c) 2025 Miles H. (Planned Pixel Studio)
Licensed for personal or educational use only.
Commercial use, redistribution, or resale requires a paid license.
Contact: miles@plannedpixel.com
"""

EXTENSIONS = {
    ".py": "#",
    ".html": "<!--",
    ".css": "/*",
    ".js": "/*",
}

EXCLUDED_PATH_SEGMENTS = {
    "staticfiles/admin",
    "static/admin",
    "static/vendor",
    "site-packages",
    "select2",
    "jsi18n",
}


EXCLUDED_DIRS = {"venv", "env", "__pycache__", "migrations", "node_modules", ".git"}
ALWAYS_INCLUDE_FILES = {"admin.py", "urls.py", "views.py", "models.py", "forms.py", "seed_demo.py"}
EXCLUDED_FILES = {"__init__.py"}

def get_commented_license(ext):
    comment_start = EXTENSIONS[ext]
    if comment_start == "#":
        return "\n".join(f"{comment_start} {line}" for line in LICENSE_TEXT.splitlines())
    elif comment_start == "/*":
        return f"/*\n{LICENSE_TEXT}\n*/"
    elif comment_start == "<!--":
        return f"<!--\n{LICENSE_TEXT}\n-->"
    return LICENSE_TEXT

def has_license(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            head = f.read(500)
            return "Planned Pixel Studio" in head
    except:
        return True

def is_eligible(file_path):
    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1]
    if ext not in EXTENSIONS:
        return False
    if filename in EXCLUDED_FILES:
        return False
    if filename in ALWAYS_INCLUDE_FILES:
        return True
    return True

def find_files(root_dir):
    eligible = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root_dir).replace("\\", "/")

            # Skip paths containing known excluded segments
            if any(exclude in relative_path for exclude in EXCLUDED_PATH_SEGMENTS):
                continue

            if is_eligible(file_path) and not has_license(file_path):
                eligible.append(file_path)
    return eligible


def apply_header(files):
    for path in files:
        ext = os.path.splitext(path)[1]
        license_header = get_commented_license(ext)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            with open(path, "w", encoding="utf-8") as f:
                f.write(license_header + "\n\n" + content)
            print(f"✔️ Updated: {path}")
        except Exception as e:
            print(f"❌ Error: {path} — {e}")

if __name__ == "__main__":
    root = os.path.abspath(".")
    print(f"\n🔍 Scanning for eligible source files in: {root}\n")
    files_to_update = find_files(root)

    if not files_to_update:
        print("✅ No files need updates.")
    else:
        print("📝 These files will be updated:\n")
        for f in files_to_update:
            print(f" - {f}")
        confirm = input("\nProceed with adding license headers to these files? (y/n): ").strip().lower()
        if confirm == "y":
            apply_header(files_to_update)
            print("\n✅ All files updated.")
        else:
            print("\n❌ Canceled. No changes made.")
