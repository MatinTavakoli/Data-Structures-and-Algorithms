#!/usr/bin/env python

from manimlib.imports import *
import itertools


# TODO make node an object, not a function (add data to it's fields)
class Tree_Node:

    def __init__(self, x, y, node_data=-1, scaling_factor=0.3, node_color=RED):
        self.node_object = Circle()
        self.data_object = TextMobject(str(node_data))
        self.data_object.move_to([x, y, 0])
        self.data = node_data
        self.node_object.move_to([x, y, 0])
        self.node_object.scale(scaling_factor)
        self.node_object.set_color(node_color)
        self.parent = None

    def set_parent(self, parent_node):
        self.parent = parent_node

    def set_data(self, node_data):
        self.data_object = TextMobject(str(node_data))
        self.data_object.move_to([self.node_object.get_x(), self.node_object.get_y(), 0])
        self.data = node_data


class Tree:
    def __init__(self, x, y, hspace=1, vspace=-1):

        self.vertices = VGroup()
        self.edges = VGroup()
        self.edge_data_objects = VGroup()

        #creating nodes!
        node1 = Tree_Node(x + 1 * hspace, y + 0 * vspace)
        node2 = Tree_Node(x - 1 * hspace, y + 1 * vspace)
        node3 = Tree_Node(x + 3 * hspace, y + 1 * vspace)
        node4 = Tree_Node(x - 2 * hspace, y + 2 * 1.25 * vspace)
        node5 = Tree_Node(x - 0 * hspace, y + 2 * 1.25 * vspace)
        node6 = Tree_Node(x + 4 * hspace, y + 2 * 1.25 * vspace)
        node7 = Tree_Node(x - 1 * hspace, y + 3 * 1.35 * vspace)
        node8 = Tree_Node(x + 1 * hspace, y + 3 * 1.35 * vspace)
        node9 = Tree_Node(x + 3 * hspace, y + 3 * 1.35 * vspace)
        self.vertices.add(node1)
        self.vertices.add(node2)
        self.vertices.add(node3)
        self.vertices.add(node4)
        self.vertices.add(node5)
        self.vertices.add(node6)
        self.vertices.add(node7)
        self.vertices.add(node8)
        self.vertices.add(node9)

        # assigning data!
        node1.set_data(2)
        node2.set_data(-1)
        node3.set_data(1)
        node4.set_data(0)
        node5.set_data(5)
        node6.set_data(2)
        node7.set_data(1)
        node8.set_data(7)
        node9.set_data(-3)
        self.edge_data_objects.add(node1.data_object)
        self.edge_data_objects.add(node2.data_object)
        self.edge_data_objects.add(node3.data_object)
        self.edge_data_objects.add(node4.data_object)
        self.edge_data_objects.add(node5.data_object)
        self.edge_data_objects.add(node6.data_object)
        self.edge_data_objects.add(node7.data_object)
        self.edge_data_objects.add(node8.data_object)
        self.edge_data_objects.add(node9.data_object)

        # parenting!
        node9.set_parent(node6)
        node8.set_parent(node5)
        node7.set_parent(node5)
        node6.set_parent(node3)
        node5.set_parent(node2)
        node4.set_parent(node2)
        node3.set_parent(node1)
        node2.set_parent(node1)

        for first_node in self.vertices:
            for second_node in self.vertices:
                if second_node.parent == first_node:
                    edge = Arrow([first_node.node_object.get_x(), first_node.node_object.get_y(), 0],
                                 [second_node.node_object.get_x(), second_node.node_object.get_y(), 0])
                    edge.scale(0.93)
                    self.edges.add(edge)

    def sketch_tree(self, scene):
        for vertice in self.vertices:
            scene.play(Write(vertice.node_object), run_time=0.35)
        scene.wait(1.5)
        for edge in self.edges:
            scene.play(Write(edge), run_time=0.35)
        scene.wait(1.5)
        for data_object in self.edge_data_objects:
            scene.play(Write(data_object), run_time=0.5)


class Tree_Scene(Scene):

    def construct(self):
        # tree = TextMobject("Tree")
        # tree.scale(2)
        # self.play(Write(tree))
        # self.wait(1)
        # self.play(FadeOut(tree))

        # node = create_node(1, 2)
        # self.play(Write(node))

        tree = Tree(1.5, 2.5)
        tree.sketch_tree(self)
