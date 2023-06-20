# Name: Kristin Eberman
# OSU Email: ebermank@oregonstate.edu
# Course: CS261 - Data Structures (section 404)
# Assignment: 6 - HashMap Implementation - Chaining
# Due Date: December 2, 2022
# Description: This assignment implements 10 methods within the HashMap class
#       using a DynamicArray to store the hash table and chaining of singly
#       linked lists for collision resolution


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds or updates a key/value pair in the hash map
        :param key: Unique key associated with value
        :param value: Value associated with key
        :return: None
        """
        # Resize the array if load factor >= 1
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # Use hash function to generate hash value and associated index
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Iterate through the Linked List stored at relevant index
        for _ in self._buckets[index]:
            # If the given key already exists, replace its value
            if _.key == key:
                _.value = value
                return

        # If key does not yet exist, insert new key/value pair & update size
        self._buckets[index].insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        :return: Integer value that represents number of empty buckets
        """
        # Initialize empty bucket value to 0
        empty_buckets = 0

        # Iterate over the dynamic array
        for i in range(self._capacity):
            # If bucket's length is 0, it is empty -> increment empty_buckets
            if self._buckets[i].length() == 0:
                empty_buckets += 1
        return empty_buckets

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        :return: Number of elements (size) / number of buckets (capacity)
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the HashMap without changing its capacity
        :return: None
        """
        # Override _buckets with empty DynamicArray of LinkedLists
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # Reset size to 0
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of the hash table; rehashes all key/value pairs
        :param new_capacity: New value for capacity of underlying array
        :return: None
        """
        # If the new_capacity < 1, don't resize
        if new_capacity < 1:
            return

        # Initialize HashMap with new capacity
        resized_hash = HashMap(new_capacity, self._hash_function)

        # Re-set capacity to 2 if it's skipped when building resized_hash
        if new_capacity == 2:
            resized_hash._buckets.pop()
            resized_hash._capacity -= 1

        # Iterate all elements in the original array and put in resized_hash
        for i in range(self._capacity):
            for _ in self._buckets[i]:
                resized_hash.put(_.key, _.value)

        # Update/re-point the original buckets and capacity variables
        self._capacity = resized_hash._capacity
        self._buckets = resized_hash._buckets

    def get(self, key: str) -> object:
        """
        Returns the value associated with a given key
        :param key: Key to search for in the HashMap
        :return: Value of given key if it exists, otherwise None
        """
        # Use hash function to find index of key
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Iterate over the LinkedList stored at relevant index
        for _ in self._buckets[index]:
            # Return value if the key is found
            if _.key == key:
                return _.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Searches for a given key within the HashMap
        :param key: Key to search for
        :return: True if the key is found, otherwise False
        """
        if self.get(key) is None:
            return False
        return True

    def remove(self, key: str) -> None:
        """
        Removes key/value pair if key exists in the HashMap
        :param key: Key to search for and remove
        :return: None
        """
        # Use hash function to find index of key
        hash = self._hash_function(key)
        index = hash % self._capacity

        # Iterate over the LinkedList stored at relevant index
        for _ in self._buckets[index]:
            # If the key exists, remove the key/value pair and decrement size
            if _.key == key:
                self._buckets[index].remove(key)
                self._size -= 1
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Creates a dynamic array that contains tuples of all key/value pairs
        stored in the HashMap
        :return: Dynamic array of key/value tuples
        """
        # Initialize an empty dynamic array to fill with tuples
        key_value_arr = DynamicArray()

        # Iterate over the HashMap to append each key/value tuple to the array
        for i in range(self._capacity):
            for _ in self._buckets[i]:
                key_value_arr.append((_.key, _.value))
        return key_value_arr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the most occurring value(s) (mode) in a given dynamic array and
    how many times the mode value(s) appear
    :param da: Dynamic array to find the mode value(s)
    :return: Tuple containing a dynamic array with the mode value/s of the
    array and an integer that represents the highest frequency
    """
    # Initialize variables to return
    mode_arr = DynamicArray()
    highest_frequency = 0

    # Set up HashMap functionality
    map = HashMap()

    # Iterate over the dynamic array
    for i in range(da.length()):
        # Set DA element (key)'s value to how many times it's in the HashMap
        value = map.get(da[i])
        value = 1 if not value else value + 1

        # Insert the key/value pair into the HashMap
        map.put(da[i], value)

        # Update highest_frequency and reset mode_arr if necessary
        if value > highest_frequency:
            highest_frequency = value
            mode_arr = DynamicArray()

        # If key is one of the mode values, append it to the mode_arr
        if value == highest_frequency:
            mode_arr.append(da[i])

    return mode_arr, highest_frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
