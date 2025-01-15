import os


def print_directory_structure(root_dir, indent='', ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = []

    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            if item in ignore_dirs:
                continue
            print(f"{indent}📁 {item}/")
            print_directory_structure(item_path, indent + '    ', ignore_dirs)


if __name__ == "__main__":
    root_directory = '.'  # Change this to your project's root directory if needed
    ignore_directories = ['venv']  # Add directories to ignore here
    print_directory_structure(root_directory, ignore_dirs=ignore_directories)
