import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
from config import TILES

def generate_and_save_world(map_size=1000, res=6, octaves=10, worlds_folder='worlds'):
    """
    Using Numpy and Scipy, it generates a fractal noise-based world map
    and saves it in PNG format with clear pixels.

    Parameters:
    ----------
    map_size : int
        Pixel width and height of the generated world map (e.g., 1000 for a 1000x1000 map).
    res : int
        Initial grid resolution for the noise. Higher values create more landmasses and islands.
    octaves : int
        fractal noise layer amount. Higher values create more detailed coastlines and mountains.
    worlds_folder : str
        target folder for saving the image. If it doesn't exist, it will be created.

    Returns:
    -------
    str: Absolute path of the saved map file.
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
        TILES["deep_water"],
        TILES["shallow_water"],
        TILES["sand"],
        TILES["grass"],
        TILES["forest"],
        TILES["mountain"],
        TILES["high_mountain"],
        TILES["peak_snow"]
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

if __name__ == "__main__":
    saved_path = generate_and_save_world(map_size=1000, res=6, octaves=10)
    print(f"File saved to: {saved_path}")