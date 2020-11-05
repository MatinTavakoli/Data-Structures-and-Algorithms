#!/usr/bin/env python

from manimlib.imports import *
import itertools


class TreeNode:

    def __init__(self, x, y, node_data, scaling_factor=0.3, node_color=RED):
        self.parent = None
        self.left = None
        self.right = None
        self.data = node_data

        self.x = x
        self.y = y
        self.right_edge = None
        self.left_edge = None
        self.node_object = Circle()
        self.data_object = TextMobject(str(node_data))
        self.data_object.move_to([x, y, 0])
        self.node_object.move_to([x, y, 0])
        self.node_object.scale(scaling_factor)
        self.node_object.set_color(node_color)

    def set_data(self, node_data):
        self.data_object = TextMobject(str(node_data))
        self.data_object.move_to([self.node_object.get_x(), self.node_object.get_y(), 0])
        self.data = node_data


##################
##################


class Tree:
    def __init__(self, x, y, hspace=1, vspace=-1):

        self.x = x
        self.y = y
        self.hspace = hspace
        self.vspace = vspace

        self.vertices = VGroup()
        self.edges = VGroup()
        self.edge_data_objects = VGroup()
        self.root = None

    def insert(self, value):

        if self.root is None:
            node = TreeNode(self.x, self.y, value)
            self.root = node
            self.vertices.add(node)
            self.edge_data_objects.add(node.data_object)

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
                    self.edge_data_objects.add(node.data_object)
                    edge.scale(0.93)
                    self.edges.add(edge)
                    break

                if value >= current.data:
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
            elif current.data == value:
                node = current
                break
            elif value >= current.data:
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
        self.edge_data_objects.remove(node.data_object)

    def sketch_tree(self, scene):
        scene.play(*[Write(vertice.node_object) for vertice in self.vertices], run_time=1.5)
        scene.wait(1.5)
        for edge in self.edges:
            scene.play(Write(edge), run_time=0.6)
        scene.wait(1.5)
        for data_object in self.edge_data_objects:
            scene.play(Write(data_object), run_time=0.5)


class TreeScene(Scene):

    def construct(self):
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
        code_lines = VGroup()

        code_line1 = TextMobject("\\texttt {public void inOrder(TreeNode node)}")
        code_line1.move_to([-3.45, 2 - 0.6 * 0, 0])
        code_lines.add(code_line1)

        parenthese1 = Text("{")
        parenthese1.move_to([0.2, 2 - 0.6 * 0, 0])
        code_lines.add(parenthese1)

        code_line2 = TextMobject("\\texttt {if (node == null)}")
        code_line2.move_to([-4.5, 2 - 0.6 * 1, 0])
        code_lines.add(code_line2)

        parenthese2 = Text("{")
        parenthese2.move_to([-2.5, 2 - 0.6 * 1, 0])
        code_lines.add(parenthese2)

        code_line3 = TextMobject("\\texttt {return;}")
        code_line3.move_to([-4.35, 2 - 0.6 * 2, 0])
        code_lines.add(code_line3)

        code_line4 = Text("}")
        code_line4.move_to([-6, 2 - 0.6 * 3, 0])
        code_lines.add(code_line4)

        code_line5 = TextMobject("\\texttt {inOrder(node.left);")
        code_line5.move_to([-4.3, 2 - 0.6 * 4, 0])
        code_lines.add(code_line5)

        code_line6 = TextMobject("\\texttt {System.out.println(node.data);")
        code_line6.move_to([-3.2, 2 - 0.6 * 5, 0])
        code_lines.add(code_line6)

        code_line7 = TextMobject("\\texttt {inOrder(node.right);")
        code_line7.move_to([-4.2, 2 - 0.6 * 6, 0])
        code_lines.add(code_line7)

        code_line8 = Text("}")
        code_line8.move_to([-6.7, 2 - 0.6 * 7, 0])
        code_lines.add(code_line8)

        for line in code_lines:
            line.scale(0.75)
            line.set_color(BLUE)
            self.play(Write(line))
