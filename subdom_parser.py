import tkinter as tk
from tkinter     import filedialog
from dataclasses import dataclass, field



@dataclass(slots=True)
class SubDomainsInfo:
    frequency: int      = 0
    domains:   set[str] = field(default_factory=set)



class SubDomainParser:

    def __init__(self):
        self._minimum:        int       = 0
        self._total_dom:      int       = 0
        self._subs_to_ignore: list[str] = []
        self._domains:        list[str] = []
        self._subdomains:     dict[str, SubDomainsInfo] = {}



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
        self._get_subdomains_to_remove()
        self._split_into_subdomains()
        self._sort_subdomains()
        self._display_results()



    def _get_minimum_occurrence(self) -> None:
        self._minimum = int(input('Minimum domain occurrences: '))



    def _get_subdomains_to_remove(self) -> None:
        subdoms           = input("Write domains to remove (Ex.: com, net, ...): ")
        self._subs_to_ignore = [ sub.strip() for sub in subdoms.split(',') ]



    def _read_file(self) -> None:
        with open(self._select_file(), "r", encoding="utf-8") as file:
            for line in file:
                self._domains.append(line.strip())
                self._total_dom += 1



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
            if subdomain in self._subs_to_ignore: continue

            self._add_new_subdomain_if_necessary(subdomain)
            self._subdomains[subdomain].frequency += 1
            self._subdomains[subdomain].domains.add(domain)



    def _add_new_subdomain_if_necessary(self, subdomain: str) -> None:
        if subdomain in self._subdomains:
            return

        self._subdomains[subdomain] = SubDomainsInfo()



    def _sort_subdomains(self) -> None:
        self._subdomains = dict(sorted(self._subdomains.items(), key=lambda item: item[1].frequency))



    def _display_results(self) -> None:
        for subdomain, info in self._subdomains.items():
            if info.frequency < self._minimum: continue

            print(f'# Subdomain: {subdomain} -> {info.frequency}')
            self._display_domains_which_contains_a_subdomain(subdomain)

        print(f'Total domains: {self._total_dom}')



    def _display_domains_which_contains_a_subdomain(self, subdomain: str) -> None:
        for domain in self._subdomains[subdomain].domains:
            dom: str = self.highlight_subdomain(domain, subdomain)
            print(f'\t|-> {dom}')
        print('\n')



    @staticmethod
    def highlight_subdomain(domain: str, subdomain: str) -> str:
        subdoms           = domain.split(".")
        highlighted_parts = [ f"\033[1;33m{sub}\033[0m" if sub == subdomain else sub for sub in subdoms ]
        return ".".join(highlighted_parts)





if __name__ == "__main__":
    dom_parser = SubDomainParser()
    dom_parser.parser()
