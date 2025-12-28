#This module contains some functions that we will use throughout our project

#make a function to create header stuff
import shutil
def header(text, char):
    console_width = shutil.get_terminal_size().columns
    header = f"{text}".center(console_width, char)
    return header

#Make a function to human like click elements
import asyncio
from playwright.async_api import async_playwright
from playwright.async_api import Locator, Page
async def human_click(page: Page, elem: Locator):
    #hover over the element first
    await elem.hover()
    await asyncio.sleep(1.32455)

    await elem.click()

#make a function to do human like typing
import random
async def human_type(keyword: str, elem: Locator):
    await elem.type(text=keyword, delay=random.uniform(100, 125))

#make a function to handle target=_blank clicks
from colorama import Fore, init
init(autoreset=True)
async def property_handler(page: Page,
                            elem_list: list):
    TABS = []
    print(Fore.BLUE + f"Found {len(elem_list)} elements to click.")
    #loop through the elem list and just keep on clicking them, do not switch to the new tab keep on the original tab
    #and then create another loop to loop through the tabs
    for elem in elem_list:
        #perform the click
        async with page.expect_popup() as popup_info:
            await human_click(page=page, elem=elem)

        new_tab = await popup_info.value
        await new_tab.wait_for_load_state("domcontentloaded")
        TABS.append(new_tab)
    return TABS

#Make a function to scroll to the bottom
async def auto_scroll(page: Page):
    print(Fore.RED + "->" + Fore.BLUE + "Scrolling to the bottom of page...")
    #Get the height of the page PRESENTLY
    page_height = await page.evaluate("document.body.scrollHeight")

    #run a while true loop to scroll to the very end
    while True:
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        #wait for the stuff to load
        await asyncio.sleep(random.uniform(2, 3))

        new_height = await page.evaluate("document.body.scrollHeight")
        if new_height == page_height: #this means that new stuff didn't load
            await asyncio.sleep(8)
            if new_height == await page.evaluate("document.body.scrollHeight"):
                break
        page_height = new_height
    