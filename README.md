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

### 17/04/2025

- **New Endpoints**:
    1. `/item-data`: Retrieves detailed information about a specific CS2 skin, including minimum price, maximum price, sales data, and rarity.
    2. `/all-items`: Fetches all market items for CS2 and stores them locally for further processing (useful for caching and matching skin names).
    
- **Response Models**:
    - `ItemResponse`: Represents detailed skin information, including minimum and maximum prices, sales data, and rarity.

- **Caching**:
    - Extended caching functionality to include the new `/item-data` and `/all-items` endpoints, improving performance and reducing repeated API calls.

- **Fuzzy Name Matching**:
    - Fuzzy matching logic has been applied to improve search accuracy, filtering and matching skin names with higher precision.

- **Error Handling**:
    - Enhanced error handling with specific exceptions (`ExternalAPIError`, `DataProcessingError`, `InternalServerError`) for new endpoints.