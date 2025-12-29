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
    await elem.evaluate("el => el.scrollIntoView()")
    await elem.hover()
    await asyncio.sleep(0.1987)

    #Click the element
    await elem.click()





#make a function to do human like typing
import random
async def human_type(keyword: str, elem: Locator):
    await elem.type(text=keyword, delay=random.uniform(100, 125))





#make a function to handle target=_blank clicks
from colorama import Fore, init, Style
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
    print(Fore.RED + Style.BRIGHT + "->" + Fore.GREEN + "Scrolling to the bottom of page...")
    #Get the height of the page PRESENTLY
    previous_height = await page.evaluate("document.body.scrollHeight")
    
    while True:
        current_scroll = await page.evaluate("window.scrollY")
        target_scroll = current_scroll + 800
        
        while current_scroll < target_scroll:
            delta = random.randint(50, 150)
            await page.mouse.wheel(0, delta)
            await asyncio.sleep(random.uniform(1, 2))
            current_scroll += delta
            
            max_h = await page.evaluate("document.body.scrollHeight")
            if current_scroll > max_h:
                break

        # Wait for potential network load
        await asyncio.sleep(random.uniform(1.5, 3.0))
        
        new_height = await page.evaluate("document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height
