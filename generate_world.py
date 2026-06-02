import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom

def generate_and_save_world(map_size=1000, res=6, octaves=10, worlds_folder='worlds'):
    """
    Numpy ve Scipy kullanarak fraktal gürültü tabanlı bir dünya haritası üretir
    ve bunu pikselleri net kalacak şekilde PNG formatında kaydeder.

    Parametreler:
    ----------
    map_size : int, varsayılan 1000
        Üretilecek haritanın piksel cinsinden genişlik ve yükseklik boyutu (Örn: 1000x1000).
    res : int, varsayılan 6
        Başlangıç ızgara (grid) çözünürlüğü. Değer büyüdükçe haritadaki ana kara ve ada sayısı artar.
    octaves : int, varsayılan 10
        Fraktal detay katmanı sayısı. Değer büyüdükçe kıyı çizgileri ve dağlar daha girintili çıkıntılı olur.
    worlds_folder : str, varsayılan 'worlds'
        Görüntünün kaydedileceği hedef klasör adı. Klasör yoksa otomatik oluşturulur.

    Döndürdüğü Değer:
    -------
    str
        Kaydedilen harita dosyasının tam yolu ve adı.
    """
    os.makedirs(worlds_folder, exist_ok=True)
    
    shape = (map_size, map_size)
    noise = np.zeros(shape)
    frequency = 1
    amplitude = 1
    persistence = 0.5
    
    for _ in range(octaves):
        grid_shape = (int(res * frequency), int(res * frequency))
        small_grid = np.random.rand(*grid_shape)
        zoom_factors = (shape[0] / grid_shape[0], shape[1] / grid_shape[1])
        scaled_noise = zoom(small_grid, zoom_factors, order=3)
        noise += scaled_noise * amplitude
        amplitude *= persistence
        frequency *= 2
        
    elevation = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))
    elevation = elevation * 2 - 1

    thresholds = [-0.35, -0.10, 0.00, 0.25, 0.50, 0.65, 0.80]
    terrain_ids = np.digitize(elevation, bins=thresholds)

    colors = np.array([
        (0, 0, 139),       # Deep Blue (Sea)
        (65, 105, 225),    # Sky Blue (Shallow Water)
        (238, 214, 175),   # Sand
        (34, 139, 34),     # Green (Grassland)
        (0, 100, 0),       # Dark Green (Forest)
        (139, 137, 137),   # Gray (Mount)
        (105, 105, 105),   # Dark Gray (High Mountain)
        (255, 255, 255)    # White (Peak Snow)
    ], dtype=np.uint8)

    image_data = colors[terrain_ids]

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(image_data, interpolation='nearest')
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    img_name = f'{worlds_folder}/world_map_s={map_size}_r={res}_o={octaves}.png'
    plt.savefig(img_name, dpi=150, bbox_inches='tight', pad_inches=0)
    plt.close()

    return img_name

# --- ÖRNEK KULLANIM ---
if __name__ == "__main__":
    saved_path = generate_and_save_world(map_size=1000, res=6, octaves=10)
    print(f"Dosya şuraya kaydedildi: {saved_path}")