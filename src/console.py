import tkinter
from tkinter import W, IntVar, StringVar, ttk, Frame, Label, Button, Entry, Event
from multiprocessing import Queue
from command import Command

def init_console(from_main: Queue, to_main: Queue):
    Console(from_main, to_main)


class Console():
    def __init__(self, from_main: Queue, to_main: Queue) -> None:
        self.from_main = from_main
        self.to_main = to_main
        self.window = tkinter.Tk()
        self.window.title("Console")
        frame = Frame(self.window, padx=10, pady=10)
        frame.grid()

        self.init_chat_injector(frame)
        self.init_help_display(frame)
        self.init_command_buttons(frame)

        self.window.mainloop()

    def init_chat_injector(self, frame: Frame):
        message_label = Label(frame, text = "Message")
        message_label.grid(column = 1, row = 0)

        amount_label = Label(frame, text = "Amount")
        amount_label.grid(column = 2, row = 0)

        send_message_button = Button(frame, text = "Inject Chat Message", command = self.on_send_pressed)
        send_message_button.grid(column = 3, row = 1)

        self.message_input = StringVar(frame, value = "tnt")
        message_entry = Entry(frame, textvariable = self.message_input)
        message_entry.grid(column = 1, row = 1)
        message_entry.bind("<Return>", self.on_message_enter)

        self.amount_input = IntVar(frame, value = 1)
        amount_entry = Entry(frame, textvariable = self.amount_input)
        amount_entry.grid(column = 2, row = 1)

    def init_help_display(self, frame: Frame):
        help_message = "Enter in chat messages in the Message box.\
 Enter the amount of that message you want to send in the Amount box, then hit inject chat message. \
View a list of avaliable commands to the left."
        help_label = Label(frame, wraplength = 400, text = help_message)
        help_label.grid(column = 2, row = 2, columnspan = 2)

    def init_command_buttons(self, frame: Frame):
        command_frame = Frame(frame)
        command_frame.grid(column = 1, row = 2)
        for i, command in enumerate(Command):

            command_button = Button(command_frame, text = command.name,
                                    command = lambda c=command: self.send_chat_message(("@ADMIN", c.name), 1))
            command_button.grid(column = 0, row = i)

    def on_message_enter(self, entry):
        self.on_send_pressed()

    def on_send_pressed(self):
        self.send_chat_message(("@ADMIN", self.message_input.get()), self.amount_input.get())

    def send_chat_message(self, chat_message: tuple[str, str], amount: int):
        for i in range(amount):
            print(f"CHAT MESSAGE: user: {chat_message[0]}, message: {chat_message[1]}")
            self.to_main.put(chat_message)
        

    