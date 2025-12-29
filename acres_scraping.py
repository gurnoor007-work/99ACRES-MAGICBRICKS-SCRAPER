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
    NUMBER = []
    #1. Create the House cards list
    property_cards = await page.locator('section[data-hydration-on-demand="true"]').all()
    #2. Loop through the property cards
    for prop in property_cards:
        config_type_count = 0
        config_elem = await prop.locator('div.configs__configCardsWrap div.configs__configCard').all()
        divider_elem = await prop.locator('div.configs__configCards div.configs__divider').all()
        config_type_count = len(config_elem)
        

        for i in range(config_type_count): #i = 0, 1, 2
            #1. Get the name
            try:
                name = await prop.locator('a.ellipsis').inner_text()
                NAME.append(str(name))
            except Exception as e:
                print(Back.RED + f"Can't extract name: {str(e)}")

            #2. Get the config
            try:
                config = prop.locator('div.cc__CarouselBox div.configs__configCard').nth(i)
                config_text = await config.locator('div.configs__ccl1').inner_text()
                CONFIG.append(config_text[0:6])
            except Exception as e:
                print(Back.RED + f"Can't extract config: {str(e)}")

            #3. Get the Price
            try:
                config = prop.locator('div.cc__CarouselBox div.configs__configCard').nth(i)
                price = await config.locator('div.configs__ccl2').inner_text()
                PRICE.append(price)
            except Exception as e:
                print(Back.RED + f"Can't extract price: {str(e)}")

            #4. Get the seller type
            try:
                seller_block = prop.locator('div.PseudoTupleRevamp__builderInfo')
                seller_type = await seller_block.locator('div.PseudoTupleRevamp__contactHeading').inner_text()
                SELLER_TYPE.append(seller_type)
            except Exception as e:
                print(Back.RED + f"Can't extract seller_type: {str(e)}")
            
            #5. Get the seller name
            try:
                seller_block = prop.locator('div.PseudoTupleRevamp__builderInfo')
                seller_name = await seller_block.locator('div.PseudoTupleRevamp__contactSubheading').inner_text()
                SELLER_NAME.append(seller_name)
            except Exception as e:
                print(Back.RED + f"Can't extract seller_type: {str(e)}")
            
            #6. Get the number
            try:
                #first click the "view_number" button
                button_elem = page.locator('div.PseudoTupleRevamp__viewNumber.pageComponent.trackGAClick[data-label="VIEW_NUMBER"]').first
                await human_click(page=page, elem=button_elem)
                await page.wait_for_selector('div.component__cnfCardCont')
                await asyncio.sleep(1)
                number = await page.locator('div.component__cnfCardCont div.component__advertiserPhone').inner_text()
                NUMBER.append(number)
                cross_button = page.locator('i.pageComponent.component__eoiLayerCrossBtn[data-label="CLOSE"]')
                await human_click(page=page, elem=cross_button)
                await asyncio.sleep(0.5)
            except Exception as e:
                print(Back.RED + f"Can't extract number: {str(e)}")

            print(Fore.YELLOW + Style.BRIGHT + name + " - " + config_text[0:6] + " - " + price + " - " + seller_type + " - " + seller_name + " - " + number)
    print(len(NAME))

#create the main function
async def main(query = "Kolkata"):
    #use stealth playwright
    async with Stealth().use_async(async_playwright()) as p:
        try:
            #create a browser
            browser = await p.chromium.launch(headless=False)
            #create a context, make sure to use cookies to act like a real user
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                storage_state="cookies/cookie_99acres.json"
            )
            page = await context.new_page()

            #Go to the desired URL
            print(Fore.RED + Style.BRIGHT + "->" + Fore.GREEN + f"Retrieving {URL}...")
            await page.goto(url=URL)
            await page.wait_for_selector('input.component__searchInput#keyword2[name="keyword"]')
            await asyncio.sleep(0.5)
            print(Fore.RED + Style.BRIGHT + "->" + Fore.GREEN + f"Search selector found, entering query...")
            #Search box located, now comes the searching part

            #enter the query
            search_box = page.locator('input.component__searchInput#keyword2[name="keyword"]')
            await human_click(page=page, elem=search_box)
            await asyncio.sleep(2)
            await human_type(keyword=query, elem=search_box)
            await page.keyboard.press('Enter')
            await page.wait_for_selector('div[data-label="SEARCH"]')
            print(Fore.RED + Style.BRIGHT + "->" + Fore.GREEN + "Reached the results page, started scraping...")
            #reached the results page
        except Exception as e:
            print(Back.RED + f"Can't reach URLS: {e}")

        """
            The only thing we can scrap on the results page is:
            1. Name
            2. Price
            3. BHKs it offers (accordingly price will be shown)
            4. Seller type
            5. Seller Name
            6. Number

            In order to handle the messy data, we will use config based data sorting
            I will judge based on BHK only because a single property card has only subunits based on BHK
        """

        try:
            #Start scraping
            #0. Scroll to the bottom first
            await auto_scroll(page=page)
            #1. Run our result scraper
            await result_scraper(page=page)
        except Exception as e:
            print(Back.RED + f"Error in Scraping: {e}")

        #finally store the cookies
        finally:
            os.makedirs('cookies', exist_ok=True)
            await context.storage_state(path='cookies/cookie_99acres.json')

if __name__ == '__main__':
    asyncio.run(main())