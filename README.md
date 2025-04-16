# CS2 Skins
 Price checker for CS2 itens with mobile app with push notifications

## Updates

### 16/04/2025

- Endpoints:
    1. `/steam-data`: Fetches the price overview for a specific CS2 skin (e.g., Fever Case).
    2. `/search-item`: Searches for CS2 skins based on a provided name and returns a list of results with their prices in both USD and EUR.

- Response Models:
    - `SearchData`: Represents individual skin information with name, price (USD), and price in EUR.
    - `SearchResponse`: Represents the response structure for the search endpoint with a total result count and a list of `SearchData`.

- Currency Conversion:
    - USD to EUR conversion is handled using an external API with proper error handling.
