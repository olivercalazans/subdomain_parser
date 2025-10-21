import tkinter as tk
from tkinter import filedialog



class SubDomainParser:

    def __init__(self):
        ...

    
    def parser(self) -> None:
        try:   self.execute()
        except FileNotFoundError: self.display_error("File not found")
        except Exception as e:    self.display_error(e)



    @staticmethod
    def display_error(msg: str) -> None:
        print(f"[ ERROR ] {msg}")



    def execute(self) -> None:
        self.read_file()
    


    def read_file(self) -> None:
        with open(self.select_file(), "r", encoding="utf-8") as file:
            for line in file:
                print(line.strip())

    

    @staticmethod
    def select_file() -> str:
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Text file", "*.txt"), ("Todos os arquivos", "*.*")]
        )





if __name__ == "__main__":
    dom_parser = SubDomainParser()
    dom_parser.parser()