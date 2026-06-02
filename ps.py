import os

def generate_tree(startpath, indent=""):
    try:
        items = sorted(os.listdir(startpath))
    except PermissionError:
        print(f"{indent}[Access Denied]")
        return

    for i, item in enumerate(items):
        if item == "ps.py":
            continue  # skip ps.py
        path = os.path.join(startpath, item)
        is_last = (i == len(items) - 1)
        
        connector = "└── " if is_last else "├── "
        
        if os.path.isdir(path): # if it's a directory
            print(f"{indent}{connector}{item}/")
            extension = "    " if is_last else "│   "
            generate_tree(path, indent + extension)
        else:
            print(f"{indent}{connector}{item}")

if __name__ == "__main__":
    main_folder = "./"
    print(f"Directory structure for: {os.path.abspath(main_folder)}")
    print(".")
    generate_tree(main_folder)