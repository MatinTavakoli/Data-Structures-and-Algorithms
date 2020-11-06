#!/usr/bin/env python

from manimlib.imports import *

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

    def insert(self, scene, value, show_sketch=False):

        if self.root is None:
            node = TreeNode(self.x, self.y, value)
            self.root = node
            self.vertices.add(node)
            self.edge_data_objects.add(node.data_object)
            node.node_object.set_color(YELLOW_E)
            if show_sketch:
                scene.play(Write(node.node_object))
                scene.play(Write(node.data_object))

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

                    node.node_object.set_color(YELLOW_E)
                    node.data_object.set_color(YELLOW_E)
                    node.parent = parent
                    self.vertices.add(node)
                    self.edge_data_objects.add(node.data_object)
                    edge.scale(0.93)
                    edge.set_color(YELLOW_E)
                    self.edges.add(edge)

                    if show_sketch:
                        scene.play(GrowArrow(edge))
                        scene.play(Write(node.node_object))
                        scene.play(Write(node.data_object))

                    break

                if show_sketch:
                    scene.play(
                        current.node_object.set_color, YELLOW_E,
                        current.data_object.set_color, YELLOW_E
                    )
                    scene.wait(0.3)

                if value >= current.data:
                    parent = current
                    current = current.right
                    dir = 'r'
                    if show_sketch and parent.right_edge is not None:
                        scene.play(parent.right_edge.set_color, YELLOW_E)
                else:
                    parent = current
                    current = current.left
                    dir = 'l'
                    if show_sketch and parent.left_edge is not None:
                        scene.play(parent.left_edge.set_color, YELLOW_E)

        self.reset_colors(scene, show_sketch)

    
    def search(self, scene, value):

        # title
        title = TextMobject("Search:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)
        scene.play(Write(title))

        # drawing the code line
        line = Line([-6.1, 1.6, 0], [-6.1, -2.4, 0])
        scene.play(FadeInFromDown(line))

        # drawing the code
        lines = [
            "def search(key, root):",
            "   current = root",
            "   while current != None:",
            "       if key == current.key:",
            "           return current",
            "       if key < current.key:",
            "           current = current.left",
            "       else:  key > current.key:",
            "           current = current.right",
            "   return current"
        ]

        code = VGroup()
        for i, l in enumerate(lines):
            t = TextMobject(l)
            t.scale(0.85)
            t.shift([0, 1.4, 0])
            t.set_color(BLUE)
            t.to_edge(LEFT, buff=1.2)
            t.shift([0.2 * (len(l) - len(l.lstrip())), -0.4 * i, 0])
            code.add(t)

        scene.play(FadeInFrom(code, 2 * LEFT), run_time=2)
        scene.wait(0.5)

        # drawing the searched value
        searched = TextMobject(f"Let's search for {value}.")
        searched.shift([0, title.get_y(), 0])
        searched.set_color(GREEN)
        scene.play(Write(searched))
        scene.wait(0.5)


        # showing the process on the tree
        current = self.root
        while True:
            if current is None:
                return
            else:
                scene.play(
                    current.node_object.set_color, YELLOW_E,
                    current.data_object.set_color, YELLOW_E
                )

                if current.data == value:
                    scene.play(
                        current.node_object.set_color, GREEN,
                        current.data_object.set_color, GREEN
                    )
                    break
                elif value >= current.data:
                    if current.right is not None:
                        scene.play(current.right_edge.set_color, YELLOW_E)
                    current = current.right
                    
                else:
                    if current.left is not None:
                        scene.play(current.left_edge.set_color, YELLOW_E)
                    current = current.left


    def delete(self, scene, value):

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

        # the node is a leaf
        if node.right is None and node.left is None:
            if dir == 'r':
                parent.right = None
                self.edges.remove(parent.right_edge)
                scene.play(
                    FadeOut(parent.right_edge),
                    FadeOut(node.node_object),
                    FadeOut(node.data_object)
                )
            else:
                parent.left = None
                self.edges.remove(parent.left_edge)
                scene.play(
                    FadeOut(parent.left_edge),
                    FadeOut(node.node_object),
                    FadeOut(node.data_object)
                )

            if node is self.root:
                self.root = None

        # the node has no right child
        elif node.right is None:
            node.left.parent = node.parent

            all_nodes_circle = VGroup()
            all_nodes_data = VGroup()
            all_edges = VGroup()
            self.get_all_subtree(all_nodes_circle, all_nodes_data, all_edges, node.left)

            self.edges.remove(node.left_edge)
            scene.play(
                FadeOut(node.left_edge),
                FadeOut(node.node_object),
                FadeOut(node.data_object)
            )
            scene.wait(1)

            scene.play(
                all_nodes_circle.shift, [self.hspace, -self.vspace, 0],
                all_nodes_data.shift, [self.hspace, -self.vspace, 0],
                all_edges.shift, [self.hspace, -self.vspace, 0],
            )

            if dir == 'r':
                parent.right = node.left
            else:
                parent.left = node.left

        # the node has no left child
        elif node.left is None:
            node.right.parent = node.parent

            all_nodes_circle = VGroup()
            all_nodes_data = VGroup()
            all_edges = VGroup()
            self.get_all_subtree(all_nodes_circle, all_nodes_data, all_edges, node.right)

            self.edges.remove(node.right_edge)
            scene.play(
                FadeOut(node.right_edge),
                FadeOut(node.node_object),
                FadeOut(node.data_object)
            )
            scene.wait(1)

            scene.play(
                all_nodes_circle.shift, [-self.hspace, -self.vspace, 0],
                all_nodes_data.shift, [-self.hspace, -self.vspace, 0],
                all_edges.shift, [-self.hspace, -self.vspace, 0],
            )

            if dir == 'r':
                parent.right = node.left
            else:
                parent.left = node.left

        # the node has left and right child
        else:
            depth = 0
            smallest = node.right
            scene.play(
                smallest.node_object.set_color, YELLOW_E,
                smallest.data_object.set_color, YELLOW_E
            )
            while smallest.left is not None:
                depth += 1
                scene.play(smallest.left_edge.set_color, YELLOW_E)
                smallest = smallest.left
                scene.play(
                    smallest.node_object.set_color, YELLOW_E,
                    smallest.data_object.set_color, YELLOW_E
                )

            node.left.parent = smallest
            smallest.left = node.left
            node.right.parent = parent

            # moving the left subtree
            all_nodes_circle = VGroup()
            all_nodes_data = VGroup()
            all_edges = VGroup()
            self.get_all_subtree(all_nodes_circle, all_nodes_data, all_edges, node.left)

            self.edges.remove(node.left_edge)
            scene.play(
                FadeOut(node.left_edge),
                all_nodes_circle.shift, [1 - depth * self.hspace, -1 + depth *self.vspace, 0],
                all_nodes_data.shift, [1 - depth * self.hspace, -1 + depth *self.vspace, 0],
                all_edges.shift, [1 - depth * self.hspace, -1 + depth *self.vspace, 0],
            )

            self.edges.remove(node.left_edge)

            edge = Arrow(
                [smallest.x, smallest.y, 0],
                [node.left.x + 1 - depth * self.hspace, node.left.y -1 + depth *self.vspace, 0]
            )
            smallest.left_edge = edge
            edge.scale(0.93)
            edge.set_color(YELLOW_E)
            self.edges.add(edge)
            scene.play(Write(edge))

            # removing the node
            # the node has no left child

            node.right.parent = node.parent

            all_nodes_circle = VGroup()
            all_nodes_data = VGroup()
            all_edges = VGroup()
            self.get_all_subtree(all_nodes_circle, all_nodes_data, all_edges, node.right)

            scene.play(
                FadeOut(node.right_edge),
                FadeOut(node.node_object),
                FadeOut(node.data_object)
            )
            scene.wait(1)

            self.edges.remove(node.right_edge)
            scene.play(
                all_nodes_circle.shift, [-self.hspace, -self.vspace, 0],
                all_nodes_data.shift, [-self.hspace, -self.vspace, 0],
                all_edges.shift, [-self.hspace, -self.vspace, 0],
            )

            if dir == 'r':
                parent.right = node.left
            else:
                parent.left = node.left


        # deleting the node from the lists
        self.vertices.remove(node)
        self.edge_data_objects.remove(node.data_object)

        scene.wait(1)
        self.reset_colors(scene, True)


    def sketch_tree(self, scene):
        scene.play(
            *[Write(v.node_object) for v in self.vertices],
            *[Write(do) for do in self.edge_data_objects],
            run_time=1.5
        )
        scene.play(*[GrowArrow(e) for e in self.edges], run_time=1.5)


    def get_all_subtree(self, all_nodes_circle, all_nodes_data, all_edges, root):
        if root is None:
            return
        
        if root.left_edge is not None:
            all_edges.add(root.left_edge)
        self.get_all_subtree(all_nodes_circle, all_nodes_data,  all_edges, root.left)
        all_nodes_circle.add(root.node_object)
        all_nodes_data.add(root.data_object)
        if root.right_edge is not None:
            all_edges.add(root.right_edge)
        self.get_all_subtree(all_nodes_circle, all_nodes_data,  all_edges, root.right)

    def reset_colors(self, scene, show_sketch=False):
        if show_sketch:
            changes = []
            for v in self.vertices:
                changes.append(v.node_object.set_color)
                changes.append(RED)
            for e in self.edges:
                changes.append(e.set_color)
                changes.append(WHITE)
            for edo in self.edge_data_objects:
                changes.append(edo.set_color)
                changes.append(WHITE)
            scene.play(*changes)
        else:
            for v in self.vertices:
                v.node_object.set_color(RED)
            for e in self.edges:
                e.set_color(WHITE)
            for edo in self.edge_data_objects:
                edo.set_color(WHITE)
            

class TreeScene(Scene):

    def construct(self):
        tree = Tree(3.7, 2.5)

        # SEARCH:
        for v in [5, 3, 7, 6, -1, 12, 2, 10, 1, 8, 11, 9]:
            tree.insert(self, v)
        self.wait(1)

        tree.sketch_tree(self)
        self.wait(1)

        tree.search(self, 8)
        self.wait(2)  

