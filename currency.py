import tkinter as tk
import geocoder
from forex_python.converter import CurrencyRates
import folium
import pycountry
import webbrowser

def convert_currency(amount, from_currency, to_currency):
    # Initialize currency rates object
    c = CurrencyRates()

    # Convert the amount from the source currency to the destination currency
    converted_amount = c.convert(from_currency, to_currency, amount)

    return converted_amount

def get_currency_code(country):
    # Get country's alpha-2 code from pycountry
    country_code = pycountry.countries.search_fuzzy(country)[0].alpha_3

    # Get currency code based on country code
    currency_code = pycountry.currencies.get(numeric=pycountry.countries.get(alpha_3=country_code).numeric).alpha_3

    return currency_code

def display_user_location_on_map():
    def convert_button_click():
        # Get the user input values
        amount = float(amount_entry.get())
        to_currency = to_currency_var.get()  # Get the selected "to" currency from the dropdown

        # Get user's location using geocoder
        g = geocoder.ip('me')
        latitude, longitude = g.latlng

        # Get user's country based on location
        country = g.country

        # Create a new window using Tkinter
        window = tk.Tk()
        window.title("User Location and Currency Converter")

        # Get currency code based on country
        currency_code = get_currency_code(country)

        # Calculate the converted amount
        converted_amount = convert_currency(amount, currency_code, to_currency)

        # Display the detected country, currency code, and converted amount in the window
        country_label = tk.Label(window, text="Detected Country: " + country)
        country_label.pack()

        currency_label = tk.Label(window, text="Currency Code: " + currency_code)
        currency_label.pack()

        converted_label = tk.Label(window, text=f'{amount} {currency_code} is equal to {converted_amount} {to_currency}')
        converted_label.pack()

        # Create a map centered around the user's location
        map_location = folium.Map(location=[latitude, longitude], zoom_start=10)

        # Add a marker for the user's location with the converted amount as a popup
        folium.Marker(
            [latitude, longitude],
            popup=f'{amount} {currency_code} is equal to {converted_amount} {to_currency}'
        ).add_to(map_location)

        # Save the map as an HTML file
        map_location.save('map.html')

        # Open the map in a web browser
        webbrowser.open('map.html', new=2)

        window.mainloop()

    # Create a new window using Tkinter
    window = tk.Tk()
    window.title("User Location and Currency Converter")

    # Create labels and input fields for amount and to_currency
    amount_label = tk.Label(window, text="Amount:")
    amount_label.pack()

    amount_entry = tk.Entry(window)
    amount_entry.pack()

    to_currency_label = tk.Label(window, text="To Currency:")
    to_currency_label.pack()

    # Get a list of all available currency codes using pycountry
    currency_codes = [currency.alpha_3 for currency in pycountry.currencies]
    to_currency_var = tk.StringVar(window)
    to_currency_var.set(currency_codes[0])  # Set the default "to" currency to the first currency in the list
    to_currency_dropdown = tk.OptionMenu(window, to_currency_var, *currency_codes)
    to_currency_dropdown.pack()

    convert_button = tk.Button(window, text="Convert", command=convert_button_click)
    convert_button.pack()

    window.mainloop()

# Call the function to display the user location on the map and currency conversion in a separate window
display_user_location_on_map()