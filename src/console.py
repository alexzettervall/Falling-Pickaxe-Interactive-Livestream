import tkinter
from tkinter import Button, Variable, ttk

def send_chat_message():
    chat_message: tuple[str, str] = ("@ADMIN", input.get())
    print(f"user: {chat_message[0]}, message: {chat_message[1]}")

window = tkinter.Tk()
frame = tkinter.Frame(window, padx=10, pady=10)
frame.grid()
ttk.Label(frame, text="Hellow World").grid(column = 1, row = 0)
button = ttk.Button(frame, text="Enter", command=send_chat_message)
button.grid(column = 2, row = 0)
input = Variable(frame)
entry = ttk.Entry(frame, textvariable=input)
entry.grid(column = 1, row = 0)

window.mainloop()