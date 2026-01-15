import tkinter
from tkinter import IntVar, StringVar, ttk
from multiprocessing import Queue

def init_console(from_main: Queue, to_main: Queue):
    Console(from_main, to_main)


class Console():
    def __init__(self, from_main: Queue, to_main: Queue) -> None:
        self.from_main = from_main
        self.to_main = to_main
        self.window = tkinter.Tk()
        frame = tkinter.Frame(self.window, padx=10, pady=10)
        frame.grid()
        button = ttk.Button(frame, text="Enter", command=self.send_chat_message)
        button.grid(column = 3, row = 0)
        self.input = StringVar(frame)
        message_entry = ttk.Entry(frame, textvariable=self.input)
        message_entry.grid(column = 1, row = 0)
        self.amount = IntVar(frame)
        amount_entry = ttk.Entry(frame, textvariable = self.amount)
        amount_entry.grid(column = 2, row = 0)

        self.window.mainloop()

    def send_chat_message(self):
        for i in range(self.amount.get()):
            chat_message: tuple[str, str] = ("@ADMIN", self.input.get())
            print(f"CHAT MESSAGE: user: {chat_message[0]}, message: {chat_message[1]}")
            self.to_main.put(chat_message)
        

    