#This module will scrape the results from 99acres.com
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from playwright.async_api import Page
import asyncio
#misc imports
from colorama import Fore, Style, Back, init
init(autoreset=True)
import os
from helper_function import human_click
from helper_function import human_type
from helper_function import property_handler, auto_scroll


URL = "https://www.99acres.com/"

#Create a function to scrap the data from the result page
async def result_scraper(page: Page):
    NAME = []
    PRICE = []
    CONFIG = []
    SELLER_TYPE = []
    SELLER_NAME = []
    LINK = []
    #1. Create the House cards list
    await asyncio.sleep(1.5)
    property_cards = await page.locator('div.PseudoTupleRevamp__tupleWrapProject.undefined').all()
    #2. Loop through the property cards
    for prop in property_cards:
        config_type_count = 0
        config_elem = prop.locator('div.configs__configCard')
        config_type_count = await config_elem.count()
        working_count = (config_type_count+1)/2 

        for i in range(working_count):
            pass

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
                5. Seller Name

                In order to handle the messy data, we will use config based data sorting
                I will judge based on BHK only because a single property card has only subunits based on BHK
            """

            #Start scraping
            #0. Scroll to the bottom first
            await auto_scroll(page=page)
            await result_scraper(page=page)
            

            
                


            await asyncio.sleep(5)

        except Exception as e:
            print(Back.RED + str(e))

        #finally store the cookies
        finally:
            os.makedirs('cookies', exist_ok=True)
            await context.storage_state(path='cookies/cookie_99acres.json')

        

if __name__ == '__main__':
    asyncio.run(main())