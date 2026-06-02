import pygame
import time
from collections import Counter
from map_manager import MapManager
from agent import Agent

NATIONS = [
    {"name": "Red", "color": (255, 0, 0)},
    {"name": "Blue", "color": (0, 100, 255)}, 
    {"name": "Yellow", "color": (255, 255, 0)},
    {"name": "Purple", "color": (128, 0, 128)},
    {"name": "Orange", "color": (255, 165, 0)},
    {"name": "Pink", "color": (255, 105, 180)}
]

def main(world_path, data_path):
    pygame.init()
    history = []
    
    screen_size = (800, 800)
    
    try:
        map_manager = MapManager(world_path, target_size=screen_size)
    except FileNotFoundError:
        print(f"Error: {world_path} not found. Please check the file path.")
        return
        
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("World Simulation")
    clock = pygame.time.Clock()

    agents = []
    person_per_nation = 10
    for nation in NATIONS:
        start_x, start_y = map_manager.get_random_walkable_pos()
        for _ in range(person_per_nation):
            x, y = map_manager.get_walkable_pos_near(start_x, start_y, radius=20)
            agents.append(Agent(x, y, nation["color"]))

    running = True
    day = 1
    start_time = time.time()
    
    font = pygame.font.SysFont("Arial", 18, bold=True)
    
    while running:
        # daily record dictionary to save in history
        day_record = {
            "Day": day,
            "Total": len(agents)
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        map_manager.update_food()
        
        new_agents = []
        for agent in agents:
            agent.update(map_manager, new_agents)
        
        day_record["Birth"] = new_agents.__len__()
        agents.extend(new_agents)
        day_record["Death"] = [a for a in agents if not a.alive].__len__()
        agents = [a for a in agents if a.alive]

        screen.blit(map_manager.bg_image, (0, 0))
        
        for agent in agents:
            agent.draw(screen)

        # How many agents of each nation are there?
        color_counts = Counter([agent.color for agent in agents])
        
        # UI and Daily Record Collection
        y_offset = 15
        day_text = font.render(f"Day: {day} | Total Population: {len(agents)}", True, (255, 255, 255))
        screen.blit(day_text, (15, y_offset))
        y_offset += 25

        for nation in NATIONS:
            # Count the number of agents for the current nation
            count = color_counts.get(nation["color"], 0)
            day_record[nation["name"]] = count 
            
            # Print the nation name and count in the nation's color with a shadow for better visibility
            text = font.render(f"{nation['name']}: {count}", True, nation["color"])
            shadow = font.render(f"{nation['name']}: {count}", True, (0, 0, 0))
            screen.blit(shadow, (16, y_offset + 1))
            screen.blit(text, (15, y_offset))
            y_offset += 20
            
        history.append(day_record)

        pygame.display.flip()
        clock.tick(60)
        day += 1

    pygame.quit()
    
    # CSV file writing
    with open(data_path, "w", encoding="utf-8") as f:
        # Headers
        headers = ["Day", "Total", "Birth", "Death"] + [nation["name"] for nation in NATIONS]
        f.write(",".join(headers) + "\n")
        
        # Write the data rows
        for record in history:
            row_data = [str(record["Day"]), str(record["Total"]), str(record["Birth"]), str(record["Death"])]
            for nation in NATIONS:
                row_data.append(str(record[nation["name"]]))
            f.write(",".join(row_data) + "\n")

    end_time = time.time()
    print(f"Simulation completed. Data saved to {data_path}.")
    print(f"Total simulation time: {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    world_path = "worlds/single_land_map.png"
    data_path = "data/population_data.csv" 
    main(world_path, data_path)