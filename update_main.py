import os
import tarfile
import shutil
import subprocess
from pathlib import Path


def main():
    print_header()

    # Получение входных данных
    last_update = input("Version of the previous release: ").strip()
    input_path = input("Enter path to Xtream_main: ").strip()

    # Валидация входных параметров
    validate_inputs(last_update, input_path)

    # Настройка путей
    tmp_path = Path("tmp")
    update_tmp = Path("/tmp/update")
    output_archive = tmp_path / "update.tar.gz"
    delete_php = tmp_path / "delete.php"

    permision_commands = [
        f"sudo find {update_tmp} -type d -exec chmod 755 {{}} \\;",
        f"sudo find {update_tmp} -type f -exec chmod 550 {{}} \\;",
        f"sudo find {os.path.join(update_tmp, 'bin/ffmpeg_bin')} -type f -exec chmod 551 {{}} \\;",
        f"chmod 0750 {os.path.join(update_tmp, 'bin')}",
        f"chmod 0750 {os.path.join(update_tmp, 'config')}",
        f"chmod 0750 {os.path.join(update_tmp, 'content')}",
        f"chmod 0750 {os.path.join(update_tmp, 'signals')}",
        f"chmod -R 0777 {os.path.join(update_tmp, 'includes')}",
        f"chmod 0771 {os.path.join(update_tmp, 'bin/daemons.sh')}",
        f"chmod 0755 {os.path.join(update_tmp, 'bin/redis/redis-server')}",
        f"chmod a+x {os.path.join(update_tmp, 'status')}",
        f"sudo chmod +x {os.path.join(update_tmp, 'bin/nginx_rtmp/sbin/nginx_rtmp')}",
    ]

    # Создание временных директорий
    create_directories(tmp_path, update_tmp)

    try:
        # Получение списка изменённых файлов
        changed_files = get_changed_files(input_path, last_update)
        changed_files.update({"tools/update_bd.php", "update.py", "tools/update.php"})

        # Копирование файлов
        copy_files(input_path, update_tmp, changed_files)

        # Установка прав
        set_permissions(update_tmp, permision_commands)

        # Создание архива
        create_archive(update_tmp, output_archive)

        # Создание delete.php
        create_delete_php(input_path, last_update, delete_php)

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

    finally:
        # Очистка временных файлов
        cleanup(update_tmp)

    print("Operation completed successfully!")


def print_header():
    print("Welcome to Xtream Updater")
    print("This script will create update.tar.gz and delete.php for you")
    print("Please enter the following information:")
    print("-------------------------------------------------")
    print("Example:")
    print("Version of the previous release : v1.2.0")
    print("Enter path to Xtream_main : /home/xtream/Xtream_main")
    print("-------------------------------------------------")


def validate_inputs(last_update, input_path):
    if not last_update:
        raise ValueError("Version cannot be empty")

    path = Path(input_path)
    if not path.exists():
        raise ValueError(f"Path {input_path} does not exist")

    if not (path / ".git").exists():
        raise ValueError(f"Directory {input_path} is not a git repository")


def create_directories(*paths):
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def get_changed_files(repo_path, last_version):
    cmd = [
        "git",
        f"--git-dir={repo_path}/.git",
        "diff-tree",
        "-r",
        "--no-commit-id",
        "--name-only",
        "--diff-filter=ACMRTU",
        last_version,
        "main",
    ]

    result = subprocess.run(cmd, check=True, text=True, capture_output=True)

    return {f.strip() for f in result.stdout.splitlines() if f.strip()}


def copy_files(source_root, dest_root, files):
    for file in files:
        src = Path(source_root) / file
        dest = dest_root / file

        if not src.exists():
            print(f"Warning: File {src} does not exist, skipping")
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def set_permissions(path, commands):
    print("Set permissions")
    for command in commands:
        os.system(command)


def create_archive(source_dir, output_path):
    print("Create update archive")
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def create_delete_php(repo_path, last_version, output_path):
    cmd = [
        "git",
        f"--git-dir={repo_path}/.git",
        "diff-tree",
        "-r",
        "--no-commit-id",
        "--name-only",
        "--diff-filter=D",
        last_version,
        "main",
    ]

    result = subprocess.run(cmd, check=True, text=True, capture_output=True)

    deleted_files = [f.strip() for f in result.stdout.splitlines() if f.strip()]

    with output_path.open("w") as f:
        f.write("<?php\n")
        for file in deleted_files:
            php_code = f"""if (file_exists({repr(file)})) {{
    @unlink({repr(file)});
}}
"""
            f.write(php_code)


def cleanup(path):
    shutil.rmtree(path, ignore_errors=True)
    print(f"Cleaned up temporary directory: {path}")


if __name__ == "__main__":
    main()
