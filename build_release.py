import os
import shutil
import tarfile
import requests
from tqdm import tqdm
import zipfile
import zipfile


def download_file(url, filename):
    # Send a GET request to the URL
    response = requests.get(url, stream=True)

    # Get the total file size
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
    with open(filename, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)


while True:
    type = input("Enter type (main or sub): ")
    if type == "main" or type == "sub":
        break
    else:
        print("Invalid type")

path_download_folder = f"Xtream_{type}/"
downloaded_file = os.path.join("tmp", f"{type}_main.zip")

# remove main_xui.tar.gz if it exists
if os.path.exists(type + "_xui.tar.gz"):
    os.remove(type + "_xui.tar.gz")
    print(f"Removed {type}_xui.tar.gz")


# remove folder Xtream_main/ if it exists
if os.path.exists(path_download_folder):
    shutil.rmtree(path_download_folder)

# create tmp folder
if not os.path.exists("tmp"):
    os.makedirs("tmp")

# download
print(f"Download Xtream_{type}")
download_file(
    f"https://github.com/Vateron-Media/Xtream_{type}/archive/refs/heads/main.zip",
    downloaded_file,
)

print(f"Unzip {type}_main.zip")
with zipfile.ZipFile(downloaded_file, "r") as zip_ref:
    zip_ref.extractall(path_download_folder)

os.remove(downloaded_file)

print("Removing trash from " + path_download_folder)

if os.path.exists(path_download_folder + ".git"):
    shutil.rmtree(path_download_folder + ".git")
    print("Removed .git from " + path_download_folder)
if os.path.exists(path_download_folder + ".vscode"):
    shutil.rmtree(path_download_folder + ".vscode")
    print("Removed .vscode from " + path_download_folder)
if os.path.exists(path_download_folder + ".gitignore"):
    os.remove(path_download_folder + ".gitignore")
    print("Removed .gitignore from " + path_download_folder)
if os.path.exists(path_download_folder + ".gitattributes"):
    os.remove(path_download_folder + ".gitattributes")
    print("Removed .gitattributes from " + path_download_folder)
if os.path.exists(path_download_folder + "update"):
    shutil.rmtree(path_download_folder + "update")
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
        tar.add(path_download_folder + file, arcname=os.path.basename(file))


print("Remove folder " + path_download_folder)
shutil.rmtree(path_download_folder)
