import json
import sys

import click
import mechanicalsoup
import pandas as pd


URL = "https://www.wdr.de/"

@click.command()
@click.option('--location', required=True)
@click.option('--format', type=click.Choice(['text', 'json'], case_sensitive=False), default='text')
def main(location, format):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(URL)
    browser.follow_link("wetter")
    browser.select_form('form[id="search-form"]')
    browser["_query"]=location
    browser.submit_selected()
    page = browser.get_current_page()
    try:
        info = page.find("span", class_="heading-text").text.strip()
        updated = page.find("div", class_="map-updated-at").text.strip()
        table = page.find_all('table')
        df = pd.read_html(str(table))[0].set_index("Datum")
        df.index = map(lambda x: x.replace("&shy", "").replace(";\xad","").replace("\xad","").replace("- ", ""), df.index)
        if format == "text":
            print(info)
            print(updated)
            print(df)
        else:
            data = { "info": info, "updated": updated, "data": json.loads(df.to_json(orient="columns")) }
            print(json.dumps(data, ensure_ascii=False, indent=4))
    except AttributeError:
        if format == "text":
            print(f"Cannot find a place like '{location}'")
        else:
            data = { "error": f"Cannot find a place like '{location}'" }
            print(json.dumps(data, ensure_ascii=False, indent=4))
        sys.exit(1)

if __name__ == "__main__":
    main()
