NATIONS = [
    {"name": "Red", "color": (255, 0, 0)},
    {"name": "Blue", "color": (0, 100, 255)}, 
    {"name": "Yellow", "color": (255, 255, 0)},
    {"name": "Purple", "color": (128, 0, 128)},
    {"name": "Orange", "color": (255, 165, 0)},
    {"name": "Pink", "color": (255, 105, 180)}
]
TILES = {
    "deep_water": (0, 0, 139),       # Deep Blue (Sea)
    "shallow_water": (65, 105, 225),    # Sky Blue (Shallow Water)
    "sand": (238, 214, 175),   # Sand
    "grass": (34, 139, 34),     # Green (Grassland)
    "forest": (0, 100, 0),       # Dark Green (Forest)
    "hill": (139, 137, 137),   # Gray (Hill)
    "high_mountain": (105, 105, 105),   # Dark Gray (High Mountain)
    "peak_snow": (255, 255, 255)    # White (Peak Snow)
}
chunk_lose_days = 25 # lose the chunk after this many days without 10 agents of the owning nation