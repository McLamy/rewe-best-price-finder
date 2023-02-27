import requests


def rewe():
    search_term = input("Nach welchem Produkt suchen Sie?: ")
    url = f'https://shop.rewe.de/api/products/?search={search_term}&market=1940130'

    response = requests.get(url)

    if response.status_code == 200:
        products = response.json()['_embedded']['products']
        # print(products[0]['_embedded']['articles'][0]['_embedded']['listing']['pricing'])

        sorted_products = sorted(products,
                                 key=lambda x: x['_embedded']['articles'][0]['_embedded']['listing']['pricing'].get(
                                     'basePrice', x['_embedded']['articles'][0]['_embedded']['listing']['pricing'][
                                         'currentRetailPrice']))

        # Define a conversion function for cents to euros
        def convert_cents_to_euros(price_in_cents):
            price_in_euros = round(price_in_cents / 100, 2)
            formatted_price = '{:.2f} €'.format(price_in_euros)
            return formatted_price

        # Print the table header
        print('{:<60} {:<20} {:<20}'.format('Product Name', 'Base Price', 'Retail Price'))
        print('-' * 100)

        # Loop through the sorted products and print each row in the table
        for product in sorted_products:
            product_name = product['productName']

            retail_price = product['_embedded']['articles'][0]['_embedded']['listing']['pricing']['currentRetailPrice']
            base_price = product['_embedded']['articles'][0]['_embedded']['listing']['pricing'].get('basePrice',
                                                                                                    retail_price)
            euro_price = convert_cents_to_euros(base_price)
            euro_retail_price = convert_cents_to_euros(retail_price)
            print('{:<60} {:<20} {:<20}'.format(product_name, euro_price, euro_retail_price))
    else:
        print(f"Request failed with status code {response.status_code}")


if __name__ == '__main__':
    rewe()
