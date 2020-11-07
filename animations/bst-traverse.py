#!/usr/bin/env python

from manimlib.imports import *
import itertools


class TreeNode:

    def __init__(self, x, y, node_key, scaling_factor=0.3, node_color=RED):
        self.parent = None
        self.left = None
        self.right = None
        self.key = node_key

        self.x = x
        self.y = y
        self.right_edge = None
        self.left_edge = None
        self.node_object = Circle()
        self.key_object = TextMobject(str(node_key))
        self.key_object.move_to([x, y, 0])
        self.node_object.move_to([x, y, 0])
        self.node_object.scale(scaling_factor)
        self.node_object.set_color(node_color)

    def set_key(self, node_key):
        self.key_object = TextMobject(str(node_key))
        self.key_object.move_to([self.node_object.get_x(), self.node_object.get_y(), 0])
        self.key = node_key

    # tree traverses
    def pre_order(self, scene, root, counter):

        if root is None:
            return

        scene.play(root.node_object.set_color, GREEN, root.node_object.set_fill, GREEN, 1, run_time=0.5)
        visited_node = TextMobject(str(root.key))
        visited_node.set_color(BLUE)
        visited_node.move_to([-7 + counter[0], -3, 0])
        scene.play(Write(visited_node))
        print(root.key)
        counter[0] = counter[0] + 1

        scene.wait(1)

        # color new edge
        if root.left_edge is not None:
            scene.play(root.left_edge.set_color, GREEN, run_time=0.5)
            scene.wait(1.5)

        # scene.play(root.node_object.set_color, GREEN, run_time=0.5)
        # scene.wait(1.5)
        #
        # # color new edge
        # if root.left_edge is not None:
        #     scene.play(root.left_edge.set_color, GREEN, run_time=0.5)
        # scene.wait(1.5)

        root.pre_order(scene, root.left, counter)

        # color new edge
        if root.right_edge is not None:
            scene.play(root.right_edge.set_color, GREEN, run_time=0.5)
            scene.wait(1.5)

        root.pre_order(scene, root.right, counter)

    def in_order(self, scene, root, counter):
        if root is None:
            return

        scene.play(root.node_object.set_color, GREEN, run_time=0.5)
        scene.wait(1.5)

        # color new edge
        if root.left_edge is not None:
            scene.play(root.left_edge.set_color, GREEN, run_time=0.5)
            scene.wait(1.5)

        root.in_order(scene, root.left, counter)

        scene.play(root.node_object.set_color, GREEN, root.node_object.set_fill, GREEN, 1, run_time=0.5)
        visited_node = TextMobject(str(root.key))
        visited_node.set_color(BLUE)
        visited_node.move_to([-7 + counter[0], -3, 0])
        scene.play(Write(visited_node))
        print(root.key)
        counter[0] = counter[0] + 1

        scene.wait(1)

        # color new edge
        if root.right_edge is not None:
            scene.play(root.right_edge.set_color, GREEN, run_time=0.5)
            scene.wait(1.5)

        root.in_order(scene, root.right, counter)

    def post_order(self, scene, root, counter):
        if root is None:
            return

        # color new edge
        if root.left_edge is not None:
            scene.play(root.left_edge.set_color, GREEN, run_time=0.5)
            scene.wait(1.5)

        root.post_order(scene, root.left, counter)

        # color new edge
        if root.right_edge is not None:
            scene.play(root.right_edge.set_color, GREEN, run_time=0.5)
            scene.wait(1.5)

        root.post_order(scene, root.right, counter)

        scene.play(root.node_object.set_color, GREEN, root.node_object.set_fill, GREEN, 1, run_time=0.5)
        visited_node = TextMobject(str(root.key))
        visited_node.set_color(BLUE)
        visited_node.move_to([-7 + counter[0], -3, 0])
        scene.play(Write(visited_node))
        print(root.key)
        counter[0] = counter[0] + 1

        scene.wait(1)


class Tree:
    root = None

    def __init__(self, x, y, hspace=1, vspace=-1):

        self.x = x
        self.y = y
        self.hspace = hspace
        self.vspace = vspace

        self.vertices = VGroup()
        self.edges = VGroup()
        self.vertice_key_objects = VGroup()

    def insert(self, value):

        if self.root is None:
            node = TreeNode(self.x, self.y, value)
            self.root = node
            self.vertices.add(node)
            self.vertice_key_objects.add(node.key_object)

        else:

            current = self.root
            parent = None
            dir = None

            while True:

                if current is None:
                    node = None
                    edge = None
                    if dir == 'r':
                        node = TreeNode(parent.x + self.hspace, parent.y + self.vspace, value)
                        parent.right = node
                        edge = Arrow([parent.x, parent.y, 0], [node.x, node.y, 0])
                        parent.right_edge = edge
                    else:
                        node = TreeNode(parent.x - self.hspace, parent.y + self.vspace, value)
                        parent.left = node
                        edge = Arrow([parent.x, parent.y, 0], [node.x, node.y, 0])
                        parent.left_edge = edge

                    node.parent = parent
                    self.vertices.add(node)
                    self.vertice_key_objects.add(node.key_object)
                    edge.scale(0.93)
                    self.edges.add(edge)
                    break

                if value >= current.key:
                    parent = current
                    current = current.right
                    dir = 'r'
                else:
                    parent = current
                    current = current.left
                    dir = 'l'

    def delete(self, value):

        # finding the node
        current = self.root
        node = None
        parent = None
        dir = None

        while True:
            if current is None:
                return
            elif current.key == value:
                node = current
                break
            elif value >= current.key:
                parent = current
                current = current.right
                dir = 'r'
            else:
                parent = current
                current = current.left
                dir = 'l'

        # deleting the node
        if node.parent is None:
            self.root = None
        elif node.right is None and node.left is None:
            if dir == 'r':
                parent.right = None
            else:
                parent.left = None
        elif node.right is None:
            node.left.parent = node.parent
            if dir == 'r':
                parent.right = node.left
            else:
                parent.left = node.left
        elif node.left is None:
            node.right.parent = node.parent
            if dir == 'r':
                parent.right = node.right
            else:
                parent.left = node.right

        else:
            smallest = node.right
            while smallest.left is not None:
                smallest = smallest.left
            node.left.parent = smallest
            smallest.left = node.left
            node.right.parent = parent
            if dir == 'r':
                parent.right = node.right
            else:
                parent.left = node.right

        # deleting the node's graphics
        self.vertices.remove(node)
        self.vertice_key_objects.remove(node.key_object)

    def sketch_tree(self, scene):
        scene.play(*[Write(vertice.node_object) for vertice in self.vertices], run_time=1.5)
        scene.wait(1.5)
        for edge in self.edges:
            scene.play(Write(edge), run_time=0.6)
        scene.wait(1.5)
        for key_object in self.vertice_key_objects:
            scene.play(Write(key_object), run_time=0.5)


# def apply_in_order_code_frame(scene, tree, in_order_code):
#     frame = SurroundingRectangle(in_order_code[0])
#     frame.set_color(YELLOW)
#     scene.play(Write(frame))
#     scene.wait(2)
#     for i in range(1, len(in_order_code)):
#         new_frame = SurroundingRectangle(in_order_code[i])
#         new_frame.set_color(YELLOW)
#         scene.play(Transform(frame, new_frame))
#         scene.wait(2)

class PreOrderScene(Scene):

    def construct(self):

        # tree construction
        tree = Tree(3.5, 2.5)
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(-1)
        tree.insert(12)
        tree.insert(6)
        tree.insert(2)
        tree.insert(10)
        tree.insert(14)
        tree.insert(-2)
        tree.insert(1)
        tree.insert(8)
        tree.insert(11)
        tree.sketch_tree(self)

        self.wait(1.5)

        # pre-order

        # title
        title = TextMobject("pre-order:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)
        self.play(Write(title))
        pre_order_code = VGroup()

        # drawing the code
        l1 = TextMobject("\\textrm{def} ", "\\textrm{preOrder}", "\\textrm{(}", "\\textrm{node}", "\\textrm{):}")
        for i, color in zip(l1, [YELLOW_B, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        pre_order_code.add(l1)

        l2 = TextMobject("    \\textrm{if} ", "\\textrm{node}", " \\textrm{==} ", "\\textrm{None}", "\\textrm{:}")
        for i, color in zip(l2, [YELLOW_B, BLUE, WHITE, YELLOW_B, WHITE]):
            i.set_color(color)
        pre_order_code.add(l2)

        l3 = TextMobject("        \\textrm{return}")
        l3.set_color(YELLOW_B)
        pre_order_code.add(l3)

        l4 = TextMobject("    \\textrm{print}", "\\textrm{(}", "\\textrm{node}", "\\textrm{.}", "\\textrm{key}",
                         "\\textrm{)}")
        for i, color in zip(l4, [BLUE, WHITE, BLUE, WHITE, PURPLE, WHITE]):
            i.set_color(color)
        pre_order_code.add(l4)

        l5 = TextMobject("    \\textrm{preOrder}", "\\textrm{(}", "\\textrm{node}", "\\textrm{.}", "\\textrm{left}",
                         "\\textrm{)}")
        for i, color in zip(l5, [BLUE, WHITE, BLUE, WHITE, PURPLE, WHITE]):
            i.set_color(color)
        pre_order_code.add(l5)

        l6 = TextMobject("    \\textrm{preOrder}", "\\textrm{(}", "\\textrm{node}", "\\textrm{.}", "\\textrm{right}",
                         "\\textrm{)}")
        for i, color in zip(l6, [BLUE, WHITE, BLUE, WHITE, PURPLE, WHITE]):
            i.set_color(color)
        pre_order_code.add(l6)

        # for line in in_order_code:
        #     for part in line:
        #         print(part)
        #         print(dir(part))
        #         part = part.become("\\textrm{}".format(part.tex_string))

        for i, l in enumerate(pre_order_code):
            l.to_edge(LEFT, buff=0.2)
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.5 * i, 0])

        pre_order_code.scale(0.85)
        pre_order_code.shift([0, 1.7, 0])

        self.play(Write(pre_order_code), run_time=2)
        self.wait(0.5)

        # result array
        res_arr = Polygon([-6.5, -3.5, 0], [6.5, -3.5, 0], [6.5, -2.5, 0], [-6.5, -2.5, 0])
        res_arr.set_color(WHITE)
        self.play(Write(res_arr))

        arr_lines = VGroup()
        for i in range(1, 13):
            line = Line([-6.5 + i, -2.5, 0], [-6.5 + i, -3.5, 0])
            arr_lines.add(line)
            self.play(Write(line), rate_func=smooth, run_time=0.2)

        res_text = TextMobject("\\textrm{printed nodes}")
        res_text.move_to([-5, -2, 0])
        self.play(Write(res_text))

        # keeping the current node in the array. starts from 1
        counter = [1]

        # applying the traverse
        tree.root.pre_order(self, tree.root, counter)


class InOrderScene(Scene):

    def construct(self):

        # tree construction
        tree = Tree(3.5, 2.5)
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(-1)
        tree.insert(12)
        tree.insert(6)
        tree.insert(2)
        tree.insert(10)
        tree.insert(14)
        tree.insert(-2)
        tree.insert(1)
        tree.insert(8)
        tree.insert(11)
        tree.sketch_tree(self)

        self.wait(1.5)

        # in-order

        # title
        title = TextMobject("in-order:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)
        self.play(Write(title))

        in_order_code = VGroup()

        # drawing the code
        l1 = TextMobject("\\textrm{def} ", "\\textrm{inOrder}", "\\textrm{(}", "\\textrm{node}", "\\textrm{):}")
        for i, color in zip(l1, [YELLOW_B, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        in_order_code.add(l1)

        l2 = TextMobject("    \\textrm{if} ", "\\textrm{node}", " \\textrm{==} ", "\\textrm{None}", "\\textrm{:}")
        for i, color in zip(l2, [YELLOW_B, BLUE, WHITE, YELLOW_B, WHITE]):
            i.set_color(color)
        in_order_code.add(l2)

        l3 = TextMobject("        \\textrm{return}")
        l3.set_color(YELLOW_B)
        in_order_code.add(l3)

        l4 = TextMobject("    \\textrm{inOrder}", "\\textrm{(}", "\\textrm{node}", "\\textrm{.}", "\\textrm{left}",
                         "\\textrm{)}")
        for i, color in zip(l4, [BLUE, WHITE, BLUE, WHITE, PURPLE, WHITE]):
            i.set_color(color)
        in_order_code.add(l4)

        l5 = TextMobject("    \\textrm{print}", "\\textrm{(}", "\\textrm{node}", "\\textrm{.}", "\\textrm{key}",
                         "\\textrm{)}")
        for i, color in zip(l5, [BLUE, WHITE, BLUE, WHITE, PURPLE, WHITE]):
            i.set_color(color)
        in_order_code.add(l5)

        l6 = TextMobject("    \\textrm{inOrder}", "\\textrm{(}", "\\textrm{node}", "\\textrm{.}", "\\textrm{right}",
                         "\\textrm{)}")
        for i, color in zip(l6, [BLUE, WHITE, BLUE, WHITE, PURPLE, WHITE]):
            i.set_color(color)
        in_order_code.add(l6)

        # for line in in_order_code:
        #     for part in line:
        #         print(part)
        #         print(dir(part))
        #         part = part.become("\\textrm{}".format(part.tex_string))

        for i, l in enumerate(in_order_code):
            l.to_edge(LEFT, buff=0.2)
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.5 * i, 0])

        in_order_code.scale(0.85)
        in_order_code.shift([0, 1.7, 0])

        self.play(Write(in_order_code), run_time=2)
        self.wait(0.5)

        # result array
        res_arr = Polygon([-6.5, -3.5, 0], [6.5, -3.5, 0], [6.5, -2.5, 0], [-6.5, -2.5, 0])
        res_arr.set_color(WHITE)
        self.play(Write(res_arr))

        arr_lines = VGroup()
        for i in range(1, 13):
            line = Line([-6.5 + i, -2.5, 0], [-6.5 + i, -3.5, 0])
            arr_lines.add(line)
            self.play(Write(line), rate_func=smooth, run_time=0.2)

        res_text = TextMobject("\\textrm{printed nodes}")
        res_text.move_to([-5, -2, 0])
        self.play(Write(res_text))

        # keeping the current node in the array. starts from 1
        counter = [1]

        # applying the traverse
        tree.root.in_order(self, tree.root, counter)


class PostOrderScene(Scene):
    def construct(self):

        # tree construction
        tree = Tree(3.5, 2.5)
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(-1)
        tree.insert(12)
        tree.insert(6)
        tree.insert(2)
        tree.insert(10)
        tree.insert(14)
        tree.insert(-2)
        tree.insert(1)
        tree.insert(8)
        tree.insert(11)
        tree.sketch_tree(self)

        self.wait(1.5)

        # post-order

        # title
        title = TextMobject("post-order:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)
        self.play(Write(title))

        post_order_code = VGroup()

        # drawing the code
        l1 = TextMobject("\\textrm{def} ", "\\textrm{postOrder}", "\\textrm{(}", "\\textrm{node}", "\\textrm{):}")
        for i, color in zip(l1, [YELLOW_B, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        post_order_code.add(l1)

        l2 = TextMobject("    \\textrm{if} ", "\\textrm{node}", " \\textrm{==} ", "\\textrm{None}", "\\textrm{:}")
        for i, color in zip(l2, [YELLOW_B, BLUE, WHITE, YELLOW_B, WHITE]):
            i.set_color(color)
        post_order_code.add(l2)

        l3 = TextMobject("        \\textrm{return}")
        l3.set_color(YELLOW_B)
        post_order_code.add(l3)

        l4 = TextMobject("    \\textrm{postOrder}", "\\textrm{(}", "\\textrm{node}", "\\textrm{.}", "\\textrm{left}",
                         "\\textrm{)}")
        for i, color in zip(l4, [BLUE, WHITE, BLUE, WHITE, PURPLE, WHITE]):
            i.set_color(color)
        post_order_code.add(l4)

        l5 = TextMobject("    \\textrm{postOrder}", "\\textrm{(}", "\\textrm{node}", "\\textrm{.}", "\\textrm{right}",
                         "\\textrm{)}")
        for i, color in zip(l5, [BLUE, WHITE, BLUE, WHITE, PURPLE, WHITE]):
            i.set_color(color)
        post_order_code.add(l5)

        l6 = TextMobject("    \\textrm{print}", "\\textrm{(}", "\\textrm{node}", "\\textrm{.}", "\\textrm{key}",
                         "\\textrm{)}")
        for i, color in zip(l6, [BLUE, WHITE, BLUE, WHITE, PURPLE, WHITE]):
            i.set_color(color)
        post_order_code.add(l6)

        # for line in in_order_code:
        #     for part in line:
        #         print(part)
        #         print(dir(part))
        #         part = part.become("\\textrm{}".format(part.tex_string))

        for i, l in enumerate(post_order_code):
            l.to_edge(LEFT, buff=0.2)
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.5 * i, 0])

        post_order_code.scale(0.85)
        post_order_code.shift([0, 1.7, 0])

        self.play(Write(post_order_code), run_time=2)
        self.wait(0.5)

        # result array
        res_arr = Polygon([-6.5, -3.5, 0], [6.5, -3.5, 0], [6.5, -2.5, 0], [-6.5, -2.5, 0])
        res_arr.set_color(WHITE)
        self.play(Write(res_arr))

        arr_lines = VGroup()
        for i in range(1, 13):
            line = Line([-6.5 + i, -2.5, 0], [-6.5 + i, -3.5, 0])
            arr_lines.add(line)
            self.play(Write(line), rate_func=smooth, run_time=0.2)

        res_text = TextMobject("\\textrm{printed nodes}")
        res_text.move_to([-5, -2, 0])
        self.play(Write(res_text))

        # keeping the current node in the array. starts from 1
        counter = [1]

        # applying the traverse
        tree.root.post_order(self, tree.root, counter)