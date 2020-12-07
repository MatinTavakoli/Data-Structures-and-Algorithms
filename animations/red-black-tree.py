#!/usr/bin/env python

from manimlib.imports import *


class RedBlackTreeNode:

    def __init__(self, x, y, node_key, node_color, scaling_factor=0.3):
        self.parent = None
        self.left = None
        self.right = None
        self.key = node_key
        self.node_color = node_color

        self.x = x
        self.y = y
        self.right_edge = None
        self.left_edge = None
        self.node_object = Circle()
        self.key_object = TextMobject(str(node_key))
        self.key_object.move_to([x, y, 0])
        self.node_object.move_to([x, y, 0])
        self.node_object.scale(scaling_factor)
        self.node_object.set_color(self.node_color)

    # tree traverses
    def pre_order(self, scene, root, counter, code):

        if root is None:
            return

        scene.play(root.node_object.set_color, GREEN, run_time=0.5)
        scene.wait(0.75)

        code[3].save_state()
        scene.play(code[3].scale, 1.25, code[3].move_to, [code[3].get_x() + 0.35, code[3].get_y(), 0],
                   code[3].set_color,
                   YELLOW, run_time=1.5)
        scene.wait(0.4)

        scene.play(root.node_object.set_color, GREEN, root.node_object.set_fill, GREEN, 1, run_time=0.25)
        visited_node = TextMobject(str(root.key))
        visited_node.set_color(BLUE)
        visited_node.move_to([-7 + counter[0], -2.8, 0])
        scene.play(Write(visited_node))

        scene.play(Restore(code[3]))

        counter[0] = counter[0] + 1

        scene.wait(0.75)

        # color new edge
        if root.left_edge is not None:
            scene.play(root.left_edge.set_color, GREEN, run_time=0.5)
            scene.wait(0.75)

        root.pre_order(scene, root.left, counter, code)

        # color new edge
        if root.right_edge is not None:
            scene.play(root.right_edge.set_color, GREEN, run_time=0.5)
            scene.wait(0.75)

        root.pre_order(scene, root.right, counter, code)

    def in_order(self, scene, root, counter, code):

        if root is None:
            return

        scene.play(root.node_object.set_color, GREEN, run_time=0.5)
        scene.wait(0.75)

        # color new edge
        if root.left_edge is not None:
            scene.play(root.left_edge.set_color, GREEN, run_time=0.5)
            scene.wait(0.75)

        root.in_order(scene, root.left, counter, code)

        code[4].save_state()
        scene.play(code[4].scale, 1.25, code[4].move_to, [code[4].get_x() + 0.35, code[4].get_y(), 0],
                   code[4].set_color,
                   YELLOW, run_time=1.5)
        scene.wait(0.4)

        scene.play(root.node_object.set_color, GREEN, root.node_object.set_fill, GREEN, 1, run_time=0.25)
        visited_node = TextMobject(str(root.key))
        visited_node.set_color(BLUE)
        visited_node.move_to([-7 + counter[0], -2.8, 0])
        scene.play(Write(visited_node))

        scene.play(Restore(code[4]))

        counter[0] = counter[0] + 1

        scene.wait(0.75)

        # color new edge
        if root.right_edge is not None:
            scene.play(root.right_edge.set_color, GREEN, run_time=0.5)
            scene.wait(0.75)

        root.in_order(scene, root.right, counter, code)

    def post_order(self, scene, root, counter, code):
        if root is None:
            return

        scene.play(root.node_object.set_color, GREEN, run_time=0.5)
        scene.wait(0.75)

        # color new edge
        if root.left_edge is not None:
            scene.play(root.left_edge.set_color, GREEN, run_time=0.5)
            scene.wait(0.75)

        root.post_order(scene, root.left, counter, code)

        # color new edge
        if root.right_edge is not None:
            scene.play(root.right_edge.set_color, GREEN, run_time=0.5)
            scene.wait(0.75)

        root.post_order(scene, root.right, counter, code)

        code[5].save_state()
        scene.play(code[5].scale, 1.25, code[5].move_to, [code[5].get_x() + 0.35, code[5].get_y(), 0],
                   code[5].set_color,
                   YELLOW, run_time=1.5)
        scene.wait(0.4)

        scene.play(root.node_object.set_color, GREEN, root.node_object.set_fill, GREEN, 1, run_time=0.25)
        visited_node = TextMobject(str(root.key))
        visited_node.set_color(BLUE)
        visited_node.move_to([-7 + counter[0], -2.8, 0])
        scene.play(Write(visited_node))

        scene.play(Restore(code[5]))

        counter[0] = counter[0] + 1

        scene.wait(0.75)


class Tree:
    def __init__(self, x, y, hspace=1, vspace=-1):

        self.x = x
        self.y = y
        self.hspace = hspace
        self.vspace = vspace

        self.vertices = VGroup()
        self.edges = VGroup()
        self.edge_key_objects = VGroup()
        self.root = None

    def insert(self, scene, show_sketch, *keys):

        # title
        title = TextMobject("Insert:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)

        # drawing the code line
        line = Line([-6.1, 1.65, 0], [-6.1, -2.3, 0])

        # drawing the code
        code = VGroup()
        l1 = TextMobject("\\textrm{def}", " \\textrm{insert}", "\\textrm{(}", "\\textrm{key}", "\\textrm{,}",
                         " \\textrm{root}", "\\textrm{):}")
        for i, color in zip(l1, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l1)

        l2 = TextMobject("   \\textrm{current}", "\\textrm{ = }", "\\textrm{root}")
        for i, color in zip(l2, [BLUE, WHITE, BLUE]):
            i.set_color(color)
        code.add(l2)

        l3 = TextMobject("   \\textrm{while}", " \\textrm{current }", "\\textrm{!= }", "\\textrm{None}", "\\textrm{:}")
        for i, color in zip(l3, [YELLOW_B, BLUE, WHITE, YELLOW_B, WHITE]):
            i.set_color(color)
        code.add(l3)

        l4 = TextMobject("       \\textrm{if}", " \\textrm{key}", "\\textrm{ >= }", "\\textrm{current}", "\\textrm{.}",
                         "\\textrm{key}", "\\textrm{:}")
        for i, color in zip(l4, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
            i.set_color(color)
        code.add(l4)

        l5 = TextMobject("           \\textrm{current}", "\\textrm{ =}", " \\textrm{current}", "\\textrm{.}",
                         "\\textrm{right}")
        for i, color in zip(l5, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l5)

        l6 = TextMobject("       \\textrm{elif}", " \\textrm{key} ", "\\textrm{< }", "\\textrm{current}", "\\textrm{.}",
                         "\\textrm{key}", "\\textrm{:}")
        for i, color in zip(l6, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l6)

        l7 = TextMobject("           \\textrm{current}", "\\textrm{ =}", "\\textrm{ current}", "\\textrm{.}",
                         "\\textrm{left}")
        for i, color in zip(l7, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l7)

        l8 = TextMobject("   \\textrm{create\_node}", "\\textrm{(}", "\\textrm{key}", "\\textrm{)}")
        for i, color in zip(l8, [BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l8)

        for i, l in enumerate(code):
            l.to_edge(LEFT, buff=0.7)
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.55 * i, 0])

        code.scale(0.85)
        code.shift([0, 1.6, 0])

        if show_sketch:

            scene.play(Write(title))
            scene.play(FadeInFromDown(line))

            for l in code:
                scene.play(FadeInFrom(l, LEFT), run_time=0.5)
            scene.wait(1)

        for key in keys:

            rect = SurroundingRectangle(l1, buff=0.06, color=WHITE)

            if show_sketch:
                # drawing the searched key
                searched = TextMobject(f"Let's insert {key}.")
                searched.shift([0, title.get_y(), 0])
                searched.set_color(GREEN)
                scene.play(Write(searched))
                scene.wait(0.5)

                scene.play(Write(rect))
                scene.wait(1)

                new_rect = SurroundingRectangle(l2, buff=0.06, color=WHITE)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.5)

                scene.wait(1)

            # showing the process on the tree

            if self.root is None:

                node = RedBlackTreeNode(self.x, self.y, key, RED)
                self.root = node
                self.vertices.add(node)
                self.edge_key_objects.add(node.key_object)
                node.node_object.set_color(GREEN)
                node.node_object.set_fill(GREEN, 1)

                if show_sketch:
                    new_rect = SurroundingRectangle(l2, buff=0.06, color=WHITE)
                    scene.play(ReplacementTransform(rect, new_rect))
                    rect = new_rect
                    scene.wait(0.5)

                    new_rect = SurroundingRectangle(l8, buff=0.06, color=GREEN)
                    scene.play(ReplacementTransform(rect, new_rect))
                    rect = new_rect
                    scene.wait(0.7)

                    scene.play(Write(node.node_object))
                    scene.play(Write(node.key_object))

            else:

                current = self.root
                parent = None
                dir = None

                pointer = TextMobject("\^")
                pointer.rotate(PI)
                pointer.move_to([current.node_object.get_x(), current.node_object.get_y() + 0.5, 0])
                pointer.set_color(ORANGE)
                pointer.scale(2)

                if show_sketch:
                    scene.play(
                        current.node_object.set_color, BLUE_C,
                        Write(pointer)
                    )
                    scene.wait(0.3)

                while True:

                    if show_sketch:
                        new_rect = SurroundingRectangle(l3, buff=0.06, color=WHITE)
                        scene.play(ReplacementTransform(rect, new_rect))
                        rect = new_rect
                        scene.wait(0.5)

                    if current is None:
                        node = None
                        edge = None
                        if dir == 'r':
                            node = RedBlackTreeNode(parent.x + self.hspace, parent.y + self.vspace, key, RED)
                            parent.right = node
                            edge = Arrow([parent.x, parent.y, 0], [node.x, node.y, 0])
                            parent.right_edge = edge
                        else:
                            node = RedBlackTreeNode(parent.x - self.hspace, parent.y + self.vspace, key, RED)
                            parent.left = node
                            edge = Arrow([parent.x, parent.y, 0], [node.x, node.y, 0])
                            parent.left_edge = edge

                        node.node_object.set_color(GREEN)
                        node.node_object.set_fill(GREEN, 1)
                        node.parent = parent
                        self.vertices.add(node)
                        self.edge_key_objects.add(node.key_object)
                        edge.scale(0.93)
                        edge.set_color(GREEN)
                        self.edges.add(edge)

                        if show_sketch:
                            new_rect = SurroundingRectangle(l8, buff=0.06, color=GREEN)
                            scene.play(ReplacementTransform(rect, new_rect))
                            rect = new_rect
                            scene.wait(0.5)

                            scene.play(GrowArrow(edge))
                            scene.play(Write(node.node_object))
                            scene.play(Write(node.key_object))

                        break

                    if show_sketch:
                        new_rect = SurroundingRectangle(l4, buff=0.06, color=WHITE)
                        scene.play(ReplacementTransform(rect, new_rect))
                        rect = new_rect
                        scene.wait(0.5)

                    if key >= current.key:
                        parent = current
                        current = current.right
                        dir = 'r'
                        if show_sketch:
                            new_rect = SurroundingRectangle(l5, buff=0.06, color=ORANGE)
                            scene.play(ReplacementTransform(rect, new_rect))
                            rect = new_rect
                            scene.wait(0.7)

                            if parent.right_edge is not None:
                                scene.play(
                                    parent.right_edge.set_color, BLUE_C,
                                    pointer.shift, [self.hspace, self.vspace, 0]
                                )
                                scene.play(current.node_object.set_color, BLUE_C)
                                scene.wait(0.3)

                            else:
                                scene.play(pointer.shift, [self.hspace, self.vspace, 0])
                                scene.wait(0.3)


                    else:

                        if show_sketch:
                            new_rect = SurroundingRectangle(l6, buff=0.06, color=WHITE)
                            scene.play(ReplacementTransform(rect, new_rect))
                            rect = new_rect
                            scene.wait(0.5)

                            new_rect = SurroundingRectangle(l7, buff=0.06, color=ORANGE)
                            scene.play(ReplacementTransform(rect, new_rect))
                            rect = new_rect
                            scene.wait(0.7)

                        parent = current
                        current = current.left
                        dir = 'l'
                        if show_sketch:

                            if parent.left_edge is not None:
                                scene.play(
                                    parent.left_edge.set_color, BLUE_C,
                                    pointer.shift, [-self.hspace, self.vspace, 0]
                                )
                                scene.play(current.node_object.set_color, BLUE_C)
                                scene.wait(0.3)

                            else:
                                scene.play(pointer.shift, [-self.hspace, self.vspace, 0])
                                scene.wait(0.3)

            if show_sketch:
                scene.wait(1)
                self.reset_colors(scene, True)
                scene.play(FadeOut(rect), FadeOut(pointer))
                scene.play(FadeOut(searched))

        if show_sketch:
            scene.wait(1)
            self.reset_colors(scene, True)

    def search(self, scene, *keys, show_sketch=False):

        if show_sketch:
            # title
            title = TextMobject("Search:")
            title.to_edge(LEFT, buff=0.8)
            title.shift([0, 3, 0])
            title.scale(1.2)
            scene.play(Write(title))

            # drawing the code line
            line = Line([-6.1, 1.85, 0], [-6.1, -2.9, 0])
            scene.play(FadeInFromDown(line))

            # drawing the code

            code = VGroup()
            l1 = TextMobject("\\textrm{def }", "\\textrm{search}", "\\textrm{(}", "\\textrm{key}", "\\textrm{,}",
                             "\\textrm{ root}", "\\textrm{):}")
            for i, color in zip(l1, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE]):
                i.set_color(color)
            code.add(l1)

            l2 = TextMobject("   \\textrm{current}", "\\textrm{ = }", "\\textrm{root}")
            for i, color in zip(l2, [BLUE, WHITE, BLUE]):
                i.set_color(color)
            code.add(l2)

            l3 = TextMobject("   \\textrm{while}", " \\textrm{current }", "\\textrm{!= }", "\\textrm{None}",
                             "\\textrm{:}")
            for i, color in zip(l3, [YELLOW_B, BLUE, WHITE, YELLOW_B, WHITE]):
                i.set_color(color)
            code.add(l3)

            l4 = TextMobject("       \\textrm{if}", " \\textrm{key }", "\\textrm{== }", "\\textrm{current}",
                             "\\textrm{.}",
                             "\\textrm{key}", ":")
            for i, color in zip(l4, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
                i.set_color(color)
            code.add(l4)

            l5 = TextMobject("           \\textrm{return}", " \\textrm{current}")
            for i, color in zip(l5, [YELLOW_B, BLUE]):
                i.set_color(color)
            code.add(l5)

            l6 = TextMobject("       \\textrm{if}", " \\textrm{key} ", "\\textrm{> }", "\\textrm{current}",
                             "\\textrm{.}",
                             "\\textrm{key}", "\\textrm{:}")
            for i, color in zip(l6, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
                i.set_color(color)
            code.add(l6)

            l7 = TextMobject("           \\textrm{current}", " \\textrm{=}", " \\textrm{current}", "\\textrm{.}",
                             "\\textrm{right}")
            for i, color in zip(l7, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
                i.set_color(color)
            code.add(l7)

            l8 = TextMobject("       \\textrm{elif}", " \\textrm{key} ", "\\textrm{< }", "\\textrm{current}",
                             "\\textrm{.}",
                             "\\textrm{key}", "\\textrm{:}")
            for i, color in zip(l8, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
                i.set_color(color)
            code.add(l8)

            l9 = TextMobject("           \\textrm{current}", " \\textrm{=}", " \\textrm{current}", "\\textrm{.}",
                             "\\textrm{left}")
            for i, color in zip(l9, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
                i.set_color(color)
            code.add(l9)

            l10 = TextMobject("   \\textrm{return}", " \\textrm{None}")
            for i, color in zip(l10, [YELLOW_B, YELLOW_B]):
                i.set_color(color)
            code.add(l10)

            for i, l in enumerate(code):
                l.to_edge(LEFT, buff=0.7)
                l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.55 * i, 0])

            code.scale(0.85)
            code.shift([0, 1.9, 0])

            for l in code:
                scene.play(FadeInFrom(l, LEFT), run_time=0.5)
            scene.wait(1)

        for key in keys:

            # doing the process on the tree
            current = self.root
            not_found = None

            # with sketch
            if show_sketch:
                # drawing the searched key
                searched = TextMobject(f"Let's search for {key}.")
                searched.shift([0, title.get_y(), 0])
                searched.set_color(GREEN)
                scene.play(Write(searched))
                scene.wait(0.5)

                rect = SurroundingRectangle(l1, buff=0.06, color=WHITE)
                scene.play(Write(rect))
                scene.wait(1)

                new_rect = SurroundingRectangle(l2, buff=0.06, color=WHITE)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.6)

                pointer = TextMobject("\^")
                pointer.rotate(PI)
                pointer.move_to([current.node_object.get_x(), current.node_object.get_y() + 0.5, 0])
                pointer.set_color(ORANGE)
                pointer.scale(2)

                if current is not None:
                    scene.play(
                        current.node_object.set_color, BLUE_C,
                        Write(pointer)
                    )

                while True:

                    new_rect = SurroundingRectangle(l3, buff=0.06, color=WHITE)
                    scene.play(ReplacementTransform(rect, new_rect))
                    rect = new_rect
                    scene.wait(0.6)

                    if current is None:
                        new_rect = SurroundingRectangle(l10, buff=0.06, color=RED)
                        scene.play(ReplacementTransform(rect, new_rect))
                        rect = new_rect
                        scene.wait(0.5)

                        not_found = TextMobject("Not Found!")
                        not_found.set_color(RED)
                        not_found.scale(0.7)
                        not_found.move_to([pointer.get_x(), pointer.get_y() - 0.4, 0])
                        scene.play(Write(not_found))
                        scene.wait(1.5)
                        scene.play(FadeOut(not_found))

                        break

                    else:

                        new_rect = SurroundingRectangle(l4, buff=0.06, color=WHITE)
                        scene.play(ReplacementTransform(rect, new_rect))
                        rect = new_rect
                        scene.wait(0.5)

                        if current.key == key:
                            new_rect = SurroundingRectangle(l5, buff=0.06, color=GREEN)
                            scene.play(ReplacementTransform(rect, new_rect))
                            rect = new_rect
                            scene.wait(0.7)

                            scene.play(
                                current.node_object.set_color, GREEN,
                                current.node_object.set_fill, GREEN, 1
                            )
                            scene.wait(0.5)
                            break

                        else:

                            new_rect = SurroundingRectangle(l6, buff=0.06, color=WHITE)
                            scene.play(ReplacementTransform(rect, new_rect))
                            rect = new_rect
                            scene.wait(0.5)

                            if key >= current.key:

                                new_rect = SurroundingRectangle(l7, buff=0.06, color=ORANGE)
                                scene.play(ReplacementTransform(rect, new_rect))
                                rect = new_rect
                                scene.wait(0.7)

                                if current.right is not None:
                                    scene.play(
                                        current.right_edge.set_color, BLUE_C,
                                        pointer.shift, [self.hspace, self.vspace, 0]
                                    )
                                else:
                                    scene.play(pointer.shift, [self.hspace, self.vspace, 0])

                                current = current.right

                                if current is not None:
                                    scene.play(current.node_object.set_color, BLUE_C)
                                    scene.wait(0.5)

                            else:

                                new_rect = SurroundingRectangle(l8, buff=0.06, color=WHITE)
                                scene.play(ReplacementTransform(rect, new_rect))
                                rect = new_rect
                                scene.wait(0.5)

                                if key < current.key:

                                    new_rect = SurroundingRectangle(l9, buff=0.06, color=ORANGE)
                                    scene.play(ReplacementTransform(rect, new_rect))
                                    rect = new_rect
                                    scene.wait(0.7)

                                    if current.left is not None:
                                        scene.play(
                                            current.left_edge.set_color, BLUE_C,
                                            pointer.shift, [-self.hspace, self.vspace, 0]
                                        )
                                    else:
                                        scene.play(pointer.shift, [-self.hspace, self.vspace, 0])

                                    current = current.left

                                    if current is not None:
                                        scene.play(current.node_object.set_color, BLUE_C)
                                        scene.wait(0.5)

            # no sketch
            else:
                while True:
                    if current is None:
                        break
                    else:
                        if current.key == key:
                            break
                        else:
                            if key >= current.key:
                                current = current.right
                            else:
                                if key < current.key:
                                    current = current.left

            if show_sketch:
                scene.wait(1)
                self.reset_colors(scene, True)
                scene.play(FadeOut(rect), FadeOut(pointer))
                scene.play(FadeOut(searched))
                scene.wait(0.3)
            return current

    def delete(self, scene, *keys):

        # title
        title = TextMobject("Delete:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)
        scene.play(Write(title))
        scene.wait(1)

        for key in keys:

            # drawing the searched key
            searched = TextMobject(f"Let's delete {key}.")
            searched.shift([0, title.get_y(), 0])
            searched.set_color(GREEN)
            scene.play(Write(searched))
            scene.wait(0.5)

            # step 1
            step1 = TextMobject("Step 1: Find the node.")
            step1.set_color(BLUE)
            step1.scale(0.85)
            step1.to_edge(LEFT, 1)
            step1.shift([0, 2, 0])
            scene.play(Write(step1))
            scene.wait(0.5)

            # finding the node
            current = self.root
            node = None
            parent = None
            dir = None

            while True:
                if current is None:
                    return
                elif current.key == key:
                    node = current
                    break
                elif key >= current.key:
                    parent = current
                    current = current.right
                    dir = 'r'
                else:
                    parent = current
                    current = current.left
                    dir = 'l'

            scene.play(
                node.node_object.set_color, GREEN,
                node.node_object.set_fill, GREEN, 1
            )
            scene.wait(1)

            # deleting the node

            # the node is a leaf
            if node.right is None and node.left is None:

                # case 1
                case = TextMobject("Case 1: The node is a leaf.")
                case.set_color(ORANGE)
                case.scale(0.85)
                case.to_edge(LEFT, 1)
                case.shift([0, 1.2, 0])
                case_box = SurroundingRectangle(case, color=ORANGE)
                scene.play(Write(case), Write(case_box))
                scene.wait(1.2)

                # step 2
                step2 = TextMobject("Step 2: Just remove the node!")
                step2.set_color(BLUE)
                step2.scale(0.85)
                step2.to_edge(LEFT, 1)
                step2.shift([0, 0.4, 0])
                scene.play(Write(step2))
                scene.wait(0.7)

                if dir == 'r':
                    parent.right = None
                    self.edges.remove(parent.right_edge)
                    scene.play(
                        FadeOut(parent.right_edge),
                        FadeOut(node.node_object),
                        FadeOut(node.key_object)
                    )
                    parent.right_edge = None

                else:
                    parent.left = None
                    self.edges.remove(parent.left_edge)
                    scene.play(
                        FadeOut(parent.left_edge),
                        FadeOut(node.node_object),
                        FadeOut(node.key_object)
                    )
                    parent.left_edge = None

                if node is self.root:
                    self.root = None

                scene.wait(0.7)
                scene.play(
                    FadeOut(step1),
                    FadeOut(case),
                    FadeOut(case_box),
                    FadeOut(step2)
                )

            # the node has no right child
            elif node.right is None:

                # case 2
                case = TextMobject("Case 2: The node has 1 child.")
                case.set_color(ORANGE)
                case.scale(0.85)
                case.to_edge(LEFT, 1)
                case.shift([0, 1.2, 0])
                case_box = SurroundingRectangle(case, color=ORANGE)
                scene.play(Write(case), Write(case_box))
                scene.wait(1.2)

                # step 2
                step2 = TextMobject("Step 2: Remove the node.")
                step2.set_color(BLUE)
                step2.scale(0.85)
                step2.to_edge(LEFT, 1)
                step2.shift([0, 0.4, 0])
                scene.play(Write(step2))
                scene.wait(0.5)

                node.left.parent = node.parent

                all_nodes_circle = VGroup()
                all_nodes_key = VGroup()
                all_edges = VGroup()
                delta_x = self.hspace
                delta_y = -self.vspace
                self.get_all_subtree(all_nodes_circle, all_nodes_key, all_edges, node.left, delta_x, delta_y)

                self.edges.remove(node.left_edge)
                scene.play(
                    FadeOut(node.left_edge),
                    FadeOut(node.node_object),
                    FadeOut(node.key_object)
                )
                scene.wait(1)

                # step 3
                step3_1 = TextMobject("Step 3: Put the child subtree")
                step3_2 = TextMobject("in the place of the parent.")
                step3_1.set_color(BLUE)
                step3_2.set_color(BLUE)
                step3_1.scale(0.85)
                step3_2.scale(0.85)
                step3_1.to_edge(LEFT, 1)
                step3_2.to_edge(LEFT, 1)
                step3_1.shift([0, -0.3, 0])
                step3_2.shift([0, -0.75, 0])
                scene.play(Write(step3_1))
                scene.play(Write(step3_2))
                scene.wait(0.5)

                scene.play(
                    all_nodes_circle.shift, [delta_x, delta_y, 0],
                    all_nodes_key.shift, [delta_x, delta_y, 0],
                    all_edges.shift, [delta_x, delta_y, 0],
                )
                scene.wait(0.5)

                if dir == 'r':
                    parent.right = node.left
                else:
                    parent.left = node.left

                scene.play(
                    FadeOut(step1),
                    FadeOut(case),
                    FadeOut(case_box),
                    FadeOut(step2),
                    FadeOut(step3_1),
                    FadeOut(step3_2)
                )

            # the node has no left child
            elif node.left is None:

                # case 2
                case = TextMobject("Case 2: The node has 1 child.")
                case.set_color(ORANGE)
                case.scale(0.85)
                case.to_edge(LEFT, 1)
                case.shift([0, 1.2, 0])
                case_box = SurroundingRectangle(case, color=ORANGE)
                scene.play(Write(case), Write(case_box))
                scene.wait(1.2)

                # step 2
                step2 = TextMobject("Step 2: Remove the node.")
                step2.set_color(BLUE)
                step2.scale(0.85)
                step2.to_edge(LEFT, 1)
                step2.shift([0, 0.4, 0])
                scene.play(Write(step2))
                scene.wait(0.5)

                node.right.parent = node.parent

                all_nodes_circle = VGroup()
                all_nodes_key = VGroup()
                all_edges = VGroup()
                delta_x = -self.hspace
                delta_y = -self.vspace
                self.get_all_subtree(all_nodes_circle, all_nodes_key, all_edges, node.right, delta_x, delta_y)

                self.edges.remove(node.right_edge)
                scene.play(
                    FadeOut(node.right_edge),
                    FadeOut(node.node_object),
                    FadeOut(node.key_object)
                )
                scene.wait(1)

                # step 3
                step3_1 = TextMobject("Step 3: Put the child subtree in")
                step3_2 = TextMobject("the place of the deleted parent.")
                step3_1.set_color(BLUE)
                step3_2.set_color(BLUE)
                step3_1.scale(0.85)
                step3_2.scale(0.85)
                step3_1.to_edge(LEFT, 1)
                step3_2.to_edge(LEFT, 1)
                step3_1.shift([0, -0.3, 0])
                step3_2.shift([0, -0.75, 0])
                scene.play(Write(step3_1))
                scene.play(Write(step3_2))
                scene.wait(0.8)

                scene.play(
                    all_nodes_circle.shift, [delta_x, delta_y, 0],
                    all_nodes_key.shift, [delta_x, delta_y, 0],
                    all_edges.shift, [delta_x, delta_y, 0],
                )
                scene.wait(1.2)

                if dir == 'r':
                    parent.right = node.right
                else:
                    parent.left = node.right

                scene.play(
                    FadeOut(step1),
                    FadeOut(case),
                    FadeOut(case_box),
                    FadeOut(step2),
                    FadeOut(step3_1),
                    FadeOut(step3_2)
                )

            # the node has left and right child
            else:

                # case 3
                case = TextMobject("Case 3: The node has 2 children.")
                case.set_color(ORANGE)
                case.scale(0.85)
                case.to_edge(LEFT, 1)
                case.shift([0, 1.2, 0])
                case_box = SurroundingRectangle(case, color=ORANGE)
                scene.play(Write(case), Write(case_box))
                scene.wait(1)

                # step 2
                step2_1 = TextMobject("Step 2: Find the smallest node")
                step2_2 = TextMobject("in the right subtree.")
                step2_1.set_color(BLUE)
                step2_2.set_color(BLUE)
                step2_1.scale(0.85)
                step2_2.scale(0.85)
                step2_1.to_edge(LEFT, 1)
                step2_2.to_edge(LEFT, 1)
                step2_1.shift([0, 0.4, 0])
                step2_2.shift([0, -0.05, 0])
                scene.play(Write(step2_1))
                scene.play(Write(step2_2))
                scene.wait(0.7)

                # finding the smallest node in the right subtree
                depth = 0
                smallest = node.right
                scene.play(
                    smallest.node_object.set_color, BLUE_C,
                    smallest.key_object.set_color, BLUE_C
                )
                while smallest.left is not None:
                    depth += 1
                    scene.play(smallest.left_edge.set_color, BLUE_C)
                    smallest = smallest.left
                    scene.play(
                        smallest.node_object.set_color, BLUE_C,
                        smallest.key_object.set_color, BLUE_C
                    )
                scene.wait(0.6)

                node.left.parent = smallest
                smallest.left = node.left
                node.right.parent = parent

                step3_1 = TextMobject("Step 3: Move the left subtree")
                step3_2 = TextMobject("below that smallest node.")
                step3_1.set_color(BLUE)
                step3_2.set_color(BLUE)
                step3_1.scale(0.85)
                step3_2.scale(0.85)
                step3_1.to_edge(LEFT, 1)
                step3_2.to_edge(LEFT, 1)
                step3_1.shift([0, -0.85, 0])
                step3_2.shift([0, -1.3, 0])
                scene.play(Write(step3_1))
                scene.play(Write(step3_2))
                scene.wait(0.8)

                # moving the left subtree
                all_nodes_circle = VGroup()
                all_nodes_key = VGroup()
                all_edges = VGroup()
                delta_x = 1 - depth * self.hspace
                delta_y = -1 + depth * self.vspace
                self.get_all_subtree(all_nodes_circle, all_nodes_key, all_edges, node.left, delta_x, delta_y)

                self.edges.remove(node.left_edge)
                scene.play(
                    FadeOut(node.left_edge),
                    all_nodes_circle.shift, [delta_x, delta_y, 0],
                    all_nodes_key.shift, [delta_x, delta_y, 0],
                    all_edges.shift, [delta_x, delta_y, 0],
                )
                scene.wait(0.2)

                self.edges.remove(node.left_edge)

                edge = Arrow(
                    [smallest.x, smallest.y, 0],
                    [node.left.x, node.left.y, 0]
                )
                smallest.left_edge = edge
                edge.scale(0.93)
                edge.set_color(BLUE_C)
                self.edges.add(edge)
                scene.play(Write(edge))
                scene.wait(0.7)

                # step 4
                step4_1 = TextMobject("Step 4: Remove the node and put")
                step4_2 = TextMobject("the right subtree in its place.")
                step4_1.set_color(BLUE)
                step4_2.set_color(BLUE)
                step4_1.scale(0.85)
                step4_2.scale(0.85)
                step4_1.to_edge(LEFT, 1)
                step4_2.to_edge(LEFT, 1)
                step4_1.shift([0, -2.1, 0])
                step4_2.shift([0, -2.55, 0])
                scene.play(Write(step4_1))
                scene.play(Write(step4_2))
                scene.wait(0.7)

                # removing the node
                node.right.parent = node.parent

                all_nodes_circle = VGroup()
                all_nodes_key = VGroup()
                all_edges = VGroup()
                delta_x = -self.hspace
                delta_y = -self.vspace
                self.get_all_subtree(all_nodes_circle, all_nodes_key, all_edges, node.right, delta_x, delta_y)

                scene.play(
                    FadeOut(node.right_edge),
                    FadeOut(node.node_object),
                    FadeOut(node.key_object)
                )
                scene.wait(1)

                self.edges.remove(node.right_edge)
                scene.play(
                    all_nodes_circle.shift, [delta_x, delta_y, 0],
                    all_nodes_key.shift, [delta_x, delta_y, 0],
                    all_edges.shift, [delta_x, delta_y, 0],
                )

                if dir == 'r':
                    parent.right = node.left
                else:
                    parent.left = node.left

                scene.wait(1)
                scene.play(
                    FadeOut(step1),
                    FadeOut(case),
                    FadeOut(case_box),
                    FadeOut(step2_1),
                    FadeOut(step2_2),
                    FadeOut(step3_1),
                    FadeOut(step3_2),
                    FadeOut(step4_1),
                    FadeOut(step4_2)
                )

            # deleting the node from the lists
            self.vertices.remove(node)
            self.edge_key_objects.remove(node.key_object)

            self.reset_colors(scene, True)
            scene.play(FadeOut(searched))

        # case 1
        case1 = TextMobject("Case 1: The node is a leaf.")
        case1.set_color(ORANGE)
        case1.scale(0.85)
        case1.to_edge(LEFT, 1)
        case1.shift([0, 1.4, 0])
        case_box1 = SurroundingRectangle(case1, color=ORANGE)
        case_exp1 = TextMobject("Just remove.")
        case_exp1.set_color(BLUE)
        case_exp1.scale(0.85)
        case_exp1.to_edge(LEFT, 1)
        case_exp1.shift([0, 0.7, 0])

        # case 2
        case2 = TextMobject("Case 2: The node has 1 child.")
        case2.set_color(ORANGE)
        case2.scale(0.85)
        case2.to_edge(LEFT, 1)
        case2.shift([0, 0, 0])
        case_box2 = SurroundingRectangle(case2, color=ORANGE)
        case_exp2 = TextMobject("Replace with child.")
        case_exp2.set_color(BLUE)
        case_exp2.scale(0.85)
        case_exp2.to_edge(LEFT, 1)
        case_exp2.shift([0, -0.7, 0])

        # case 3
        case3 = TextMobject("Case 3: The node has 2 children.")
        case3.set_color(ORANGE)
        case3.scale(0.85)
        case3.to_edge(LEFT, 1)
        case3.shift([0, -1.4, 0])
        case_box3 = SurroundingRectangle(case3, color=ORANGE)
        case_exp3 = TextMobject("Merge subtrees and replace.")
        case_exp3.set_color(BLUE)
        case_exp3.scale(0.85)
        case_exp3.to_edge(LEFT, 1)
        case_exp3.shift([0, -2.1, 0])

        scene.play(
            FadeIn(case1),
            FadeIn(case2),
            FadeIn(case3),
            FadeIn(case_exp1),
            FadeIn(case_exp2),
            FadeIn(case_exp3),
            FadeIn(case_box1),
            FadeIn(case_box2),
            FadeIn(case_box3),
        )

    def inorder_successor(self, scene, *keys):

        # title
        title = TextMobject("In-Order Successor:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)

        # drawing the code line
        line = Line([-6.1, 2.2, 0], [-6.1, -3.5, 0])

        # drawing the code
        code = VGroup()
        l1 = TextMobject("\\textrm{def}", " \\textrm{in\_order\_successor}", "\\textrm{(}", "\\textrm{node}",
                         "\\textrm{):}")
        for i, color in zip(l1, [YELLOW_B, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l1)

        l2 = TextMobject("   \\textrm{if}", " \\textrm{node}", "\\textrm{.}", "\\textrm{right}",
                         " \\textrm{is not None}", "\\textrm{:}")
        for i, color in zip(l2, [YELLOW_B, BLUE, WHITE, PURPLE_C, YELLOW_B, WHITE]):
            i.set_color(color)
        code.add(l2)

        l3 = TextMobject("      \\textrm{return}", " \\textrm{min}", "\\textrm{(}", "\\textrm{node}", "\\textrm{.}",
                         "\\textrm{right}", "\\textrm{)}")
        for i, color in zip(l3, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
            i.set_color(color)
        code.add(l3)

        l4 = TextMobject("   \\textrm{else}", "\\textrm{:}")
        for i, color in zip(l4, [YELLOW_B, WHITE]):
            i.set_color(color)
        code.add(l4)

        l5 = TextMobject("      \\textrm{current}", "\\textrm{ =}", " \\textrm{node}")
        for i, color in zip(l5, [BLUE, WHITE, BLUE]):
            i.set_color(color)
        code.add(l5)

        l6 = TextMobject("      \\textrm{parent}", "\\textrm{ =}", " \\textrm{node}", "\\textrm{.}", "\\textrm{parent}")
        for i, color in zip(l6, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l6)

        l7 = TextMobject("      \\textrm{while}", "\\textrm{ parent}", " \\textrm{ is not None}", "\\textrm{:}")
        for i, color in zip(l7, [YELLOW_B, BLUE, YELLOW_B, WHITE]):
            i.set_color(color)
        code.add(l7)

        l8 = TextMobject("         \\textrm{if}", " \\textrm{current}", "\\textrm{ != }", "\\textrm{parent}",
                         "\\textrm{.}", "\\textrm{right}", "\\textrm{:}")
        for i, color in zip(l8, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
            i.set_color(color)
        code.add(l8)

        l9 = TextMobject("            \\textrm{break}")
        for i, color in zip(l9, [YELLOW_B]):
            i.set_color(color)
        code.add(l9)

        l10 = TextMobject("         \\textrm{current}", "\\textrm{ =}", " \\textrm{parent}")
        for i, color in zip(l10, [BLUE, WHITE, BLUE]):
            i.set_color(color)
        code.add(l10)

        l11 = TextMobject("         \\textrm{parent}", "\\textrm{ =}", " \\textrm{parent}", "\\textrm{.}",
                          "\\textrm{parent}")
        for i, color in zip(l11, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l11)

        l12 = TextMobject("      \\textrm{return}", "\\textrm{ parent}")
        for i, color in zip(l12, [YELLOW_B, BLUE]):
            i.set_color(color)
        code.add(l12)

        for i, l in enumerate(code):
            l.to_edge(LEFT, buff=0.7)
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.55 * i, 0])

        code.scale(0.85)
        code.shift([0, 2.4, 0])

        scene.play(Write(title))
        scene.play(FadeInFromDown(line))

        for l in code:
            scene.play(FadeInFrom(l, LEFT), run_time=0.5)
        scene.wait(1)

        for key in keys:

            # drawing the searched key
            searched = TextMobject(f"What's the successor of {key}?")
            searched.shift([2.5, title.get_y(), 0])
            searched.set_color(GREEN)
            scene.play(Write(searched))
            scene.wait(0.5)

            # finding the node
            current = self.root
            node = None
            parent = None
            dir = None

            while True:
                if current is None:
                    return
                elif current.key == key:
                    node = current
                    break
                elif key >= current.key:
                    parent = current
                    current = current.right
                    dir = 'r'
                else:
                    parent = current
                    current = current.left
                    dir = 'l'

            scene.play(
                node.node_object.set_color, GREEN,
                node.node_object.set_fill, GREEN, 1
            )
            scene.wait(1)

            # rectangle
            rect = SurroundingRectangle(l1, buff=0.06, color=WHITE)
            scene.play(Write(rect))
            scene.wait(1)

            new_rect = SurroundingRectangle(l2, buff=0.06, color=WHITE)
            scene.play(ReplacementTransform(rect, new_rect))
            rect = new_rect
            scene.wait(0.6)

            # case 1: the node has right child
            if node.right is not None:

                new_rect = SurroundingRectangle(l3, buff=0.06, color=BLUE_C)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.6)

                # finding the smallest node in the right subtree
                smallest = node.right
                scene.play(
                    smallest.node_object.set_color, BLUE_C,
                    smallest.key_object.set_color, BLUE_C
                )

                while smallest.left is not None:
                    scene.play(smallest.left_edge.set_color, BLUE_C)
                    smallest = smallest.left
                    scene.play(
                        smallest.node_object.set_color, BLUE_C,
                        smallest.key_object.set_color, BLUE_C
                    )

                scene.wait(0.5)
                new_rect = SurroundingRectangle(l3, buff=0.06, color=ORANGE)
                scene.play(
                    smallest.node_object.set_fill, ORANGE, 1,
                    smallest.node_object.set_color, ORANGE,
                    smallest.key_object.set_color, WHITE,
                    ReplacementTransform(rect, new_rect)
                )
                rect = new_rect
                scene.wait(0.6)

                answer = TextMobject(smallest.key_object.get_tex_string())
                answer.set_color(ORANGE)
                answer.next_to(searched, RIGHT, buff=0.25)
                scene.play(TransformFromCopy(smallest.key_object, answer))

                scene.wait(1)
                scene.play(FadeOut(new_rect))
                self.reset_colors(scene, True)
                scene.play(FadeOut(searched), FadeOut(answer))


            else:  # case 2: the node doesn't have a right child

                new_rect = SurroundingRectangle(l4, buff=0.06, color=WHITE)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.4)

                new_rect = SurroundingRectangle(l5, buff=0.06, color=TEAL_D)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.6)

                current = node
                c_pointer = TextMobject("\^")
                c_pointer.rotate(PI)
                c_pointer.move_to([current.node_object.get_x(), current.node_object.get_y() + 0.5, 0])
                c_pointer.set_color(TEAL_D)
                c_pointer.scale(2)
                scene.play(Write(c_pointer))
                scene.wait(0.5)

                new_rect = SurroundingRectangle(l6, buff=0.06, color=PURPLE_C)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.6)

                parent = node.parent
                p_pointer = TextMobject("\^")
                p_pointer.rotate(PI)
                p_pointer.move_to([parent.node_object.get_x(), parent.node_object.get_y() + 0.5, 0])
                p_pointer.set_color(PURPLE_B)
                p_pointer.scale(2)
                scene.play(Write(p_pointer))
                scene.wait(0.5)

                new_rect = SurroundingRectangle(l7, buff=0.06, color=WHITE)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.6)

                # going up left in tree

                while parent is not None:

                    new_rect = SurroundingRectangle(l8, buff=0.06, color=WHITE)
                    scene.play(ReplacementTransform(rect, new_rect))
                    rect = new_rect
                    scene.wait(0.6)

                    if current != parent.right:
                        new_rect = SurroundingRectangle(l9, buff=0.06, color=WHITE)
                        scene.play(ReplacementTransform(rect, new_rect))
                        rect = new_rect
                        scene.wait(0.6)
                        break

                    new_rect = SurroundingRectangle(l10, buff=0.06, color=TEAL_D)
                    scene.play(ReplacementTransform(rect, new_rect))
                    scene.wait(0.6)
                    rect = new_rect
                    scene.play(c_pointer.shift, [-self.hspace, self.hspace, 0])
                    scene.wait(0.6)

                    new_rect = SurroundingRectangle(l11, buff=0.06, color=PURPLE_C)
                    scene.play(ReplacementTransform(rect, new_rect))
                    rect = new_rect
                    scene.play(ReplacementTransform(rect, new_rect))
                    scene.wait(0.6)

                    if parent == parent.parent.right:
                        scene.play(p_pointer.shift, [-self.hspace, self.hspace, 0])
                    else:
                        scene.play(p_pointer.shift, [self.hspace, self.hspace, 0])

                    scene.wait(0.6)
                    parent = parent.parent
                    current = current.parent

                    new_rect = SurroundingRectangle(l7, buff=0.06, color=WHITE)
                    scene.play(ReplacementTransform(rect, new_rect))
                    rect = new_rect
                    scene.wait(0.6)

                new_rect = SurroundingRectangle(l12, buff=0.06, color=ORANGE)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.6)

                scene.play(
                    parent.node_object.set_fill, ORANGE, 1,
                    parent.node_object.set_color, ORANGE,
                    parent.key_object.set_color, WHITE
                )
                scene.wait(0.6)

                answer = TextMobject(parent.key_object.get_tex_string())
                answer.set_color(ORANGE)
                answer.next_to(searched, RIGHT, buff=0.25)
                scene.play(TransformFromCopy(parent.key_object, answer))

                scene.wait(1)
                scene.play(FadeOut(new_rect), FadeOut(c_pointer), FadeOut(p_pointer))
                self.reset_colors(scene, True)
                scene.play(FadeOut(searched), FadeOut(answer))

        all_nodes_circle = VGroup()
        all_nodes_key = VGroup()
        all_edges = VGroup()
        self.get_all_subtree(all_nodes_circle, all_nodes_key, all_edges, self.root)
        all_tree = VGroup(*all_nodes_circle, *all_nodes_key, *all_edges)

        scene.play(FadeOut(line), FadeOut(code), all_tree.shift, [0, 0.5, 0])
        scene.wait(2)

        # case 1
        case1 = TextMobject("Case 1: The node has a right child.")
        case1.set_color(ORANGE)
        case1.scale(0.8)
        case1.to_edge(LEFT, 1)
        case1.shift([0, 1.4, 0])
        case_box1 = SurroundingRectangle(case1, color=ORANGE)
        case_exp1_1 = TextMobject("Find the smallest node in the")
        case_exp1_2 = TextMobject("right subtree.")
        case_exp1_1.set_color(BLUE)
        case_exp1_2.set_color(BLUE)
        case_exp1_1.scale(0.8)
        case_exp1_2.scale(0.8)
        case_exp1_1.to_edge(LEFT, 1)
        case_exp1_2.to_edge(LEFT, 1)
        case_exp1_1.shift([0, 0.7, 0])
        case_exp1_2.shift([0, 0.25, 0])

        # case 2
        case2 = TextMobject("Case 2: The node doesn't have a right child.")
        case2.set_color(ORANGE)
        case2.scale(0.8)
        case2.to_edge(LEFT, 1)
        case2.shift([0, -1.4, 0])
        case_box2 = SurroundingRectangle(case2, color=ORANGE)
        case_exp2_1 = TextMobject("Go up the tree until you are a left child.")
        case_exp2_2 = TextMobject("Select parent of that node.")
        case_exp2_1.set_color(BLUE)
        case_exp2_2.set_color(BLUE)
        case_exp2_1.scale(0.8)
        case_exp2_2.scale(0.8)
        case_exp2_1.to_edge(LEFT, 1)
        case_exp2_2.to_edge(LEFT, 1)
        case_exp2_1.shift([0, -2.1, 0])
        case_exp2_2.shift([0, -2.55, 0])

        scene.play(
            FadeIn(case1),
            FadeIn(case2),
            FadeIn(case_exp1_1),
            FadeIn(case_exp1_2),
            FadeIn(case_exp2_1),
            FadeIn(case_exp2_2),
            FadeIn(case_box1),
            FadeIn(case_box2),
        )

    def inorder_predecessor(self, scene, *keys):

        # title
        title = TextMobject("In-Order Predecessor:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)

        # drawing the code line
        line = Line([-6.1, 2.2, 0], [-6.1, -3.5, 0])

        # drawing the code
        code = VGroup()
        l1 = TextMobject("\\textrm{def}", " \\textrm{in\_order\_predecessor}", "\\textrm{(}", "\\textrm{node}",
                         "\\textrm{):}")
        for i, color in zip(l1, [YELLOW_B, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l1)

        l2 = TextMobject("   \\textrm{if}", " \\textrm{node}", "\\textrm{.}", "\\textrm{left}",
                         " \\textrm{is not None}", "\\textrm{:}")
        for i, color in zip(l2, [YELLOW_B, BLUE, WHITE, PURPLE_C, YELLOW_B, WHITE]):
            i.set_color(color)
        code.add(l2)

        l3 = TextMobject("      \\textrm{return}", " \\textrm{max}", "\\textrm{(}", "\\textrm{node}", "\\textrm{.}",
                         "\\textrm{left}", "\\textrm{)}")
        for i, color in zip(l3, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
            i.set_color(color)
        code.add(l3)

        l4 = TextMobject("   \\textrm{else}", "\\textrm{:}")
        for i, color in zip(l4, [YELLOW_B, WHITE]):
            i.set_color(color)
        code.add(l4)

        l5 = TextMobject("      \\textrm{current}", "\\textrm{ =}", " \\textrm{node}")
        for i, color in zip(l5, [BLUE, WHITE, BLUE]):
            i.set_color(color)
        code.add(l5)

        l6 = TextMobject("      \\textrm{parent}", "\\textrm{ =}", " \\textrm{node}", "\\textrm{.}", "\\textrm{parent}")
        for i, color in zip(l6, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l6)

        l7 = TextMobject("      \\textrm{while}", "\\textrm{ parent}", " \\textrm{ is not None}", "\\textrm{:}")
        for i, color in zip(l7, [YELLOW_B, BLUE, YELLOW_B, WHITE]):
            i.set_color(color)
        code.add(l7)

        l8 = TextMobject("         \\textrm{if}", " \\textrm{current}", "\\textrm{ != }", "\\textrm{parent}",
                         "\\textrm{.}", "\\textrm{left}", "\\textrm{:}")
        for i, color in zip(l8, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
            i.set_color(color)
        code.add(l8)

        l9 = TextMobject("            \\textrm{break}")
        for i, color in zip(l9, [YELLOW_B]):
            i.set_color(color)
        code.add(l9)

        l10 = TextMobject("         \\textrm{current}", "\\textrm{ =}", " \\textrm{parent}")
        for i, color in zip(l10, [BLUE, WHITE, BLUE]):
            i.set_color(color)
        code.add(l10)

        l11 = TextMobject("         \\textrm{parent}", "\\textrm{ =}", " \\textrm{parent}", "\\textrm{.}",
                          "\\textrm{parent}")
        for i, color in zip(l11, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l11)

        l12 = TextMobject("      \\textrm{return}", "\\textrm{ parent}")
        for i, color in zip(l12, [YELLOW_B, BLUE]):
            i.set_color(color)
        code.add(l12)

        for i, l in enumerate(code):
            l.to_edge(LEFT, buff=0.7)
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.55 * i, 0])

        code.scale(0.85)
        code.shift([0, 2.4, 0])

        scene.play(Write(title))
        scene.play(FadeInFromDown(line))

        for l in code:
            scene.play(FadeInFrom(l, LEFT), run_time=0.5)
        scene.wait(1)

        for key in keys:

            # drawing the searched key
            searched = TextMobject(f"What's the predecessor of {key}?")
            searched.shift([2.5, title.get_y(), 0])
            searched.set_color(GREEN)
            scene.play(Write(searched))
            scene.wait(0.5)

            # finding the node
            current = self.root
            node = None
            parent = None
            dir = None

            while True:
                if current is None:
                    return
                elif current.key == key:
                    node = current
                    break
                elif key >= current.key:
                    parent = current
                    current = current.right
                    dir = 'r'
                else:
                    parent = current
                    current = current.left
                    dir = 'l'

            scene.play(
                node.node_object.set_color, GREEN,
                node.node_object.set_fill, GREEN, 1
            )
            scene.wait(1)

            # rectangle
            rect = SurroundingRectangle(l1, buff=0.06, color=WHITE)
            scene.play(Write(rect))
            scene.wait(1)

            new_rect = SurroundingRectangle(l2, buff=0.06, color=WHITE)
            scene.play(ReplacementTransform(rect, new_rect))
            rect = new_rect
            scene.wait(0.6)

            # case 1: the node has left child
            if node.left is not None:

                new_rect = SurroundingRectangle(l3, buff=0.06, color=BLUE_C)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.6)

                # finding the biggest node in the left subtree
                biggest = node.left
                scene.play(
                    biggest.node_object.set_color, BLUE_C,
                    biggest.key_object.set_color, BLUE_C
                )

                while biggest.right is not None:
                    scene.play(biggest.right_edge.set_color, BLUE_C)
                    biggest = biggest.right
                    scene.play(
                        biggest.node_object.set_color, BLUE_C,
                        biggest.key_object.set_color, BLUE_C
                    )

                scene.wait(0.5)
                new_rect = SurroundingRectangle(l3, buff=0.06, color=ORANGE)
                scene.play(
                    biggest.node_object.set_fill, ORANGE, 1,
                    biggest.node_object.set_color, ORANGE,
                    biggest.key_object.set_color, WHITE,
                    ReplacementTransform(rect, new_rect)
                )
                rect = new_rect
                scene.wait(0.6)

                answer = TextMobject(biggest.key_object.get_tex_string())
                answer.set_color(ORANGE)
                answer.next_to(searched, RIGHT, buff=0.25)
                scene.play(TransformFromCopy(biggest.key_object, answer))

                scene.wait(1)
                scene.play(FadeOut(new_rect))
                self.reset_colors(scene, True)
                scene.play(FadeOut(searched), FadeOut(answer))


            else:  # case 2: the node doesn't have a left child

                new_rect = SurroundingRectangle(l4, buff=0.06, color=WHITE)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.4)

                new_rect = SurroundingRectangle(l5, buff=0.06, color=TEAL_D)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.6)

                current = node
                c_pointer = TextMobject("\^")
                c_pointer.rotate(PI)
                c_pointer.move_to([current.node_object.get_x(), current.node_object.get_y() + 0.5, 0])
                c_pointer.set_color(TEAL_D)
                c_pointer.scale(2)
                scene.play(Write(c_pointer))
                scene.wait(0.5)

                new_rect = SurroundingRectangle(l6, buff=0.06, color=PURPLE_C)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.6)

                parent = node.parent
                p_pointer = TextMobject("\^")
                p_pointer.rotate(PI)
                p_pointer.move_to([parent.node_object.get_x(), parent.node_object.get_y() + 0.5, 0])
                p_pointer.set_color(PURPLE_B)
                p_pointer.scale(2)
                scene.play(Write(p_pointer))
                scene.wait(0.5)

                new_rect = SurroundingRectangle(l7, buff=0.06, color=WHITE)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.6)

                # going up right in tree

                while parent is not None:

                    new_rect = SurroundingRectangle(l8, buff=0.06, color=WHITE)
                    scene.play(ReplacementTransform(rect, new_rect))
                    rect = new_rect
                    scene.wait(0.6)

                    if current != parent.left:
                        new_rect = SurroundingRectangle(l9, buff=0.06, color=WHITE)
                        scene.play(ReplacementTransform(rect, new_rect))
                        rect = new_rect
                        scene.wait(0.6)
                        break

                    new_rect = SurroundingRectangle(l10, buff=0.06, color=TEAL_D)
                    scene.play(ReplacementTransform(rect, new_rect))
                    scene.wait(0.6)
                    rect = new_rect
                    scene.play(c_pointer.shift, [self.hspace, self.hspace, 0])
                    scene.wait(0.6)

                    new_rect = SurroundingRectangle(l11, buff=0.06, color=PURPLE_C)
                    scene.play(ReplacementTransform(rect, new_rect))
                    rect = new_rect
                    scene.play(ReplacementTransform(rect, new_rect))
                    scene.wait(0.6)

                    if parent == parent.parent.left:
                        scene.play(p_pointer.shift, [self.hspace, self.hspace, 0])
                    else:
                        scene.play(p_pointer.shift, [-self.hspace, self.hspace, 0])

                    scene.wait(0.6)
                    parent = parent.parent
                    current = current.parent

                    new_rect = SurroundingRectangle(l7, buff=0.06, color=WHITE)
                    scene.play(ReplacementTransform(rect, new_rect))
                    rect = new_rect
                    scene.wait(0.6)

                new_rect = SurroundingRectangle(l12, buff=0.06, color=ORANGE)
                scene.play(ReplacementTransform(rect, new_rect))
                rect = new_rect
                scene.wait(0.6)

                scene.play(
                    parent.node_object.set_fill, ORANGE, 1,
                    parent.node_object.set_color, ORANGE,
                    parent.key_object.set_color, WHITE
                )
                scene.wait(0.6)

                answer = TextMobject(parent.key_object.get_tex_string())
                answer.set_color(ORANGE)
                answer.next_to(searched, RIGHT, buff=0.25)
                scene.play(TransformFromCopy(parent.key_object, answer))

                scene.wait(1)
                scene.play(FadeOut(new_rect), FadeOut(c_pointer), FadeOut(p_pointer))
                self.reset_colors(scene, True)
                scene.play(FadeOut(searched), FadeOut(answer))

        all_nodes_circle = VGroup()
        all_nodes_key = VGroup()
        all_edges = VGroup()
        self.get_all_subtree(all_nodes_circle, all_nodes_key, all_edges, self.root)
        all_tree = VGroup(*all_nodes_circle, *all_nodes_key, *all_edges)

        scene.play(FadeOut(line), FadeOut(code), all_tree.shift, [0.3, 0.5, 0])
        scene.wait(2)

        # case 1
        case1 = TextMobject("Case 1: The node has a left child.")
        case1.set_color(ORANGE)
        case1.scale(0.8)
        case1.to_edge(LEFT, 0.4)
        case1.shift([0, 1.4, 0])
        case_box1 = SurroundingRectangle(case1, color=ORANGE)
        case_exp1_1 = TextMobject("Find the biggest node in the")
        case_exp1_2 = TextMobject("left subtree.")
        case_exp1_1.set_color(BLUE)
        case_exp1_2.set_color(BLUE)
        case_exp1_1.scale(0.8)
        case_exp1_2.scale(0.8)
        case_exp1_1.to_edge(LEFT, 0.4)
        case_exp1_2.to_edge(LEFT, 0.4)
        case_exp1_1.shift([0, 0.7, 0])
        case_exp1_2.shift([0, 0.25, 0])

        # case 2
        case2 = TextMobject("Case 2: The node doesn't have a left child.")
        case2.set_color(ORANGE)
        case2.scale(0.8)
        case2.to_edge(LEFT, 0.4)
        case2.shift([0, -0.9, 0])
        case_box2 = SurroundingRectangle(case2, color=ORANGE)
        case_exp2_1 = TextMobject("Go up the tree until you are a right child.")
        case_exp2_2 = TextMobject("Select parent of that node.")
        case_exp2_1.set_color(BLUE)
        case_exp2_2.set_color(BLUE)
        case_exp2_1.scale(0.8)
        case_exp2_2.scale(0.8)
        case_exp2_1.to_edge(LEFT, 0.4)
        case_exp2_2.to_edge(LEFT, 0.4)
        case_exp2_1.shift([0, -1.6, 0])
        case_exp2_2.shift([0, -2.05, 0])

        scene.play(
            FadeIn(case1),
            FadeIn(case2),
            FadeIn(case_exp1_1),
            FadeIn(case_exp1_2),
            FadeIn(case_exp2_1),
            FadeIn(case_exp2_2),
            FadeIn(case_box1),
            FadeIn(case_box2),
        )

    def left_rotate(self, scene, root):

        current = self.search(scene, root)

        all_left_nodes_circle = VGroup()
        all_left_nodes_key = VGroup()
        all_left_edges = VGroup()
        left_delta_x = -2 * self.hspace
        left_delta_y = self.vspace
        self.get_all_subtree(all_left_nodes_circle, all_left_nodes_key, all_left_edges, current.left, left_delta_x,
                             left_delta_y)

        all_right_nodes_circle = VGroup()
        all_right_nodes_key = VGroup()
        all_right_edges = VGroup()
        right_delta_x = -self.hspace
        right_delta_y = -self.vspace
        self.get_all_subtree(all_right_nodes_circle, all_right_nodes_key, all_right_edges, current.right, right_delta_x,
                             right_delta_y)

        new_left_edge = Arrow(
            [current.right.node_object.get_x() + right_delta_x, current.right.node_object.get_y() + right_delta_y,
             0],
            [current.node_object.get_x() + left_delta_x, current.node_object.get_y() + left_delta_y, 0])

        new_left_edge.scale(0.93)

        if current.right.left is not None:
            all_rightleft_nodes_circle = VGroup()
            all_rightleft_nodes_key = VGroup()
            all_rightleft_edges = VGroup()
            rightleft_delta_x = -self.hspace // 2
            rightleft_delta_y = -self.vspace // 2
            self.get_all_subtree(all_rightleft_nodes_circle, all_rightleft_nodes_key, all_rightleft_edges,
                                 current.right.left,
                                 rightleft_delta_x,
                                 rightleft_delta_y)

            new_leftright_edge = Arrow(
                [current.node_object.get_x() + left_delta_x, current.node_object.get_y() + left_delta_y,
                 0],
                [current.right.left.node_object.get_x() + rightleft_delta_x, current.right.left.node_object.get_y() + rightleft_delta_y, 0])

            new_leftright_edge.scale(0.93)

            scene.play(

                all_left_nodes_circle.shift, [left_delta_x, left_delta_y, 0],
                all_left_nodes_key.shift, [left_delta_x, left_delta_y, 0],
                all_left_edges.shift, [left_delta_x, left_delta_y, 0],

                current.node_object.shift, [left_delta_x, left_delta_y, 0],
                current.key_object.shift, [left_delta_x, left_delta_y, 0],
                current.left_edge.shift, [left_delta_x, left_delta_y, 0],

                all_right_nodes_circle.shift, [right_delta_x, right_delta_y, 0],
                all_right_nodes_key.shift, [right_delta_x, right_delta_y, 0],
                all_right_edges.shift, [right_delta_x, right_delta_y, 0],

                all_rightleft_nodes_circle.shift, [rightleft_delta_x, rightleft_delta_y, 0],
                all_rightleft_nodes_key.shift, [rightleft_delta_x, rightleft_delta_y, 0],
                all_rightleft_edges.shift, [rightleft_delta_x, rightleft_delta_y, 0],

                ReplacementTransform(current.right.left_edge, new_left_edge),
                ReplacementTransform(current.right_edge, new_leftright_edge),

            )

            current.right_edge = new_leftright_edge

        else:
            scene.play(

                all_left_nodes_circle.shift, [left_delta_x, left_delta_y, 0],
                all_left_nodes_key.shift, [left_delta_x, left_delta_y, 0],
                all_left_edges.shift, [left_delta_x, left_delta_y, 0],

                current.node_object.shift, [left_delta_x, left_delta_y, 0],
                current.key_object.shift, [left_delta_x, left_delta_y, 0],
                current.left_edge.shift, [left_delta_x, left_delta_y, 0],

                all_right_nodes_circle.shift, [right_delta_x, right_delta_y, 0],
                all_right_nodes_key.shift, [right_delta_x, right_delta_y, 0],
                all_right_edges.shift, [right_delta_x, right_delta_y, 0],

            )

        current.right.left_edge = new_left_edge

        tmp = current.right.left
        current.right.left = current
        current.parent = current.right
        current.right = tmp

        self.root = current.parent

    def sketch_tree(self, scene):
        scene.play(
            *[Write(v.node_object) for v in self.vertices],
            *[Write(do) for do in self.edge_key_objects],
            run_time=1.5
        )
        scene.play(*[GrowArrow(e) for e in self.edges], run_time=1.5)

    def get_all_subtree(self, all_nodes_circle, all_nodes_key, all_edges, root, delta_x=0, delta_y=0):
        # if delta_x and delta_y are set, nodes' x and y field will be updated
        # this doesn't actully move the nodes!

        if root is None:
            return

        if root.left_edge is not None:
            all_edges.add(root.left_edge)
        self.get_all_subtree(all_nodes_circle, all_nodes_key, all_edges, root.left, delta_x, delta_y)
        all_nodes_circle.add(root.node_object)
        all_nodes_key.add(root.key_object)
        root.x += delta_x
        root.y += delta_y
        if root.right_edge is not None:
            all_edges.add(root.right_edge)
        self.get_all_subtree(all_nodes_circle, all_nodes_key, all_edges, root.right, delta_x, delta_y)

    def reset_colors(self, scene, show_sketch=False):
        if show_sketch:
            changes = []
            for v in self.vertices:
                changes.append(v.node_object.set_fill)
                changes.append(RED)
                changes.append(0)
                changes.append(v.node_object.set_color)
                changes.append(RED)
            for e in self.edges:
                changes.append(e.set_color)
                changes.append(WHITE)
            for edo in self.edge_key_objects:
                changes.append(edo.set_color)
                changes.append(WHITE)
            scene.play(*changes)
        else:
            for v in self.vertices:
                v.node_object.set_color(RED)
                v.node_object.set_fill(RED, 0)
            for e in self.edges:
                e.set_color(WHITE)
            for edo in self.edge_key_objects:
                edo.set_color(WHITE)


class Rotation(Scene):

    def construct(self):
        # Introduction
        title_l1 = TextMobject("Red Black Tree")
        title_l2 = TextMobject("Rotation")
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

        tree = Tree(3.3, 2)
        tree.insert(self, False, 5, 4, 7, 6, -1, 12, 2, 10, 11)
        tree.reset_colors(self)
        self.wait(1)

        tree.sketch_tree(self)
        self.wait(1)

        tree.left_rotate(self, 5)
        self.wait(2)
        tree.left_rotate(self, 7)
        self.wait(2)


class Insert(Scene):

    def construct(self):
        # Introduction
        title_l1 = TextMobject("Binary Search Tree")
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

        tree = Tree(3.3, 2)
        tree.insert(self, False, 5, 4, 7, 6, -1, 12, 2, 10, 11)
        tree.reset_colors(self)
        self.wait(1)

        tree.sketch_tree(self)
        self.wait(1)

        tree.insert(self, True, 1, 12)
        self.wait(2)


class Search(Scene):

    def construct(self):
        # Introduction
        title_l1 = TextMobject("Binary Search Tree")
        title_l2 = TextMobject("Search")
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

        tree = Tree(3.7, 2.5)
        tree.insert(self, False, 5, 3, 7, 6, -1, 12, 2, 10, 1, 8, 11, 9)
        tree.reset_colors(self)
        self.wait(1)

        tree.sketch_tree(self)
        self.wait(1)

        tree.search(self, 11, -4, show_sketch=True)
        self.wait(2)


class Delete(Scene):

    def construct(self):
        # Introduction
        title_l1 = TextMobject("Binary Search Tree")
        title_l2 = TextMobject("Delete")
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
        self.wait(1)

        tree = Tree(3.1, 1.7)
        tree.insert(self, False, 3, 2, 7, 6, 5, -1, 12, 9, 8, 15, 10)
        tree.reset_colors(self)
        self.wait(1)

        tree.sketch_tree(self)
        self.wait(1)

        tree.delete(self, 15, 12, 7)
        self.wait(2)


class InOrderSuccessor(Scene):

    def construct(self):
        # Introduction
        title_l1 = TextMobject("Binary Search Tree")
        title_l2 = TextMobject("In-order Successor")
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
        self.wait(1)

        tree = Tree(3, 2)
        tree.insert(self, False, 9, 10, 11, 16, 14, 13, 15, 2, 1, 6, 4, 8, 7)
        tree.reset_colors(self)
        self.wait(1)

        tree.sketch_tree(self)
        self.wait(1)

        tree.inorder_successor(self, 11, 8, 4)

        self.wait(2)


class InOrderPredecessor(Scene):

    def construct(self):
        # Introduction
        title_l1 = TextMobject("Binary Search Tree")
        title_l2 = TextMobject("In-order Predecessor")
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
        self.wait(1)

        tree = Tree(3, 2)
        tree.insert(self, False, 2, 1, 12, 10, 5, 3, 8, 6, 9, 14, 13, 20, 17, 18)
        tree.reset_colors(self)
        self.wait(1)

        tree.sketch_tree(self)
        self.wait(1)

        tree.inorder_predecessor(self, 10, 3, 18)

        self.wait(2)


class PreOrderScene(Scene):

    def construct(self):

        # Introduction
        title_l1 = TextMobject("Binary Search Tree")
        title_l2 = TextMobject("Pre-order Traversal")
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

        # tree construction
        tree = Tree(2.5, 2.5)
        tree.insert(self, False, 5, 3, 7, -1, 12, 6, 2, 10, 14, -2, 1, 8, 11)
        tree.reset_colors(self)
        tree.sketch_tree(self)
        self.wait(1.5)

        # pre-order

        # title
        title = TextMobject("Pre-order:")
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

        for i, l in enumerate(pre_order_code):
            l.to_edge(LEFT, buff=0.2)
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.55 * i, 0])

        pre_order_code.scale(0.85)
        pre_order_code.shift([0, 1.7, 0])

        self.play(Write(pre_order_code), run_time=2)
        self.wait(0.5)

        # result array
        res_arr = Polygon([-6.5, -3.3, 0], [6.5, -3.3, 0], [6.5, -2.3, 0], [-6.5, -2.3, 0])
        res_arr.set_color(WHITE)
        self.play(Write(res_arr))

        arr_lines = VGroup()
        for i in range(1, 13):
            line = Line([-6.5 + i, -2.3, 0], [-6.5 + i, -3.3, 0])
            arr_lines.add(line)
            self.play(Write(line), rate_func=smooth, run_time=0.2)

        res_text = TextMobject("\\textrm{printed nodes}")
        res_text.move_to([-5, -1.9, 0])
        self.play(Write(res_text))

        # keeping the current node in the array. starts from 1
        counter = [1]

        self.wait(1.2)

        # applying the traverse
        tree.root.pre_order(self, tree.root, counter, pre_order_code)

        self.wait(0.5)
        tree.reset_colors(self, True)
        self.wait(2)


class InOrderScene(Scene):

    def construct(self):

        # Introduction
        title_l1 = TextMobject("Binary Search Tree")
        title_l2 = TextMobject("In-order Traversal")
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

        # tree construction
        tree = Tree(2.5, 2.5)
        tree.insert(self, False, 5, 3, 7, -1, 12, 6, 2, 10, 14, -2, 1, 8, 11)
        tree.reset_colors(self)
        tree.sketch_tree(self)
        self.wait(1.5)

        # in-order

        # title
        title = TextMobject("In-order:")
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

        for i, l in enumerate(in_order_code):
            l.to_edge(LEFT, buff=0.2)
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.55 * i, 0])

        in_order_code.scale(0.85)
        in_order_code.shift([0, 1.7, 0])

        self.play(Write(in_order_code), run_time=2)
        self.wait(0.5)

        # result array
        res_arr = Polygon([-6.5, -3.3, 0], [6.5, -3.3, 0], [6.5, -2.3, 0], [-6.5, -2.3, 0])
        res_arr.set_color(WHITE)
        self.play(Write(res_arr))

        arr_lines = VGroup()
        for i in range(1, 13):
            line = Line([-6.5 + i, -2.3, 0], [-6.5 + i, -3.3, 0])
            arr_lines.add(line)
            self.play(Write(line), rate_func=smooth, run_time=0.2)

        res_text = TextMobject("\\textrm{printed nodes}")
        res_text.move_to([-5, -1.9, 0])
        self.play(Write(res_text))

        # keeping the current node in the array. starts from 1
        counter = [1]

        self.wait(1.2)

        # applying the traverse
        tree.root.in_order(self, tree.root, counter, in_order_code)

        self.wait(0.5)
        tree.reset_colors(self, True)
        self.wait(2)


class PostOrderScene(Scene):
    def construct(self):

        # Introduction
        title_l1 = TextMobject("Binary Search Tree")
        title_l2 = TextMobject("Post-order Traversal")
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

        # tree construction
        tree = Tree(2.5, 2.5)
        tree.insert(self, False, 5, 3, 7, -1, 12, 6, 2, 10, 14, -2, 1, 8, 11)
        tree.reset_colors(self)
        tree.sketch_tree(self)
        self.wait(1.5)

        # post-order

        # title
        title = TextMobject("Post-order:")
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

        for i, l in enumerate(post_order_code):
            l.to_edge(LEFT, buff=0.2)
            l.shift([0.2 * (len(l[0].get_tex_string()) - len(l[0].get_tex_string().lstrip())), -0.55 * i, 0])

        post_order_code.scale(0.85)
        post_order_code.shift([0, 1.7, 0])

        self.play(Write(post_order_code), run_time=2)
        self.wait(0.5)

        # result array
        res_arr = Polygon([-6.5, -3.3, 0], [6.5, -3.3, 0], [6.5, -2.3, 0], [-6.5, -2.3, 0])
        res_arr.set_color(WHITE)
        self.play(Write(res_arr))

        arr_lines = VGroup()
        for i in range(1, 13):
            line = Line([-6.5 + i, -2.3, 0], [-6.5 + i, -3.3, 0])
            arr_lines.add(line)
            self.play(Write(line), rate_func=smooth, run_time=0.2)

        res_text = TextMobject("\\textrm{printed nodes}")
        res_text.move_to([-5, -1.9, 0])
        self.play(Write(res_text))

        # keeping the current node in the array. starts from 1
        counter = [1]

        self.wait(1.2)

        # applying the traverse
        tree.root.post_order(self, tree.root, counter, post_order_code)

        self.wait(0.5)
        tree.reset_colors(self, True)
        self.wait(2)
