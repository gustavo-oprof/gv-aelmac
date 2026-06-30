import logging
import tkinter
from tkinter import messagebox

logging.basicConfig(
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()],
    encoding='utf-8',
    format='%(asctime)s [%(levelname)s: %(filename)s (line %(lineno)d)] %(message)s',
    datefmt='%d/%m/%Y - %H:%M:%S',
    level=logging.INFO
)


def show_box(type: str, message: str):
    root = tkinter.Tk()
    root.withdraw()

    match type:
        case 'ERRO':
            messagebox.showerror(type, str(message))
            logging.critical(str(message).replace('\n',' '))
        case 'ATENÇÃO':
            messagebox.showwarning(type, str(message))
        case 'SELEÇÃO':
            choice = messagebox.askquestion(type, str(message))
            tkinter.Tk().destroy()
            return choice
        case _:
            messagebox.showinfo(type, str(message))

    tkinter.Tk().destroy()
