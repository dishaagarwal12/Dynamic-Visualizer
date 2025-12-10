import tkinter as tk
from tkinter import messagebox, ttk

class MemoryBlock:
    def __init__(self, start, size, allocated=False, process=""):
        self.start = start
        self.size = size
        self.allocated = allocated
        self.process = process


class MemoryVisualizer:
    def __init__(self, master):
        self.master = master
        master.title("Dynamic Memory Management Visualizer")
        master.geometry("900x650")
        master.configure(bg="#f3f3f3")

        self.memory_size = 1000
        self.blocks = [MemoryBlock(0, self.memory_size)]

        # Title
        tk.Label(master, text="Dynamic Memory Management Visualizer",
                 font=("Arial", 16, "bold"), bg="#f3f3f3").pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(master, bg="#ffffff", bd=2, relief="groove")
        input_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(input_frame, text="Process Name:", bg="#ffffff").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(input_frame, text="Memory Required:", bg="#ffffff").grid(row=1, column=0, padx=10, pady=10)

        self.process_entry = tk.Entry(input_frame)
        self.size_entry = tk.Entry(input_frame)

        self.process_entry.grid(row=0, column=1)
        self.size_entry.grid(row=1, column=1)

        # Buttons
        tk.Button(input_frame, text="Allocate", command=self.allocate_memory,
                  bg="#4caf50", fg="white", width=10).grid(row=0, column=2, padx=15)

        tk.Button(input_frame, text="Free", command=self.free_memory,
                  bg="#f44336", fg="white", width=10).grid(row=1, column=2, padx=15)

        # Canvas
        self.canvas = tk.Canvas(master, width=800, height=400, bg="white", relief="ridge", bd=2)
        self.canvas.pack(pady=10)

        self.update_visual()

    def allocate_memory(self):
        process = self.process_entry.get()
        size = self.size_entry.get()

        if not process or not size.isdigit():
            messagebox.showerror("Error", "Enter valid process name and size!")
            return

        size = int(size)

        for block in self.blocks:
            if not block.allocated and block.size >= size:
                new_block = MemoryBlock(block.start, size, True, process)

                block.start += size
                block.size -= size

                self.blocks.insert(self.blocks.index(block), new_block)

                if block.size == 0:
                    self.blocks.remove(block)

                self.merge_free_blocks()
                self.update_visual()
                return

        messagebox.showwarning("Warning", "Not enough free memory!")

    def free_memory(self):
        process = self.process_entry.get()

        for block in self.blocks:
            if block.allocated and block.process == process:
                block.allocated = False
                block.process = ""
                self.merge_free_blocks()
                self.update_visual()
                return

        messagebox.showerror("Error", "Process not found!")

    def merge_free_blocks(self):
        merged = []
        self.blocks.sort(key=lambda b: b.start)

        for block in self.blocks:
            if merged and not block.allocated and not merged[-1].allocated:
                merged[-1].size += block.size
            else:
                merged.append(block)

        self.blocks = merged

    def update_visual(self):
        self.canvas.delete("all")

        x_start = 10
        total_width = 780

        for block in self.blocks:
            width = (block.size / self.memory_size) * total_width
            color = "#4caf50" if block.allocated else "#bbdefb"

            self.canvas.create_rectangle(x_start, 50, x_start + width, 200, fill=color)
            label = f"{block.process} ({block.size})" if block.allocated else f"Free ({block.size})"
            self.canvas.create_text(x_start + width / 2, 125, text=label, font=("Arial", 10))

            x_start += width


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryVisualizer(root)
    root.mainloop()
