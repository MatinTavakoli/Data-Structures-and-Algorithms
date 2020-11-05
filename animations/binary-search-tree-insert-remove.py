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
        self.right_edge = None
        self.left_edge = None
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
                    edge = None
                    if dir == 'r':
                        node = Node(parent.x + self.hspace, parent.y + self.vspace, value)
                        parent.right = node
                        edge = Arrow([parent.x, parent.y, 0], [node.x, node.y, 0])
                        parent.right_edge = edge
                    else:
                        node = Node(parent.x - self.hspace, parent.y + self.vspace, value)
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