import os

def generate_tree(startpath, indent=""):
    """
    Belirtilen dizin altındaki tüm dosya ve klasörleri 
    ağaç yapısı şeklinde yazdırır.
    """
    # Dizindeki öğeleri listele ve alfabetik sırala
    try:
        items = sorted(os.listdir(startpath))
    except PermissionError:
        print(f"{indent}[Erişim Engellendi]")
        return

    for i, item in enumerate(items):
        if item == "ps.py":
            continue  # ps.py dosyasını atla
        path = os.path.join(startpath, item)
        is_last = (i == len(items) - 1)
        
        # Görsel bağlantı karakterlerini belirle
        connector = "└── " if is_last else "├── "
        
        # Eğer öğe bir klasörse, içine gir (recursion)
        if os.path.isdir(path):
            print(f"{indent}{connector}{item}/")
            extension = "    " if is_last else "│   "
            generate_tree(path, indent + extension)
        else:
            print(f"{indent}{connector}{item}")

if __name__ == "__main__":
    # Buraya kendi dosya yolunu yazabilirsin
    main_folder = "./"  # Mevcut dizin için "./", tam yol için "C:/Users/..." gibi
    
    print(f"Directory structure for: {os.path.abspath(main_folder)}")
    print(".")
    generate_tree(main_folder)