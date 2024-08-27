import os
import shutil
import tarfile

# remove folder Xtream_main/ if it exists
if os.path.exists("Xtream_main/"):
    shutil.rmtree("Xtream_main/")

# create tmp folder
if not os.path.exists("tmp"):
    os.makedirs("tmp")

# git clone
print("Cloning Xtream_main")
os.system("git clone https://github.com/Vateron-Media/Xtream_main.git")

# remove .git with Xtream_main/
print("Removing trash from Xtream_main/")

if os.path.exists("Xtream_main/.git"):
    shutil.rmtree("Xtream_main/.git")
    print("Removed .git from Xtream_main/")
if os.path.exists("Xtream_main/.vscode"):
    shutil.rmtree("Xtream_main/.vscode")
    print("Removed .vscode from Xtream_main/")
if os.path.exists("Xtream_main/.gitignore"):
    os.remove("Xtream_main/.gitignore")
    print("Removed .gitignore from Xtream_main/")
if os.path.exists("Xtream_main/.gitattributes"):
    os.remove("Xtream_main/.gitattributes")
    print("Removed .gitattributes from Xtream_main/")
if os.path.exists("Xtream_main/update"):
    shutil.rmtree("Xtream_main/update")
    print("Removed update from Xtream_main/")

# delete .gitkeep everywhere
for root, dirs, files in os.walk("Xtream_main/"):
    for file in files:
        if file == ".gitkeep":
            os.remove(os.path.join(root, file))
            print("Removed .gitkeep from " + root)

print("Creating main_xui.tar.gz")
allfile = os.listdir("Xtream_main/")
with tarfile.open("tmp/main_xui.tar.gz", "w:gz") as tar:
    for file in allfile:
        tar.add("Xtream_main/" + file, arcname=os.path.basename(file))


print("Remove folder Xtream_main/")
shutil.rmtree("Xtream_main/")
