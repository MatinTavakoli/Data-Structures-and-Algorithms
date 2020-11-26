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

    def swap_nodes(self, i, j, scene=None, show_sketch=False, extra_anims=[]):

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
                *extra_anims
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

    def heapify(self, scene, index, code, prev_rect=None):

        root = self.arr[index]
        left = self.left(index)
        right = self.right(index)     

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

        big_pointer = TextMobject("\^")
        big_pointer.rotate(PI)
        big_pointer.move_to([self.arr[big].node_obj.get_x(), self.arr[big].node_obj.get_y() + 0.5, 0])
        big_pointer.set_color(BLUE_C)
        big_pointer.scale(2)
        scene.play(Write(big_pointer))
        scene.wait(0.5)

        new_rect = SurroundingRectangle(code[3], buff=0.06, color=WHITE)
        scene.play(ReplacementTransform(rect, new_rect))
        rect = new_rect
        scene.wait(0.7)

        if self.arr[big].key > self.arr[index].key:
           
            new_rect = SurroundingRectangle(code[4], buff=0.06, color=WHITE)
            scene.play(ReplacementTransform(rect, new_rect))
            rect = new_rect
            scene.wait(0.5)

            extra_anims = [
                big_pointer.shift,
                [
                    -self.arr[big].node_obj.get_x() + root.node_obj.get_x(),
                    -self.arr[big].node_obj.get_y() + root.node_obj.get_y(),
                    0
                ],
            ]

            self.swap_nodes(big, index, scene, True, extra_anims)
            scene.wait(0.5)

            scene.play(FadeOut(big_pointer))
            scene.wait(0.3)
               
            new_rect = SurroundingRectangle(code[5], buff=0.06, color=WHITE)
            scene.play(ReplacementTransform(rect, new_rect))
            rect = new_rect
            scene.wait(0.5)

            self.heapify(scene, big, code, rect)
        
        else:
            new_rect = SurroundingRectangle(code[6], buff=0.06, color=WHITE)
            scene.play(ReplacementTransform(rect, new_rect))
            rect = new_rect
            scene.wait(1.5)
            scene.play(
                FadeOut(rect),
                FadeOut(big_pointer),
                self.arr[index].node_obj.set_color, TEAL_E
            )
            scene.wait(0.5)

            


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
            print(self.arr[i].key, end=" ")

    def sketch_heap(self, scene):
        for node in self.nodes:
            scene.play(
                Write(node.node_obj),
                Write(node.key_obj),
                run_time=0.3
            )
        scene.play(*[GrowArrow(e) for e in self.edges], run_time=1.5)

    def clear_heap(self, scene):
        scene.play(
            *[FadeOut(node.node_obj) for node in self.nodes],
            *[FadeOut(node.key_obj) for node in self.nodes],
            *[FadeOut(e) for e in self.edges]
        )

    def blur_heap(self, scene, opacity, *skip_list):
        blur_list = []
        for node in self.nodes:
            if node not in skip_list:
                blur_list.append(node.node_obj.set_opacity)
                blur_list.append(opacity)
                blur_list.append(node.node_obj.set_fill)
                blur_list.append(RED)
                blur_list.append(0)
                blur_list.append(node.key_obj.set_opacity)
                blur_list.append(opacity)
                blur_list.append(node.index_obj.set_opacity)
                blur_list.append(opacity)
        for edge in self.edges:
            if edge not in skip_list:
                blur_list.append(edge.set_opacity)
                blur_list.append(opacity)

        scene.play(
            *[b for b in blur_list],
        )	


class Intro(Scene):

    def construct(self):

        # part 1: heap invariant

        # title
        title = TextMobject("Introduction:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)
        self.play(Write(title))
        self.wait(0.5)

        # arr = [4, 7, -1, 2, 0, 3, 5, 1]
        arr = [7, 4, 5, 2, 0, 3, -1, 1]
        # arr = [3, 5, 0, 8, 5, -1, -2, 10, 1]
        # arr = [10, 8, 0, 5, 5, -1, -2, 3, 1, 2, 4, -3, -1, -4, -6]
        # arr = [-4, 3, 0, 1, 2, -1, -2, -6, -3, -1]
        max_heap = MaxHeap(arr, 3.8, 2.2, hspace=3, node_color=TEAL_E)
        # max_heap.build()
        max_heap.sketch_heap(self)
        self.wait(0.7)

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
        self.wait(0.6)
        self.play(Write(def_3))
        self.play(Write(def_4))
        self.wait(1.2)

        self.play(FadeOut(def_1), FadeOut(def_2), FadeOut(def_3), FadeOut(def_4), run_time=1.5)

        # part 2: implementation
        def_1 = TextMobject("A Binary Max Heap can be implemented")
        def_2 = TextMobject("using a simple array.")
        def_3 = TextMobject("We store the nodes, line by line,")
        def_4 = TextMobject("inside an array.")
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
        self.wait(1)
        self.play(Write(def_3))
        self.play(Write(def_4))
        self.wait(0.5)

        # result array
        heap_arr = Polygon([-3.5, -2.3, 0], [4.5, -2.3, 0], [4.5, -1.3, 0], [-3.5, -1.3, 0])
        heap_arr.set_color(WHITE)
        heap_arr.shift([0, -0.8, 0])
        self.play(Write(heap_arr))

        arr_lines = VGroup()
        for i in range(1, 8):
            line = Line([-3.5 + i, -1.3, 0], [-3.5 + i, -2.3, 0])
            line.shift([0, -0.8, 0])
            arr_lines.add(line)
            self.play(Write(line), rate_func=smooth, run_time=0.2)

        res_text = TextMobject("\\textrm{arr}")
        res_text.move_to([-4.2, -1.8, 0])
        res_text.shift([0, -0.8, 0])
        self.play(Write(res_text))

        self.wait(0.7)

        indices = VGroup()
        for i in range(max_heap.size):
            val = TextMobject(str(i))
            indices.add(val)
            val.set_color(RED)
            val.scale(0.8)
            val.move_to([-3 + i, -2.8, 0])
            val.shift([0, -0.65, 0])
            self.play(Write(val), run_time=0.2)

        self.wait(1)

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
            val.shift([0, -0.8, 0])
            self.play(TransformFromCopy(node.key_obj, val))
            values.add(val)

        self.wait(1)
        self.play(FadeOut(def_1), FadeOut(def_2), FadeOut(def_3), FadeOut(def_4), FadeOut(rect))
        self.wait(0.4)

        # part 3: where are parent and children?

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
        def_3.to_edge(LEFT, 2.2)
        def_4.to_edge(LEFT, 2.2)
        def_5.to_edge(LEFT, 2.2)

        def_0.shift([0, 1.7, 0])
        def_1.shift([0, 1.25, 0])
        def_21.shift([0, 0.8, 0])
        def_22.shift([0, 0.35, 0])
        def_3.shift([0, -0.25, 0])
        def_4.shift([0, -0.7, 0])
        def_5.shift([0, -1.15, 0])

        self.play(Write(def_0))
        self.play(Write(def_1[0]))
        self.wait(1)
        self.play(Write(def_1[1]))
        self.play(Write(def_1[2]))
        self.play(Write(def_21[0]))
        self.wait(0.6)
        self.play(Write(def_21[1]))
        self.play(Write(def_22))
        self.wait(0.6)
        self.play(Write(def_3))
        self.play(Write(def_4))
        self.play(Write(def_5))

        self.wait(0.5)

        # fade instructions. draw rectangle
        self.play(FadeOut(def_0), FadeOut(def_1), FadeOut(def_21), FadeOut(def_22))
        self.play(
            def_3.shift, [0, 1, 0],
            def_3.scale, 1.1,
            def_4.shift, [0, 1, 0],
            def_4.scale, 1.1,
            def_5.shift, [0, 1, 0],
            def_5.scale, 1.1,
            run_time=1.5
        )

        formulas = VGroup()
        formulas.add(def_3)
        formulas.add(def_4)
        formulas.add(def_5)
        formulas_rect = SurroundingRectangle(formulas, buff=0.16, color=ORANGE)
        self.play(Write(formulas_rect))
        self.wait(0.7)

        for i, index in enumerate(indices):
            self.play(TransformFromCopy(index, max_heap.arr[i].index_obj), run_time=0.3)
        
        self.wait(1.2)

        question = TextMobject("Let's look at the node with index '", "1", "'.")
        question.set_color(BLUE)
        question.scale(0.85)
        question.to_edge(LEFT, 0.7)
        question.shift([0, 1.5, 0])
        self.play(Write(question))
        self.wait(1)

        max_heap.blur_heap(self, 0.4, max_heap.arr[1])
        self.wait(1)

        params = VGroup()

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

        params.add(param, param2)

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

        params.add(param, param2)

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

        params.add(param, param2)

        self.wait(1)

        self.play(
            ReplacementTransform(params[0], def_3[1]),
            ReplacementTransform(params[1], def_3[3]),
            ReplacementTransform(params[2], def_4[1]),
            ReplacementTransform(params[3], def_4[3]),
            ReplacementTransform(params[4], def_5[1]),
            ReplacementTransform(params[5], def_5[3]),
            FadeOut(question)
        )
        max_heap.blur_heap(self, 1)
        self.wait(1)

        self.play(
            formulas.shift, [-1.6, -1, 0],
            formulas.scale, 0.9,
            FadeOut(formulas_rect)
        )

        rev_1 = TextMobject("Binary Max Heap is a data structure which is")
        rev_2 = TextMobject("implemented with an array, and follows a rule:")
        rev_3 = TextMobject("\"Each node must be greater than or equal")
        rev_4 = TextMobject(" to its children.\"")

        rev_1.set_color(GOLD_B)
        rev_2.set_color(GOLD_B)
        rev_3.set_color(MAROON_D)
        rev_4.set_color(MAROON_D)

        rev_1.scale(0.75)
        rev_2.scale(0.75)
        rev_3.scale(0.75)
        rev_4.scale(0.75)

        rev_1.to_edge(LEFT, 0.5)
        rev_2.to_edge(LEFT, 0.5)
        rev_3.to_edge(LEFT, 0.5)
        rev_4.to_edge(LEFT, 0.65)

        rev_1.shift([0, 1.9, 0])
        rev_2.shift([0, 1.45, 0])
        rev_3.shift([0, 0.95, 0])
        rev_4.shift([0, 0.55, 0])

        self.play(
            FadeIn(rev_1),
            FadeIn(rev_2),
            FadeIn(rev_3),
            FadeIn(rev_4),
        )

        self.wait(2)

class Heapify(Scene):

    def construct(self):

        # title
        title = TextMobject("Max Heapify:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)
        self.play(Write(title))
        self.wait(0.5)

        # problem statement
        prob_1 = TextMobject("Suppose we have a tree that the root's left and right")
        prob_2 = TextMobject("subtree are Max-Heaps, but the whole tree is not,")
        prob_3 = TextMobject("i.e. the root doesn't follow the rule.")

        prob_1.set_color(GOLD_B)
        prob_2.set_color(GOLD_B)
        prob_3.set_color(GOLD_B)

        prob_1.scale(0.75)
        prob_2.scale(0.75)
        prob_3.scale(0.75)

        prob_1.to_edge(LEFT, 0.5)
        prob_2.to_edge(LEFT, 0.5)
        prob_3.to_edge(LEFT, 0.5)

        prob_1.shift([0, 1, 0])
        prob_2.shift([0, 0.55, 0])
        prob_3.shift([0, 0.1, 0])

        self.play(Write(prob_1))
        self.play(Write(prob_2))
        self.play(Write(prob_3))
        self.wait(1)

        # drawing the tree
        arr = [2, 5, 6, 1, 4, 3, -1]
        max_heap = MaxHeap(arr, 3.8, 1, hspace=3, node_color=TEAL_E)
        max_heap.arr[0].node_obj.set_color(RED)
        max_heap.sketch_heap(self)
        self.wait(0.7)

        # left triangle
        left_root = [max_heap.x -1.5, max_heap.y - 0.38, 0]
        left_tri = Polygon(
            left_root,
            [left_root[0] - 1.47, left_root[1] - 2, 0],
            [left_root[0] + 1.47, left_root[1] - 2, 0],
        )
        left_tri.set_color(YELLOW)
        self.play(ShowCreation(left_tri))

        # right triangle
        right_root = [max_heap.x + 1.5, max_heap.y - 0.38, 0]
        right_tri = Polygon(
            right_root,
            [right_root[0] - 1.47, right_root[1] - 2, 0],
            [right_root[0] + 1.47, right_root[1] - 2, 0],
        )
        right_tri.set_color(YELLOW)
        self.play(ShowCreation(right_tri))
        self.wait(1)

        # asking
        ask = TextMobject("How can we make the whole tree a Max-Heap?")
        ask.scale(0.9)
        ask.set_color(BLUE)
        ask.shift([0, -2.6, 0])
        self.play(Write(ask))
        self.wait(1.5)

        # fading the problem statement and triangles
        self.play(
            FadeOut(prob_1),
            FadeOut(prob_2),
            FadeOut(prob_3),
            FadeOut(left_tri),
            FadeOut(right_tri),
        )
        self.wait(0.5)

        # drawing the code line
        line = Line([-6.1, 1.45, 0], [-6.1, -2.2, 0])
        self.play(
            FadeOutAndShiftDown(ask, 2*DOWN),
            FadeInFromDown(line)
        )

        # source code
        code = VGroup()
        l1 = TextMobject(
            "def ", "heapify", "(", "root", "):"
        )
        for i, color in zip(l1, [YELLOW_B, PURPLE_C, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l1)

        l2 = TextMobject(
            "   index\\_max ", "= ", "index\\_of\\_max", "("
        )
        for i, color in zip(l2, [BLUE, WHITE, PURPLE_C, WHITE]):
            i.set_color(color)
        code.add(l2)

        l3 = TextMobject(
            "      root", ", ",  "left", "(", "root", "), ", "right", "(", "root", "))"
        )
        for i, color in zip(l3, [BLUE, WHITE, PURPLE_C, WHITE, BLUE, WHITE, PURPLE_C, WHITE, BLUE, WHITE, WHITE]):
            i.set_color(color)
        code.add(l3)

        l4 = TextMobject(
            "   if ", "index\\_max ",  "!= ", "root", ":"
        )
        for i, color in zip(l4, [YELLOW_B, BLUE, WHITE, BLUE]):
            i.set_color(color)
        code.add(l4)

        l5 = TextMobject(
            "      swap", "(", "root", ", ", "index\\_max", ")"
        )
        for i, color in zip(l5, [PURPLE_C, WHITE, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l5)

        l6 = TextMobject(
            "      heapify", "(", "index\\_max", ")"
        )
        for i, color in zip(l6, [PURPLE_C, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l6)

        l7 = TextMobject(
            "   return"
        )
        for i, color in zip(l7, [YELLOW_B]):
            i.set_color(color)
        code.add(l7)

        # drawing the source code
        for i, l in enumerate(code):
            l.to_edge(LEFT, buff=0.7)
            if i >= 3:
                l.shift([0, -0.1, 0])
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.55 * i, 0])

        code.scale(0.85)
        code.shift([0, 1.3, 0])

        for l in code:
            self.play(FadeIn(l), run_time=0.5)
        self.wait(1)

        # calling heapify
        max_heap.heapify(self, 0, code)
        self.wait(1)

        # clearing the heap
        max_heap.clear_heap(self)
        self.wait(0.5)


        # another example
        another = TextMobject("Let's look at another exmaple.")
        another.set_color(GOLD_B)
        another.scale(0.85)
        another.to_edge(LEFT, buff=1)
        another.shift([0, 2, 0])
        self.play(Write(another))
        self.wait(1)
        self.play(FadeOut(another))
        self.wait(0.2)

        # drawing the tree
        arr = [0, 7, 5, 3, 2, 4, 1, 1, -1]
        max_heap = MaxHeap(arr, 3.8, 1.5, hspace=3, node_color=TEAL_E)
        max_heap.arr[0].node_obj.set_color(RED)
        max_heap.sketch_heap(self)
        self.wait(0.7)

        # calling heapify
        max_heap.heapify(self, 0, code)

        self.wait(3)
