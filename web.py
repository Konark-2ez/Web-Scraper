# Part 1
# In this assignment you are required to scrape all products from this URL:
# https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2
# C283&ref=sr_pg_1
# Need to scrape atleast 20 pages of product listing pages
# Items to scrape
# • Product URL
# • Product Name
# • Product Price
# • Rating
# • Number of reviews
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_product_listings(url, num_pages):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    products_data = []
    
    for page_num in range(1, num_pages + 1):
        page_url = url + f'&page={page_num}'
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_list = soup.find_all('div', class_='s-include-content-margin')
        
        for product in product_list:
            product_url = product.find('a', class_='a-link-normal')['href']
            product_name = product.find('span', class_='a-size-medium').text.strip()
            product_price = product.find('span', class_='a-offscreen').text.strip()
            product_rating = product.find('span', class_='a-icon-alt')
            product_rating = float(product_rating.text.split()[0]) if product_rating else None
            product_num_reviews = product.find('span', {'aria-label': True})
            product_num_reviews = int(product_num_reviews['aria-label'].split()[0].replace(',', '')) if product_num_reviews else None
            
            products_data.append({
                'Product URL': product_url,
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': product_rating,
                'Number of Reviews': product_num_reviews
            })
    
    return products_data


search_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
num_pages_to_scrape = 20
products_list = scrape_product_listings(search_url, num_pages_to_scrape)
products_df = pd.DataFrame(products_list)
products_df.to_csv('product_listings.csv', index=False)

# Part 2
# With the Product URL received in the above case, hit each URL, and add below items:
# • Description
# • ASIN
# • Product Description
# • Manufacturer
# Need to hit around 200 product URL’s and fetch various information.
# The entire data needs to be exported in a csv format
# You are free to use third party packages for scraping
def scrape_product_details(product_urls):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    product_details = []
    
    for product_url in product_urls:
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting ASIN (Amazon Standard Identification Number)
        asin = soup.find('th', text='ASIN').find_next_sibling('td').text.strip()
        
        # Extracting Product Description
        product_desc = soup.find('div', id='productDescription').text.strip() if soup.find('div', id='productDescription') else None
        
        # Extracting Manufacturer
        manufacturer = soup.find('a', href=lambda x: x and 'seller' in x.lower())
        manufacturer = manufacturer.text.strip() if manufacturer else None
        
        product_details.append({
            'Product URL': product_url,
            'ASIN': asin,
            'Product Description': product_desc,
            'Manufacturer': manufacturer
        })
    
    return product_details
product_urls_list = products_df['Product URL'].tolist()
product_details_list = scrape_product_details(product_urls_list[:200]) 
product_details_df = pd.DataFrame(product_details_list)
product_details_df.to_csv('product_details.csv', index=False)
