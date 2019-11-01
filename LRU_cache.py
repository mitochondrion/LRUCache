def validated(func):
    def wrapped(*args, **kwargs):
        self = args[0]
        self.validate()
        print('🔥🔥🔥 {}{}'.format(func.__name__, args[1:]))
        result = func(*args, **kwargs)
        self.validate()
        return result

    return wrapped

class LRUCache:
    class __CacheItem:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.next_newest_item: LRUCache.__CacheItem = None
            self.next_oldest_item: LRUCache.__CacheItem = None

        def is_oldest(self) -> bool:
            return self.next_oldest_item == None

        def is_newest(self) -> bool:
            return self.next_newest_item == None

        def __repr__(self):
            older = self.next_oldest_item.dump() if self.next_oldest_item else 'NULL'
            newer = self.next_newest_item.dump() if self.next_newest_item else 'NULL'
            return '{} < {} > {}'.format(older, self.dump(), newer)

        def dump(self):
            return '({}, {})'.format(self.key, self.value)

    def __init__(self, capacity: int):
        self.__capacity = capacity
        self.__item_count = 0
        self.__cache = {}
        self.__oldest_item: LRUCache.__CacheItem = None
        self.__newest_item: LRUCache.__CacheItem = None

    def validate(self) -> bool:
        self.__dump()

        if self.__item_count is 0: return True

        item_set = set()

        item = self.__oldest_item
        item_set.add(item)
        assert item.next_oldest_item is None
        assert item.is_oldest()

        while True:
            if item.is_newest():
                assert item.next_newest_item is None
                assert self.__newest_item is item
                break
            item.next_newest_item.next_oldest_item is item
            item = item.next_newest_item
            assert item not in item_set
            item_set.add(item)

        for item in item_set:
            assert item.key in self.__cache

        for value in self.__cache.values():
            assert value in item_set

        assert self.__item_count <= self.__capacity
        assert self.__item_count is len(item_set) is len(self.__cache)

        return True

    def __dump(self):
        print('==========')
        print('ITEM COUNT: {}/{}'.format(self.__item_count, self.__capacity))
        print('OLDEST: {}'.format(self.__oldest_item))
        print('NEWEST: {}'.format(self.__newest_item))
        print('CACHE:')
        print(self.__cache)
        print('QUEUE:')
        item = self.__oldest_item
        if item:
            while (not item.is_newest()):
                print(item)
                item = item.next_newest_item
            print(item)
        print('==========')

    @validated
    def get(self, key: int) -> int:
        if self.__capacity is 0: return -1

        if key in self.__cache:
            item = self.__cache[key]
            self.__renew_item(item)
            return item.value
        else:
            return -1

    @validated
    def put(self, key: int, value: int) -> None:
        if self.__capacity is 0: return

        if key in self.__cache:
            # Handle existing key
            item = self.__cache[key]
            item.value = value
            self.__renew_item(item)
        else:
            # Handle new key
            item = LRUCache.__CacheItem(key, value)
            self.__cache[key] = item

            if self.__item_count is 0:
                self.__oldest_item = item
                self.__newest_item = item
                self.__item_count += 1
            else:
                # Put new item at front of queue
                self.__newest_item.next_newest_item = item
                item.next_oldest_item = self.__newest_item
                self.__newest_item = item

                if not self.__capacity_reached():
                    self.__item_count += 1
                else:
                    # Eject oldest item from queue
                    self.__cache.pop(self.__oldest_item.key, None)
                    self.__oldest_item = self.__oldest_item.next_newest_item
                    self.__oldest_item.next_oldest_item = None

    def __capacity_reached(self) -> bool:
        return self.__item_count >= self.__capacity

    def __renew_item(self, item: __CacheItem) -> None:
        if item.is_newest():
            return

        # Remove item from queue
        if item.is_oldest():
            self.__oldest_item = item.next_newest_item
            self.__oldest_item.next_oldest_item = None
        else:
            item.next_oldest_item.next_newest_item = item.next_newest_item
            item.next_newest_item.next_oldest_item = item.next_oldest_item

        # Put item at front of queue
        item.next_newest_item = None
        item.next_oldest_item = self.__newest_item
        self.__newest_item.next_newest_item = item
        self.__newest_item = item
