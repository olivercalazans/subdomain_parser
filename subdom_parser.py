import tkinter as tk
from tkinter import filedialog



class SubDomainParser:

    def __init__(self):
        self._minimum:    int            = 0
        self._domains:    list[str]      = []
        self._subdomains: dict[str, int] = {}


    
    def parser(self) -> None:
        try:   self._execute()
        except FileNotFoundError: self._display_error('File not found')
        except ValueError as e:   self._display_error(f'Invalid input -> {e}') 
        except Exception as e:    self._display_error(f'Unknown error -> {e}')



    @staticmethod
    def _display_error(msg: str) -> None:
        print(f"[ ERROR ] {msg}")



    def _execute(self) -> None:
        self._read_file()
        self._get_minimum_occurrence()
        self._split_into_subdomains()
        self._sort_subdomains()
        self._display_results()

    

    def _get_minimum_occurrence(self) -> None:
        self._minimum = int(input('Minimum domain occurrences: '))



    def _read_file(self) -> None:
        with open(self._select_file(), "r", encoding="utf-8") as file:
            for line in file:
                self._domains.append(line.strip())

    

    @staticmethod
    def _select_file() -> str:
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Text file", "*.txt"), ("Todos os arquivos", "*.*")]
        )
    


    def _split_into_subdomains(self) -> None:
        for domain in self._domains:
            self._count_subdomains(domain)

    

    def _count_subdomains(self, domain: str) -> None:
        for subdomain in domain.split('.'):
            self._add_new_subdomain_if_necessary(subdomain)
            self._subdomains[subdomain] += 1
    


    def _add_new_subdomain_if_necessary(self, subdomain: str) -> None:
        if not subdomain in self._subdomains:
            self._subdomains[subdomain] = 0



    def _sort_subdomains(self) -> None:
        self._subdomains = dict(sorted(self._subdomains.items(), key=lambda item: item[1]))
    


    def _display_results(self) -> None:
        for subdomain, num in self._subdomains.items():
            if num < self._minimum: continue
            print(f'{num:>3}: {subdomain}')
        
            






if __name__ == "__main__":
    dom_parser = SubDomainParser()
    dom_parser.parser()