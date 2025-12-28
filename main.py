#This module compiles everything
from helper_function import header
from colorama import Fore, Style, init
init(autoreset=True)


print(Fore.MAGENTA + header("99ACRES-MAGICBRICKS-SCRAPER", '='))
#get which site to scrape
while True:
    site = input(Fore.GREEN + "Enter site (99acres/magicbricks): ")

    if site == "99acres":
        import acres_scraping
        break
    elif site == "magicbricks":
        import magicbricks_scraping
        break
    else:
        print(Fore.RED + "Please Enter a valid site (99acres/magicbricks)!")







print(Fore.MAGENTA + header("99ACRES-MAGICBRICKS-SCRAPER", '='))