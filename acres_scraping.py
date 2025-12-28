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
            print(Fore.RED + "->" + Fore.GREEN + f"Retrieving {URL}...")
            await page.goto(url=URL)
            await page.wait_for_selector('input.component__searchInput#keyword2[name="keyword"]')
            print(Fore.RED + "->" + Fore.GREEN + f"Search selector found, entering query...")

            #enter the query
            search_box = page.locator('input.component__searchInput#keyword2[name="keyword"]')
            await human_click(page=page, elem=search_box)
            await asyncio.sleep(2)
            await human_type(keyword=query, elem=search_box)
            await page.keyboard.press('Enter')

            #now just scrape everything
            await page.wait_for_selector('div.r_srp__rightSection')
            elem_list = await page.locator('div.tupleNew__headingCont').all()
            await auto_scroll(page=page)
            await property_handler(page=page, elem_list=elem_list)



            await asyncio.sleep(5)

        except Exception as e:
            print(Back.RED + str(e))

        #finally store the cookies
        finally:
            os.makedirs('cookies', exist_ok=True)
            await context.storage_state(path='cookies/cookie_99acres.json')

        

if __name__ == '__main__':
    asyncio.run(main())