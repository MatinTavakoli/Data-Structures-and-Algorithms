#!/usr/bin/env python

from manimlib.imports import *


class Node:

    def __init__(self, x, y, node_data, scaling_factor=0.3, node_color=RED):

        self.parent = None
        self.left = None
        self.right = None
        self.data = node_data

        self.x = x
        self.y = y
        self.node_object = Circle()
        self.data_object = TextMobject(str(node_data))
        self.data_object.move_to([x, y, 0])
        self.node_object.move_to([x, y, 0])
        self.node_object.scale(scaling_factor)
        self.node_object.set_color(node_color)
        
    def set_data(self, node_data):
        self.data = node_data
        self.data_object = TextMobject(str(node_data))


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
            node = Node(self.x, self.y, value)
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
                    if dir == 'r':
                        node = Node(parent.x + self.hspace, parent.y + self.vspace, value)
                        parent.right = node
                    else:
                        node = Node(parent.x - self.hspace, parent.y + self.vspace, value)
                        parent.left = node

                    node.parent = parent
                    self.vertices.add(node)
                    self.edge_data_objects.add(node.data_object)
                    edge = Arrow([parent.node_object.get_x(), parent.node_object.get_y(), 0],
                                 [node.node_object.get_x(), node.node_object.get_y(), 0])
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


    def sketch_tree(self, scene):
        scene.play(*[Write(v.node_object) for v in self.vertices], run_time=1)
        scene.wait(1)

        scene.play(*[Write(e) for e in self.edges], run_time=1)
        scene.wait(1)

        scene.play(*[Write(d) for d in self.edge_data_objects], run_time=1)
        scene.wait(1)



class Tree_Scene(Scene):

    def construct(self):

        tree = Tree(1.5, 2.5)
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        tree.insert(-1)
        tree.insert(12)
        tree.insert(6)
        tree.sketch_tree(self)
