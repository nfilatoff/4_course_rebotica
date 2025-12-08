import tkinter as tk

low = 1
high = 100
guess = (low + high) // 2

def update_label():
    label.config(text=f"Компьютер думает: {guess}")

def more():
    global low, guess
    low = guess + 1
    new_guess()

def less():
    global high, guess
    high = guess - 1
    new_guess()

def new_guess():
    global guess, low, high
    if low > high:
        label.config(text="Что-то пошло не так...")
        return
    guess = (low + high) // 2
    update_label()

def correct():
    label.config(text=f"Загаданное число: {guess}")

root = tk.Tk()
root.title("Бинарное угадывание")

label = tk.Label(root, text=f"Компьютер думает: {guess}", font=("Arial", 18))
label.pack(pady=20)

btn_more = tk.Button(root, text="Больше", width=12, command=more)
btn_less = tk.Button(root, text="Меньше", width=12, command=less)
btn_ok = tk.Button(root, text="Угадал!", width=12, command=correct)

btn_more.pack(pady=5)
btn_less.pack(pady=5)
btn_ok.pack(pady=5)

root.mainloop()