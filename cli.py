from cache import Cache
import random

def main():
    print(" Cache Policy Simulator - LRU vs FIFO)")
    print("Commands: policy lru|fifo, capacity N, run N [zipf], stats, quit")
    
    cache = None
    while True:
        cmd = input("> ").strip().split()
        if not cmd: continue
        
        if cmd[0] == "policy" and len(cmd) > 1:
            policy = cmd[1]
            cap = cache.capacity if cache else 3
            cache = Cache(cap, policy)
            print(f" Policy: {policy.upper()}")
        
        elif cmd[0] == "capacity" and len(cmd) > 1:
            cap = int(cmd[1])
            cache = Cache(cap, cache.policy if cache else "lru")
            print(f"✅ Capacity: {cap}")
        
        elif cmd[0] == "run" and len(cmd) > 1:
            n = int(cmd[1])
            workload = "zipf" if len(cmd) > 2 and cmd[2] == "zipf" else "random"
            simulate_workload(cache, n, workload)
            print(cache.stats())
        
        elif cmd[0] == "stats":
            print(cache.stats() if cache else "No cache")
        
        elif cmd[0] == "quit":
            break
        else:
            print("policy lru|fifo, capacity N, run N [zipf], stats, quit")

def simulate_workload(cache, n, pattern):
    keys = list(range(100))
    for i in range(n):
        if pattern == "zipf":
            key = i % 20 
        else:
            key = random.choice(keys)
        cache.put(key, f"data-{key}")
        cache.get(key)

if __name__ == "__main__":
    main()
