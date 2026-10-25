"""Build the ZIP submitted to the OpenAI plugin directory.

Bundle the hosted MCP connection and every repository skill with its supporting
files. Local Blender workflows still require a compatible Blender environment;
bundling their instructions does not install Blender or its extension.

Usage: python3 scripts/package_openai.py [output.zip]
"""

import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
INCLUDE = [
    "plugin.json",
    "mcp.json",
    "LICENSE",
    "assets/worldlabs-logo.png",
    "assets/worldlabs-logo.svg",
    "skills",
]


def main() -> None:
    output = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "dist/worldlabs-openai.zip")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for entry in INCLUDE:
            path = ROOT / entry
            files = sorted(
                p for p in path.rglob("*")
                if p.is_file()
                and not any(part.startswith(".") or part == "__pycache__" for part in p.relative_to(path).parts)
                and p.suffix not in {".pyc", ".pyo"}
            ) if path.is_dir() else [path]
            for file in files:
                archive.write(file, file.relative_to(ROOT).as_posix())
    print(output)


if __name__ == "__main__":
    main()
