import tkinter
from tkinter import Button, Variable, ttk
import chat
from world import World

class Console():
    def __init__(self, world: World) -> None:
        self.world: World = world
        
        window = tkinter.Tk()
        frame = tkinter.Frame(window, padx=10, pady=10)
        frame.grid()
        ttk.Label(frame, text="Hellow World").grid(column = 1, row = 0)
        button = ttk.Button(frame, text="Enter", command=self.send_chat_message)
        button.grid(column = 2, row = 0)
        self.input = Variable(frame)
        entry = ttk.Entry(frame, textvariable=self.input)
        entry.grid(column = 1, row = 0)

        window.mainloop()

    def send_chat_message(self):
        chat_message: tuple[str, str] = ("@ADMIN", self.input.get())
        print(f"user: {chat_message[0]}, message: {chat_message[1]}")
        self.world.chat.send_chat_message(chat_message)
        

    