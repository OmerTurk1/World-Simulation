import os

def generate_tree(startpath, indent="", current_depth=0, max_depth=None):
    if max_depth is not None and current_depth > max_depth:
        return

    try:
        items = sorted(os.listdir(startpath))
    except PermissionError:
        print(f"{indent}[Access Denied]")
        return

    items = [item for item in items if item != "ps.py"]

    for i, item in enumerate(items):
        path = os.path.join(startpath, item)
        is_last = (i == len(items) - 1)
        
        connector = "└── " if is_last else "├── "
        
        if os.path.isdir(path):
            print(f"{indent}{connector}{item}/")
            
            if max_depth is None or current_depth < max_depth:
                extension = "    " if is_last else "│   "
                generate_tree(path, indent + extension, current_depth + 1, max_depth)
        else:
            if max_depth is None or current_depth <= max_depth:
                print(f"{indent}{connector}{item}")

if __name__ == "__main__":
    main_folder = "./"
    MAX_DEPTH_LIMIT = 2

    print(f"Directory structure for: {os.path.abspath(main_folder)} (Max Depth: {MAX_DEPTH_LIMIT})")
    print(".")
    generate_tree(main_folder, max_depth=MAX_DEPTH_LIMIT)