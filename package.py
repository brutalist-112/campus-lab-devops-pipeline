#!/usr/bin/env python3
"""
Build and packaging script for Campus Lab Resources Management API.
Creates a portable release artifact (.tar.gz) in the dist/ directory
suitable for Jenkins artifact archiving, Ansible distribution, and deployment.
"""

import os
import tarfile
import sys
import shutil

VERSION = "1.0.0"
ARTIFACT_NAME = f"campus-lab-api-{VERSION}.tar.gz"
DIST_DIR = "dist"


def build_package():
    print(f"[*] Starting build process for campus-lab-api v{VERSION}...")

    # Ensure dist folder exists and is clean
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR, exist_ok=True)

    target_archive = os.path.join(DIST_DIR, ARTIFACT_NAME)

    files_to_pack = [
        "requirements.txt",
        "README.md"
    ]

    dirs_to_pack = [
        "src"
    ]

    print(f"[*] Packaging files into {target_archive}...")
    with tarfile.open(target_archive, "w:gz") as tar:
        for f in files_to_pack:
            if os.path.exists(f):
                tar.add(f, arcname=f)
                print(f"  + Added file: {f}")
        for d in dirs_to_pack:
            if os.path.exists(d):
                tar.add(d, arcname=d)
                print(f"  + Added directory: {d}")

    print(f"[✓] Build SUCCESS! Artifact created at: {target_archive}")
    print(f"[✓] File size: {os.path.getsize(target_archive)} bytes")
    return target_archive


if __name__ == "__main__":
    build_package()
