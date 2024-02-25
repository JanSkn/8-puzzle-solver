import tkinter as tk

root = tk.Tk()
root.title("8-puzzle solver")
root.geometry("600x600")  # Fenstergröße

container = tk.Frame(root)
container.place(relx=0.5, rely=0.5, anchor="center")

labels = {}

def create_board(array):
    for i in range(3):  
        for j in range(3):  
            frame = tk.Frame(container, borderwidth=2, relief="ridge", width=100, height=100)
            frame.grid(row=i, column=j, padx=5, pady=5)
            frame.grid_propagate(False)  
            
            text = "" if array[i, j] == 0 else str(array[i, j])
            label = tk.Label(frame, text=text, font=('Arial', 24))
            label.place(relx=0.5, rely=0.5, anchor="center") 
            
            labels[(i, j)] = label

def update_board(arr, index=0):
        if index < len(arr):
            create_board(arr[index])
            root.after(500, update_board, arr, index + 1)

def button(arr):
    button = tk.Button(root, text="find solution", command=lambda: update_board(arr))
    button.pack(side="bottom", pady=20)