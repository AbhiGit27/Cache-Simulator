class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = self.next = None

class Cache:
    def __init__(self, capacity, policy="lru"):
        self.capacity = capacity
        self.policy = policy
        self.cache = {}
        self.hits = self.misses = self.evictions = 0
        
        if policy == "lru":
            self.head = Node()
            self.tail = Node()
            self.head.next = self.tail
            self.tail.prev = self.head
        else:  # FIFO
            self.order = []
    
    def get(self, key):
        if key not in self.cache:
            self.misses += 1
            return -1
        
        self.hits += 1
        value = self.cache[key]
        
        if self.policy == "lru":
            self._lru_move(key)
        return value
    
    def put(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            if self.policy == "lru":
                self._lru_move(key)
        else:
            if len(self.cache) == self.capacity:
                if self.policy == "lru":
                    self._lru_evict()
                else:
                    self._fifo_evict()
            
            self.cache[key] = value
            if self.policy == "lru":
                self._lru_add(key, value)
            else:
                self.order.append(key)
    
    def _lru_add(self, key, value):
        node = Node(key, value)
        self.cache[key] = node
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _lru_remove(self, node):
        prev = node.prev
        next_node = node.next
        prev.next = next_node
        next_node.prev = prev
    
    def _lru_move(self, key):
        node = self.cache[key]
        self._lru_remove(node)
        self._lru_add(key, node.value)
    
    def _lru_evict(self):
        lru = self.tail.prev
        self._lru_remove(lru)
        del self.cache[lru.key]
        self.evictions += 1
    
    def _fifo_evict(self):
        lru_key = self.order.pop(0)
        del self.cache[lru_key]
        self.evictions += 1
    
    def stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return f"Hit: {hit_rate:.1f}% | Evict: {self.evictions}"
