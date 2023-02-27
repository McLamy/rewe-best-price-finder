import requests


def get_all_products(search_term, market_id):
    # Set the initial page and object per page values
    page = 0
    objects_per_page = 80

    # Initialize an empty list to store the products
    all_products = []

    # Loop until there are no more products to retrieve
    while True:
        # Construct the URL with the search term, market ID, page, and objects per page
        url = f"https://shop.rewe.de/api/products/?search={search_term}&market={market_id}&page={page}&objectsPerPage={objects_per_page}"

        # Send the request and check the status code
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            return None

        # Extract the products from the response and append to the list of all products
        products = response.json()["_embedded"]["products"]
        all_products.extend(products)

        # Check if there are more pages to retrieve
        if len(products) < objects_per_page:
            break

        # Increment the page number for the next request
        page += 1

    # Return the list of all products
    return all_products


def rewe():
    # Set the search term and market ID
    search_term = input("What to search?: ")
    market_id = "1940130"

    # Retrieve all the available products that match the search term and market ID
    products = get_all_products(search_term, market_id)

    # Sort the products by base price or retail price
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
    print('{:<60} {:<20} {:<20}'.format(f'Product Name ({len(sorted_products)} items)', 'Base Price', 'Retail Price'))
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


if __name__ == '__main__':
    rewe()
