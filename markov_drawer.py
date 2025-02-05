#!/usr/bin/env python3
import math
import tkinter as tk
from tkinter import simpledialog

import numpy as np


class MarkovChainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Markov Chain Drawer")

        # Create a button frame at the top.
        top_frame = tk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        self.clear_button = tk.Button(
            top_frame, text="Clear Everything", command=self.clear_all
        )
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create the canvas.
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events, Escape, and CTRL+Z.
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", self.on_escape)
        self.root.bind("<Control-z>", self.undo_last_action)

        # Data structures and variables.
        self.nodes = []  # List of node dicts.
        self.edges = []  # List of edge dicts.
        self.history = []  # History stack for undo.
        self.last_node = None  # For auto-connecting new nodes.
        self.last_created_node = None  # For highlighting the most recently added node.
        self.node_count = 0  # To assign node IDs.
        self.node_radius = 20  # Radius of each node.
        self.drag_source = None  # Source node when dragging.
        self.temp_line = None  # Temporary line drawn during a drag.
        self.results_text_id = None  # Canvas item id for the results text.

    def get_node_at(self, x, y):
        """Return the node dict if (x,y) is inside a node's circle; otherwise, return None."""
        for node in self.nodes:
            dx = x - node["x"]
            dy = y - node["y"]
            if math.hypot(dx, dy) <= self.node_radius:
                return node
        return None

    def create_node(self, x, y):
        """Creates a new node at (x, y), auto-connects it if applicable, and updates highlighting."""
        # Revert the fill color of the last created node (if not the first).
        if self.last_created_node is not None and self.last_created_node["id"] != 0:
            self.canvas.itemconfig(self.last_created_node["circle"], fill="lightblue")

        r = self.node_radius
        color = (
            "green" if self.node_count == 0 else "orange"
        )  # First node green, others orange.
        # Draw the node with a red outline (indicating no outgoing edge yet).
        circle = self.canvas.create_oval(
            x - r, y - r, x + r, y + r, fill=color, outline="red"
        )
        text = self.canvas.create_text(x, y, text=str(self.node_count))
        new_node = {
            "id": self.node_count,
            "x": x,
            "y": y,
            "circle": circle,
            "text": text,
            "has_outgoing": False,
        }
        self.node_count += 1
        self.nodes.append(new_node)

        # Record this action for undo.
        self.history.append({"action": "create_node", "node": new_node})

        # Auto-connect: if a previous node exists, create an edge from it.
        if self.last_node is not None:
            self.draw_edge(self.last_node, new_node)
        self.last_node = new_node
        self.last_created_node = new_node

        self.update_results()

    def on_button_press(self, event):
        """On mouse press: if over an existing node, begin a drag; otherwise, create a node."""
        node = self.get_node_at(event.x, event.y)
        if node is not None:
            self.drag_source = node
            self.temp_line = self.canvas.create_line(
                node["x"],
                node["y"],
                event.x,
                event.y,
                arrow=tk.LAST,
                dash=(4, 2),
                fill="black",
            )
        else:
            self.create_node(event.x, event.y)
            self.drag_source = None
            if self.temp_line is not None:
                self.canvas.delete(self.temp_line)
                self.temp_line = None

    def on_mouse_move(self, event):
        """While dragging, update the temporary line to follow the mouse."""
        if self.drag_source is not None and self.temp_line is not None:
            self.canvas.coords(
                self.temp_line,
                self.drag_source["x"],
                self.drag_source["y"],
                event.x,
                event.y,
            )

    def on_button_release(self, event):
        """On releasing the mouse button, if dragging from a node and over a different node, create an edge."""
        if self.drag_source is not None:
            target = self.get_node_at(event.x, event.y)
            if target is not None and target != self.drag_source:
                self.draw_edge(self.drag_source, target)
            if self.temp_line is not None:
                self.canvas.delete(self.temp_line)
            self.temp_line = None
            self.drag_source = None

    def draw_edge(self, source, target):
        """Draws an edge (arrow) from source to target, asking for a probability.
        If an overlapping edge exists, draws a curved (smooth) line."""
        x1, y1 = source["x"], source["y"]
        x2, y2 = target["x"], target["y"]
        # Check for overlapping edge (same or reverse connection).
        overlap = False
        for edge in self.edges:
            if (
                "source" in edge
                and "target" in edge
                and (
                    (
                        edge["source"]["id"] == source["id"]
                        and edge["target"]["id"] == target["id"]
                    )
                    or (
                        edge["source"]["id"] == target["id"]
                        and edge["target"]["id"] == source["id"]
                    )
                )
            ):
                overlap = True
                break

        if overlap:
            # Compute a control point for a curved line.
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            dx = x2 - x1
            dy = y2 - y1
            length = math.hypot(dx, dy)
            if length == 0:
                length = 1
            perp_x = -dy / length
            perp_y = dx / length
            offset = 20  # Offset magnitude.
            control_x = mid_x + perp_x * offset
            control_y = mid_y + perp_y * offset
            line_id = self.canvas.create_line(
                x1,
                y1,
                control_x,
                control_y,
                x2,
                y2,
                smooth=True,
                splinesteps=36,
                arrow=tk.LAST,
                width=2,
            )
            text_x, text_y = control_x, control_y
        else:
            line_id = self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2)
            text_x = (x1 + x2) / 2
            text_y = (y1 + y2) / 2

        prompt = f"Enter transition probability from node {source['id']} to node {target['id']}:"
        prob = simpledialog.askfloat(
            "Transition Probability", prompt, minvalue=0.0, maxvalue=1.0
        )
        text_id = None
        if prob is not None:
            text_id = self.canvas.create_text(
                text_x, text_y, text=str(prob), fill="red", font=("Arial", 12)
            )
            edge_record = {"source": source, "target": target, "prob": prob}
            self.edges.append(edge_record)
            # Mark the source node as having an outgoing edge.
            source["has_outgoing"] = True
            self.canvas.itemconfig(source["circle"], outline="black")
            # Record this action for undo.
            self.history.append(
                {
                    "action": "create_edge",
                    "edge": edge_record,
                    "line_id": line_id,
                    "text_id": text_id,
                }
            )
        else:
            # If no probability is provided, remove the drawn line.
            self.canvas.delete(line_id)
            line_id = None

        self.update_results()

    def on_escape(self, event):
        """Pressing ESC breaks the auto-connection chain."""
        self.last_node = None

    def undo_last_action(self, event=None):
        """Undo the last action (node or edge creation)."""
        if not self.history:
            return
        last_action = self.history.pop()
        if last_action["action"] == "create_edge":
            # Delete the canvas items for the edge.
            if last_action.get("line_id"):
                self.canvas.delete(last_action["line_id"])
            if last_action.get("text_id"):
                self.canvas.delete(last_action["text_id"])
            # Remove the edge record.
            if last_action["edge"] in self.edges:
                self.edges.remove(last_action["edge"])
            # If this was the only outgoing edge from the source, mark it as not having outgoing edges.
            source = last_action["edge"]["source"]
            outgoing = [
                e
                for e in self.edges
                if e["source"]["id"] == source["id"]
                and e["target"]["id"] != source["id"]
            ]
            if not outgoing:
                self.canvas.itemconfig(source["circle"], outline="red")
                source["has_outgoing"] = False
            self.update_results()
        elif last_action["action"] == "create_node":
            node = last_action["node"]
            # Remove any edges that originate or target this node.
            edges_to_remove = [
                edge
                for edge in self.edges
                if edge["source"]["id"] == node["id"]
                or edge["target"]["id"] == node["id"]
            ]
            for edge in edges_to_remove:
                # For self-loops, an arc and a text label may exist.
                if "arc_id" in edge:
                    self.canvas.delete(edge["arc_id"])
                if "text_id" in edge:
                    self.canvas.delete(edge["text_id"])
                # For normal edges, try to delete the line if recorded in history.
                # (This is a best-effort removal.)
                self.edges.remove(edge)
            # Delete the node’s canvas items.
            self.canvas.delete(node["circle"])
            self.canvas.delete(node["text"])
            if node in self.nodes:
                self.nodes.remove(node)
            # Update last_node and last_created_node if necessary.
            if self.last_created_node and self.last_created_node["id"] == node["id"]:
                if self.nodes:
                    self.last_created_node = self.nodes[-1]
                    self.last_node = self.nodes[-1]
                else:
                    self.last_created_node = None
                    self.last_node = None
            self.update_results()

    def clear_all(self):
        """Clears the canvas and resets all data."""
        self.canvas.delete("all")
        self.nodes = []
        self.edges = []
        self.history = []
        self.last_node = None
        self.last_created_node = None
        self.node_count = 0
        self.results_text_id = None

    def update_self_loops(self):
        """
        For each node, ensure a self-loop exists if the sum of outgoing (non-self-loop) probabilities is less than 1.
        If such a self-loop exists, update its probability and displayed text.
        If the remainder is zero or negative, remove any existing self-loop.
        Self-loops are drawn as an arc above the node.
        """
        for node in self.nodes:
            non_self_loop_sum = sum(
                edge["prob"]
                for edge in self.edges
                if edge["source"]["id"] == node["id"]
                and edge["target"]["id"] != node["id"]
            )
            remainder = 1 - non_self_loop_sum

            # Look for an existing self-loop.
            self_loop_edge = None
            for edge in self.edges:
                if (
                    edge["source"]["id"] == node["id"]
                    and edge["target"]["id"] == node["id"]
                ):
                    self_loop_edge = edge
                    break

            if remainder <= 0 or abs(remainder) < 1e-9:
                if self_loop_edge is not None:
                    if "arc_id" in self_loop_edge:
                        self.canvas.delete(self_loop_edge["arc_id"])
                    if "text_id" in self_loop_edge:
                        self.canvas.delete(self_loop_edge["text_id"])
                    self.edges.remove(self_loop_edge)
            else:
                if self_loop_edge is not None:
                    self_loop_edge["prob"] = remainder
                    if "text_id" in self_loop_edge:
                        self.canvas.itemconfig(
                            self_loop_edge["text_id"], text=f"{remainder:.2f}"
                        )
                else:
                    # Draw a self-loop as an arc above the node.
                    x = node["x"]
                    y = node["y"]
                    r = self.node_radius
                    arc_id = self.canvas.create_arc(
                        x - r,
                        y - 2 * r,
                        x + r,
                        y,
                        start=0,
                        extent=300,
                        style=tk.ARC,
                        outline="black",
                        width=2,
                    )
                    text_id = self.canvas.create_text(
                        x,
                        y - 2 * r,
                        text=f"{remainder:.2f}",
                        fill="red",
                        font=("Arial", 12),
                    )
                    new_self_loop = {
                        "source": node,
                        "target": node,
                        "prob": remainder,
                        "arc_id": arc_id,
                        "text_id": text_id,
                    }
                    self.edges.append(new_self_loop)

    def update_results(self):
        """
        First update self-loops so that each node’s outgoing probabilities sum to 1.
        Then compute and display (in the bottom-right corner) for each ending (absorbing) node:
          - The eventual absorption probability (from node 0).
          - The expected number of steps to reach that node.
        A node is considered absorbing if it has no outgoing edges (other than a self-loop with prob < 1)
        or if it has a self-loop with probability 1.
        """
        self.update_self_loops()

        n = len(self.nodes)
        if n == 0:
            return

        # Sort nodes by id.
        nodes_sorted = sorted(self.nodes, key=lambda node: node["id"])
        id_to_index = {node["id"]: i for i, node in enumerate(nodes_sorted)}

        # Build the transition matrix P.
        P = np.zeros((n, n))

        def is_absorbing(node):
            node_id = node["id"]
            outgoing = [edge for edge in self.edges if edge["source"]["id"] == node_id]
            if len(outgoing) == 0:
                return True
            for edge in outgoing:
                if edge["target"]["id"] == node_id and abs(edge["prob"] - 1) < 1e-9:
                    return True
            return False

        absorbing_indices = []
        transient_indices = []
        for node in nodes_sorted:
            i = id_to_index[node["id"]]
            if is_absorbing(node):
                P[i, i] = 1
                absorbing_indices.append(i)
            else:
                outgoing = [
                    edge for edge in self.edges if edge["source"]["id"] == node["id"]
                ]
                for edge in outgoing:
                    j = id_to_index[edge["target"]["id"]]
                    P[i, j] += edge["prob"]
                transient_indices.append(i)

        start_index = id_to_index.get(0, None)
        results_text = ""
        if start_index is None:
            results_text = "No starting node (id 0) found."
        else:
            if start_index in absorbing_indices:
                results_text += "Node 0: P = 1, E = 0\n"
            else:
                T = transient_indices
                A = absorbing_indices
                if len(T) == 0 or len(A) == 0:
                    results_text += (
                        "Chain is incomplete (missing transient or absorbing states).\n"
                    )
                else:
                    Q = P[np.ix_(T, T)]
                    R = P[np.ix_(T, A)]
                    I = np.eye(len(Q))
                    try:
                        N = np.linalg.inv(I - Q)
                    except np.linalg.LinAlgError:
                        results_text += "Error in inverting (I-Q) matrix.\n"
                        N = None
                    if N is not None:
                        B = N.dot(R)
                        N2 = N.dot(N)
                        try:
                            i0 = T.index(start_index)
                        except ValueError:
                            i0 = None
                        if i0 is not None:
                            for a in A:
                                a_idx_in_R = A.index(a)
                                prob = B[i0, a_idx_in_R]
                                if prob > 0:
                                    expected_steps = N2.dot(R)[i0, a_idx_in_R] / prob
                                    node_id = nodes_sorted[a]["id"]
                                    results_text += f"Node {node_id}: P = {prob:.3f}, E = {expected_steps:.3f}\n"
                                else:
                                    node_id = nodes_sorted[a]["id"]
                                    results_text += f"Node {node_id}: P = 0, E = N/A\n"
                        else:
                            results_text += (
                                "Starting node not found among transient states.\n"
                            )

        # Display the results in the bottom-right corner.
        canvas_width = int(self.canvas.cget("width"))
        canvas_height = int(self.canvas.cget("height"))
        if self.results_text_id is not None:
            self.canvas.itemconfig(self.results_text_id, text=results_text)
        else:
            self.results_text_id = self.canvas.create_text(
                canvas_width - 10,
                canvas_height - 10,
                text=results_text,
                anchor=tk.SE,
                fill="black",
                font=("Arial", 12),
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkovChainApp(root)
    root.mainloop()
