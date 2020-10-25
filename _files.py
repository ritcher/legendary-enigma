import os

from _config import current_path

with open("logins.txt", mode="r", encoding="utf-8") as file:
    content = file.readlines()

for file in ["lives.txt", "bads.txt"]:
    try:
        os.remove(file)
    except FileNotFoundError:
        pass
    os.system(f"touch {current_path}/{file}")

bads = open(f"{current_path}/bads.txt", mode="a", encoding="utf-8")
lives = open(f"{current_path}/lives.txt", mode="a", encoding="utf-8")
