import json
from os import path, mkdir
from rich import print


def generate(metadata):
    title, fn_name = metadata["title"], metadata["fn_name"]
    sign = ", ".join(
        [
            f"{metadata['signature'][index]}: {inp}"
            for index, inp in enumerate(metadata["input"])
        ]
    )
    retval = ", ".join(metadata["output"])

    return f"""from typing import List
from ..util import preheat

type IMG = List[List[int]]
type D = List[int]
type Z = int

@preheat("{title}")
def {fn_name}({sign}) -> {retval}:
	pass
"""


def file_exists(filename):
    return path.exists(filename)


def write_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)


def create_folder(foldername):
    mkdir(foldername)


def check_folder(foldername):
    if not file_exists(foldername):
        create_folder(foldername)
        print(f"✅ /{foldername} written.")
    else:
        print(f"👍 /{foldername} folder already exists.")


def main():
    parent = "algorithms"

    with open("schema.json", "r") as file:
        schema = json.loads(file.read())

    for folder in schema:
        check_folder(path.join(parent, folder))

        for title in schema[folder]:
            filename = path.join(parent, folder, title + ".py")
            try:
                if not file_exists(filename):
                    write_file(
                        filename, generate({**schema[folder][title], "title": title})
                    )
                    print(f"✅ {filename} written.")
                else:
                    print(f"👍 {filename} already exists.")
            except Exception as e:
                print(f"❌ {filename} can't be created.")


if __name__ == "__main__":
    main()
