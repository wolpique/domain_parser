from flask_pymongo import PyMongo
import requests
import logging 
from flask import Flask
from bs4 import BeautifulSoup


app = Flask(__name__)

logger = logging.getLogger(__name__)

def get_response(domain_name):
    try:
        url = f"https://ps.kz/domains/whois/result?q={domain_name}"
        # https://www.ps.kz/domains/whois/result?q=youtube.com
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup
    except:
        logger.error(f"Domain error {domain_name}")
        return None

def clean_text(text):
    return text.strip().replace("\n", " ").replace("\r", "").replace("  ", " ")

def get_data(soup):
    all_data = {}
    title = soup.find_all("div", class_="col-xs-12")
    for description in title: 
        domainAbsent = description.find("div", class_ ="domains-whois__result")
        domainExist = description.find("div", class_="domains-whois--busy")

        if domainExist:
            all_data['description'] = clean_text(domainExist.get_text())
            all_data.update(get_additional_data(soup))
            return all_data
        elif domainAbsent:
            reference = domainAbsent.find('a', href=True)
            if reference:
                all_data['description'] = clean_text(domainAbsent.get_text())
                all_data['register_domain_link'] = reference['href']
            return all_data
        else:
            logger.debug(f'Type mistake') 
    return all_data
                
def get_additional_data(soup):   
    data = {}
    div_tables = soup.find_all("div", class_="col-xs-12")
    for div_table in div_tables: 
            table = div_table.find("table", class_="table")
            if table:
                all_tr = table.find_all('tr')
                for tr in all_tr:
                    all_td = tr.find_all('td')
                    for td in all_td:
                        text = td.get_text().strip()
                        if len(all_td) >= 2:  
                            key = clean_text(all_td[0].get_text())
                            value = clean_text(all_td[1].get_text())
                            data[key] = value

    logger.debug(f'Data extracted: {data}') 
    return data

