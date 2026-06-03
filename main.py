import pygame
import time
from collections import Counter
from map_manager import MapManager
from agent import Agent
from config import NATIONS, chunk_lose_days

def main(world_path, data_path, screen_size):
    pygame.init()
    history = []
    
    try:
        map_manager = MapManager(world_path, target_size=screen_size, chunk_size=25)
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
    chunk_cooldowns = {}
    
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

        chunk_populations = {} # {(cx, cy): {color: count}}
        
        for agent in agents:
            if agent.alive:
                cx, cy = map_manager.get_chunk(agent.x, agent.y)
                if (cx, cy) not in chunk_populations:
                    chunk_populations[(cx, cy)] = {}
                chunk_populations[(cx, cy)][agent.color] = chunk_populations[(cx, cy)].get(agent.color, 0) + 1

        max_cx = map_manager.width // map_manager.chunk_size
        max_cy = map_manager.height // map_manager.chunk_size
        
        for cx in range(max_cx):
            for cy in range(max_cy):
                pops = chunk_populations.get((cx, cy), {})
                current_owner = map_manager.get_chunk_owner(cx, cy)
                
                if current_owner is not None:
                    if pops.get(current_owner, 0) < 10: # chunk owner number reduced to 10
                        if (cx, cy) not in chunk_cooldowns:
                            chunk_cooldowns[(cx, cy)] = chunk_lose_days
                        else: # there is already a countdown, decrease it by 1
                            chunk_cooldowns[(cx, cy)] -= 1
                            
                        if chunk_cooldowns[(cx, cy)] <= 0: # time is upi lose the chunk
                            map_manager.set_chunk_owner(cx, cy, None)
                            chunk_cooldowns.pop((cx, cy), None)
                    else: # population restored
                        chunk_cooldowns.pop((cx, cy), None)
                else:
                    # conquer empty chunk
                    best_color = None
                    max_count = 0
                    for color, count in pops.items():
                        if count >= 10 and count > max_count:
                            max_count = count
                            best_color = color
                    if best_color:
                        map_manager.set_chunk_owner(cx, cy, best_color)
                        chunk_cooldowns.pop((cx, cy), None)
        
        # calculate how many chunks each nation owns for the daily record
        active_owners = list(map_manager.chunk_owners.values())
        for nation in NATIONS:
            owned_chunks_count = active_owners.count(nation["color"])
            day_record[f"{nation['name']}_chunks"] = owned_chunks_count
        
        new_agents = []
        for agent in agents:
            agent.update(map_manager, new_agents)
        
        day_record["Birth"] = new_agents.__len__()
        agents.extend(new_agents)
        day_record["Death"] = [a for a in agents if not a.alive].__len__()
        agents = [a for a in agents if a.alive]

        screen.blit(map_manager.bg_image, (0, 0))

        overlay = pygame.Surface(screen_size, pygame.SRCALPHA)
        
        # fill chunks with semi-transparent color based on ownership
        for (cx, cy), owner_color in map_manager.chunk_owners.items():
            if owner_color is not None:
                rect_x = cx * map_manager.chunk_size
                rect_y = cy * map_manager.chunk_size
                pygame.draw.rect(overlay, (*owner_color, 60), (rect_x, rect_y, map_manager.chunk_size, map_manager.chunk_size))
        
        # draw lines only on edges where neighboring chunk has different owner or is unowned
        for (cx, cy), owner_color in map_manager.chunk_owners.items():
            if owner_color is not None:
                rect_x = cx * map_manager.chunk_size
                rect_y = cy * map_manager.chunk_size
                cs = map_manager.chunk_size
                
                # Check owners of neighboring chunks
                left_owner  = map_manager.get_chunk_owner(cx - 1, cy)
                right_owner = map_manager.get_chunk_owner(cx + 1, cy)
                top_owner   = map_manager.get_chunk_owner(cx, cy - 1)
                bottom_owner= map_manager.get_chunk_owner(cx, cy + 1)
                
                # Left side
                if left_owner != owner_color:
                    pygame.draw.line(overlay, owner_color, (rect_x, rect_y), (rect_x, rect_y + cs), 2)
                    
                # Right side
                if right_owner != owner_color:
                    pygame.draw.line(overlay, owner_color, (rect_x + cs, rect_y), (rect_x + cs, rect_y + cs), 2)
                    
                # Top side
                if top_owner != owner_color:
                    pygame.draw.line(overlay, owner_color, (rect_x, rect_y), (rect_x + cs, rect_y), 2)
                    
                # Bottom side
                if bottom_owner != owner_color:
                    pygame.draw.line(overlay, owner_color, (rect_x, rect_y + cs), (rect_x + cs, rect_y + cs), 2)

        screen.blit(overlay, (0, 0))
        
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
            chunks_count = day_record[f"{nation['name']}_chunks"]
            
            # Print the nation name and count in the nation's color with a shadow for better visibility
            text = font.render(f"{nation['name']}: {count} | Chunks: {chunks_count}", True, nation["color"])
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
        headers = ["Day", "Total", "Birth", "Death"] 
        headers += [nation["name"] for nation in NATIONS]
        headers += [f"{nation['name']}_chunks" for nation in NATIONS] # Red_chunks, Blue_chunks vb.
        f.write(",".join(headers) + "\n")
        
        # Write the data rows
        for record in history:
            row_data = [str(record["Day"]), str(record["Total"]), str(record["Birth"]), str(record["Death"])]
            for nation in NATIONS:
                row_data.append(str(record[nation["name"]]))
            for nation in NATIONS:
                row_data.append(str(record[f"{nation['name']}_chunks"]))
                
            f.write(",".join(row_data) + "\n")

    end_time = time.time()
    print(f"Simulation completed. Data saved to {data_path}.")
    print(f"Total simulation time: {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    world_path = "worlds/single_land_map.png"
    data_path = "data/population_data.csv"
    screen_size = (800, 800)
    main(world_path, data_path, screen_size)