from manimlib.imports import *
import math


class Node:
    def __init__(self, index, key, x, y, scaling_factor=0.3, node_color=TEAL_E):
        self.key = key
        self.index = index

        self.left_edge = None
        self.right_edge = None

        self.node_obj = Circle()
        self.node_obj.move_to([x, y, 0])
        self.node_obj.scale(scaling_factor)
        self.node_obj.set_color(node_color)

        self.key_obj = TextMobject(str(key))
        self.key_obj.move_to([x, y, 0])

        # TODO this shit must be set and updated in heap operations
        self.index_obj = TextMobject(str(index))
        self.index_obj.set_color(RED)
        self.index_obj.move_to([x, y, 0])
        self.index_obj.scale(0.7)
        self.index_obj.shift([-0.5, 0, 0])
        


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
                node = None
                node = Node(i, key, node_parent.node_obj.get_x() + delta_x, node_parent.node_obj.get_y() + delta_y)
                
                self.nodes.add(node)

                edge = Arrow([node_parent.node_obj.get_x(), node_parent.node_obj.get_y(), 0],
                             [node.node_obj.get_x(), node.node_obj.get_y(), 0])
                edge.scale(0.93)
                if self.left(node_parent.index) == i:
                    node_parent.left_edge = edge
                else:
                    node_parent.right_edge = edge

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

        i_left = self.arr[i].left_edge
        i_right = self.arr[i].right_edge

        self.arr[i].left_edge = self.arr[j].left_edge
        self.arr[i].right_edge = self.arr[j].right_edge

        self.arr[j].left_edge = i_left
        self.arr[j].right_edge = i_right

    def parent(self, index):
        return (index - 1) // 2

    def left(self, index):
        if 2 * index + 1 < self.size:
            return 2 * index + 1
        else:
            return None

    def right(self, index):
        if 2 * index + 2 < self.size:
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
            if self.left(node_parent.index) == i:
                node_parent.left_edge = edge
            else:
                node_parent.right_edge = edge

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
        return self.delete(0)

    def delete(self, index):

        node_parent = self.parent(self.size - 1)
        if self.left(node_parent) == self.size - 1:
            self.edges.remove(self.arr[node_parent].left_edge)
            self.arr[node_parent].left_edge = None
        else:
            self.edges.remove(self.arr[node_parent].right_edge)
            self.arr[node_parent].right_edge = None

        self.swap_nodes(index, self.size - 1)
        node = self.arr[self.size - 1]
        self.nodes.remove(node)

        self.size = self.size - 1
        if self.size != 0:
            self.height = math.floor(math.log2(self.size))
        else:
            self.height = 0
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
            # self.arr[size - i - 1] = node
            res_arr.append(node.key)

        return res_arr

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

    # def add_heap(self, scene):
    #     scene.add()
    #     scene.add(
    #         *[Write(node.node_obj) for node in self.nodes],
    #         *[Write(node.key_obj) for node in self.nodes],
    #         *[GrowArrow(e) for e in self.edges]
    #     )

    def clear_heap(self, scene):
        scene.remove(
            *[node.node_obj for node in self.nodes],
            *[node.key_obj for node in self.nodes],
            *[e for e in self.edges]
        )

    def blur_heap(self, scene, *skip_list):
        blur_list = []
        for node in self.nodes:
            if node not in skip_list:
                blur_list.append(node.node_obj.set_opacity)
                blur_list.append(0.4)
                blur_list.append(node.node_obj.set_fill)
                blur_list.append(RED)
                blur_list.append(0)
                blur_list.append(node.key_obj.set_opacity)
                blur_list.append(0.4)
                blur_list.append(node.index_obj.set_opacity)
                blur_list.append(0.4)
        for edge in self.edges:
            if edge not in skip_list:
                blur_list.append(edge.set_opacity)
                blur_list.append(0.4)

        scene.play(
            *[b for b in blur_list],
        )	


class Intro(Scene):

    def construct(self):

        # part 1: heap invariant

        # title
        title = TextMobject("Binary Max Heap:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)
        self.play(Write(title))

        # arr = [4, 7, -1, 2, 0, 3, 5, 1]
        arr = [7, 4, 5, 2, 0, 3, -1, 1]
        # arr = [3, 5, 0, 8, 5, -1, -2, 10, 1]
        # arr = [10, 8, 0, 5, 5, -1, -2, 3, 1, 2, 4, -3, -1, -4, -6]
        # arr = [-4, 3, 0, 1, 2, -1, -2, -6, -3, -1]
        max_heap = MaxHeap(arr, 3.8, 3, hspace=3, node_color=TEAL_E)
        # max_heap.build()
        max_heap.sketch_heap(self)

        # part 1: definition
        def_1 = TextMobject("A Binary Max Heap is a data structure")
        def_2 = TextMobject("which follows an", " invariant/rule:")
        def_3 = TextMobject("\"Each node must be greater than")
        def_4 = TextMobject("or equal to its children.\"")
        def_1.set_color(GOLD_B)
        def_2[0].set_color(GOLD_B)
        def_2[1].set_color(RED)
        def_3.set_color(MAROON_D)
        def_4.set_color(MAROON_D)
        def_1.scale(0.85)
        def_2.scale(0.85)
        def_3.scale(0.85)
        def_4.scale(0.85)
        def_1.to_edge(LEFT, 0.5)
        def_2.to_edge(LEFT, 0.5)
        def_3.to_edge(LEFT, 0.5)
        def_4.to_edge(LEFT, 0.5)
        def_1.shift([0, 1.7, 0])
        def_2.shift([0, 1.25, 0])
        def_3.shift([0, 0.6, 0])
        def_4.shift([0, 0.15, 0])
        self.play(Write(def_1))
        self.play(Write(def_2))
        self.play(Write(def_3))
        self.play(Write(def_4))
        self.wait(0.5)

        self.play(FadeOut(def_1), FadeOut(def_2), FadeOut(def_3), FadeOut(def_4), run_time=1.5)

        # part 2: implementation
        def_1 = TextMobject("A Binary Max Heap can be implemented")
        def_2 = TextMobject("using a simple array.")
        def_3 = TextMobject("We traverse through the heap, line by")
        def_4 = TextMobject("line, and store the values in the array.")
        def_1.set_color(GOLD_B)
        def_2.set_color(GOLD_B)
        def_3.set_color(GOLD_B)
        def_4.set_color(GOLD_B)
        def_1.scale(0.85)
        def_2.scale(0.85)
        def_3.scale(0.85)
        def_4.scale(0.85)
        def_1.to_edge(LEFT, 0.5)
        def_2.to_edge(LEFT, 0.5)
        def_3.to_edge(LEFT, 0.5)
        def_4.to_edge(LEFT, 0.5)
        def_1.shift([0, 1.7, 0])
        def_2.shift([0, 1.25, 0])
        def_3.shift([0, 0.6, 0])
        def_4.shift([0, 0.15, 0])
        self.play(Write(def_1))
        self.play(Write(def_2))
        self.play(Write(def_3))
        self.play(Write(def_4))
        self.wait(0.5)

        # result array
        heap_arr = Polygon([-3.5, -2.3, 0], [4.5, -2.3, 0], [4.5, -1.3, 0], [-3.5, -1.3, 0])
        heap_arr.set_color(WHITE)
        self.play(Write(heap_arr))

        arr_lines = VGroup()
        for i in range(1, 8):
            line = Line([-3.5 + i, -1.3, 0], [-3.5 + i, -2.3, 0])
            arr_lines.add(line)
            self.play(Write(line), rate_func=smooth, run_time=0.2)

        res_text = TextMobject("\\textrm{values}")
        res_text.move_to([-4.5, -1.8, 0])
        self.play(Write(res_text))

        rect = SurroundingRectangle(max_heap.arr[0].node_obj, buff=0.06, color=YELLOW)

        values = VMobject()

        for i, node in enumerate(max_heap.arr):
            if i != 0:
                new_rect = SurroundingRectangle(node.node_obj, buff=0.06, color=YELLOW)
                self.play(Transform(rect, new_rect))
            else:
                self.play(Write(rect))
            self.wait(0.4)
            val = TextMobject(str(node.key))
            val.set_color(PURPLE)
            val.move_to([-3 + i, -1.8, 0])
            self.play(TransformFromCopy(node.key_obj, val))
            values.add(val)

        self.play(FadeOut(def_1), FadeOut(def_2), FadeOut(def_3), FadeOut(def_4), FadeOut(rect))

        # part 3: pointers

        def_0 = TextMobject("But how can we find a node's parent")
        def_1 = TextMobject("and children?", " Suppose a node is in index", " i")
        def_21 = TextMobject("of the array.", " Then we can access its parent")
        def_22 = TextMobject("and children using the following formulas:")
        def_3 = TextMobject("left(", "i", ") = 2 * ", "i", " + 1")
        def_4 = TextMobject("right(", "i", ") =  2 * ", "i", " + 2")
        def_5 = TextMobject("parent(", "i", ") = [(", "i", " - 1) / 2]")

        def_0.set_color(GOLD_B)
        def_1[0].set_color(GOLD_B)
        def_1[1].set_color(GOLD)
        def_1[2].set_color(MAROON_D)
        def_21.set_color(GOLD_B)
        def_22.set_color(GOLD_B)
        def_3.set_color(MAROON_D)
        def_4.set_color(MAROON_D)
        def_5.set_color(MAROON_D)

        def_0.scale(0.75)
        def_1.scale(0.75)
        def_21.scale(0.75)
        def_22.scale(0.75)
        def_3.scale(0.75)
        def_4.scale(0.75)
        def_5.scale(0.75)

        def_0.to_edge(LEFT, 0.5)
        def_1.to_edge(LEFT, 0.5)
        def_21.to_edge(LEFT, 0.5)
        def_22.to_edge(LEFT, 0.5)
        def_3.to_edge(LEFT, 0.5)
        def_4.to_edge(LEFT, 0.5)
        def_5.to_edge(LEFT, 0.5)

        def_0.shift([0, 2.2, 0])
        def_1.shift([0, 1.75, 0])
        def_21.shift([0, 1.3, 0])
        def_22.shift([0, 0.85, 0])
        def_3.shift([0, 0.25, 0])
        def_4.shift([0, -0.2, 0])
        def_5.shift([0, -0.65, 0])

        self.play(Write(def_0))
        self.play(Write(def_1[0]))
        self.wait(1)
        self.play(Write(def_1[1]))
        self.play(Write(def_1[2]))
        self.play(Write(def_21[0]))
        self.wait(0.6)
        self.play(Write(def_21[1]))
        self.play(Write(def_22))
        self.play(Write(def_3))
        self.play(Write(def_4))
        self.play(Write(def_5))

        self.wait(0.5)

        # fade instructions. draw rectangle
        self.play(FadeOut(def_0), FadeOut(def_1), FadeOut(def_21), FadeOut(def_22))
        self.play(def_3.shift, [0, 1, 0], def_4.shift, [0, 1, 0], def_5.shift, [0, 1, 0], run_time=1.5)

        formulas = VGroup()
        formulas.add(def_3)
        formulas.add(def_4)
        formulas.add(def_5)
        formulas_rect = SurroundingRectangle(formulas, buff=0.16, color=ORANGE)
        self.play(Write(formulas_rect))
        self.wait(0.7)

        res_text = TextMobject("\\textrm{indices}")
        res_text.move_to([-4.5, -2.8, 0])
        self.play(Write(res_text))

        indices = VGroup()
        for i, value in enumerate(values):
            val = TextMobject(str(i))
            indices.add(val)
            val.set_color(RED)
            val.move_to([-3 + i, -2.8, 0])
            self.play(TransformFromCopy(value, val), run_time=0.3)

        self.wait(0.5)

        for i, index in enumerate(indices):
            self.play(TransformFromCopy(index, max_heap.arr[i].index_obj), run_time=0.3)

        question = TextMobject("Let's look at index '", "1", "'")
        question.set_color(BLUE)
        question.scale(0.75)
        question.to_edge(LEFT, 0.5)
        question.shift([0, 2, 0])
        self.play(Write(question))
        self.wait(1)

        max_heap.blur_heap(self, max_heap.arr[1])
        self.wait(1)

        # LEFT
        param = TextMobject("1")
        param.set_color(BLUE)
        param.scale(0.75)
        param.move_to([def_3[1].get_x(), def_3[1].get_y(), 0])

        self.play(
            FadeOut(def_3[1]),
            TransformFromCopy(question[1], param)
        )
        self.wait(0.5)

        param2 = TextMobject("1")
        param2.set_color(BLUE)
        param2.scale(0.75)
        param2.move_to([def_3[3].get_x(), def_3[3].get_y(), 0])

        self.play(
            FadeOut(def_3[3]),
            TransformFromCopy(param, param2)
        )
        self.wait(1)

        left_node = max_heap.arr[3]
        unblur_list = []
        unblur_list.append(left_node.node_obj.set_opacity)
        unblur_list.append(1)
        unblur_list.append(left_node.node_obj.set_fill)
        unblur_list.append(RED)
        unblur_list.append(0)
        unblur_list.append(left_node.key_obj.set_opacity)
        unblur_list.append(1)
        unblur_list.append(left_node.index_obj.set_opacity)
        unblur_list.append(1)

        left_edge = max_heap.arr[1].left_edge
        unblur_list.append(left_edge.set_opacity)
        unblur_list.append(1)

        self.play(
            *[b for b in unblur_list],
        )

        self.wait(1)

        # RIGHT
        param = TextMobject("1")
        param.set_color(BLUE)
        param.scale(0.75)
        param.move_to([def_4[1].get_x(), def_4[1].get_y(), 0])

        self.play(
            FadeOut(def_4[1]),
            TransformFromCopy(question[1], param)
        )
        self.wait(0.5)

        param2 = TextMobject("1")
        param2.set_color(BLUE)
        param2.scale(0.75)
        param2.move_to([def_4[3].get_x(), def_4[3].get_y(), 0])

        self.play(
            FadeOut(def_4[3]),
            TransformFromCopy(param, param2)
        )
        self.wait(1)

        right_node = max_heap.arr[4]
        unblur_list = []
        unblur_list.append(right_node.node_obj.set_opacity)
        unblur_list.append(1)
        unblur_list.append(right_node.node_obj.set_fill)
        unblur_list.append(RED)
        unblur_list.append(0)
        unblur_list.append(right_node.key_obj.set_opacity)
        unblur_list.append(1)
        unblur_list.append(right_node.index_obj.set_opacity)
        unblur_list.append(1)

        right_edge = max_heap.arr[1].right_edge
        unblur_list.append(right_edge.set_opacity)
        unblur_list.append(1)

        self.play(
            *[b for b in unblur_list],
        )

        # PARENT
        param = TextMobject("1")
        param.set_color(BLUE)
        param.scale(0.75)
        param.move_to([def_5[1].get_x(), def_5[1].get_y(), 0])

        self.play(
            FadeOut(def_5[1]),
            TransformFromCopy(question[1], param)
        )
        self.wait(0.5)

        param2 = TextMobject("1")
        param2.set_color(BLUE)
        param2.scale(0.75)
        param2.move_to([def_5[3].get_x(), def_5[3].get_y(), 0])

        self.play(
            FadeOut(def_5[3]),
            TransformFromCopy(param, param2)
        )
        self.wait(1)

        parent_node = max_heap.arr[0]
        unblur_list = []
        unblur_list.append(parent_node.node_obj.set_opacity)
        unblur_list.append(1)
        unblur_list.append(parent_node.node_obj.set_fill)
        unblur_list.append(RED)
        unblur_list.append(0)
        unblur_list.append(parent_node.key_obj.set_opacity)
        unblur_list.append(1)
        unblur_list.append(parent_node.index_obj.set_opacity)
        unblur_list.append(1)

        parent_edge = max_heap.arr[0].left_edge
        unblur_list.append(parent_edge.set_opacity)
        unblur_list.append(1)

        self.play(
            *[b for b in unblur_list],
        )


        self.wait(2)

        #draw arrow and ^ pointers
        # index = 0

        # arrow = Arrow([values[index].get_x(), values[index].get_y() - 2.2, 0],
        #               [values[index].get_x(), values[index].get_y() - 1.1, 0])
        # arrow.set_color(ORANGE)
        # self.play(Write(arrow))
        # self.wait(1)

        # pointer = TextMobject("\^")
        # pointer.rotate(PI)
        # pointer.move_to([max_heap.arr[index].node_obj.get_x(), max_heap.arr[index].node_obj.get_y() + 0.5, 0])
        # pointer.set_color(ORANGE)
        # pointer.scale(2)
        # self.play(Write(pointer))
        # self.wait(1)

        # for i in range(3):
        #     if max_heap.left(index) is not None:
        #         new_arrow = Arrow([values[max_heap.left(index)].get_x(), values[max_heap.left(index)].get_y() - 2.2, 0],
        #                           [values[max_heap.left(index)].get_x(), values[max_heap.left(index)].get_y() - 1.1, 0])
        #         new_arrow.set_color(ORANGE)
        #         self.wait(1)

        #         new_pointer = TextMobject("\^")
        #         new_pointer.rotate(PI)
        #         new_pointer.move_to([max_heap.arr[max_heap.left(index)].node_obj.get_x(),
        #                              max_heap.arr[max_heap.left(index)].node_obj.get_y() + 0.5, 0])
        #         new_pointer.set_color(ORANGE)
        #         new_pointer.scale(2)
        #         self.play(Transform(pointer, new_pointer), Transform(arrow, new_arrow))
        #         self.wait(1)

        #         index = max_heap.left(index)

        # self.play(FadeOut(def_3), FadeOut(def_4), FadeOut(def_5), FadeOut(formulas_rect))
