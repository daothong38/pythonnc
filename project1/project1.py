import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

# Hàm giải phương trình bậc 2
def solve_quadratic():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
        
        delta = b**2 - 4*a*c
        
        if delta > 0:
            x1 = (-b + math.sqrt(delta)) / (2*a)
            x2 = (-b - math.sqrt(delta)) / (2*a)
            result_label.config(text=f"Nghiệm x1 = {x1:.2f}, x2 = {x2:.2f}")
        elif delta == 0:
            x = -b / (2*a)
            result_label.config(text=f"Nghiệm kép x = {x:.2f}")
        else:
            result_label.config(text="Phương trình vô nghiệm")
    except ValueError:
        result_label.config(text="Vui lòng nhập đúng giá trị số!")

# Hàm xử lý khi nhấn nút trong Tic Tac Toe
def buttonClick(index):
    global currentPlayer

    if gameBoard[index] == "":
        gameBoard[index] = currentPlayer
        buttons[index].config(text=currentPlayer)

        if checkWinner():
            messagebox.showinfo("Tic Tac Toe", f"Player {currentPlayer} wins!")
            resetGame()
        elif "" not in gameBoard:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            resetGame()
        else:
            currentPlayer = "O" if currentPlayer == "X" else "X"

# Hàm kiểm tra người chiến thắng Tic Tac Toe
def checkWinner():
    winningCombinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winningCombinations:
        if gameBoard[combo[0]] == gameBoard[combo[1]] == gameBoard[combo[2]] != "":
            return True
    return False

# Hàm đặt lại trò chơi Tic Tac Toe
def resetGame():
    global currentPlayer, gameBoard
    currentPlayer = "X"
    gameBoard = ["", "", "", "", "", "", "", "", ""]
    for button in buttons:
        button.config(text="")

# Tạo cửa sổ chính
window = tk.Tk()
window.title("Tic Tac Toe và Giải phương trình bậc 2")
x = (window.winfo_screenwidth()//2)-(300//2)
y = (window.winfo_screenheight()//2)-(400//2)
window.geometry("{}x{}+{}+{}".format(300,320,x,y))


# Tạo notebook để có tab
notebook = ttk.Notebook(window)
notebook.pack(pady=10, expand=True)

# Tab 1 - Tic Tac Toe
tic_tac_toe_tab = ttk.Frame(notebook)
notebook.add(tic_tac_toe_tab, text="Tic Tac Toe")

currentPlayer = "X"
gameBoard = ["", "", "", "", "", "", "", "", ""]
buttons = []

for i in range(9):
    button = tk.Button(tic_tac_toe_tab, text="", font=('Arial', 20), width=5, height=2, 
                       command=lambda i=i: buttonClick(i))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

# Tab 2 - Giải phương trình bậc 2
quadratic_tab = ttk.Frame(notebook)
notebook.add(quadratic_tab, text="Giải phương trình bậc 2")

# Giao diện giải phương trình bậc 2
label_a = tk.Label(quadratic_tab, text="Nhập a:")
label_a.grid(row=0, column=0, padx=5, pady=5)
entry_a = tk.Entry(quadratic_tab)
entry_a.grid(row=0, column=1, padx=5, pady=5)

label_b = tk.Label(quadratic_tab, text="Nhập b:")
label_b.grid(row=1, column=0, padx=5, pady=5)
entry_b = tk.Entry(quadratic_tab)
entry_b.grid(row=1, column=1, padx=5, pady=5)

label_c = tk.Label(quadratic_tab, text="Nhập c:")
label_c.grid(row=2, column=0, padx=5, pady=5)
entry_c = tk.Entry(quadratic_tab)
entry_c.grid(row=2, column=1, padx=5, pady=5)

solve_button = tk.Button(quadratic_tab, text="Giải", command=solve_quadratic)
solve_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

result_label = tk.Label(quadratic_tab, text="")
result_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Chạy chương trình
window.resizable(False,False)
window.mainloop()
