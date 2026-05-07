import tkinter as tk
from tkinter import ttk, scrolledtext

# 🌳 Tree Node
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []


class ExpressionParser:
    def __init__(self):
        self.input = ""
        self.pos = 0

        # LL(1) Parsing Table
        self.table = {
            ('E', 'i'): "TX",
            ('E', '('): "TX",

            ('X', '+'): "+TX",
            ('X', ')'): "ε",
            ('X', '$'): "ε",

            ('T', 'i'): "FY",
            ('T', '('): "FY",

            ('Y', '*'): "*FY",
            ('Y', '+'): "ε",
            ('Y', ')'): "ε",
            ('Y', '$'): "ε",

            ('F', 'i'): "i",
            ('F', '('): "(E)"
        }

    def parse(self, input_string):
        # Preprocess input
        input_string = self.preprocess(input_string)
        original_input = input_string

        stack = ['$', 'E']
        input_string += '$'
        i = 0

        # 🌳 Tree init
        root = TreeNode('E')
        node_stack = [root]

        self.output = []

        # ===== HEADER =====
        self.output.append("══════════════════════════════════════════════")
        self.output.append("         LL(1) PARSER EXECUTION TRACE")
        self.output.append("══════════════════════════════════════════════\n")

        self.output.append(f"🔹 Original Input   : {original_input}")
        self.output.append(f"🔹 Processed Input  : {input_string}")
        self.output.append(f"🔹 Start Symbol     : E")
        self.output.append(f"🔹 Parsing Method   : Table-Driven LL(1)\n")

        # Table Header
        self.output.append("Step | Stack        | Input        | Action")
        self.output.append("──── | ──────────── | ──────────── | ─────────────────────────")

        step = 1

        while len(stack) > 0:
            stack_str = ''.join(stack)
            remaining_input = input_string[i:] if i < len(input_string) else ""

            # SAFETY CHECK
            if i >= len(input_string):
                raise ValueError("Unexpected end of input")

            top = stack[-1]
            current = input_string[i]

            log_line = f"{step:<4} | {stack_str:<12} | {remaining_input:<12} | "

            # ===== CASE 1: MATCH TERMINAL =====
            if top == current:
                stack.pop()

                if node_stack:
                    node_stack.pop()

                i += 1
                log_line += f"✔ Matched terminal '{current}'"

            # ===== CASE 2: NON-TERMINAL =====
            elif top in ['E', 'X', 'T', 'Y', 'F']:
                production = self.table.get((top, current))

                if not production:
                    log_line += f"✖ ERROR: No rule for ({top}, {current})"
                    self.output.append(log_line)
                    raise ValueError(f"Parsing error at symbol '{current}'")

                stack.pop()

                current_node = node_stack.pop() if node_stack else None

                if production != "ε":
                    new_nodes = []
                    for symbol in production:
                        child = TreeNode(symbol)
                        new_nodes.append(child)

                    if current_node:
                        current_node.children = new_nodes

                    for node in reversed(new_nodes):
                        stack.append(node.value)
                        node_stack.append(node)

                log_line += f"{top} → {production}"

            # ===== CASE 3: INVALID =====
            else:
                log_line += f"✖ INVALID SYMBOL '{top}'"
                self.output.append(log_line)
                raise ValueError("Invalid symbol in parsing")

            self.output.append(log_line)
            step += 1

        # ===== FINAL RESULT =====
        self.output.append("\n══════════════════════════════════════════════")

        if len(stack) == 0 and i == len(input_string):
            self.output.append("✅ FINAL RESULT: STRING ACCEPTED")
        else:
            self.output.append("❌ FINAL RESULT: STRING REJECTED")

        self.output.append("══════════════════════════════════════════════")

        # STORE TREE
        self.tree_root = root

        return "\n".join(self.output)

    def preprocess(self, expr):
        """
        Handles:
        - spaces
        - multi-digit numbers
        - safe normalization
        """
        result = ""
        i = 0

        while i < len(expr):
            # remove spaces
            if expr[i].isspace():
                i += 1
                continue

            # numbers → 'i'
            if expr[i].isdigit():
                while i < len(expr) and expr[i].isdigit():
                    i += 1
                result += 'i'
            else:
                result += expr[i]
                i += 1

        return result


class ParserGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Parser Studio")
        self.master.geometry("1000x650")
        self.master.configure(bg="#020617")

        self.parser = ExpressionParser()

        self.create_widgets()

    def create_widgets(self):
        # ===== HEADER =====
        header = tk.Frame(self.master, bg="#020617")
        header.pack(fill="x", pady=10)

        tk.Label(header, text="⚡ Parser Studio",
                 font=("Segoe UI", 20, "bold"),
                 bg="#020617", fg="#38bdf8").pack()

        tk.Label(header, text="Recursive Descent Parser • Live Analyzer",
                 font=("Segoe UI", 10),
                 bg="#020617", fg="#94a3b8").pack()

        # ===== MAIN CONTAINER =====
        container = tk.Frame(self.master, bg="#020617")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # ===== LEFT PANEL =====
        left = tk.Frame(container, bg="#0f172a")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="Input",
                 font=("Segoe UI", 12, "bold"),
                 bg="#0f172a", fg="#e2e8f0").pack(anchor="w", padx=10, pady=5)

        self.input_entry = tk.Entry(
            left,
            font=("Consolas", 13),
            bg="#020617",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.input_entry.pack(fill="x", padx=10, pady=5, ipady=8)

        # Live parsing
        self.input_entry.bind("<KeyRelease>", self.live_parse)
        self.input_entry.bind("<Return>", lambda e: self.parse_expression())

        # Buttons
        btn_frame = tk.Frame(left, bg="#0f172a")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Parse",
                  font=("Segoe UI", 10, "bold"),
                  bg="#22c55e", fg="white",
                  relief="flat",
                  command=self.parse_expression).grid(row=0, column=0, padx=5, ipadx=10, ipady=4)

        tk.Button(btn_frame, text="Clear",
                  font=("Segoe UI", 10),
                  bg="#334155", fg="white",
                  relief="flat",
                  command=self.clear_all).grid(row=0, column=1, padx=5, ipadx=10, ipady=4)

        tk.Button(btn_frame, text="Show Tree",
                  font=("Segoe UI", 10),
                  bg="#9333ea", fg="white",
                  relief="flat",
                  command=self.show_tree).grid(row=0, column=2, padx=5, ipadx=10, ipady=4)

        # ===== RIGHT PANEL =====
        right = tk.Frame(container, bg="#0f172a")
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="Output",
                 font=("Segoe UI", 12, "bold"),
                 bg="#0f172a", fg="#e2e8f0").pack(anchor="w", padx=10, pady=5)

        self.output_area = scrolledtext.ScrolledText(
            right,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg="#020617",
            fg="#e2e8f0",
            insertbackground="white",
            relief="flat"
        )
        self.output_area.pack(fill="both", expand=True, padx=10, pady=5)

        # ===== STATUS BAR =====
        self.status = tk.Label(
            self.master,
            text="Ready",
            font=("Segoe UI", 10),
            bg="#020617",
            fg="#94a3b8"
        )
        self.status.pack(anchor="w", padx=20, pady=5)
    def show_tree(self):
        if not hasattr(self.parser, "tree_root"):
            return

        window = tk.Toplevel(self.master)
        window.title("Parse Tree")
        window.geometry("800x600")

        canvas = tk.Canvas(window, bg="white")
        canvas.pack(fill="both", expand=True)

        def draw(node, x, y, dx):
            canvas.create_text(
                x, y,
                text=node.value,
                font=("Arial", 12, "bold")
            )

            if node.children:
                gap = max(dx // len(node.children), 40)

                for i, child in enumerate(node.children):
                    child_x = x - dx // 2 + gap // 2 + i * gap
                    child_y = y + 80

                    canvas.create_line(
                        x, y + 15,
                        child_x, child_y - 15
                    )

                    draw(child, child_x, child_y, gap)

        draw(self.parser.tree_root, 400, 50, 400)


    def parse_expression(self):
        expr = self.input_entry.get().strip()
        self.output_area.delete(1.0, tk.END)

        if not expr:
            self.status.config(text="⚠ Enter an expression", fg="#facc15")
            return

        try:
            result = self.parser.parse(expr)

            self.output_area.insert(tk.END, "✔ Parsing Successful\n\n")
            self.output_area.insert(tk.END, result)

            self.status.config(text="Success", fg="#22c55e")

        except Exception as e:
            self.output_area.insert(tk.END, f"✖ Error: {str(e)}")
            self.status.config(text="Error", fg="#ef4444")


    def live_parse(self, event=None):
        expr = self.input_entry.get().strip()

        if not expr:
            return

        try:
            self.parser.parse(expr)
            self.status.config(text="Typing... Valid so far", fg="#38bdf8")
        except:
            self.status.config(text="Typing... Error detected", fg="#ef4444")


    def clear_all(self):
        self.input_entry.delete(0, tk.END)
        self.output_area.delete(1.0, tk.END)
        self.status.config(text="Cleared", fg="#94a3b8")


if __name__ == "__main__":
    root = tk.Tk()
    app = ParserGUI(root)
    root.mainloop()

   