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