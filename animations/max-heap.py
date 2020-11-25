from manimlib.imports import *
import math


class Node:
    def __init__(self, index, key, x, y, scaling_factor=0.3, node_color=RED):
        self.key = key
        self.index = index

        self.node_obj = Circle()
        self.node_obj.move_to([x, y, 0])
        self.node_obj.scale(scaling_factor)
        self.node_obj.set_color(node_color)
        self.key_obj = TextMobject(str(key))
        self.key_obj.move_to([x, y, 0])


class MaxHeap:

    def __init__(self, arr, x, y, hspace=4, vspace=-1, scaling_factor=0.3, node_color=RED):

        self.x = x
        self.y = y
        self.size = len(arr)
        if self.size != 0:
            self.height = math.floor(math.log2(self.size))
        else:
            self.height = 0

        self.hspace = hspace
        self.vspace = vspace
        self.scaling_factor = scaling_factor
        self.node_color = node_color

        self.nodes = VGroup()
        self.edges = VGroup()

        self.arr = []

        for i, key in enumerate(arr):

            if i == 0:
                node = Node(i, key, self.x, self.y)
                self.nodes.add(node)

            else:

                node_height = math.floor(math.log2(i + 1))
                delta_x = 0.5 ** node_height * hspace
                node_parent = self.arr[self.parent(i)]

                if self.left(node_parent.index) == i:
                    delta_x *= -1

                delta_y = self.vspace

                node = Node(i, key, node_parent.node_obj.get_x() + delta_x, node_parent.node_obj.get_y() + delta_y)
                self.nodes.add(node)

                edge = Arrow([node_parent.node_obj.get_x(), node_parent.node_obj.get_y(), 0],
                             [node.node_obj.get_x(), node.node_obj.get_y(), 0])
                edge.scale(0.93)
                self.edges.add(edge)

            self.arr.append(node)

    def swap_nodes(self, i, j):
        tmp = self.arr[i]
        self.arr[i] = self.arr[j]
        self.arr[j] = tmp

        child_x = self.arr[i].node_obj.get_x()
        child_y = self.arr[i].node_obj.get_y()

        self.arr[i].node_obj.set_x(self.arr[j].node_obj.get_x())
        self.arr[i].node_obj.set_y(self.arr[j].node_obj.get_y())
        self.arr[i].key_obj.set_x(self.arr[j].key_obj.get_x())
        self.arr[i].key_obj.set_y(self.arr[j].key_obj.get_y())

        self.arr[j].node_obj.set_x(child_x)
        self.arr[j].node_obj.set_y(child_y)
        self.arr[j].key_obj.set_x(child_x)
        self.arr[j].key_obj.set_y(child_y)

    def parent(self, index):
        return (index - 1) // 2

    def left(self, index):
        if 2 * index + 1 < self.size:
            return 2 * index + 1
        else:
            return None

    def right(self, index):
        if 2 * index + 1 < self.size:
            return 2 * index + 2
        else:
            return None

    def insert(self, key):

        if self.size == 0:
            node = Node(0, key, self.x, self.y)
            self.nodes.add(node)

        else:
            index = self.size

            node_height = math.floor(math.log2(index + 1))
            delta_x = 0.5 ** node_height * self.hspace
            node_parent = self.parent(index)

            if 2 * node_parent + 1 == index:
                delta_x *= -1

            delta_y = self.vspace

            node = Node(index, key, self.arr[node_parent].node_obj.get_x() + delta_x,
                        self.arr[node_parent].node_obj.get_y() + delta_y)
            self.nodes.add(node)

            edge = Arrow([self.arr[node_parent].node_obj.get_x(), self.arr[node_parent].node_obj.get_y(), 0],
                         [node.node_obj.get_x(), node.node_obj.get_y(), 0])
            edge.scale(0.93)
            self.edges.add(edge)


        self.arr.append(node)

        self.size = self.size + 1
        self.height = math.floor(math.log2(self.size))
        child_index = self.size - 1
        if child_index != 0:
            parent_index = self.parent(child_index)
            while self.arr[child_index].key > self.arr[parent_index].key:
                self.swap_nodes(parent_index, child_index)
                child_index = parent_index
                if child_index == 0:
                    break
                parent_index = self.parent(child_index)

    def pop(self):
        node = self.arr[0]
        self.arr[0] = self.arr[self.size - 1]
        self.size = self.size - 1
        self.height = math.floor(math.log2(self.size))
        self.heapify(0)
        return node

    def delete(self, index):
        node = self.arr[index]
        self.arr[index] = self.arr[self.size - 1]
        self.size = self.size - 1
        self.height = math.floor(math.log2(self.size))
        self.heapify(index)
        return node

    def heapify(self, index):
        left = self.left(index)
        right = self.right(index)

        big = None
        if right is not None:
            if self.arr[left].key >= self.arr[right].key:
                big = left
            else:
                big = right

        elif right is None and left is not None:
            big = left

        else:
            return

        if self.arr[big].key > self.arr[index].key:
            self.swap_nodes(big, index)
            self.heapify(big)

    def build(self):
        for i in range(self.size // 2 - 1, -1, -1):
            self.heapify(i)

    def heap_sort(self):
        size = self.size
        res_arr = []

        for i in range(size):
            node = self.pop()
            self.arr[size - i - 1] = node
            res_arr.append(node.key)

    def print_heap(self):
        for i in range(self.size):
            print(self.arr[i].key)

    def sketch_heap(self, scene):
        scene.play(
            *[Write(node.node_obj) for node in self.nodes],
            *[Write(node.key_obj) for node in self.nodes],
            run_time=1.5
        )
        scene.play(*[GrowArrow(e) for e in self.edges], run_time=1.5)


class Intro(Scene):

    def construct(self):
        # arr = [4, 7, -1, 2, 0, 3, 5]
        # arr = [3, 5, 0, 8, 5, -1, -2, 10, 1]
        max_heap = MaxHeap([], 2.5, 2)
        arr = [10, 8, 0, 5, 5, -1, -2, 3, 1, 2, 4, -3, -1, -4, -6]
        # max_heap.build()
        for key in arr:
            max_heap.insert(key)
        # max_heap.insert(9)
        # max_heap.insert(10)
        max_heap.insert(12)
        max_heap.sketch_heap(self)
        max_heap.print_heap()

        self.wait(2)
