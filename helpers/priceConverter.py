import requests

def convert_to_eur(price_in_cents, from_currency="USD"):
    try:
        price = price_in_cents / 100
        url = f"https://v6.exchangerate-api.com/v6/89012612c66299ef25481075/pair/{from_currency}/EUR/{price}"
        res = requests.get(url)
        data = res.json()

        if data.get("result") == "success":
            return round(data["conversion_result"], 2)
        else:
            raise ValueError(f"Conversion failed: {data}")
    except Exception as e:
        print(f"[Currency API Error] {e}")
        return None
