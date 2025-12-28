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
    