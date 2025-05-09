"""
Custom data structures for performance optimization in the FarmLore platform.
"""
import re
from typing import Dict, List, Set, Tuple, Optional, Any, Callable
from functools import lru_cache
from threading import Lock
import heapq
import time

class TrieNode:
    """Node in a Trie data structure."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.entity_type = None
        self.value = None

class EntityTrie:
    """Trie data structure for efficient entity extraction."""
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word: str, entity_type: str, value: Any = None) -> None:
        """Insert a word into the trie with its entity type and optional value."""
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.entity_type = entity_type
        node.value = value or word
        
    def search_entities(self, text: str) -> List[Tuple[str, str, int, int]]:
        """
        Search for entities in the text.
        Returns a list of tuples (entity_value, entity_type, start_pos, end_pos)
        """
        results = []
        text_lower = text.lower()
        
        for i in range(len(text_lower)):
            node = self.root
            j = i
            longest_match = None
            longest_end = i
            
            while j < len(text_lower) and text_lower[j] in node.children:
                node = node.children[text_lower[j]]
                j += 1
                
                if node.is_end_of_word:
                    longest_match = node
                    longest_end = j
            
            if longest_match:
                results.append((
                    longest_match.value,
                    longest_match.entity_type,
                    i,
                    longest_end
                ))
                
        return results


class LRUCache:
    """Thread-safe LRU Cache implementation."""
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.lock = Lock()
        self.access_times = {}
        
    def get(self, key: str) -> Any:
        """Get an item from the cache."""
        with self.lock:
            if key in self.cache:
                self.access_times[key] = time.time()
                return self.cache[key]
            return None
        
    def put(self, key: str, value: Any) -> None:
        """Put an item in the cache."""
        with self.lock:
            self.cache[key] = value
            self.access_times[key] = time.time()
            
            if len(self.cache) > self.max_size:
                # Find the least recently used item
                oldest_key = min(self.access_times.items(), key=lambda x: x[1])[0]
                del self.cache[oldest_key]
                del self.access_times[oldest_key]


class SimpleBloomFilter:
    """Simple Bloom filter implementation using hash functions."""
    def __init__(self, size: int = 10000, hash_count: int = 5):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size
        
    def _hash_functions(self, item: str) -> List[int]:
        """Generate hash values for the item."""
        # Simple hash functions
        hashes = []
        for i in range(self.hash_count):
            # Use different seeds for each hash function
            hash_val = hash(f"{item}_{i}") % self.size
            hashes.append(hash_val)
        return hashes
        
    def add(self, item: str) -> None:
        """Add an item to the Bloom filter."""
        for hash_index in self._hash_functions(item):
            self.bit_array[hash_index] = 1
            
    def might_contain(self, item: str) -> bool:
        """Check if an item might be in the set."""
        for hash_index in self._hash_functions(item):
            if self.bit_array[hash_index] == 0:
                return False
        return True


class PriorityQueue:
    """Priority queue implementation for query processing."""
    def __init__(self):
        self.queue = []
        self.counter = 0
        self.lock = Lock()
        
    def add_query(self, query: Any, priority: int) -> None:
        """Add a query to the queue with a priority."""
        with self.lock:
            heapq.heappush(self.queue, (priority, self.counter, query))
            self.counter += 1
        
    def get_next_query(self) -> Optional[Any]:
        """Get the next query from the queue."""
        with self.lock:
            if self.queue:
                return heapq.heappop(self.queue)[2]
            return None
            
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        with self.lock:
            return len(self.queue) == 0


class InvertedIndex:
    """Inverted index for efficient symptom-based pest identification."""
    def __init__(self):
        self.index = {}  # symptom -> list of pests
        
    def add_item(self, key: str, value: str) -> None:
        """Add an item to the index."""
        if key not in self.index:
            self.index[key] = set()
        self.index[key].add(value)
        
    def get_values(self, keys: List[str]) -> Set[str]:
        """Get values that match all the given keys."""
        if not keys:
            return set()
        
        # Start with values from the first key
        result = self.index.get(keys[0], set()).copy()
        
        # Intersect with values from other keys
        for key in keys[1:]:
            result &= self.index.get(key, set())
            
        return result
        
    def get_all_values(self) -> Set[str]:
        """Get all values in the index."""
        result = set()
        for values in self.index.values():
            result.update(values)
        return result


class ConcurrentCache:
    """Thread-safe cache for concurrent requests with enhanced performance."""
    def __init__(self, max_size: int = 1000, expiration_seconds: int = 86400):
        self.cache = {}
        self.locks = {}
        self.global_lock = Lock()
        self.max_size = max_size
        self.access_times = {}
        self.creation_times = {}
        self.expiration_seconds = expiration_seconds  # Default 24 hours
        
    def get(self, key: str) -> Any:
        """
        Get an item from the cache.
        Returns None if the key doesn't exist or if the entry has expired.
        """
        with self.global_lock:
            if key not in self.cache:
                return None
                
            # Check if entry has expired
            current_time = time.time()
            if (current_time - self.creation_times[key]) > self.expiration_seconds:
                # Remove expired entry
                self._remove_key(key)
                return None
                
            # Update access time and return value
            self.access_times[key] = current_time
            return self.cache[key]
        
    def put(self, key: str, value: Any) -> None:
        """Put an item in the cache."""
        with self.global_lock:
            current_time = time.time()
            self.cache[key] = value
            self.access_times[key] = current_time
            self.creation_times[key] = current_time
            
            # Check if we need to evict entries
            self._evict_if_needed()
    
    def _evict_if_needed(self) -> None:
        """Evict entries if the cache exceeds maximum size."""
        if len(self.cache) <= self.max_size:
            return
            
        # Calculate how many entries to remove
        num_to_remove = len(self.cache) - self.max_size
        
        # Find the least recently used entries
        sorted_keys = sorted(self.access_times.items(), key=lambda x: x[1])
        keys_to_remove = [k for k, _ in sorted_keys[:num_to_remove]]
        
        # Remove entries
        for key in keys_to_remove:
            self._remove_key(key)
    
    def _remove_key(self, key: str) -> None:
        """Remove a key from all dictionaries."""
        if key in self.cache:
            del self.cache[key]
        if key in self.access_times:
            del self.access_times[key]
        if key in self.creation_times:
            del self.creation_times[key]
            
    def clear_expired(self) -> int:
        """
        Clear all expired entries from the cache.
        Returns the number of entries removed.
        """
        with self.global_lock:
            current_time = time.time()
            expired_keys = [
                key for key, creation_time in self.creation_times.items()
                if (current_time - creation_time) > self.expiration_seconds
            ]
            
            for key in expired_keys:
                self._remove_key(key)
                
            return len(expired_keys)
            
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the cache."""
        with self.global_lock:
            current_time = time.time()
            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "expired_entries": sum(
                    1 for creation_time in self.creation_times.values()
                    if (current_time - creation_time) > self.expiration_seconds
                ),
                "oldest_entry_age": max(
                    current_time - min(self.creation_times.values()) if self.creation_times else 0,
                    0
                ),
                "newest_entry_age": min(
                    current_time - max(self.creation_times.values()) if self.creation_times else 0,
                    0
                ),
            }


class AutocompleteTrie:
    """Prefix tree for auto-completion suggestions."""
    def __init__(self):
        self.root = {}
        self.end_symbol = '*'
        
    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        node = self.root
        for char in word.lower():
            if char not in node:
                node[char] = {}
            node = node[char]
        node[self.end_symbol] = True
        
    def find_prefix(self, prefix: str) -> List[str]:
        """Find all words that start with the given prefix."""
        node = self.root
        for char in prefix.lower():
            if char not in node:
                return []
            node = node[char]
        
        return self._get_all_words(node, prefix.lower())
        
    def _get_all_words(self, node: Dict, prefix: str) -> List[str]:
        """Get all words from a node with the given prefix."""
        results = []
        if self.end_symbol in node:
            results.append(prefix)
            
        for char in node:
            if char != self.end_symbol:
                results.extend(self._get_all_words(node[char], prefix + char))
                
        return results


class SimilarQueryDetector:
    """Simple implementation of similar query detection."""
    def __init__(self, threshold: float = 0.7):
        self.queries = {}  # query_id -> (query, response)
        self.counter = 0
        self.threshold = threshold
        
    def add_query(self, query: str, response: str) -> None:
        """Add a query and its response to the detector."""
        query_id = str(self.counter)
        self.queries[query_id] = (query.lower(), response)
        self.counter += 1
        
    def find_similar_query(self, query: str) -> Optional[Tuple[str, str]]:
        """Find a similar query and its response."""
        query_lower = query.lower()
        tokens = set(self._tokenize(query_lower))
        
        best_match = None
        best_similarity = 0
        
        for _, (stored_query, response) in self.queries.items():
            stored_tokens = set(self._tokenize(stored_query))
            
            # Calculate Jaccard similarity
            if not tokens or not stored_tokens:
                continue
                
            intersection = len(tokens.intersection(stored_tokens))
            union = len(tokens.union(stored_tokens))
            
            if union == 0:
                continue
                
            similarity = intersection / union
            
            if similarity > best_similarity and similarity >= self.threshold:
                best_similarity = similarity
                best_match = (stored_query, response)
                
        return best_match
        
    def _tokenize(self, query: str) -> List[str]:
        """Simple tokenization."""
        return re.findall(r'\b\w+\b', query.lower())
