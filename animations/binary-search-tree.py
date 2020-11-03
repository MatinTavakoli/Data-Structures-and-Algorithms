#!/usr/bin/env python

from manimlib.imports import *

#TODO make node an object, not a function (add data to it's fields)
def create_node(x, y, scale=0.4, color=BLUE):
    node = Circle()
    node.move_to([x, y, 0])
    node.scale(0.4)
    node.set_color(BLUE)
    return node

#TODO bring this function to the node class
def write_data(node, data):
    self.play(Write())


def create_tree(x, y, n, hspace=1.5, vspace=-0.4):
    nodes = VGroup()
    for i in range(n):
        node = create_node(x + i * hspace, y * i * vspace)
        nodes.add(node)
    return nodes


class Tree(Scene):

    def construct(self):
        # tree = TextMobject("Tree")
        # tree.scale(2)
        # self.play(Write(tree))
        # self.wait(1)
        # self.play(FadeOut(tree))

        # node = create_node(1, 2)
        # self.play(Write(node))

        tree = create_tree(-5, 2, 5)
        self.play(Write(tree))
