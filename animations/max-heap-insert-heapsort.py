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

    def swap_nodes(self, i, j, scene=None, show_sketch=False, run_time=1.0):

        i_x = self.arr[i].node_obj.get_x()
        i_y = self.arr[i].node_obj.get_y()
        j_x = self.arr[j].node_obj.get_x()
        j_y = self.arr[j].node_obj.get_y()

        # swapping the nodes positions
        if not show_sketch:

            # the not-visual way
            self.arr[i].node_obj.set_x(j_x)
            self.arr[i].node_obj.set_y(j_y)
            self.arr[i].key_obj.set_x(j_x)
            self.arr[i].key_obj.set_y(j_y)

            self.arr[j].node_obj.set_x(i_x)
            self.arr[j].node_obj.set_y(i_y)
            self.arr[j].key_obj.set_x(i_x)
            self.arr[j].key_obj.set_y(i_y)

        else:

            # the visual way
            scene.play(
                self.arr[i].node_obj.move_to, [j_x, j_y, 0],
                self.arr[i].key_obj.move_to, [j_x, j_y, 0],
                self.arr[j].node_obj.move_to, [i_x, i_y, 0],
                self.arr[j].key_obj.move_to, [i_x, i_y, 0],
                run_time=run_time
            )

        # swapping the edges between the 2 nodes (not visual)
        i_left = self.arr[i].left_edge
        i_right = self.arr[i].right_edge

        self.arr[i].left_edge = self.arr[j].left_edge
        self.arr[i].right_edge = self.arr[j].right_edge

        self.arr[j].left_edge = i_left
        self.arr[j].right_edge = i_right

        # swapping the nodes in array (not visual)
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
        if 2 * index + 2 < self.size:
            return 2 * index + 2
        else:
            return None

    def insert(self, key, scene, *keys):

        # title
        title = TextMobject("Insert:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)

        # drawing the code line
        line = Line([-6.1, 2.2, 0], [-6.1, -2.15, 0])

        # drawing the code
        code = VGroup()
        l1 = TextMobject("\\textrm{def}", " \\textrm{insert}", "\\textrm{(}", "\\textrm{key}", "\\textrm{):}")
        for i, color in zip(l1, [YELLOW_B, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l1)

        l2 = TextMobject("    \\textrm{arr}", "\\textrm{[}", "\\textrm{arr}", "\\textrm{.}", "\\textrm{size}",
                         "\\textrm{] = }", "\\textrm{key}")
        for i, color in zip(l2, [BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE, BLUE]):
            i.set_color(color)
        code.add(l2)

        l3 = TextMobject("    \\textrm{c}", " \\textrm{= }", "\\textrm{arr}", "\\textrm{.}", "\\textrm{size}",
                         "\\textrm{ \# child index}")
        for i, color in zip(l3, [BLUE, WHITE, BLUE, WHITE, PURPLE_C, GREY]):
            i.set_color(color)
        code.add(l3)

        l4 = TextMobject("    \\textrm{arr}", "\\textrm{.}", "\\textrm{size}", "\\textrm{ =}", " \\textrm{arr}",
                         "\\textrm{.}", "\\textrm{size}", "\\textrm{ + }", "\\textrm{1}")
        for i, color in zip(l4, [BLUE, WHITE, PURPLE_C, WHITE, BLUE, WHITE, PURPLE_C, WHITE, BLUE]):
            i.set_color(color)
        code.add(l4)

        l5 = TextMobject("    \\textrm{p}", "\\textrm{ = }", "\\textrm{parent}", "\\textrm{(}", "\\textrm{c}",
                         "\\textrm{)}", " \\textrm{\# parent index}")
        for i, color in zip(l5, [BLUE, WHITE, BLUE, WHITE, BLUE, WHITE, GREY]):
            i.set_color(color)
        code.add(l5)

        l6 = TextMobject("    \\textrm{while}", " \\textrm{arr}", "\\textrm{[}", "\\textrm{c}", "\\textrm{] > }",
                         "\\textrm{arr}", "\\textrm{[}",
                         "\\textrm{p}",
                         "\\textrm{]:}")
        for i, color in zip(l6, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l6)

        l7 = TextMobject("        \\textrm{swap}", "\\textrm{(}", "\\textrm{c}",
                         "\\textrm{, }",
                         "\\textrm{p}", "\\textrm{)}")
        for i, color in zip(l7, [BLUE, WHITE, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l7)

        l8 = TextMobject("        \\textrm{c}", "\\textrm{ = }", "\\textrm{p}")
        for i, color in zip(l8, [BLUE, WHITE, BLUE]):
            i.set_color(color)
        code.add(l8)

        l9 = TextMobject("        \\textrm{p}", "\\textrm{ = }", "\\textrm{parent}", "\\textrm{(}", "\\textrm{c}",
                         "\\textrm{)}")
        for i, color in zip(l9, [BLUE, WHITE, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l9)

        for i, l in enumerate(code):
            l.to_edge(LEFT, buff=0.7)
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.55 * i + 0.65, 0])

        code.scale(0.85)
        code.shift([0, 1.6, 0])

        scene.play(Write(title))
        scene.play(FadeInFromDown(line))

        for l in code:
            scene.play(FadeInFrom(l, LEFT), run_time=0.5)
        scene.wait(1)

        # result array
        heap_arr = Polygon([-4.55, -3.3, 0], [4.55, -3.3, 0], [4.55, -2.6, 0], [-4.55, -2.6, 0])
        heap_arr.set_color(WHITE)
        scene.play(Write(heap_arr))

        arr_lines = VGroup()
        for i in range(1, 11):
            line = Line([-4.55 + 0.7 * i, -2.6, 0], [-4.55 + 0.7 * i, -3.3, 0])
            arr_lines.add(line)
            scene.play(Write(line), rate_func=smooth, run_time=0.2)

        res_text = TextMobject("\\textrm{arr}")
        res_text.scale(0.7)
        res_text.move_to([-5, -2.95, 0])
        scene.play(Write(res_text))

        values = VMobject()

        for i, node in enumerate(self.arr):
            val = TextMobject(str(node.key))
            val.set_color(TEAL_E)
            val.scale(0.7)
            val.move_to([-4.2 + 0.7 * i, -2.95, 0])
            values.add(val)

        scene.play(*[Write(value) for value in values])

        for key in keys:

            rect = SurroundingRectangle(l1, buff=0.04, color=WHITE)

            # drawing the searched key
            new_insert = TextMobject(f"Let's insert {key}.")
            new_insert.shift([0, title.get_y(), 0])
            new_insert.set_color(GREEN)
            scene.play(Write(new_insert))
            scene.wait(0.5)

            scene.play(Write(rect))
            scene.wait(0.7)

            if self.size == 0:
                new_rect = SurroundingRectangle(l2, buff=0.04, color=TEAL_E)
                scene.play(ReplacementTransform(rect, new_rect))
                scene.wait(0.7)

                node = Node(0, key, self.x, self.y)
                self.nodes.add(node)

                scene.play(Write(node.node_obj))
                scene.play(Write(node.key_obj))
                scene.wait(0.5)

                val = TextMobject(str(node.key))
                val.set_color(TEAL_E)
                val.scale(0.7)
                val.move_to([-4.2 + 0.7 * len(values), -2.95, 0])
                scene.play(Write(val))
                values.add(val)
                scene.wait(0.7)

            else:
                new_rect = SurroundingRectangle(l2, buff=0.04, color=TEAL_E)
                scene.play(ReplacementTransform(rect, new_rect))
                scene.wait(0.7)

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
                if self.left(node_parent) == index:
                    self.arr[node_parent].left_edge = edge
                else:
                    self.arr[node_parent].right_edge = edge

                scene.play(Write(node.node_obj))
                scene.play(Write(node.key_obj))
                scene.play(Write(edge))
                scene.wait(0.5)

                val = TextMobject(str(node.key))
                val.set_color(TEAL_E)
                val.scale(0.7)
                val.move_to([-4.2 + 0.7 * len(values), -2.95, 0])
                scene.play(Write(val))
                values.add(val)
                scene.wait(0.7)

            self.arr.append(node)

            self.size = self.size + 1
            self.height = math.floor(math.log2(self.size))

            rect = new_rect
            new_rect = SurroundingRectangle(l3, buff=0.04, color=ORANGE)
            scene.play(ReplacementTransform(rect, new_rect))
            scene.wait(0.7)

            child_pointer = TextMobject("\^")
            child_pointer.rotate(PI)
            child_pointer.move_to([node.node_obj.get_x(), node.node_obj.get_y() + 0.5, 0])
            child_pointer.set_color(ORANGE)
            child_pointer.scale(2)
            scene.play(Write(child_pointer))

            scene.wait(0.5)

            rect = new_rect
            new_rect = SurroundingRectangle(l4, buff=0.04, color=WHITE)
            scene.play(ReplacementTransform(rect, new_rect))
            scene.wait(0.7)

            child_index = self.size - 1

            line = Line([-4.55 + 0.7 * (len(arr_lines) + 1), -2.6, 0], [-4.55 + 0.7 * (len(arr_lines) + 1), -3.3, 0])
            arr_lines.add(line)
            scene.play(Write(line), rate_func=smooth, run_time=0.2)
            scene.wait(0.7)

            if child_index != 0:

                rect = new_rect
                new_rect = SurroundingRectangle(l5, buff=0.04, color=PURPLE)
                scene.play(ReplacementTransform(rect, new_rect))
                scene.wait(0.7)

                parent_index = self.parent(child_index)

                parent_pointer = TextMobject("\^")
                parent_pointer.rotate(PI)
                parent_pointer.move_to(
                    [self.arr[parent_index].node_obj.get_x(), self.arr[parent_index].node_obj.get_y() + 0.5, 0])
                parent_pointer.set_color(PURPLE_B)
                parent_pointer.scale(2)
                scene.play(Write(parent_pointer))

                rect = new_rect
                new_rect = SurroundingRectangle(l6, buff=0.04, color=WHITE)
                scene.play(ReplacementTransform(rect, new_rect))
                scene.wait(0.7)

                while self.arr[child_index].key > self.arr[parent_index].key:

                    rect = new_rect
                    new_rect = SurroundingRectangle(l7, buff=0.04, color=RED)
                    scene.play(ReplacementTransform(rect, new_rect))
                    scene.wait(0.7)

                    self.swap_nodes(parent_index, child_index, scene)

                    scene.play(values[child_index].set_color, RED, values[parent_index].set_color, RED)

                    scene.wait(0.7)

                    i, j = parent_index, child_index

                    i_x = self.arr[i].node_obj.get_x()
                    i_y = self.arr[i].node_obj.get_y()
                    j_x = self.arr[j].node_obj.get_x()
                    j_y = self.arr[j].node_obj.get_y()

                    # swapping the nodes positions
                    # the visual way
                    scene.play(
                        self.arr[i].node_obj.move_to, [j_x, j_y, 0],
                        self.arr[i].key_obj.move_to, [j_x, j_y, 0],
                        self.arr[j].node_obj.move_to, [i_x, i_y, 0],
                        self.arr[j].key_obj.move_to, [i_x, i_y, 0],
                        values[child_index].move_to,
                        [values[parent_index].get_x(), values[parent_index].get_y(), 0],
                        values[parent_index].move_to,
                        [values[child_index].get_x(), values[child_index].get_y(), 0])

                    # just dirty code:)
                    new_values = VGroup()
                    for i, val in enumerate(values):
                        if i == child_index:
                            new_values.add(values[parent_index])
                        elif i == parent_index:
                            new_values.add(values[child_index])
                        else:
                            new_values.add(values[i])
                    values = new_values

                    # tmp = values[child_index]
                    # values.set(values[parent_index])
                    # values[parent_index].set(tmp)

                    scene.wait(0.7)

                    scene.play(values[child_index].set_color, TEAL_E, values[parent_index].set_color, TEAL_E)

                    rect = new_rect
                    new_rect = SurroundingRectangle(l8, buff=0.04, color=ORANGE)
                    scene.play(ReplacementTransform(rect, new_rect))
                    scene.wait(0.7)

                    scene.play(child_pointer.move_to,
                               [self.arr[parent_index].node_obj.get_x(),
                                self.arr[parent_index].node_obj.get_y() + 0.5, 0])

                    child_index = parent_index

                    if child_index == 0:
                        break

                    rect = new_rect
                    new_rect = SurroundingRectangle(l9, buff=0.04, color=PURPLE)
                    scene.play(ReplacementTransform(rect, new_rect))
                    scene.wait(0.7)

                    scene.play(parent_pointer.move_to,
                               [self.arr[self.parent(child_index)].node_obj.get_x(),
                                self.arr[self.parent(child_index)].node_obj.get_y() + 0.5, 0])

                    parent_index = self.parent(child_index)

                    rect = new_rect
                    new_rect = SurroundingRectangle(l6, buff=0.04, color=WHITE)
                    scene.play(ReplacementTransform(rect, new_rect))
                    scene.wait(0.7)

                scene.wait(0.7)
                scene.play(FadeOut(rect), FadeOut(new_rect), FadeOut(child_pointer), FadeOut(parent_pointer),
                           FadeOut(new_insert))

    def extract_max(self, scene, run_time=1.0):
        return self.delete(0, scene, run_time)

    def delete(self, index, scene, run_time=1.0):

        node_parent = self.parent(self.size - 1)
        if self.left(node_parent) == self.size - 1:
            self.edges.remove(self.arr[node_parent].left_edge)
            self.arr[node_parent].left_edge = None
        else:
            self.edges.remove(self.arr[node_parent].right_edge)
            self.arr[node_parent].right_edge = None

        self.swap_nodes(index, self.size - 1, scene, True, run_time)
        node = self.arr[self.size - 1]
        self.arr.remove(node)
        self.nodes.remove(node)

        self.size = self.size - 1
        if self.size != 0:
            self.height = math.floor(math.log2(self.size))
        else:
            self.height = 0
        # self.heapify(scene, index)
        return node

    def heapify(self, scene, index, code, prev_rect=None, show_rect=True, run_time=1.0):

        left = self.left(index)
        right = self.right(index)

        rect = None
        new_rect = None

        if show_rect:
            rect = SurroundingRectangle(code[0], buff=0.06, color=RED)
            if prev_rect is None:
                scene.play(Write(rect))
            else:
                scene.play(ReplacementTransform(prev_rect, rect))

            scene.wait(1)

            new_rect = SurroundingRectangle(VGroup(code[1], code[2]), buff=0.06, color=BLUE_C)
            scene.play(ReplacementTransform(rect, new_rect))
            rect = new_rect
            scene.wait(0.5)

        big = None
        if right is not None:
            if self.arr[left].key >= self.arr[right].key:
                big = left
            else:
                big = right
        elif right is None and left is not None:
            big = left
        else:
            big = index

        if self.arr[big].key <= self.arr[index].key:
            big = index

        big_pointer = TextMobject("\^")
        big_pointer.rotate(PI)
        big_pointer.move_to([self.arr[big].node_obj.get_x(), self.arr[big].node_obj.get_y() + 0.5, 0])
        big_pointer.set_color(BLUE_C)
        big_pointer.scale(2)
        scene.play(Write(big_pointer), run_time=run_time)
        scene.wait(0.5)

        if show_rect:
            new_rect = SurroundingRectangle(code[3], buff=0.06, color=WHITE)
            scene.play(ReplacementTransform(rect, new_rect))
            rect = new_rect
            scene.wait(0.7)

        if self.arr[big].key > self.arr[index].key:

            if show_rect:
                new_rect = SurroundingRectangle(code[4], buff=0.06, color=WHITE)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.5)

            self.swap_nodes(big, index, scene, True, run_time)
            scene.wait(0.8)

            if show_rect:
                new_rect = SurroundingRectangle(code[5], buff=0.06, color=WHITE)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.5)

            scene.play(FadeOut(big_pointer), run_time=run_time)

            self.heapify(scene, big, code, rect, show_rect, run_time=run_time)

        else:
            if show_rect:
                new_rect = SurroundingRectangle(code[6], buff=0.06, color=WHITE)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(1.5)
                scene.play(FadeOut(rect))

            scene.play(
                FadeOut(big_pointer),
                self.arr[index].node_obj.set_color, TEAL_E,
                run_time=run_time
            )
            scene.wait(0.5)

    def build(self, scene):
        for i in range(self.size // 2 - 1, -1, -1):
            self.heapify(i, scene)

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
        for node in self.nodes:
            scene.play(
                Write(node.node_obj),
                Write(node.key_obj),
                run_time=0.3
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
            val.set_color(TEAL_E)
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


class Insert(Scene):

    def construct(self):
        # Introduction
        title_l1 = TextMobject("Binary Max Heap")
        title_l2 = TextMobject("Insert")
        title_l1.scale(1.8)
        title_l2.scale(1.3)
        title_l1.shift([0, 0.5, 0])
        title_l2.shift([0, -0.35, 0])
        line = Line([-3.8, 0, 0], [3.8, 0, 0])
        line.set_stroke(WHITE, 1.1, 1)
        creators = TextMobject("Made by Matin Tavakoli \& Hossein Zaredar")
        creators.scale(0.4)
        creators.move_to([5, -3.7, 0])
        self.add(title_l1)
        self.add(title_l2)
        self.add(line)
        self.wait(2)
        self.play(Write(creators), run_time=0.7)
        self.wait(2)
        self.play(FadeOut(title_l1), FadeOut(title_l2), FadeOut(line))
        self.wait(1.5)

        # arr = [-4, 5, 0, 1, 2, -1, -2, -6, -3, -1]
        arr = [5, 2, 0, 1, -1, -1, -2, -6, -3, -4]
        max_heap = MaxHeap(arr, 3.8, 1.7, hspace=3, node_color=TEAL_E)
        max_heap.sketch_heap(self)
        max_heap.insert(6, self, 4, 6, -3)
        self.wait(3)


class HeapSort(Scene):

    def construct(self):

        # Introduction
        title_l1 = TextMobject("Binary Max Heap")
        title_l2 = TextMobject("Heap Sort")
        title_l1.scale(1.8)
        title_l2.scale(1.3)
        title_l1.shift([0, 0.5, 0])
        title_l2.shift([0, -0.35, 0])
        line = Line([-3.8, 0, 0], [3.8, 0, 0])
        line.set_stroke(WHITE, 1.1, 1)
        creators = TextMobject("Made by Matin Tavakoli \& Hossein Zaredar")
        creators.scale(0.4)
        creators.move_to([5, -3.7, 0])
        self.add(title_l1)
        self.add(title_l2)
        self.add(line)
        self.wait(2)
        self.play(Write(creators), run_time=0.7)
        self.wait(2)
        self.play(FadeOut(title_l1), FadeOut(title_l2), FadeOut(line))
        self.wait(1.5)

        # title
        title = TextMobject("Heap Sort:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)
        self.play(Write(title))
        self.wait(0.5)

        # problem statement
        prob_1 = TextMobject("Suppose we have an array of size", " n ", "and we want to sort it.")
        prob_2 = TextMobject("We can use Heap Sort, by first calling ", "Build Max Heap", ",")
        prob_3 = TextMobject("and then calling ", "Extract Max", " n ", "times.")
        prob_4 = TextMobject("Let's see how it's done!")

        prob_1[0].set_color(BLUE)
        prob_1[1].set_color(RED)
        prob_1[2].set_color(BLUE)
        prob_2[0].set_color(BLUE)
        prob_2[1].set_color(GOLD_B)
        prob_2[2].set_color(BLUE)
        prob_3[0].set_color(BLUE)
        prob_3[1].set_color(GOLD_B)
        prob_3[2].set_color(RED)
        prob_3[3].set_color(BLUE)
        prob_4.set_color(BLUE)

        prob_1.scale(0.8)
        prob_2.scale(0.8)
        prob_3.scale(0.8)
        prob_4.scale(0.8)

        prob_1.to_edge(LEFT, 0.5)
        prob_2.to_edge(LEFT, 0.5)
        prob_3.to_edge(LEFT, 0.5)
        prob_4.to_edge(LEFT, 0.5)

        prob_1.shift([0, 2.2, 0])
        prob_2.shift([0, 1.8, 0])
        prob_3.shift([0, 1.3, 0])
        prob_4.shift([0, 0.5, 0])

        self.play(Write(prob_1), run_time=2.5)
        self.wait(1)

        # result array
        arr = Polygon([-3.5, -2.5, 0], [3.5, -2.5, 0], [3.5, -1.5, 0], [-3.5, -1.5, 0])
        arr.set_color(WHITE)
        arr.shift([0, -0.7, 0])
        self.play(Write(arr))

        orig_arr = [1, 4, 2, 8, -3, -1, 0]
        heap_arr = [8, 4, 2, 1, -3, -1, 0]

        arr_lines = VGroup()
        for i in range(1, len(orig_arr) + 1):
            line = Line([-3.5 + i, -1.5, 0], [-3.5 + i, -2.5, 0])
            line.shift([0, -0.7, 0])
            arr_lines.add(line)
            self.play(Write(line), rate_func=smooth, run_time=0.2)

        arr_text = TextMobject("\\textrm{arr}")
        arr_text.move_to([-4.2, -2, 0])
        arr_text.shift([0, -0.7, 0])
        self.play(Write(arr_text))

        self.wait(0.7)

        values = VGroup()
        for i, elem in enumerate(orig_arr):
            val = TextMobject(str(elem))
            val.set_color(TEAL_E)
            val.move_to([-3 + i, -2, 0])
            val.shift([0, -0.7, 0])
            self.play(Write(val), run_time=0.2)
            values.add(val)

        sorted_values = VGroup()
        for i, elem in enumerate(heap_arr):
            val = TextMobject(str(elem))
            val.set_color(TEAL_E)
            val.move_to([-3 + i, -2, 0])
            val.shift([0, -0.7, 0])
            # self.play(Write(val), run_time=0.2)
            sorted_values.add(val)

        self.wait(1)

        self.play(Write(prob_2), run_time=2.5)
        self.wait(1)

        # drawing the tree
        max_heap = MaxHeap(orig_arr, 3.8, 1, hspace=3, node_color=TEAL_E)
        built_max_heap = MaxHeap(heap_arr, 3.8, 1, hspace=3, node_color=TEAL_E)
        max_heap.sketch_heap(self)
        self.wait(1)

        self.play(*[FadeOut(node.key_obj) for node in max_heap.arr], *[FadeOut(val) for val in values])

        for i, node in enumerate(max_heap.arr):
            # self.play(node.node_obj.set_opacity, 0, run_time=0.05)
            max_heap.arr[i].key_obj = built_max_heap.arr[i].key_obj
            max_heap.arr[i].key = built_max_heap.arr[i].key

        values = sorted_values

        self.wait(1.5)
        self.play(*[FadeIn(node.key_obj) for node in max_heap.arr], *[FadeIn(val) for val in values])
        self.wait(0.7)

        # step 0: find the root
        self.play(Write(prob_3))
        self.wait(2)
        self.play(Write(prob_4))
        self.wait(1)

        self.play(FadeOut(arr_text), FadeOut(arr), FadeOut(arr_lines), FadeOut(values))

        # result array
        heap_arr = Polygon([-3.5, -3.2, 0], [3.5, -3.2, 0], [3.5, -2.2, 0], [-3.5, -2.2, 0])
        heap_arr.set_color(WHITE)
        self.play(Write(heap_arr))

        arr_lines = VGroup()
        for i in range(1, len(max_heap.arr)):
            line = Line([-3.5 + i, -2.2, 0], [-3.5 + i, -3.2, 0])
            arr_lines.add(line)
            self.play(Write(line), rate_func=smooth, run_time=0.2)

        sorted_text = TextMobject("\\textrm{sorted arr}")
        sorted_text.move_to([-4.8, -2.7, 0])
        self.play(Write(sorted_text))

        values = VMobject()

        n = len(max_heap.arr)

        for i in range(n):

            run_time = 1 - 0.14 * i

            self.play(max_heap.arr[0].node_obj.set_color, YELLOW, run_time=run_time)
            self.wait(1 * run_time)

            self.play(
                max_heap.arr[0].node_obj.shift, [0, 0.6, 0],
                max_heap.arr[0].key_obj.shift, [0, 0.6, 0],
                run_time=run_time
            )
            self.wait(1 * run_time)

            val = max_heap.arr[0].key_obj.copy()
            val.set_color(PURPLE)
            val.move_to([-3 + i, -2.7, 0])
            values.add(val)

            self.play(TransformFromCopy(max_heap.arr[0].key_obj, val), run_time=run_time)

            self.wait(0.5 * run_time)

            self.play(
                max_heap.arr[0].node_obj.set_opacity, 0,
                max_heap.arr[0].key_obj.set_opacity, 0,
                run_time=run_time
            )

            self.play(
                max_heap.arr[0].node_obj.shift, [0, -0.6, 0],
                max_heap.arr[0].key_obj.shift, [0, -0.6, 0],
                run_time=run_time
            )

            # edge...
            edge = None

            if i != n - 1:
                parent = max_heap.parent(len(max_heap.arr) - 1)
                if max_heap.left(parent) == len(max_heap.arr) - 1:
                    edge = max_heap.arr[parent].left_edge
                elif max_heap.right(parent) == len(max_heap.arr) - 1:
                    edge = max_heap.arr[parent].right_edge

            self.wait(1 * run_time)
            max_heap.extract_max(self, run_time=run_time)

            if i != n - 1:
                # removing the edge
                self.play(FadeOut(edge), run_time=run_time)
                self.wait(1 * run_time)

            # we need to heapify

            if i == 0:
                prob_8 = TextMobject("Now we apply Heapify!")
                prob_8.set_color(BLUE)
                prob_8.scale(0.8)
                prob_8.to_edge(LEFT, 0.5)
                prob_8.shift([0, -0.3, 0])
                self.play(Write(prob_8))
                self.wait(1 * run_time)

            # calling heapify
            if len(max_heap.arr) != 0:
                self.play(max_heap.arr[0].node_obj.set_color, RED, run_time=run_time)
                self.wait(1 * run_time)
                max_heap.heapify(self, 0, None, None, False, run_time=run_time)

            if i == 0:
                prob_9 = TextMobject("...and repeat!")
                prob_9.set_color(BLUE)
                prob_9.scale(0.8)
                prob_9.to_edge(LEFT, 0.5)
                prob_9.shift([0, -1.3, 0])
                self.play(Write(prob_9))
                self.wait(1 * run_time)

            self.wait(1.5 * run_time)

        for i in range(len(values)):
            if i == 0 or i == 1:
                self.play(values[i].scale, 1.428, values[i].set_color, YELLOW, run_time=0.15)
                self.wait(0.12)
            else:
                self.play(values[i].scale, 1.428, values[i].set_color, YELLOW, values[i - 2].scale, 0.7,
                          values[i - 2].set_color, PURPLE, run_time=0.24)

        self.wait(0.12)
        self.play(values[n - 2].scale, 0.7, values[n - 2].set_color, PURPLE, run_time=0.12)
        self.wait(0.12)
        self.play(values[n - 1].scale, 0.7, values[n - 1].set_color, PURPLE, run_time=0.12)
        self.wait(0.7)

        prob_12 = TextMobject("And now we have a sorted array!")
        prob_12.set_color(BLUE)
        prob_12.scale(0.8)
        prob_12.to_edge(LEFT, 0.5)
        prob_12.shift([0, 2.2, 0])
        self.play(
            FadeOutAndShift(prob_1, direction=[0, 0.5, 0]),
            FadeOutAndShift(prob_2, direction=[0, 1, 0]),
            FadeOutAndShift(prob_3, direction=[0, 1.5, 0]),
            FadeOutAndShift(prob_4, direction=[0, 2, 0]),
            FadeOutAndShift(prob_8, direction=[0, 2.5, 0]),
            ReplacementTransform(prob_9, prob_12)
        )
        self.wait(2)

        prob_15 = TextMobject("So, the code for Heap Sort is this...")
        prob_15.set_color(BLUE)
        prob_15.scale(0.8)
        prob_15.to_edge(LEFT, 0.5)
        prob_15.shift([0, 1.7, 0])
        self.play(Write(prob_15))
        self.wait(1)
        self.play(FadeOut(prob_12), FadeOut(prob_15))
        self.wait(1)

        # writing the code

        # drawing the code line
        line = Line([-5.9, 1.8, 0], [-5.9, -0.7, 0])

        code = VGroup()
        l1 = TextMobject("def", " heap\\_sort", "(", "arr", "):")
        for i, color in zip(l1, [YELLOW_B, PURPLE_C, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l1)

        l2 = TextMobject("    sorted\\_arr", " = ", "[ ]")
        for i, color in zip(l2, [BLUE, WHITE, WHITE]):
            i.set_color(color)
        code.add(l2)

        l3 = TextMobject("    for", " i", " = ", "0", " to", " n", " -", " 1" ":")
        for i, color in zip(l3, [YELLOW_B, BLUE, WHITE, BLUE, YELLOW_B, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l3)

        l4 = TextMobject("        sorted\\_arr", ".", "add", "(", "extract\\_max", "(", "i", "))")
        for i, color in zip(l4, [BLUE, WHITE, YELLOW_B, WHITE, PURPLE_C, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l4)

        l4 = TextMobject("    return ", "sorted\\_arr")
        for i, color in zip(l4, [YELLOW_B, BLUE]):
            i.set_color(color)
        code.add(l4)

        for i, l in enumerate(code):
            l.to_edge(LEFT, buff=0.9)
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.55 * i + 0.65, 0])

        code.scale(0.85)
        code.shift([0, 1, 0])

        self.play(FadeInFromDown(line))

        for l in code:
            self.play(FadeInFrom(l, LEFT), run_time=0.5)

        self.wait(3)
