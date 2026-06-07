import pygame
import time
from collections import Counter
from map_manager import MapManager
from agent import Agent
from config import NATIONS, chunk_lose_days
from state import NationState

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

    nation_states = {}
    for nation in NATIONS:
        nation_states[nation["color"]] = NationState(nation["name"], nation["color"], chunk_lose_days)

    agents = []
    person_per_nation = 10
    for state in nation_states.values():
        start_x, start_y = map_manager.get_random_walkable_pos()
        for _ in range(person_per_nation):
            x, y = map_manager.get_walkable_pos_near(start_x, start_y, radius=20)
            agents.append(Agent(x, y, state.color))

    running = True
    day = 1
    start_time = time.time()
    
    font = pygame.font.SysFont("Arial", 18, bold=True)
    
    while running:
        day_record = {
            "Day": day,
            "Total": len(agents)
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        map_manager.update_resources()

        chunk_populations = {}
        for agent in agents:
            if agent.alive:
                cx, cy = map_manager.get_chunk(agent.x, agent.y)
                if (cx, cy) not in chunk_populations:
                    chunk_populations[(cx, cy)] = {}
                chunk_populations[(cx, cy)][agent.color] = chunk_populations[(cx, cy)].get(agent.color, 0) + 1

        max_cx = map_manager.width // map_manager.chunk_size
        max_cy = map_manager.height // map_manager.chunk_size
        
        for (cx, cy), pops in chunk_populations.items():
            current_owner_color = map_manager.get_chunk_owner(cx, cy)
            
            if current_owner_color is None:
                best_color = None
                max_count = 0
                for color, count in pops.items():
                    if count >= 10 and count > max_count:
                        max_count = count
                        best_color = color
                if best_color:
                    map_manager.set_chunk_owner(cx, cy, best_color)
                    nation_states[best_color].add_chunk(cx, cy)

        for state in nation_states.values():
            state.update_chunk_cooldowns(chunk_populations, map_manager)
        
        for state in nation_states.values():
            day_record[f"{state.name}_chunks"] = state.chunks_count

        new_agents = []
        for agent in agents:
            agent.update(map_manager, nation_states[agent.color], new_agents)
        
        day_record["Birth"] = len(new_agents)
        agents.extend(new_agents)
        
        dead_count = sum(1 for a in agents if not a.alive)
        day_record["Death"] = dead_count
        agents = [a for a in agents if a.alive]

        screen.blit(map_manager.bg_image, (0, 0))

        overlay = pygame.Surface(screen_size, pygame.SRCALPHA)
        
        for (cx, cy), owner_color in map_manager.chunk_owners.items():
            if owner_color is not None:
                rect_x = cx * map_manager.chunk_size
                rect_y = cy * map_manager.chunk_size
                pygame.draw.rect(overlay, (*owner_color, 60), (rect_x, rect_y, map_manager.chunk_size, map_manager.chunk_size))
        
        for (cx, cy), owner_color in map_manager.chunk_owners.items():
            if owner_color is not None:
                rect_x = cx * map_manager.chunk_size
                rect_y = cy * map_manager.chunk_size
                cs = map_manager.chunk_size
                
                left_owner  = map_manager.get_chunk_owner(cx - 1, cy)
                right_owner = map_manager.get_chunk_owner(cx + 1, cy)
                top_owner   = map_manager.get_chunk_owner(cx, cy - 1)
                bottom_owner= map_manager.get_chunk_owner(cx, cy + 1)
                
                if left_owner != owner_color:
                    pygame.draw.line(overlay, owner_color, (rect_x, rect_y), (rect_x, rect_y + cs), 2)
                    
                if right_owner != owner_color:
                    pygame.draw.line(overlay, owner_color, (rect_x + cs, rect_y), (rect_x + cs, rect_y + cs), 2)
                    
                if top_owner != owner_color:
                    pygame.draw.line(overlay, owner_color, (rect_x, rect_y), (rect_x + cs, rect_y), 2)
                    
                if bottom_owner != owner_color:
                    pygame.draw.line(overlay, owner_color, (rect_x, rect_y + cs), (rect_x + cs, rect_y + cs), 2)

        screen.blit(overlay, (0, 0))
        
        for agent in agents:
            agent.draw(screen)

        color_counts = Counter([agent.color for agent in agents])
        
        y_offset = 15
        day_text = font.render(f"Day: {day} | Total Population: {len(agents)}", True, (255, 255, 255))
        screen.blit(day_text, (15, y_offset))
        y_offset += 25

        for state in nation_states.values():
            color = state.color
            state.population_count = color_counts.get(color, 0)

            state_wood = state.resources["wood"]["current"]
            state_stone = state.resources["stone"]["current"]
            state_gold = state.resources["gold"]["current"]
            
            day_record[state.name] = state.population_count
            day_record[f"{state.name}_chunks"] = state.chunks_count
            day_record[f"{state.name}_wood"] = state_wood
            day_record[f"{state.name}_stone"] = state_stone
            day_record[f"{state.name}_gold"] = state_gold
            
            text = font.render(
                f"{state.name}: {state.population_count} | Chunks: {state.chunks_count} | W:{state_wood} S:{state_stone} G:{state_gold}",
                True, state.color
            )
            screen.blit(text, (15, y_offset))
            y_offset += 20
            
        history.append(day_record)

        pygame.display.flip()
        clock.tick(60)
        day += 1

    pygame.quit()
    
    with open(data_path, "w", encoding="utf-8") as f:
        headers = ["Day", "Total", "Birth", "Death"] 
        headers += [state.name for state in nation_states.values()]
        headers += [f"{state.name}_chunks" for state in nation_states.values()]
        headers += [f"{state.name}_wood" for state in nation_states.values()]
        headers += [f"{state.name}_stone" for state in nation_states.values()]
        headers += [f"{state.name}_gold" for state in nation_states.values()]
        f.write(",".join(headers) + "\n")
        
        for record in history:
            row_data = [str(record["Day"]), str(record["Total"]), str(record["Birth"]), str(record["Death"])]
            for state in nation_states.values():
                row_data.append(str(record[state.name]))
            for state in nation_states.values():
                row_data.append(str(record[f"{state.name}_chunks"]))
            for state in nation_states.values():
                row_data.append(str(record[f"{state.name}_wood"]))
            for state in nation_states.values():
                row_data.append(str(record[f"{state.name}_stone"]))
            for state in nation_states.values():
                row_data.append(str(record[f"{state.name}_gold"]))
                
            f.write(",".join(row_data) + "\n")

    end_time = time.time()
    print(f"Simulation completed. Data saved to {data_path}.")
    print(f"Total simulation time: {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    world_path = "worlds/single_land_map.png"
    data_path = "data/population_data.csv"
    screen_size = (800, 800)
    main(world_path, data_path, screen_size)