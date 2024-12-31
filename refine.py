import tkinter as tk
from tkinter import messagebox, ttk
import os
import threading
import queue
import re

# List of input files
input_files = ["input.txt", "input-1.txt", "input-2.txt", "input-3.txt"]

# Queue for thread-safe result communication
result_queue = queue.Queue()

default_max_results = 100
searching = False

# History for input fields
include_history = ""
exclude_history = ""

# Function to search files
def search_file(file_name, include_keywords, exclude_keywords, max_results):
    results = []
    line_number = 0
    try:
        with open(file_name, "r", encoding="utf-8", errors="replace") as infile:
            for line in infile:
                line_number += 1
                if len(results) >= max_results:
                    break
                line_lower = line.lower()
                if any(re.search(keyword, line_lower) for keyword in include_keywords) and not any(
                    re.search(keyword, line_lower) for keyword in exclude_keywords
                ):
                    results.append((line_number, file_name, line.strip()))
    except Exception as e:
        results.append((None, file_name, f"Error processing {file_name}: {e}"))
    return results

# Function to refine lines dynamically
def refine_lines():
    global searching
    if searching:
        return

    include_keywords = keyword_entry.get().strip()
    exclude_keywords = exclude_entry.get().strip()

    if not include_keywords:
        tree.delete(*tree.get_children())  # Clear table if no keywords are entered
        return

    # Save to history
    global include_history, exclude_history
    include_history = include_keywords
    exclude_history = exclude_keywords

    # Prepare keywords as regex patterns
    include_keywords = [re.escape(keyword.strip()) for keyword in include_keywords.split(",")]
    exclude_keywords = [re.escape(keyword.strip()) for keyword in exclude_keywords.split(",")] if exclude_keywords else []

    max_results = int(result_limit_entry.get()) if result_limit_entry.get().isdigit() else default_max_results

    progress_var.set(0)
    progress_bar["maximum"] = 100  # Set progress bar max value
    progress_bar["value"] = 0

    def process():
        global searching
        searching = True
        results = []
        file_count = sum(1 for file_var in file_vars if file_var.get())  # Count selected files
        progress_step = 100 / file_count if file_count else 100  # Progress step per file

        for file_var, file_name in zip(file_vars, input_files):
            if file_var.get() and os.path.exists(file_name):
                results.extend(search_file(file_name, include_keywords, exclude_keywords, max_results))
                progress_var.set(progress_var.get() + progress_step)
                progress_bar["value"] = progress_var.get()
                root.update_idletasks()
        result_queue.put(results)  # Add results to the queue
        searching = False

    threading.Thread(target=process, daemon=True).start()
    root.after(100, update_results)

# Function to update results dynamically
def update_results():
    try:
        results = result_queue.get_nowait()  # Non-blocking queue retrieval
        tree.delete(*tree.get_children())  # Clear the table for new results
        file_summary = {}
        if results:
            for idx, (line_number, file_name, line_content) in enumerate(results, start=1):
                # Add data to the table
                tree.insert(
                    "", "end",
                    values=(idx, line_number if line_number else "N/A", file_name, line_content),
                    tags=("oddrow" if idx % 2 == 0 else "evenrow"),
                )
                if file_name in file_summary:
                    file_summary[file_name] += 1
                else:
                    file_summary[file_name] = 1
        else:
            tree.insert("", "end", values=("No results", "", "", ""))

        # Update summary label
        summary_text = "Total Refined Lines: " + ", ".join(f"{file}: {count}" for file, count in file_summary.items())
        total_label.config(text=summary_text)
        progress_var.set(100)
        progress_bar["value"] = 100  # Set progress bar to complete
    except queue.Empty:
        if searching:
            root.after(100, update_results)  # Keep checking the queue

# Function to clear results
def clear_results():
    tree.delete(*tree.get_children())  # Clear the Treeview
    keyword_entry.delete(0, tk.END)  # Clear the keyword input field
    exclude_entry.delete(0, tk.END)  # Clear the exclude input field
    total_label.config(text="Total Refined Lines: 0")  # Reset total refined lines
    progress_var.set(0)  # Reset the progress bar

# Function to save displayed results
def save_results():
    output_file = "refined_results.txt"
    displayed_results = tree.get_children()
    if not displayed_results:
        messagebox.showinfo("Save Error", "No results to save.")
        return
    try:
        with open(output_file, "w", encoding="utf-8") as outfile:
            for item in displayed_results:
                values = tree.item(item, "values")
                outfile.write("\t".join(map(str, values)) + "\n")
        messagebox.showinfo("Saved", f"Results saved to '{output_file}'.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {e}")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Dynamic Refine Lines with Save and Copy Features")
root.geometry("1400x900")  # Larger default size

# Input widgets
keyword_label = tk.Label(root, text="Include Keywords (comma-separated):", font=("Arial", 12))
keyword_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
keyword_entry = tk.Entry(root, width=60, font=("Arial", 12))
keyword_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

exclude_label = tk.Label(root, text="Exclude Keywords (comma-separated):", font=("Arial", 12))
exclude_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
exclude_entry = tk.Entry(root, width=60, font=("Arial", 12))
exclude_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

result_limit_label = tk.Label(root, text="Max Results (default 100):", font=("Arial", 12))
result_limit_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
result_limit_entry = tk.Entry(root, width=10, font=("Arial", 12))
result_limit_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
result_limit_entry.insert(0, str(default_max_results))

# File checkboxes with color indicators
file_vars = [tk.IntVar(value=1) for _ in input_files]
file_frame = tk.Frame(root)
file_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="w")
for idx, file_name in enumerate(input_files):
    color = "green" if os.path.exists(file_name) else "red"
    checkbox = tk.Checkbutton(file_frame, text=file_name, variable=file_vars[idx], font=("Arial", 10), fg=color)
    checkbox.grid(row=0, column=idx + 1, padx=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=4, column=0, columnspan=2, pady=10)
search_button = tk.Button(button_frame, text="Search", command=refine_lines, bg="lightblue", width=15)
search_button.grid(row=0, column=0, padx=5)
save_button = tk.Button(button_frame, text="Save Results", command=save_results, bg="lightgreen", width=15)
save_button.grid(row=0, column=1, padx=5)
clear_button = tk.Button(button_frame, text="Clear Results", command=clear_results, bg="lightcoral", width=15)  # Fixed Clear Button
clear_button.grid(row=0, column=2, padx=5)

# Results table with scrollbars
tree_frame = tk.Frame(root)
tree_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

tree = ttk.Treeview(tree_frame, columns=("No.", "Line", "File", "Content"), show="headings")
tree.heading("No.", text="No.")
tree.heading("Line", text="Line")
tree.heading("File", text="File")
tree.heading("Content", text="Content")

tree.column("No.", width=50, anchor="center")
tree.column("Line", width=100, anchor="center")
tree.column("File", width=150, anchor="center")
tree.column("Content", width=1000, anchor="w")  # Wider column for longer lines

# Apply larger font
style = ttk.Style()
style.configure("Treeview", font=("Arial", 16))  # Larger font for table content
style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

# Scrollbars
scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar_y.set)

scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
tree.configure(xscrollcommand=scrollbar_x.set)

tree.pack(fill=tk.BOTH, expand=True)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.grid(row=6, column=0, columnspan=2, pady=10)

# Total refined lines label
total_label = tk.Label(root, text="Total Refined Lines: 0", font=("Arial", 12), fg="blue")
total_label.grid(row=7, column=0, columnspan=2, pady=5)

# Set up resizing for dynamic layout
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(1, weight=1)

# Run Tkinter loop
root.mainloop()
