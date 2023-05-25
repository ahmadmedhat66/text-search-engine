import tkinter as tk
from tkinter import filedialog, messagebox
import time

def brute_force_search(text, keyword):
    start_time = time.time()
    results = []
    index = 0
    while index != -1:
        index = text.lower().find(keyword.lower(), index)
        if index != -1:
            results.append(index)
            index += len(keyword)
    end_time = time.time()
    return results, end_time - start_time

def boyer_moore_search(text, keyword):
    start_time = time.time()
    m = len(keyword)
    n = len(text)
    results = []
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and keyword[j].lower() == text[i + j].lower():
            j -= 1
        if j == -1:
            results.append(i)
            i += m
        else:
            skip = max(1, j - keyword.rfind(text[i + j]))
            i += skip
    end_time = time.time()
    return results, end_time - start_time

def kmp_search(text, keyword):
    start_time = time.time()
    results = []
    m = len(keyword)
    n = len(text)
    lps = compute_lps(keyword)
    i = 0
    j = 0
    while i < n:
        if keyword[j].lower() == text[i].lower():
            i += 1
            j += 1
        if j == m:
            results.append(i - j)
            j = lps[j - 1]
        elif i < n and keyword[j].lower() != text[i].lower():
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    end_time = time.time()
    return results, end_time - start_time

def compute_lps(keyword):
    m = len(keyword)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if keyword[i].lower() == keyword[length].lower():
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    entry_file.delete(0, tk.END)
    entry_file.insert(tk.END, filepath)

def search():
    keyword = entry_keyword.get()
    filepath = entry_file.get()

    if not keyword:
        messagebox.showwarning("Missing Keyword", "Please enter a keyword.")
        return

    if not filepath:
        messagebox.showwarning("Missing File", "Please select a file.")
        return

    try:
        with open(filepath, "r") as file:
            text = file.read()
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "The selected file does not exist.")
        return
    except:
        messagebox.showerror("Error", "An error occurred while reading the file.")
        return

    algorithm = algorithm_choice.get()

    if algorithm == "Brute Force":
        results, execution_time = brute_force_search(text, keyword)
    elif algorithm == "Boyer-Moore":
        results, execution_time = boyer_moore_search(text, keyword)
    elif algorithm == "Knuth-Morris-Pratt":
        results, execution_time = kmp_search(text, keyword)

    show_search_result(results, execution_time)

def show_search_result(results, execution_time):
    if not results:
        messagebox.showinfo("Search Result", "Keyword not found!")
    else:
        result_message = f"Keyword found at indices: {', '.join(map(str, results))}\n"
        result_message += f"Execution time: {execution_time:.6f} seconds"
        messagebox.showinfo("Search Result", result_message)

# Create the GUI
root = tk.Tk()
root.title("Keyword Search")
root.geometry("600x400")
root.resizable(False, False)

# Set window icon
icon = tk.PhotoImage(file="search_icon.png")
root.iconphoto(True, icon)

# Algorithm selection
algorithm_label = tk.Label(root, text="Select Algorithm:", font=("Arial", 14))
algorithm_label.pack(pady=10)

algorithm_choice = tk.StringVar(root)
algorithm_choice.set("Brute Force")  # Default algorithm choice

algorithm_optionmenu = tk.OptionMenu(root, algorithm_choice, "Brute Force", "Boyer-Moore", "Knuth-Morris-Pratt")
algorithm_optionmenu.config(font=("Arial", 12))
algorithm_optionmenu.pack()

# Keyword input
keyword_label = tk.Label(root, text="Enter Keyword:", font=("Arial", 14))
keyword_label.pack(pady=10)

entry_keyword = tk.Entry(root, font=("Arial", 12))
entry_keyword.pack()

# File selection
file_label = tk.Label(root, text="Select File:", font=("Arial", 14))
file_label.pack(pady=10)

file_frame = tk.Frame(root)
file_frame.pack()

entry_file = tk.Entry(file_frame, font=("Arial", 12))
entry_file.pack(side=tk.LEFT, padx=(0, 10))

browse_button = tk.Button(file_frame, text="Browse", command=browse_file, font=("Arial", 12),
                          bg="#2196F3", fg="white")
browse_button.pack(side=tk.LEFT)

# Search button
search_button = tk.Button(root, text="Search", command=search, font=("Arial", 16), padx=20, pady=10,
                          bg="#4CAF50", fg="white")
search_button.pack(pady=20)

root.mainloop()
