# install_deps.py
import subprocess

def main():
    # Download fido 1.60.rc5
    # cd to the download directory
    # python -m setup install
    subprocess.run(["pip", "install", "fido"])
    subprocess.run(["curl", "-LO", "https://github.com/richardlehane/siegfried/releases/download/v1.9.1/siegfried_darwin_amd64.tar.gz"])
    subprocess.run(["tar", "-xzf", "siegfried_darwin_amd64.tar.gz"])
    subprocess.run(["sudo", "mv", "sf", "/usr/local/bin/"])
    subprocess.run(["sf", "-version"])

if __name__ == "__main__":
    main()