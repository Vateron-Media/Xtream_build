import os
import tarfile
import shutil


print("Welcome to Xtream Updater")
print("This script will create update.tar.gz and delete.php for you")
print("Please enter the following information:")
print("-------------------------------------------------")
print("Example:")
print("Version of the previous release : v1.2.0")
print("Enter path to Xtream_main : /home/xtream/Xtream_main")
print("-------------------------------------------------")


lastUpdate = input("Version of the previous release : ")
inputPath = input("Enter path to Xtream_main : ")

# create tmp folder
if not os.path.exists("tmp"):
    os.makedirs("tmp")

if not os.path.exists("/tmp/update"):
    os.makedirs("/tmp/update")

# run comand and get output
files = os.popen(
    f"git --git-dir={inputPath}/.git diff-tree -r --no-commit-id --name-only --diff-filter=ACMRTU {lastUpdate} main"
).read()

files = files.split("\n")
files.remove("")
files.append("tools/update_bd.php")
files.append("update.py")
files.append("tools/update.php")

# copy files to tmp folder
for file in files:
    if os.path.exists(inputPath + "/" + file):
        if not os.path.exists("/tmp/update/" + file):
            os.makedirs(os.path.dirname("/tmp/update/" + file), exist_ok=True)
        shutil.copy(inputPath + "/" + file, "/tmp/update/" + file)

os.system("sudo chown root:root -R /tmp/update/ > /dev/null")
os.system("sudo find /tmp/update/ -type d -exec chmod 755 {} \\;")
os.system("sudo find /tmp/update/ -type f -exec chmod 550 {} \\;")

files = os.popen("ls /tmp/update").read().split("\n")

print("Creating update.tar.gz")
with tarfile.open("tmp/update.tar.gz", "w:gz") as tar:
    for file in files:
        tar.add("/tmp/update/" + file, arcname=file)


# Create delete.php
print("Creating delete.php")
filesD = os.popen(
    f"git --git-dir={inputPath}/.git diff-tree -r --no-commit-id --name-only --diff-filter=D {lastUpdate} main"
).read()

with open("tmp/delete.php", "w") as f:
    f.write("<?php\n")
    for file in filesD.split("\n"):
        if file != "":
            PHPDeleteCOmand = "if (file_exists('%s')) {\n\tunlink('%s');\n}\n" % (
                file,
                file,
            )
            f.write(PHPDeleteCOmand)
