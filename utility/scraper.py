from utility.variables import *

async def scrape(url: str, html_path: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            log = f"\n>> scraper.py > scrape \n> Connecting to '{url}'... "
            async with session.get(url) as response:
                if response.ok:
                    print(log + f"({response.status}) successful response.")
                    html = await response.text()
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(html)
                    print(f"\n>> scraper.py > scrape \n> Updated '{html_path}'")
                    return True
                else:
                    print(log + f"({response.status}) connection error.")
                    return False
    except Exception as e:
        print(f"\n>> scraper.py > scrape \n> Error: {e}")
        return False

# ---------------------------------------------------------------------------------------------------- #

async def scrape_parse_cna():
    file_path = data_path + "/" + cna_html
    success = asyncio.get_event_loop().create_task(scrape(url=cna_url, html_path=file_path))
    await success

    # If scrape is successful, parse html
    if success:    
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        # Grab tags with attribute 'data-category' that are in defined categories
        # Then get attributes 'data-category', 'data-heading', 'data-link_absolute'
        categories = ["Business", "World", "Asia", "East Asia"]
        tags = soup(attrs={"data-category": categories})
        news_dict = defaultdict(list)
        for tag in tags:
            category = tag["data-category"]
            link     = tag["data-link_absolute"]
            title    = tag["data-heading"]
            news_dict[category].append([title, link])
        
        # Save news_dict into .json
        with open(data_path + "/" + cna_json, 'w') as file:
            json.dump(news_dict, file, indent=4)
        print(f"\n>> scraper.py > scrape_parse_cna \n> Updated {cna_json} in {data_path}")
    else:
        print(f"\n>> scraper.py > scrape_parse_cna \n> Could not scrape from '{cna_url}' ...")

# ---------------------------------------------------------------------------------------------------- #

def filter_attr_href(tag):
    return tag.has_attr('href')

async def scrape_parse_gn():
    news_dict = defaultdict(list)

    for topic in gn_topics:
        gn_url_topic = gn_url + topic
        gn_html = "news_gn_" + topic + ".html"
        file_path = data_path + "/" + gn_html

        success = asyncio.get_event_loop().create_task(scrape(url=gn_url_topic, html_path=file_path))
        await success

        # If scrape is successful, parse html
        if success:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')

            # (1) Grab attributes 'href', which are article links when appended to https://ground.news/ 
            # (2) Make the article title from these links
            # Remove /article/
            # Replace "-" characters with " "
            # Ignore string past "_" if any
            # Capitalise first character of each word
            
            tags = soup(filter_attr_href)
            articles = set()

            for tag in tags:
                if "article" in tag["href"] and tag["href"] not in articles:
                    link = tag["href"]
                    articles.add(link)
                    title = link[9:].replace("-", " ")
                    title = title[:title.find("_")] if "_" in title else title
                    title = title.title()
                    news_dict[gn_topics[topic]].append([title, gn_base + link])
        else:
            print(f"\n>> scraper.py > scrape_parse_gn \n> Could not scrape from '{gn_url_topic}' ...")
        
    # Save news_dict into .json
    with open(data_path + "/" + gn_json, 'w') as file:
        json.dump(news_dict, file, indent=4)
    print(f"\n>> scraper.py > scrape_parse_gn \n> Updated {gn_json} in {data_path}")

# ---------------------------------------------------------------------------------------------------- #