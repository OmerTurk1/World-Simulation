class NationState:
    def __init__(self, name, color, chunk_lose_days):
        self.name = name
        self.color = color
        self.chunk_lose_days = chunk_lose_days
        
        # Chunk mechanics
        self.owned_chunks = set()          # Unique chunk coordinates like {(cx, cy), (cx2, cy2)}
        self.chunk_cooldowns = {}          # Countdown values like {(cx, cy): remained_days}
        self.population_count = 0          # Daily population count (for UI and logging)
        self.chunks_count = 0              # Daily chunk count

        # resources
        self.resources = {
            "wood": {
                "current": 0,
                "max": 0
            },
            "stone": {
                "current": 0,
                "max": 0
            },
            "gold": {
                "current": 0,
                "max": 0
            }
        }
        self.update_max_resources()

    def update_max_resources(self):
        self.resources["wood"]["max"] = 200 * len(self.owned_chunks)
        self.resources["stone"]["max"] = 200 * len(self.owned_chunks)
        self.resources["gold"]["max"] = 200 * len(self.owned_chunks)

    def add_resource(self, resource, amount=1):
        if self.resources[resource]["current"] >= self.resources[resource]["max"]:
            return
        self.resources[resource]["current"] = min(self.resources[resource]["current"] + amount, self.resources[resource]["max"])

    def add_chunk(self, cx, cy):
        self.owned_chunks.add((cx, cy))
        self.chunk_cooldowns.pop((cx, cy), None)
        self.chunks_count = len(self.owned_chunks)
        self.update_max_resources()

    def remove_chunk(self, cx, cy):
        self.owned_chunks.discard((cx, cy))
        self.chunk_cooldowns.pop((cx, cy), None)
        self.chunks_count = len(self.owned_chunks)
        self.update_max_resources()

    def update_chunk_cooldowns(self, chunk_populations, map_manager):
        current_chunks = list(self.owned_chunks)
        
        for (cx, cy) in current_chunks:
            pops = chunk_populations.get((cx, cy), {})
            my_pop = pops.get(self.color, 0)
            
            if my_pop < 10:
                if (cx, cy) not in self.chunk_cooldowns:
                    self.chunk_cooldowns[(cx, cy)] = self.chunk_lose_days
                else:
                    self.chunk_cooldowns[(cx, cy)] -= 1
                
                if self.chunk_cooldowns[(cx, cy)] <= 0:
                    self.remove_chunk(cx, cy)
                    map_manager.set_chunk_owner(cx, cy, None)
            else:
                self.chunk_cooldowns.pop((cx, cy), None)