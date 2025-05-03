from tkinter import *
from tkinter import Tk, RIGHT, BOTH, RAISED
from tkinter.ttk import Frame, Button, Style


class Example(Frame):

   def __init__(self):
      super().__init__()
      self.initUI()

   def initUI(self):
      self.master.title("СОЛО")
      self.style = Style()
      self.style.theme_use("default")

      frame = Frame(self, relief=RAISED, borderwidth=1)
      frame.pack(fill=BOTH, expand=True)

      self.pack(fill=BOTH, expand=True)

      closeButton = Button(self, text="Закрыть")
      closeButton.pack(side=RIGHT, padx=5, pady=5)
      okButton = Button(self, text="Готово")
      okButton.pack(side=RIGHT)


def main():
   root = Tk()
   # getting screen width and height of display
   width = 1000 #root.winfo_screenwidth()
   height = 700 #root.winfo_screenheight()
   # setting tkinter window size
   root.geometry("%dx%d" % (width, height))
   #root.geometry("300x200+300+300")
   app = Example()
   root.mainloop()


if __name__ == '__main__':
   main()