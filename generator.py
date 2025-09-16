import os
import dotenv
import pathlib


dotenv.load_dotenv()


URL: str = os.getenv("URL", "")
PATH: pathlib.Path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))


if not URL:
    raise ValueError("URL not defined in .env")


def main(root: pathlib.Path):
    res: str
    current_path: pathlib.Path
    current_path_str: str
    for dirpath, dirnames, filenames in os.walk(root):
        current_path = pathlib.Path(dirpath).relative_to(PATH)
        current_path_str = str(current_path).replace("\\", "/")

        if current_path_str.startswith(".git"):
            continue

        res = ""
        if current_path_str != ".":
            parent = os.path.dirname(current_path_str)
            res += f"## [{parent}/]({URL + ('/' if parent != "" else "") + parent}/){os.path.basename(current_path_str)}/\n\n"

        for folder in dirnames:
            if folder.startswith(".git"):
                continue
            res += f"- d: [{folder}/]({URL + '/' + (current_path_str if current_path_str != "." else "") + ('/' if current_path_str != "." else "") + folder}/)\n"

        for file in filenames:
            if file == "README.md" or (current_path_str == "." and (file == "LICENSE" or file == "CNAME" or file == ".env" or file == "generator.py")) or file.startswith(".git"):
                continue
            res += f"- f: [{file}]({URL + '/' + (current_path_str if current_path_str != "." else "") + ('/' if current_path_str != "." else "") + file})\n"

        with open(os.path.join(dirpath, "README.md"), "w", encoding="utf-8") as f:
            f.write(res)


if __name__ == "__main__":
    main(PATH)

