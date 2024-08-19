import os
import tarfile


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

# Create update.tar.gz
print("Creating update.tar.gz")
# run comand and get output
files = os.popen(
    f"git --git-dir={inputPath}/.git diff-tree -r --no-commit-id --name-only --diff-filter=ACMRT {lastUpdate} main"
).read()

files = files.split("\n")
files.remove("")

with tarfile.open("tmp/update.tar.gz", "w:gz") as tar:
    for file in files:
        tar.add(inputPath + "/" + file, arcname=file)


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
