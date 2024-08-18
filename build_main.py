import os
import shutil
import tarfile

# place input path to xtream_main
input_path = input("Enter path to Xtream_main: ")


# remove folder build_main if it exists
if os.path.exists("build_main"):
    shutil.rmtree("build_main")

print("Copying folder xtream_main to build_main")
shutil.copytree(input_path, "build_main")

# remove .git with build_main
print("Removing trash from build_main")

if os.path.exists("build_main/.git"):
    shutil.rmtree("build_main/.git")
    print("Removed .git from build_main")
if os.path.exists("build_main/.vscode"):
    shutil.rmtree("build_main/.vscode")
    print("Removed .vscode from build_main")
if os.path.exists("build_main/.gitignore"):
    os.remove("build_main/.gitignore")
    print("Removed .gitignore from build_main")
if os.path.exists("build_main/.gitattributes"):
    os.remove("build_main/.gitattributes")
    print("Removed .gitattributes from build_main")
if os.path.exists("build_main/update"):
    shutil.rmtree("build_main/update")
    print("Removed update from build_main")


print("Creating main_xui.tar.gz")
allfile = os.listdir("build_main")
with tarfile.open("main_xui.tar.gz", "w:gz") as tar:
    for file in allfile:
        tar.add("build_main/" + file, arcname=os.path.basename(file))


print("Remove folder build_main")
shutil.rmtree("build_main")
