from PIL import Image
import os
from collections import defaultdict

def get_files() -> dict[str, list[str]]:
    files_by_directory = defaultdict(list)
    for root, dirs, files in os.walk("Renders/"):
        for file in files:
            if file.endswith(".png"):
                files_by_directory[root].append(file)
    return files_by_directory


def get_resolution(file: str) -> tuple[int, int]:
    with Image.open(file) as img:
        return img.size

def compile_spritesheet(files: list[str]) -> Image:
    sizes = [get_resolution(file) for file in files]

    if len(set(sizes)) != 1:
        print("Images are not the same size")
        return
    
    width, height = sizes[0]
    spritesheet = Image.new("RGBA", (width * len(files), height))
    for i, file in enumerate(files):
        with Image.open(file) as img:
            spritesheet.paste(img, (i * width, 0))

    return spritesheet

def main():
    all_files = get_files()

    if not os.path.exists("/tmp/spritesheets/"):
        os.makedirs("/tmp/spritesheets/")

        for root, dirs, files in os.walk("/tmp/spritesheets/"):
            for file in files:
                os.remove(os.path.join(root, file))
    
    for directory, files in all_files.items():

        name = directory.split("/")[-1]
        path = directory.replace(f"/{name}", "").replace("Renders/", "")

        print(f"Compiling {os.path.join(path, name)}")

        if ".nospritesheet" in os.listdir(directory):
            print("Contains .nospritesheet file, copying original")
            for file in files:
                original_path = os.path.join(directory, file)
                destination_path = os.path.join("/tmp/spritesheets", path, name, file)

                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                with open(original_path, 'rb') as src_file:
                    with open(destination_path, 'wb') as dst_file:
                        dst_file.write(src_file.read())
            continue

        spritesheet = compile_spritesheet([f"{directory}/{file}" for file in files])
        
        if not os.path.exists(f"/tmp/spritesheets/{path}"):
            os.makedirs(f"/tmp/spritesheets/{path}")

        spritesheet.save(f"/tmp/spritesheets/{path}/{name}.png")

if __name__ == "__main__":
    main()