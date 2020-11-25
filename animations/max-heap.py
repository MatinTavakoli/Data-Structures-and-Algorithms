from manimlib.imports import *
import math


class MaxHeap:

    def __init__(self, arr, x, y, hspace=1, vspace=-1, scaling_factor=0.3, node_color=RED):
        self.arr = arr
        self.x = x
        self.y = y
        self.size = len(self.arr)

        self.hspace = hspace
        self.vspace = vspace
        self.scaling_factor = scaling_factor
        self.node_color = node_color

        self.nodes = VGroup()
        self.keys = VGroup()

    def swap(self, i, j):
        tmp = self.arr[i]
        self.arr[i] = self.arr[j]
        self.arr[j] = tmp

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
        self.arr.append(key)
        self.size = self.size + 1
        child_index = self.size - 1
        parent_index = self.parent(child_index)
        while self.arr[child_index] > self.arr[parent_index]:
            self.swap(parent_index, child_index)

            child_index = parent_index
            parent_index = self.parent(child_index)

    def pop(self):
        self.arr[0] = self.arr[self.size - 1]
        key = self.arr[self.size - 1]
        self.size = self.size - 1
        self.heapify(0)
        return key

    def delete(self, index):
        self.arr[index] = self.arr[self.size - 1]
        self.arr[self.size - 1] = None
        self.size = self.size - 1
        self.heapify(index)

    def heapify(self, index):
        left = self.left(index)
        right = self.right(index)

        big = None
        if right is not None:
            if self.arr[left] >= self.arr[right]:
                big = left
            else:
                big = right

        elif right is None and left is not None:
            big = left

        else:
            return

        if self.arr[big] > self.arr[index]:
            self.swap(big, index)
            self.heapify(big)

    def build(self):
        for i in range(self.size // 2 - 1, -1, -1):
            self.heapify(i)

    def heap_sort(self):
        size = self.size
        res_arr = []

        for i in range(size):
            key = self.pop()
            self.arr[size - i - 1] = key
            res_arr.append(key)

    def print_heap(self):
        for i in range(self.size):
            print('################')
            print(self.arr[i])
            print(self.nodes[i].get_x(), self.nodes[i].get_y())
            print('################')

    def sketch_heap(self, scene):
        for i in range(len(self.arr)):
            node = Circle()
            key = TextMobject(str(self.arr[i]))
            delta_x = - math.floor(math.log2(i + 1)) * self.hspace + 2 * (
                    i - ((2 ** math.floor(math.log2(i + 1))) - 1)) * self.hspace
            delta_y = math.floor(math.log2(i + 1)) * self.vspace

            print('&&&&&&&&&&&&&&&&&&')
            print(delta_x, delta_y)
            print('&&&&&&&&&&&&&&&&&&')

            node.move_to([self.x + delta_x, self.y + delta_y, 0])
            key.move_to([self.x + delta_x, self.y + delta_y, 0])
            node.scale(self.scaling_factor)
            node.set_color(self.node_color)

            self.nodes.add(node)
            self.keys.add(key)

        scene.play(
            *[Write(node) for node in self.nodes],
            *[Write(key) for key in self.keys],
            run_time=1.5
        )
        # scene.play(*[GrowArrow(e) for e in self.edges], run_time=1.5)


class Intro(Scene):

    def construct(self):
        text = TextMobject("Hello! We are here to fuck!")
        self.play(Write(text))

        self.wait(2)

        # arr = [4, 7, -1, 2, 0, 3, 5]
        arr = [3, 5, 0, 8, 5, -1, -2, 10, 1]
        max_heap = MaxHeap(arr, 2, 2)
        max_heap.build()
        max_heap.sketch_heap(self)
        max_heap.print_heap()
