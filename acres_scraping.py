#This module will scrape the results from 99acres.com
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import asyncio
#misc imports
from colorama import Fore, Style, Back, init
init(autoreset=True)
import os
from helper_function import human_click
from helper_function import human_type
from helper_function import property_handler, auto_scroll


URL = "https://www.99acres.com/"

#create the main function
async def main(query = "Kolkata"):
    #use stealth playwright
    async with Stealth().use_async(async_playwright()) as p:
        try:
            #create a browser
            browser = await p.chromium.launch(headless=False)
            #create a context
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                storage_state="cookies/cookie_99acres.json"
            )
            page = await context.new_page()

            #Go to the desired URL
            print(Fore.RED + Style.BRIGHT + "->" + Fore.GREEN + f"Retrieving {URL}...")
            await page.goto(url=URL)
            await page.wait_for_selector('input.component__searchInput#keyword2[name="keyword"]')
            print(Fore.RED + Style.BRIGHT + "->" + Fore.GREEN + f"Search selector found, entering query...")

            #enter the query
            search_box = page.locator('input.component__searchInput#keyword2[name="keyword"]')
            await human_click(page=page, elem=search_box)
            await asyncio.sleep(2)
            await human_type(keyword=query, elem=search_box)
            await page.keyboard.press('Enter')
            await page.wait_for_selector('div[data-label="SEARCH"]')
            print(Fore.RED + Style.BRIGHT + "->" + Fore.GREEN + "Reached the results page, started scraping...")
            #reached the results page

            """
                The only thing we can scrap on the results page is:
                1. Name
                2. Price
                3. BHKs it offers (accordingly price will be shown)
                4. Seller type

                In order to handle the messy data, we will use config based data sorting
                I will judge based on BHK only because a single property card has only subunits based on BHK
            """

            #Start scraping
            NAMES_LIST = []
            SELLER_TYPE_LIST = []
            SELLER_NAME_LIST = []
            CONFIGS = []
            #0. Scroll to the bottom first
            await auto_scroll(page=page)
            #1. Scrap the names
            try:
                NAMES_LIST = await page.locator('div.PseudoTupleRevamp__headNrating a.ellipsis').evaluate_all("els => els.map(e => e.title)")
                print(Style.BRIGHT + Fore.YELLOW + f"Got {len(NAMES_LIST)} names!!!")
            except Exception as e:
                print(Back.RED + f"Can't extract names, error: {e}")

            #2. Scrap the Seller type
            try:
                seller_type_list_raw = await page.locator('div.PseudoTupleRevamp__contactHeading').all()
                for i in seller_type_list_raw:
                    text = await i.inner_text()
                    SELLER_TYPE_LIST.append(text)

                print(Fore.YELLOW + Style.BRIGHT + f"Found {len(SELLER_TYPE_LIST)} seller types!!!")
            except Exception as e:
                print(Back.RED + f"Can't extract seller_types, error: {e}")

            #3. Scrap the Seller names type
            try:
                seller_name_list_raw = await page.locator('div.PseudoTupleRevamp__contactSubheading').all()
                for i in seller_name_list_raw:
                    text = await i.inner_text()
                    SELLER_NAME_LIST.append(text)

                print(Fore.YELLOW + Style.BRIGHT + f"Found {len(SELLER_NAME_LIST)} seller names!!!")
                for name, seller_type, seller_name in zip(NAMES_LIST, SELLER_TYPE_LIST, SELLER_NAME_LIST):
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + name + " - " + seller_type + " - " + seller_name)
                    await asyncio.sleep(0.5)
            except Exception as e:
                print(Back.RED + f"Can't extract seller_names, error: {e}")

            #4. The most important, house config
            try:
                pass
            except:
                print(Back.RED + f"Can't extract configs, error: {e}")
                


            await asyncio.sleep(5)

        except Exception as e:
            print(Back.RED + str(e))

        #finally store the cookies
        finally:
            os.makedirs('cookies', exist_ok=True)
            await context.storage_state(path='cookies/cookie_99acres.json')

        

if __name__ == '__main__':
    asyncio.run(main())