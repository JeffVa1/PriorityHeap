from typing import List, Tuple, Any
"""
Author - Jeffrey Valentic
11/17/2020
"""


class Node:
    __slots__ = ['key', 'value']

    def __init__(self, k: Any, v: Any):
        """
        Initializes node
        :param k: key to be stored in the node
        :param v: value to be stored in the node
        """
        self.key = k
        self.value = v

    def __lt__(self, other):
        """
        Less than comparator
        :param other: second node to be compared to
        :return: True if the node is less than other, False if otherwise
        """
        return self.key < other.key or (self.key == other.key and self.value < other.value)

    def __gt__(self, other):
        """
        Greater than comparator
        :param other: second node to be compared to
        :return: True if the node is greater than other, False if otherwise
        """
        return self.key > other.key or (self.key == other.key and self.value > other.value)

    def __eq__(self, other):
        """
        Equality comparator
        :param other: second node to be compared to
        :return: True if the nodes are equal, False if otherwise
        """
        return self.key == other.key and self.value == other.value

    def __str__(self):
        """
        Converts node to a string
        :return: string representation of node
        """
        return '({0}, {1})'.format(self.key, self.value)

    __repr__ = __str__


class PriorityQueue:
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = []

    def __str__(self) -> str:
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data)

    __repr__ = __str__

    def to_tree_format_string(self) -> str:
        """
        Prints heap in Breadth First Ordering Format
        :return: String to print
        """
        string = ""
        # level spacing - init
        nodes_on_level = 0
        level_limit = 1
        spaces = 10 * int(1 + len(self))

        for i in range(len(self)):
            space = spaces // level_limit
            # determine spacing

            # add node to str and add spacing
            string += str(self.data[i]).center(space, ' ')

            # check if moving to next level
            nodes_on_level += 1
            if nodes_on_level == level_limit:
                string += '\n'
                level_limit *= 2
                nodes_on_level = 0
            i += 1

        return string

    def __getitem__(self, index: int) -> Node:
        """Shorthand for self.data[index]

        Args:
            index (int): the index to get

        Returns:
            Node: the node at that index
        """
        return self.data[index]

    def __setitem__(self, index: int, new_val: Node) -> None:
        """Shorthand for self.data[index] = new_val

        Args:
            index (int): the index to set at
            new_val (Node): the new value to set
        """
        self.data[index] = new_val

    def __len__(self) -> int:
        """
        Returns the length of a heap.
        return: int, the length of a heap.
        """
        return len(self.data)

    def empty(self) -> bool:
        """
        Checks if the heap is empty or contains elements
        return: True if heap has no elements, false if it does.
        """
        if len(self.data) == 0:
            return True
        return False

    def top(self) -> Node:
        """
        Finds and returns the first node in a heap
        return: Node that is the root of a heap.
        """
        if self.empty():
            return None

        return self[0]

    def get_left_child_index(self, index: int) -> int:
        """
        Returns the location of the left child of node at location index
        param index: the location of the node whose left child needs to be found
        return: the index of the left child of node at location index
        """
        child_ind = 2 * index + 1
        if len(self.data) <= child_ind:
            return None
        else:
            return child_ind

    def get_right_child_index(self, index: int) -> int:
        """
        Returns the location of the right child of node at location index
        param index: the location of the node whose right child needs to be found
        return: the index of the right child of node at location index
        """
        child_ind = 2 * index + 2
        if len(self.data) <= child_ind:
            return None
        else:
            return child_ind

    def get_parent_index(self, index: int) -> int:
        """
        Returns the location of the parent node to the node at location index.
        param index: the location of the node whose parent needs to be found
        return: the index of the found parent.
        """
        if index == 0:
            return None

        return (index - 1) // 2

    def push(self, key: Any, val: Any) -> None:
        """
        Inserts a node into the correct position in a heap
        param key: the key (priority) of the item to be inserted
        param val: the value of the item to be inserted
        return: none
        """
        new_node = Node(key, val)
        self.data.append(new_node)
        self.percolate_up(len(self.data)-1)
        return None

    def pop(self) -> Node:
        """
        Removes and returns the last node in a heap.
        return: Node, the last item in the heap.
        """
        if len(self.data) > 0:

            k, v = self[0].key, self[0].value
            self[0], self[-1] = self[-1], self[0]

            pop_val = self.data.pop()

            self.percolate_down(0)

            return pop_val

        return None

    def get_min_child_index(self, index: int) -> int:
        """
        Finds the minimum child of the node at position index
        param index: the location of the item whose children need to be checked.
        return: index of the child with minimum value
        """
        l_child = self.get_left_child_index(index)
        r_child = self.get_right_child_index(index)

        if l_child is None and r_child is None:
            return None

        if l_child is None:
            return r_child

        if r_child is None:
            return l_child

        if self[l_child] < self[r_child]:
            return l_child

        return r_child

    def percolate_up(self, index: int) -> None:
        """
        Moves the item at index up in the heap until it reaches the proper location
        param index: the location of the item to be moved.
        return: none
        """
        if index != 0:
            par_ind = self.get_parent_index(index)
            if self[index] < self[par_ind]:
                self[index], self[par_ind] = self[par_ind], self[index]
                self.percolate_up(par_ind)
            else:
                return None

    def percolate_down(self, index: int) -> None:
        """
        Moves the item at index down in the heap until it reaches the proper location
        param index: the location of the item to be moved.
        return: none
        """
        if index != len(self.data):
            min_ind = self.get_min_child_index(index)

            if min_ind is not None and self[index] > self[min_ind]:
                self[index], self[min_ind] = self[min_ind], self[index]
                self.percolate_down(min_ind)

        return None


class MaxHeap:
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = PriorityQueue()

    def __str__(self):
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data.data)

    def __len__(self):
        """
        Length override function
        :return: Length of the data inside the heap
        """
        return len(self.data)

    def print_tree_format(self):
        """
        Prints heap in bfs format
        """
        self.data.tree_format()


    def empty(self) -> bool:
        """
        Checks if the heap is empty or contains elements
        return: True if heap has no elements, false if it does.
        """
        if len(self.data.data) == 0:
            return True

        return False

    def top(self) -> int:
        """
        returns the value of the first item in the heap.
        """
        if self.empty():
            return None

        return self.data.data[0].value

    def push(self, key: int) -> None:
        """
        Inserts an item to the heap with high to low order
        param key: the value to be inserted to the heap.
        return: none
        """
        self.data.push(-1*key, key)
        return None

    def pop(self) -> int:
        """
        returns and removes the largest item in the heap
        """
        return self.data.pop().value


def heap_sort(array):
    """
    Sorts an array from least to greatest
    param array: the array of data to sort
    return: the sorted array
    """
    max_heap = MaxHeap()
    for i in range(len(array)):
        val = array[i]
        max_heap.push(val)

    ind = len(max_heap) - 1
    while not max_heap.empty():
        array[ind] = max_heap.pop()
        ind -= 1

    return array


def find_ranking(rank, results: List[Tuple[int, str]]) -> str:
    """
    Finds the item in results that is at the rank location
    param rank: The order of the item to return
    param results: The list of total results to search through
    return: the value in results at location rank
    """
    pq = PriorityQueue()

    for i in results:
        pq.push(i[0], i[1])

    for x in range(rank):
        final_result = pq.pop()

    if final_result is not None:
        return final_result.value
    return None
