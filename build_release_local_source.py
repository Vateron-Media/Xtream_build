import os
import shutil
import tarfile

while True:
    type = input("Enter type (main or sub): ")
    if type == "main" or type == "sub":
        break
    else:
        print("Invalid type")

input = input("Enter path to Xtream source folder: ")
if not os.path.exists(input):
    print("Path does not exist")
    exit()

path_download_folder = os.path.join("tmp", f"Xtream_{type}")

# create tmp folder
if not os.path.exists("tmp"):
    os.makedirs("tmp")

# remove main_xui.tar.gz if it exists
if os.path.exists("tmp/{type}_xui.tar.gz"):
    os.remove(type + "_xui.tar.gz")
    print(f"Removed old {type}_xui.tar.gz")

# copy files to tmp folder
print(f"Copy files from {input} to {path_download_folder}")
shutil.copytree(input, path_download_folder)

print("Removing trash from " + path_download_folder)
if os.path.exists(path_download_folder + "/.git"):
    shutil.rmtree(path_download_folder + "/.git")
    print("Removed .git from " + path_download_folder)
if os.path.exists(path_download_folder + "/.github"):
    shutil.rmtree(path_download_folder + "/.github")
    print("Removed .github from " + path_download_folder)
if os.path.exists(path_download_folder + "/.vscode"):
    shutil.rmtree(path_download_folder + "/.vscode")
    print("Removed .vscode from " + path_download_folder)
if os.path.exists(path_download_folder + "/.gitignore"):
    os.remove(path_download_folder + "/.gitignore")
    print("Removed .gitignore from " + path_download_folder)
if os.path.exists(path_download_folder + "/.gitattributes"):
    os.remove(path_download_folder + "/.gitattributes")
    print("Removed .gitattributes from " + path_download_folder)
if os.path.exists(path_download_folder + "/update"):
    shutil.rmtree(path_download_folder + "/update")
    print("Removed update from " + path_download_folder)

# delete .gitkeep everywhere
for root, dirs, files in os.walk(path_download_folder):
    for file in files:
        if file == ".gitkeep":
            os.remove(os.path.join(root, file))
            print("Removed .gitkeep from " + root)   

print(f"Creating {type}_xui.tar.gz")
allfile = os.listdir(path_download_folder)
with tarfile.open(f"tmp/{type}_xui.tar.gz", "w:gz") as tar:
    for file in allfile:
        tar.add(path_download_folder + "/" + file, arcname=os.path.basename(file))


print("Remove folder " + path_download_folder)
shutil.rmtree(path_download_folder)