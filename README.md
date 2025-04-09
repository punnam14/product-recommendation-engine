## AI-Powered Product Recommendation Engine

### Overview

This project builds a product recommendation system that leverages LLMs to generate personalized recommendations based on user preferences and browsing history. This system demonstrates techniques such as prompt engineering, building APIs, and creating a functional frontend interface.

### 🌐 Live Demo

- **Frontend** (React + Netlify):  
  🔗 [https://product-reccomendation-engine.netlify.app](https://product-reccomendation-engine.netlify.app)  

- **Backend** (FastAPI + Render):  
  🔗 [https://product-recommendation-engine.onrender.com/api/products](https://product-recommendation-engine.onrender.com/api/products)

### Setup Instructions

#### Backend Setup
1. Navigate to the `backend` directory
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file based on `.env.example` and add your LLM API key
6. Run the application: `python app.py`
7. The backend runs on `http://0.0.0.0:4000`

#### Frontend Setup
1. Navigate to the `frontend` directory
2. When running locally, navigate to `services/api.js` and uncomment line 1 `const API_BASE_URL = 'http://localhost:4000/api';`
3. Install dependencies: `npm install`
4. Start the development server: `npm start`
5. The application should open at `http://localhost:3000`

#### Testing
1. Navigate to the root directory.
2. Run the following command: `python tests/test_services.py`
3. Run the following command: `python tests/test.py`
4. The script will output the result of each function test.

#### Logging
1. To monitor LLM token usage and help optimize prompt design, the backend includes a lightweight logging system that estimates how many tokens were sent and received per API call.
2. It logs Input Tokens: Approximate count of tokens sent in the prompt (based on character length).
3. Output Tokens: Approximate count of tokens returned by the LLM response.
4. Timestamps: Logs the date and time of each interaction.
5. Logs are saved to `logs/output_token_log.txt`
![Screenshot 2025-04-08 at 11 04 38 PM](https://github.com/user-attachments/assets/a89e9e77-9654-4e1a-9b1e-c437d7fa2882)

### Recommendation Generation Logic (LLM Service)

The recommendation engine is powered by a custom-built `LLMService` that leverages Google's Gemini model to generate personalized product suggestions based on user preferences and browsing behavior.

#### 🔍 High-Level Approach

**Filtering Phase**:  
Before involving the LLM, we narrow down the product catalog to the most relevant candidates by applying filters such as:  
- Price range (`under50`, `50to100`, `over100`)
- User-selected and browsed categories
- Brands inferred from the user’s browsing history
- Related tags (identified via a secondary LLM call using browsing tags)

**Prompt Engineering**:  
A structured prompt is crafted containing:

- User preferences and a summary of their browsing history
- A filtered product list to ensure only known items are recommended
- Clear instructions to return a JSON list with:
  - `product_id`
  - `explanation` (in a shopping-assistant tone)
  - `score` (confidence rating 1–10)

**LLM Response Handling**:
- The prompt is sent to the Gemini API for content generation.
- The response is parsed to extract product IDs and their associated explanations.
- Each ID is mapped back to the full product metadata before returning final recommendations to the user.

**Additional Enhancements**:

- Uses **semantic tag expansion** via the LLM to discover related product tags based on the user’s behavior.
- Logs estimated token usage per call to track prompt size and response length.
- Includes **fallback logic** to ensure a minimum number of candidates are always available for recommendation.

This modular structure ensures **tunability** and a high degree of control over both *what* is sent to the LLM and *how* the results are interpreted.

### Project 

#### Backend (Python)
- Develops a REST API that interfaces with an LLM (Gemini - gemini-2.0-flash)
- Implements prompt engineering to optimize product recommendations based on user preferences
- Creates endpoints for:
  - Accepting user preference data
  - Processing browsing history
  - Returning personalized product recommendations with explanations

#### Frontend (React)
- Builds a clean interface showing the product catalog
- Implements a user preference form to capture interests (e.g., preferences for categories, price ranges, styles)
- Creates a browsing history simulation (users can click on products to add them to history)
- Displays personalized recommendations with reasoning from the LLM

#### Backend Structure
```
backend/
│
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── config.py            # Configuration (add your API keys here)
├── data/
│   └── products.json    # Sample product catalog
│
├── services/
│   ├── __init__.py
│   ├── llm_service.py   # Service for LLM interactions (implement this)
│   └── product_service.py  # Service for product data operations
│
└── README.md            # Backend setup instructions
```

#### Frontend Structure
```
frontend/
│
├── public/
│   └── index.html
│
├── src/
│   ├── App.js           # Main application component
│   ├── index.js         # Entry point
│   ├── components/
│   │   ├── Catalog.js   # Product catalog display (implement this)
│   │   ├── UserPreferences.js  # Preference form (implement this)
│   │   ├── Recommendations.js  # Recommendations display (implement this)
│   │   └── BrowsingHistory.js  # Browsing history component (implement this)
│   │
│   ├── services/
│   │   └── api.js       # API client for backend communication
│   │
│   └── styles/
│       └── App.css      # Styling
│
├── package.json         # NPM dependencies
└── README.md            # Frontend setup instructions
```

### Sample Dataset

The sample product catalog (`products.json`) contains 50 products across various categories. Each product has the following structure:

```json
{
  "id": "product123",
  "name": "Ultra-Comfort Running Shoes",
  "category": "Footwear",
  "subcategory": "Running",
  "price": 89.99,
  "brand": "SportsFlex",
  "description": "Lightweight running shoes with responsive cushioning and breathable mesh upper.",
  "features": ["Responsive cushioning", "Breathable mesh", "Durable outsole"],
  "rating": 4.7,
  "inventory": 45,
  "tags": ["running", "athletic", "comfortable", "lightweight"]
}
```

The dataset includes products from categories such as:
- Electronics (smartphones, laptops, headphones, etc.)
- Clothing (shirts, pants, dresses, etc.)
- Home goods (furniture, kitchenware, decor, etc.)
- Beauty & Personal Care (skincare, makeup, fragrances, etc.)
- Sports & Outdoors (equipment, apparel, accessories, etc.)

### Key Implementation Guidelines

#### LLM Integration
- Uses Gemini - gemini-2.0-flash 
- Implements proper error handling for API calls
- Uses appropriate context windows and token limits

#### Prompt Engineering
- Designs prompts that effectively leverage product metadata and user preferences
- Ensures your prompts provide reasoning for recommendations
- Considers how to handle context limitations for larger product catalogs

#### API Design
- Creates RESTful endpoints with proper request/response formats
- Implements appropriate error handling
- Considers performance and optimization

#### React Frontend
- Focuses on clean, functional UI rather than elaborate designs
- Implements responsive components that adapt to different screen sizes
- Uses React state management appropriately (useState, useContext, etc.)

### In Progress 

1. Add user authentication and profile persistence
2. Implement caching for LLM responses to improve performance
3. Add filtering and sorting options to the product catalog
4. Create A/B testing for different prompt strategies
5. Add unit and/or integration tests

### Notes and Tips

- **API Keys**: Never commit your API keys to GitHub. Use environment variables.
- **Documentation**: Document your approach, especially your prompt engineering strategy.
- **Code Quality**: Clean, well-organized code is more important than feature quantity.

### Resources

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

