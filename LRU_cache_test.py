import unittest
from LRU_cache import *


class LRUCacheTest(unittest.TestCase):
    def test_size_1_cache(self):
        cache = LRUCache(1)

        self.assertEqual(cache.get(11), -1)
        cache.put(11, 1)
        self.assertEqual(cache.get(11), 1)

        cache.put(22, 2)
        cache.put(22, 2)
        cache.put(22, 2)
        self.assertEqual(cache.get(11), -1)
        self.assertEqual(cache.get(22), 2)

        cache.put(22, 42)
        self.assertEqual(cache.get(22), 42)

    def test_size_2_cache(self):
        cache = LRUCache(2)

        self.assertEqual(cache.get(11), -1)
        cache.put(11, 1)
        self.assertEqual(cache.get(11), 1)

        cache.put(22, 2)
        cache.put(22, 2)
        cache.put(22, 2)
        self.assertEqual(cache.get(11), 1)
        self.assertEqual(cache.get(22), 2)

        cache.put(11, 1)
        cache.put(11, 6)
        cache.put(11, 1)
        self.assertEqual(cache.get(11), 1)
        self.assertEqual(cache.get(22), 2)

        cache.put(11, 42)
        self.assertEqual(cache.get(11), 42)
        self.assertEqual(cache.get(22), 2)

        cache.put(33, 3)
        cache.put(33, 3)
        cache.put(33, 3)
        self.assertEqual(cache.get(11), -1)
        self.assertEqual(cache.get(22), 2)
        self.assertEqual(cache.get(33), 3)

        cache.get(22)
        cache.put(44, 4)

        self.assertEqual(cache.get(22), 2)
        self.assertEqual(cache.get(33), -1)
        self.assertEqual(cache.get(44), 4)

    def test_size_3_cache(self):
        cache = LRUCache(3)

        self.assertEqual(cache.get(11), -1)
        cache.put(11, 1)
        self.assertEqual(cache.get(11), 1)

        cache.put(22, 2)
        cache.put(22, 2)
        cache.put(22, 2)
        self.assertEqual(cache.get(11), 1)
        self.assertEqual(cache.get(22), 2)

        cache.put(11, 1)
        cache.put(11, 6)
        cache.put(11, 1)
        self.assertEqual(cache.get(11), 1)
        self.assertEqual(cache.get(22), 2)

        cache.put(11, 42)
        self.assertEqual(cache.get(11), 42)
        self.assertEqual(cache.get(22), 2)

        cache.put(33, 3)
        cache.put(33, 3)
        cache.put(33, 3)
        self.assertEqual(cache.get(11), 42)
        self.assertEqual(cache.get(22), 2)
        self.assertEqual(cache.get(33), 3)

        cache.put(44, 4)
        cache.put(44, 4)
        cache.put(44, 4)
        self.assertEqual(cache.get(11), -1)
        self.assertEqual(cache.get(22), 2)
        self.assertEqual(cache.get(33), 3)
        self.assertEqual(cache.get(44), 4)

        cache.put(55, 5)
        self.assertEqual(cache.get(11), -1)
        self.assertEqual(cache.get(22), -1)
        self.assertEqual(cache.get(33), 3)
        self.assertEqual(cache.get(44), 4)
        self.assertEqual(cache.get(55), 5)

        cache.put(22, 666)
        cache.put(222, 777)
        cache.put(2222, 888)
        self.assertEqual(cache.get(55), -1)
        self.assertEqual(cache.get(22), 666)
        self.assertEqual(cache.get(222), 777)
        self.assertEqual(cache.get(2222), 888)

        cache.get(22)
        cache.put(55, 5)
        cache.put(66, 6)

        self.assertEqual(cache.get(22), 666)
        self.assertEqual(cache.get(222), -1)
        self.assertEqual(cache.get(2222), -1)
        self.assertEqual(cache.get(55), 5)
        self.assertEqual(cache.get(66), 6)


if __name__ == '__main__':
    unittest.main()
