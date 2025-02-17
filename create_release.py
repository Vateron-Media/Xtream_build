"""
Xtream Updater Script

This script automates the creation of update packages for Xtream software:
1. Creates a full release archive with proper permissions and cleaned-up files
2. Generates an incremental update package based on git changes since last version
3. Produces a delete.php script to remove obsolete files during updates

Key features:
- Handles both full releases and incremental updates
- Maintains proper file system permissions
- Cleans unnecessary development files
- Uses git to detect changed files between versions
- Generates PHP helper scripts for update operations
"""

import os
import shutil
import tarfile
import argparse
import subprocess
from pathlib import Path

# --------------------------
# Configuration Constants
# --------------------------

# Directory paths
SCRIPT_DIR = Path(__file__).resolve().parent  # Where this script lives
LOCAL_TMP = SCRIPT_DIR / "tmp"  # Local temporary storage
SYSTEM_TMP = Path("/tmp")  # System temp directory

# Build artifacts paths (will be constructed dynamically)
UPDATE_PATH = SYSTEM_TMP / "Xtream_Update"  # Update package staging area

# Output file paths
UPDATE_ARCHIVE_PATH = LOCAL_TMP / "update.tar.gz"  # Update archive
DELETE_PHP = LOCAL_TMP / "delete.php"  # File deletion script

# --------------------------
# Permission Configuration
# --------------------------

PERMISSION_COMMANDS = [
    "sudo find {build_folder} -type d -exec chmod 755 {{}} \\;",
    "sudo find {build_folder} -type f -exec chmod 550 {{}} \\;",
    "sudo find {build_folder}/bin/ffmpeg_bin -type f -exec chmod 551 {{}} \\;",
    "chmod 0750 {build_folder}/bin",
    "chmod 0750 {build_folder}/config",
    "chmod 0750 {build_folder}/content",
    "chmod 0750 {build_folder}/signals",
    "chmod -R 0777 {build_folder}/includes",
    "chmod 0771 {build_folder}/bin/daemons.sh",
    "chmod 0755 {build_folder}/bin/redis/redis-server",
    "chmod a+x {build_folder}/status",
    "sudo chmod +x {build_folder}/bin/nginx_rtmp/sbin/nginx_rtmp",
]

# --------------------------
# File Cleanup Configuration
# --------------------------

REMOVE_ITEMS = [
    (".git", "dir"),
    (".github", "dir"),
    (".vscode", "dir"),
    (".gitignore", "file"),
    (".gitattributes", "file"),
    (".repomixignore", "file"),
    ("CONTRIBUTING.md", "file"),
    ("CONTRIBUTORS.md", "file"),
    ("repomix-output.md", "file"),
    ("repomix.config.json", "file"),
    ("update", "dir"),
    ("doc", "dir"),
]

# --------------------------
# Core Functions
# --------------------------


def print_header():
    """Display welcome message and usage instructions"""
    print("Welcome to Xtream Updater")
    print("This script will create update.tar.gz and delete.php for you")
    print("Please enter the following information:")
    print("-------------------------------------------------")
    print("Example:")
    print("Version of the previous release : v1.2.0")
    print("Enter path to Xtream_main : /home/xtream/Xtream_main")
    print("-------------------------------------------------")


def validate_source_path(source_path):
    """Verify that source directory exists"""
    if not source_path.is_dir():
        raise FileNotFoundError(f"Source directory {source_path} does not exist.")


def validate_inputs(last_update, input_path):
    """Validate user-provided inputs"""
    if not last_update:
        raise ValueError("Version cannot be empty")

    path = Path(input_path)
    if not path.exists():
        raise ValueError(f"Path {input_path} does not exist")

    if not (path / ".git").exists():
        raise ValueError(f"Directory {input_path} is not a git repository")


def create_directories(*paths):
    """Create required working directories"""
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def cleanup_previous_artifacts(archive_path, build_folder):
    """Remove old build artifacts from previous runs"""
    if archive_path.exists():
        archive_path.unlink()
        print(f"Removed old archive: {archive_path}")

    if build_folder.exists():
        shutil.rmtree(build_folder)
        print(f"Cleaned existing build folder: {build_folder}")


def copy_source_files(source_path, build_folder):
    """Copy source files to temporary build directory"""
    print(f"Copying files to system temp: {build_folder}")
    shutil.copytree(source_path, build_folder)


def remove_unnecessary_files(build_folder):
    """Remove development artifacts from build directory"""
    for item, item_type in REMOVE_ITEMS:
        path = build_folder / item
        if path.exists():
            if item_type == "dir":
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"Removed {item_type}: {item}")


def remove_gitkeep_files(build_folder):
    """Clean up .gitkeep files from directory structure"""
    gitkeep_count = 0
    for root, dirs, files in os.walk(build_folder):
        for name in dirs + files:
            full_path = Path(root) / name
            if name == ".gitkeep":
                full_path.unlink()
                gitkeep_count += 1
    print(f"Removed {gitkeep_count} .gitkeep files")


def set_permissions(build_folder):
    """Apply security permissions to build directory"""
    for command in PERMISSION_COMMANDS:
        command_with_path = command.format(build_folder=build_folder)
        subprocess.run(command_with_path, shell=True, check=False)
    print("Permissions set for all files and directories")


def create_archive(build_folder, archive_path):
    """Create compressed tar archive of build directory"""
    print(f"Creating archive at: {archive_path}")
    with tarfile.open(archive_path, "w:gz") as tar:
        for file in build_folder.iterdir():
            tar.add(file, arcname=file.name)


def cleanup(path):
    """Remove temporary build directory"""
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
        print(f"Cleaned up temporary directory: {path}")


def get_changed_files(repo_path, last_version):
    """Get list of changed files using git diff"""
    cmd = f"git --git-dir={repo_path}/.git diff-tree -r --no-commit-id --name-only --diff-filter=ACMRTU {last_version} main"
    result = subprocess.run(
        cmd, shell=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return {f.strip() for f in result.stdout.decode("utf-8").splitlines() if f.strip()}


def copy_files(source_root, dest_root, files):
    """Copy changed files to update staging area"""
    for file in files:
        src = Path(source_root) / file
        dest = dest_root / file

        if not src.exists():
            print(f"Warning: File {src} does not exist, skipping")
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def create_delete_php(repo_path, last_version, output_path):
    """Generate PHP script to delete obsolete files"""
    cmd = f"git --git-dir={repo_path}/.git diff-tree -r --no-commit-id --name-only --diff-filter=D {last_version} main"
    result = subprocess.run(
        cmd, shell=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    deleted_files = [
        f.strip() for f in result.stdout.decode("utf-8").splitlines() if f.strip()
    ]

    # Generate PHP unlink commands
    with output_path.open("w") as f:
        f.write("<?php\n")
        for file in deleted_files:
            php_code = f"""if (file_exists({repr(file)})) {{
    @unlink({repr(file)});
}}
"""
            f.write(php_code)


# --------------------------
# Main Workflows
# --------------------------


def create_release(source_path, build_type):
    """Create full release package"""
    try:
        release_path = SYSTEM_TMP / f"Xtream_{build_type}"
        release_archive_path = LOCAL_TMP / f"{build_type}_xui.tar.gz"

        validate_source_path(source_path)
        cleanup_previous_artifacts(release_archive_path, release_path)
        copy_source_files(source_path, release_path)
        remove_unnecessary_files(release_path)
        remove_gitkeep_files(release_path)
        set_permissions(release_path)
        create_archive(release_path, release_archive_path)
        print("Release creation completed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)
    finally:
        cleanup(release_path)


def create_update(source_path, last_update):
    """Create incremental update package"""
    try:
        changed_files = get_changed_files(source_path, last_update)
        changed_files.update(
            {
                "includes/cli_tool/update_bd.php",
                "update.py",
                "includes/cli_tool/update.php",
            }
        )

        cleanup_previous_artifacts(UPDATE_ARCHIVE_PATH, UPDATE_PATH)
        copy_files(source_path, UPDATE_PATH, changed_files)
        set_permissions(UPDATE_PATH)
        remove_unnecessary_files(UPDATE_PATH)
        remove_gitkeep_files(UPDATE_PATH)
        create_archive(UPDATE_PATH, UPDATE_ARCHIVE_PATH)
        create_delete_php(source_path, last_update, DELETE_PHP)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


# --------------------------
# Entry Point
# --------------------------


def main():
    """Main execution flow"""
    parser = argparse.ArgumentParser(description="Xtream Updater Script")
    parser.add_argument(
        "--build",
        default="main",
        help="Build type used in archive naming (default: main)",
    )
    args = parser.parse_args()

    print_header()

    last_update = input("Version of the previous release: ").strip()
    source_path = Path(input("Enter path to Xtream source folder: ").strip())

    validate_inputs(last_update, source_path)
    create_directories(LOCAL_TMP, SYSTEM_TMP / f"Xtream_{args.build}", UPDATE_PATH)

    create_release(source_path, args.build)
    create_update(source_path, last_update)

    print("All operations completed successfully!")


if __name__ == "__main__":
    main()
