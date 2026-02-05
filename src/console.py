import tkinter
from tkinter import W, IntVar, StringVar, ttk, Frame, Label, Button, Entry, Event
from multiprocessing import Queue

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
        self.init_command_display(frame)
        self.init_help_display(frame)

        self.window.mainloop()

    def init_chat_injector(self, frame: Frame):
        message_label = Label(frame, text = "Message")
        message_label.grid(column = 1, row = 0)

        amount_label = Label(frame, text = "Amount")
        amount_label.grid(column = 2, row = 0)

        send_message_button = Button(frame, text = "Inject Chat Message", command = self.send_chat_message)
        send_message_button.grid(column = 3, row = 1)

        self.message_input = StringVar(frame, value = "tnt")
        message_entry = Entry(frame, textvariable = self.message_input)
        message_entry.grid(column = 1, row = 1)
        message_entry.bind("<Return>", self.on_message_enter)

        self.amount_input = IntVar(frame, value = 1)
        amount_entry = Entry(frame, textvariable = self.amount_input)
        amount_entry.grid(column = 2, row = 1)

    def init_command_display(self, frame: Frame):
        commands = "Commands:\n\n"
        commands += "tnt\n" + "avalanche\n" + "big\n" +  "small\n" + "fast\n" + "slow\n"\
            + "wood\n" + "stone\n" + "copper\n" + "iron\n" + "gold\n" + "diamond\n" + "netherite\n"
        commands_list = Label(frame, text = commands, justify = "left", compound= "left")
        commands_list.grid(sticky = W, column = 1, row = 2)

    def init_help_display(self, frame: Frame):
        help_message = "This is a helper console. Enter in chat messages in the Message box.\
 Enter the amount of that message you want to send in the Amount box, then hit inject chat message. \
View a list of avaliable commands to the left."
        help_label = Label(frame, wraplength = 400, text = help_message)
        help_label.grid(column = 2, row = 2, columnspan = 2)

    def on_message_enter(self, entry):
        self.send_chat_message()

    def send_chat_message(self):
        for i in range(self.amount_input.get()):
            chat_message: tuple[str, str] = ("@ADMIN", self.message_input.get())
            print(f"CHAT MESSAGE: user: {chat_message[0]}, message: {chat_message[1]}")
            self.to_main.put(chat_message)
        

    