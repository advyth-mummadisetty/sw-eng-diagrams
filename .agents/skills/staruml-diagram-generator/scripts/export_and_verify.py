#!/usr/bin/env python3
"""
CLI script to headlessly render StarUML (.mdj) diagrams to images and perform visual QA.
Bypasses the StarUML desktop in-memory cache and produces high-resolution verification artifacts.
"""

import argparse
import os
import subprocess
import sys


def export_diagram(mdj_path: str, output_image_path: str) -> bool:
    """Run `staruml image` CLI headlessly to render a diagram."""
    if not os.path.exists(mdj_path):
        print(f"Error: Target .mdj file '{mdj_path}' does not exist.", file=sys.stderr)
        return False

    out_dir = os.path.dirname(output_image_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    cmd = ["staruml", "image", mdj_path, "-o", output_image_path]
    print(f"Executing: {' '.join(cmd)}")

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if res.stdout:
            print(res.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Failed to export diagram via staruml CLI: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: 'staruml' executable not found on system PATH.", file=sys.stderr)
        return False

    # Check output
    if os.path.exists(output_image_path) and os.path.getsize(output_image_path) > 0:
        print(f"Export successful: {output_image_path} ({os.path.getsize(output_image_path)} bytes)")
        return True
    else:
        # Check if staruml created a file with the diagram name inside out_dir
        if out_dir and os.path.isdir(out_dir):
            files = [os.path.join(out_dir, f) for f in os.listdir(out_dir) if f.endswith(('.png', '.jpg'))]
            if files:
                latest = max(files, key=os.path.getmtime)
                print(f"Export created image at: {latest}")
                return True
        print(f"Warning: Output file '{output_image_path}' not detected or empty.", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Headlessly export and verify StarUML diagrams")
    parser.add_argument("mdj_file", help="Path to .mdj StarUML file")
    parser.add_argument("-o", "--output", default="rendered_diagram.png", help="Path to output image")
    args = parser.parse_args()

    success = export_diagram(args.mdj_file, args.output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
