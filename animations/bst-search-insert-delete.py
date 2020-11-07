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

    def insert(self, scene, show_sketch, *values):

        # title
        title = TextMobject("Insert:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)

        # drawing the code line
        line = Line([-6.1, 1.65, 0], [-6.1, -2.3, 0])

        # drawing the code
        code = VGroup()
        l1 = TextMobject("\\textrm{def}", " \\textrm{insert}", "\\textrm{(}", "\\textrm{key}", "\\textrm{,}", " \\textrm{root}", "\\textrm{):}")
        for i,color in zip(l1, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l1)

        l2 = TextMobject("   \\textrm{current}", "\\textrm{ = }", "\\textrm{root}")
        for i,color in zip(l2, [BLUE, WHITE, BLUE]):
            i.set_color(color)
        code.add(l2)

        l3 = TextMobject("   \\textrm{while}", " \\textrm{current }", "\\textrm{!= }", "\\textrm{None}", "\\textrm{:}")
        for i,color in zip(l3, [YELLOW_B, BLUE, WHITE, YELLOW_B, WHITE]):
            i.set_color(color)
        code.add(l3)

        l4 = TextMobject("       \\textrm{if}",  " \\textrm{key}", "\\textrm{ >= }", "\\textrm{current}", "\\textrm{.}", "\\textrm{key}", "\\textrm{:}")
        for i,color in zip(l4, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
            i.set_color(color)
        code.add(l4)

        l5 = TextMobject("           \\textrm{current}", "\\textrm{ =}", " \\textrm{current}", "\\textrm{.}", "\\textrm{right}")
        for i,color in zip(l5, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l5)

        l6 = TextMobject("       \\textrm{elif}", " \\textrm{key} ",  "\\textrm{< }", "\\textrm{current}", "\\textrm{.}", "\\textrm{key}", "\\textrm{:}")
        for i,color in zip(l6, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l6)

        l7 = TextMobject("           \\textrm{current}", "\\textrm{ =}", "\\textrm{ current}", "\\textrm{.}", "\\textrm{left}")
        for i,color in zip(l7, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l7)

        l8 = TextMobject("   \\textrm{create\_node}", "\\textrm{(}", "\\textrm{key}", "\\textrm{)}")
        for i,color in zip(l8, [BLUE, WHITE, BLUE, WHITE]):
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


        for value in values:

            rect = SurroundingRectangle(l1, buff=0.06, color=WHITE)

            if show_sketch:
                # drawing the searched value
                searched = TextMobject(f"Let's insert {value}.")
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

                node = TreeNode(self.x, self.y, value)
                self.root = node
                self.vertices.add(node)
                self.edge_data_objects.add(node.data_object)
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
                    scene.wait(0.5)

                    scene.play(Write(node.node_object))
                    scene.play(Write(node.data_object))

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
                            node = TreeNode(parent.x + self.hspace, parent.y + self.vspace, value)
                            parent.right = node
                            edge = Arrow([parent.x, parent.y, 0], [node.x, node.y, 0])
                            parent.right_edge = edge
                        else:
                            node = TreeNode(parent.x - self.hspace, parent.y + self.vspace, value)
                            parent.left = node
                            edge = Arrow([parent.x, parent.y, 0], [node.x, node.y, 0])
                            parent.left_edge = edge

                        node.node_object.set_color(GREEN)
                        node.node_object.set_fill(GREEN, 1)
                        node.parent = parent
                        self.vertices.add(node)
                        self.edge_data_objects.add(node.data_object)
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
                            scene.play(Write(node.data_object))

                        break

                    if show_sketch:

                        new_rect = SurroundingRectangle(l4, buff=0.06, color=WHITE)
                        scene.play(ReplacementTransform(rect, new_rect))
                        rect = new_rect
                        scene.wait(0.5)

                    if value >= current.data:
                        parent = current
                        current = current.right
                        dir = 'r'
                        if show_sketch:
                            new_rect = SurroundingRectangle(l5, buff=0.06, color=ORANGE)
                            scene.play(ReplacementTransform(rect, new_rect))
                            rect = new_rect
                            scene.wait(0.5)

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
                            scene.wait(0.5)

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

    
    def search(self, scene, *values):

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
        l1 = TextMobject("\\textrm{def }", "\\textrm{search}", "\\textrm{(}", "\\textrm{key}", "\\textrm{,}", "\\textrm{ root}", "\\textrm{):}")
        for i,color in zip(l1, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, BLUE, WHITE]):
            i.set_color(color)
        code.add(l1)

        l2 = TextMobject("   \\textrm{current}", "\\textrm{ = }", "\\textrm{root}")
        for i,color in zip(l2, [BLUE, WHITE, BLUE]):
            i.set_color(color)
        code.add(l2)

        l3 = TextMobject("   \\textrm{while}", " \\textrm{current }", "\\textrm{!= }", "\\textrm{None}", "\\textrm{:}")
        for i,color in zip(l3, [YELLOW_B, BLUE, WHITE, YELLOW_B, WHITE]):
            i.set_color(color)
        code.add(l3)

        l4 = TextMobject("       \\textrm{if}",  " \\textrm{key }", "\\textrm{== }", "\\textrm{current}", "\\textrm{.}", "\\textrm{key}", ":")
        for i,color in zip(l4, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
            i.set_color(color)
        code.add(l4)

        l5 = TextMobject("           \\textrm{return}", " \\textrm{current}")
        for i,color in zip(l5, [YELLOW_B, BLUE]):
            i.set_color(color)
        code.add(l5)

        l6 = TextMobject("       \\textrm{if}", " \\textrm{key} ",  "\\textrm{> }", "\\textrm{current}", "\\textrm{.}", "\\textrm{key}", "\\textrm{:}")
        for i,color in zip(l6, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
            i.set_color(color)
        code.add(l6)

        l7 = TextMobject("           \\textrm{current}", " \\textrm{=}", " \\textrm{current}", "\\textrm{.}", "\\textrm{right}")
        for i,color in zip(l7, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l7)

        l8 = TextMobject("       \\textrm{elif}", " \\textrm{key} ",  "\\textrm{< }", "\\textrm{current}", "\\textrm{.}", "\\textrm{key}", "\\textrm{:}")
        for i,color in zip(l8, [YELLOW_B, BLUE, WHITE, BLUE, WHITE, PURPLE_C, WHITE]):
            i.set_color(color)
        code.add(l8)

        l9 = TextMobject("           \\textrm{current}", " \\textrm{=}", " \\textrm{current}", "\\textrm{.}", "\\textrm{left}")
        for i,color in zip(l9, [BLUE, WHITE, BLUE, WHITE, PURPLE_C]):
            i.set_color(color)
        code.add(l9)

        l10 = TextMobject("   \\textrm{return}", " \\textrm{None}")
        for i,color in zip(l10, [YELLOW_B, YELLOW_B]):
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

        for value in values:

            # drawing the searched value
            searched = TextMobject(f"Let's search for {value}.")
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
            scene.wait(0.5)
            

            # showing the process on the tree
            current = self.root
            not_found = None

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
                scene.wait(0.5)

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
                    scene.wait(1)
                    scene.play(FadeOut(not_found))

                    break

                else:

                    new_rect = SurroundingRectangle(l4, buff=0.06, color=WHITE)
                    scene.play(ReplacementTransform(rect, new_rect))
                    rect = new_rect
                    scene.wait(0.5)

                    if current.data == value:
                        new_rect = SurroundingRectangle(l5, buff=0.06, color=GREEN)
                        scene.play(ReplacementTransform(rect, new_rect))
                        rect = new_rect
                        scene.wait(0.5)

                        scene.play(
                            current.node_object.set_color, GREEN,
                            current.node_object.set_fill, GREEN, 1
                        )
                        break

                    else:

                        new_rect = SurroundingRectangle(l6, buff=0.06, color=WHITE)
                        scene.play(ReplacementTransform(rect, new_rect))
                        rect = new_rect
                        scene.wait(0.5)

                        if value >= current.data:

                            new_rect = SurroundingRectangle(l7, buff=0.06, color=ORANGE)
                            scene.play(ReplacementTransform(rect, new_rect))
                            rect = new_rect
                            scene.wait(0.5)

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

                            if value < current.data:

                                new_rect = SurroundingRectangle(l9, buff=0.06, color=ORANGE)
                                scene.play(ReplacementTransform(rect, new_rect))
                                rect = new_rect
                                scene.wait(0.5)

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
                                    
            scene.wait(1)
            self.reset_colors(scene, True)
            scene.play(FadeOut(rect), FadeOut(pointer))
            scene.play(FadeOut(searched))
            scene.wait(0.3)


    def delete(self, scene, *values):

        # title
        title = TextMobject("Delete:")
        title.to_edge(LEFT, buff=0.8)
        title.shift([0, 3, 0])
        title.scale(1.2)
        scene.play(Write(title))
        scene.wait(1)

        for value in values:

            # drawing the searched value
            searched = TextMobject(f"Let's delete {value}.")
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
                scene.wait(1)

                # step 2
                step2 = TextMobject("Step 2: Just remove the node!")
                step2.set_color(BLUE)
                step2.scale(0.85)
                step2.to_edge(LEFT, 1)
                step2.shift([0, 0.4, 0])
                scene.play(Write(step2))
                scene.wait(0.5)

                if dir == 'r':
                    parent.right = None
                    self.edges.remove(parent.right_edge)
                    scene.play(
                        FadeOut(parent.right_edge),
                        FadeOut(node.node_object),
                        FadeOut(node.data_object)
                    )
                    parent.right_edge = None

                else:
                    parent.left = None
                    self.edges.remove(parent.left_edge)
                    scene.play(
                        FadeOut(parent.left_edge),
                        FadeOut(node.node_object),
                        FadeOut(node.data_object)
                    )
                    parent.left_edge = None

                if node is self.root:
                    self.root = None

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
                scene.wait(1)

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
                all_nodes_data = VGroup()
                all_edges = VGroup()
                delta_x = self.hspace
                delta_y = -self.vspace
                self.get_all_subtree(all_nodes_circle, all_nodes_data, all_edges, node.left, delta_x, delta_y)

                self.edges.remove(node.left_edge)
                scene.play(
                    FadeOut(node.left_edge),
                    FadeOut(node.node_object),
                    FadeOut(node.data_object)
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
                    all_nodes_data.shift, [delta_x, delta_y, 0],
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
                scene.wait(1)

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
                all_nodes_data = VGroup()
                all_edges = VGroup()
                delta_x = -self.hspace
                delta_y = -self.vspace
                self.get_all_subtree(all_nodes_circle, all_nodes_data, all_edges, node.right, delta_x, delta_y)

                self.edges.remove(node.right_edge)
                scene.play(
                    FadeOut(node.right_edge),
                    FadeOut(node.node_object),
                    FadeOut(node.data_object)
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
                scene.wait(0.5)

                scene.play(
                    all_nodes_circle.shift, [delta_x, delta_y, 0],
                    all_nodes_data.shift, [delta_x, delta_y, 0],
                    all_edges.shift, [delta_x, delta_y, 0],
                )
                scene.wait(0.5)

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
                scene.wait(0.5)

                # finding the smallest node in the right subtree
                depth = 0
                smallest = node.right
                scene.play(
                    smallest.node_object.set_color, BLUE_C,
                    smallest.data_object.set_color, BLUE_C
                )
                while smallest.left is not None:
                    depth += 1
                    scene.play(smallest.left_edge.set_color, BLUE_C)
                    smallest = smallest.left
                    scene.play(
                        smallest.node_object.set_color, BLUE_C,
                        smallest.data_object.set_color, BLUE_C
                    )
                scene.wait(0.5)

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
                scene.wait(0.5)

                # moving the left subtree
                all_nodes_circle = VGroup()
                all_nodes_data = VGroup()
                all_edges = VGroup()
                delta_x = 1 - depth * self.hspace
                delta_y = -1 + depth *self.vspace
                self.get_all_subtree(all_nodes_circle, all_nodes_data, all_edges, node.left, delta_x, delta_y)

                self.edges.remove(node.left_edge)
                scene.play(
                    FadeOut(node.left_edge),
                    all_nodes_circle.shift, [delta_x, delta_y, 0],
                    all_nodes_data.shift, [delta_x, delta_y, 0],
                    all_edges.shift, [delta_x, delta_y, 0],
                )

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
                scene.wait(0.5)

                # removing the node
                node.right.parent = node.parent

                all_nodes_circle = VGroup()
                all_nodes_data = VGroup()
                all_edges = VGroup()
                delta_x = -self.hspace
                delta_y = -self.vspace
                self.get_all_subtree(all_nodes_circle, all_nodes_data, all_edges, node.right, delta_x, delta_y)

                scene.play(
                    FadeOut(node.right_edge),
                    FadeOut(node.node_object),
                    FadeOut(node.data_object)
                )
                scene.wait(1)

                self.edges.remove(node.right_edge)
                scene.play(
                    all_nodes_circle.shift, [delta_x, delta_y, 0],
                    all_nodes_data.shift, [delta_x, delta_y, 0],
                    all_edges.shift, [delta_x, delta_y, 0],
                )

                if dir == 'r':
                    parent.right = node.left
                else:
                    parent.left = node.left

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
            self.edge_data_objects.remove(node.data_object)

            scene.wait(1)
            self.reset_colors(scene, True)

            scene.play(FadeOut(searched))


    def sketch_tree(self, scene):
        scene.play(
            *[Write(v.node_object) for v in self.vertices],
            *[Write(do) for do in self.edge_data_objects],
            run_time=1.5
        )
        scene.play(*[GrowArrow(e) for e in self.edges], run_time=1.5)


    def get_all_subtree(self, all_nodes_circle, all_nodes_data, all_edges, root, delta_x=0, delta_y=0):
        # if delta_x and delta_y are set, nodes' x and y field will be updated
        # this doesn't actully move the nodes!

        if root is None:
            return
        
        if root.left_edge is not None:
            all_edges.add(root.left_edge)
        self.get_all_subtree(all_nodes_circle, all_nodes_data,  all_edges, root.left, delta_x, delta_y)
        all_nodes_circle.add(root.node_object)
        all_nodes_data.add(root.data_object)
        root.x += delta_x
        root.y += delta_y
        if root.right_edge is not None:
            all_edges.add(root.right_edge)
        self.get_all_subtree(all_nodes_circle, all_nodes_data,  all_edges, root.right, delta_x, delta_y)

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
            for edo in self.edge_data_objects:
                changes.append(edo.set_color)
                changes.append(WHITE)
            scene.play(*changes)
        else:
            for v in self.vertices:
                v.node_object.set_color(RED)
                v.node_object.set_fill(RED, 0)
            for e in self.edges:
                e.set_color(WHITE)
            for edo in self.edge_data_objects:
                edo.set_color(WHITE)


class Insert(Scene):

    def construct(self):

        # Introduction
        title_l1 = TextMobject("Binary Search Tree")
        title_l2 = TextMobject("Insert")
        title_l1.scale(1.8)
        title_l2.scale(1.3)
        title_l1.shift([0, 0.5, 0])
        title_l2.shift([0, -0.3, 0])
        creators = TextMobject("Made by Matin Tavakoli \& Hossein Zaredar")
        creators.scale(0.4)
        creators.move_to([5, -3.7, 0])
        self.add(title_l1)
        self.add(title_l2)
        self.wait(2)
        self.play(Write(creators), run_time=0.7)
        self.wait(2)
        self.play(FadeOut(title_l1), FadeOut(title_l2))
        self.wait(2)

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
        title_l2.shift([0, -0.3, 0])
        creators = TextMobject("Made by Matin Tavakoli \& Hossein Zaredar")
        creators.scale(0.4)
        creators.move_to([5, -3.7, 0])
        self.add(title_l1)
        self.add(title_l2)
        self.wait(2)
        self.play(Write(creators), run_time=0.7)
        self.wait(2)
        self.play(FadeOut(title_l1), FadeOut(title_l2))
        self.wait(2)

        tree = Tree(3.7, 2.5)
        tree.insert(self, False, 5, 3, 7, 6, -1, 12, 2, 10, 1, 8, 11, 9)
        tree.reset_colors(self)
        self.wait(1)

        tree.sketch_tree(self)
        self.wait(1)

        tree.search(self, 11, -4)
        self.wait(2)


class Delete(Scene):

    def construct(self):

        # Introduction
        title_l1 = TextMobject("Binary Search Tree")
        title_l2 = TextMobject("Delete")
        title_l1.scale(1.8)
        title_l2.scale(1.3)
        title_l1.shift([0, 0.5, 0])
        title_l2.shift([0, -0.3, 0])
        creators = TextMobject("Made by Matin Tavakoli \& Hossein Zaredar")
        creators.scale(0.4)
        creators.move_to([5, -3.7, 0])
        self.add(title_l1)
        self.add(title_l2)
        self.wait(2)
        self.play(Write(creators), run_time=0.7)
        self.wait(2)
        self.play(FadeOut(title_l1), FadeOut(title_l2))
        self.wait(2)

        tree = Tree(3.1, 1.7)
        for v in [3, 2, 7, 6, 5, -1, 12, 9, 8, 15, 10]:
            tree.insert(self, v)
        tree.reset_colors(self)
        self.wait(1)

        tree.sketch_tree(self)
        self.wait(1)

        tree.delete(self, 15, 12, 7)
        self.wait(2)

