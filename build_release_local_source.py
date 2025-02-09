import os
import shutil
import tarfile

# Определяем пути
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_TMP = os.path.join(SCRIPT_DIR, "tmp")
SYSTEM_TMP = "/tmp"


print("-------------------------------------------------")
print("Example:")
print("Enter type (main or sub): main")
print("Enter path to Xtream_main : /home/xtream/Xtream_main")
print("-------------------------------------------------")

while True:
    build_type = input("Enter type (main or sub): ").lower()
    if build_type in ("main", "sub"):
        break
    print("Invalid type, please try again")

source_path = input("Enter path to Xtream source folder: ")
if not os.path.isdir(source_path):
    print("Error: Source directory does not exist")
    exit(1)

# Пути для работы
build_folder = os.path.join(SYSTEM_TMP, f"Xtream_{build_type}")
archive_path = os.path.join(LOCAL_TMP, f"{build_type}_xui.tar.gz")

permision_commands = [
    f"sudo find {build_folder} -type d -exec chmod 755 {{}} \\;",
    f"sudo find {build_folder} -type f -exec chmod 550 {{}} \\;",
    f"sudo find {os.path.join(build_folder, 'bin/ffmpeg_bin')} -type f -exec chmod 551 {{}} \\;",
    f"chmod 0750 {os.path.join(build_folder, 'bin')}",
    f"chmod 0750 {os.path.join(build_folder, 'config')}",
    f"chmod 0750 {os.path.join(build_folder, 'content')}",
    f"chmod 0750 {os.path.join(build_folder, 'signals')}",
    f"chmod -R 0777 {os.path.join(build_folder, 'includes')}",
    f"chmod 0771 {os.path.join(build_folder, 'bin/daemons.sh')}",
    f"chmod 0755 {os.path.join(build_folder, 'bin/redis/redis-server')}",
    f"chmod a+x {os.path.join(build_folder, 'status')}",
    f"sudo chmod +x {os.path.join(build_folder, 'bin/nginx_rtmp/sbin/nginx_rtmp')}",
]

try:
    # Создаем локальную временную папку
    os.makedirs(LOCAL_TMP, exist_ok=True)

    # Очистка предыдущих артефактов
    if os.path.exists(archive_path):
        os.remove(archive_path)
        print(f"Removed old archive: {archive_path}")

    if os.path.exists(build_folder):
        shutil.rmtree(build_folder)
        print(f"Cleaned existing build folder: {build_folder}")

    # Копируем исходные файлы
    print(f"Copying files to system temp: {build_folder}")
    shutil.copytree(source_path, build_folder)

    # Удаляем ненужные элементы
    remove_items = [
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

    for item, item_type in remove_items:
        path = os.path.join(build_folder, item)
        if not os.path.exists(path):
            continue
            
        if item_type == "dir":
            shutil.rmtree(path)
        else:
            os.remove(path)
        print(f"Removed {item_type}: {item}")

    # Удаляем .gitkeep и устанавливаем права
    gitkeep_count = 0
    for root, dirs, files in os.walk(build_folder):
        for name in dirs + files:
            full_path = os.path.join(root, name)
            
            # Удаляем .gitkeep
            if name == ".gitkeep":
                os.remove(full_path)
                gitkeep_count += 1
                continue
                
    for command in permision_commands:
        os.system(command)

    print(f"Removed {gitkeep_count} .gitkeep files")
    print("Permissions set for all files and directories")

    # Создаем архив
    print(f"Creating archive at: {archive_path}")
    allfile = os.listdir(build_folder)
    with tarfile.open(archive_path, "w:gz") as tar:
        for file in allfile:
            tar.add(f"{build_folder}/{file}", arcname=os.path.basename(file))

    print("Operation completed successfully!")

except Exception as e:
    print(f"Error: {str(e)}")
    exit(1)

finally:
    # Очистка системной временной папки
    if os.path.exists(build_folder):
        shutil.rmtree(build_folder)
        print(f"Cleaned system temp folder: {build_folder}")