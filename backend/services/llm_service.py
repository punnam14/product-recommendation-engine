import openai
import requests
import json
from config import config

class LLMService:
    """
    Service to handle interactions with the LLM API
    """
    
    def __init__(self):
        """
        Initialize the LLM service with configuration
        """
        openai.api_key = config['OPENAI_API_KEY']
        self.model_name = config['MODEL_NAME']
        self.max_tokens = config['MAX_TOKENS']
        self.temperature = config['TEMPERATURE']
        self.api_key = config['OPENAI_API_KEY']
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
    
    def generate_recommendations(self, user_preferences, browsing_history, all_products):
        """
        Generate personalized product recommendations based on user preferences and browsing history
        
        Parameters:
        - user_preferences (dict): User's stated preferences
        - browsing_history (list): List of product IDs the user has viewed
        - all_products (list): Full product catalog
        
        Returns:
        - dict: Recommended products with explanations
        """
        # TODO: Implement LLM-based recommendation logic
        # This is where your prompt engineering expertise will be evaluated
        
        # Get browsed products details
        browsed_products = []
        for product_id in browsing_history:
            for product in all_products:
                if product["id"] == product_id:
                    browsed_products.append(product)
                    break
        
        # Create a prompt for the LLM
        # IMPLEMENT YOUR PROMPT ENGINEERING HERE
        prompt = self._create_recommendation_prompt(user_preferences, browsed_products, all_products)
        
        # Call the LLM API
        try:
            response = requests.post(
                self.gemini_url,
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                }
            )

            if response.status_code != 200:
                raise Exception(f"Gemini API error: {response.text}")

            raw_text = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("RAW LLM RESPONSE:", raw_text)
            
            # Parse the LLM response to extract recommendations
            # IMPLEMENT YOUR RESPONSE PARSING LOGIC HERE
            recommendations = self._parse_recommendation_response(raw_text, all_products)
            return recommendations
            
        except Exception as e:
            # Handle any errors from the LLM API
            print(f"Error calling LLM API: {str(e)}")
            raise Exception(f"Failed to generate recommendations: {str(e)}")
    
    def _create_recommendation_prompt(self, user_preferences, browsed_products, all_products):
        """
        Create a prompt for the LLM to generate recommendations
        
        This is where you should implement your prompt engineering strategy.
        
        Parameters:
        - user_preferences (dict): User's stated preferences
        - browsed_products (list): Products the user has viewed
        - all_products (list): Full product catalog
        
        Returns:
        - str: Prompt for the LLM
        """
        # TODO: Implement your prompt engineering strategy
        # THIS FUNCTION MUST BE IMPLEMENTED BY THE CANDIDATE
        
        # Example basic prompt structure (you should significantly improve this):
        prompt = "Based on the following user preferences and browsing history, recommend 5 products from the catalog with explanations.\n\n"
        
        # Add user preferences to the prompt
        prompt += "User Preferences:\n"
        for key, value in user_preferences.items():
            prompt += f"- {key}: {value}\n"
        
        # Add browsing history to the prompt
        prompt += "\nBrowsing History:\n"
        for product in browsed_products:
            prompt += f"- {product['name']} (Category: {product['category']}, Price: ${product['price']})\n"
        
        # Add instructions for the response format
        prompt += (
            "\nPlease recommend 5 products from the catalog that match the user's preferences and browsing history.\n"
            "For each recommendation, include:\n"
            "- 'product_id': must match an existing ID from the catalog below\n"
            "- 'explanation': a friendly, persuasive message that tells the user why they'll love this product\n"
            "  — Use a tone like a shopping assistant helping them, not a developer or analyst.\n"
            "  — Speak directly to the user (use phrases like 'you' and 'your').\n"
            "  — Mention things like preferences, categories, or brands in a natural way.\n"
            "- 'score': your confidence in the recommendation, 1 to 10.\n"
        )
        prompt += "\nFormat your response as a JSON array with objects containing 'product_id', 'explanation', and 'score' (1-10 indicating confidence)."
        prompt += ("\nIMPORTANT: Only recommend products that exist in the following catalog. "
                    "Use the exact 'id' values provided below. Do not invent product names or IDs.\n")
        
        prompt += "\nHere are product IDs and names in the catalog:\n"
        for product in all_products[:20]:  
            prompt += f"- {product['id']}: {product['name']}\n"

        # You would likely want to include the product catalog in the prompt
        # But be careful about token limits!
        # For a real implementation, you might need to filter the catalog to relevant products first
        
        return prompt
    
    def _parse_recommendation_response(self, llm_response, all_products):
        """
        Parse the LLM response to extract product recommendations
        
        Parameters:
        - llm_response (str): Raw response from the LLM
        - all_products (list): Full product catalog to match IDs with full product info
        
        Returns:
        - dict: Structured recommendations
        """
        # TODO: Implement response parsing logic
        # THIS FUNCTION MUST BE IMPLEMENTED BY THE CANDIDATE
        
        # Example implementation (very basic, should be improved):
        try:
            import json
            # Attempt to parse JSON from the response
            # Note: This is a simplistic approach and should be made more robust
            # The candidate should implement better parsing logic
            
            # Find JSON content in the response
            start_idx = llm_response.find('[')
            end_idx = llm_response.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                # Fallback if JSON parsing fails
                return {
                    "recommendations": [],
                    "error": "Could not parse recommendations from LLM response"
                }
            
            json_str = llm_response[start_idx:end_idx]
            rec_data = json.loads(json_str)
            print("PARSED LLM JSON RESPONSE:", rec_data)
            
            # Enrich recommendations with full product details
            recommendations = []
            for rec in rec_data:
                product_id = rec.get('product_id')
                print("Matching LLM product_id:", rec.get("product_id"))
                product_details = None
                
                # Find the full product details
                for product in all_products:
                    if product['id'] == product_id:
                        product_details = product
                        break
                
                if product_details:
                    print("Matched product:", product_details["id"])
                    recommendations.append({
                        "product": product_details,
                        "explanation": rec.get('explanation', ''),
                        "confidence_score": rec.get('score', 5)
                    })
                else:
                    print("Could not find product_id:", product_id)
            
            return {
                "recommendations": recommendations,
                "count": len(recommendations)
            }
            
        except Exception as e:
            print(f"Error parsing LLM response: {str(e)}")
            return {
                "recommendations": [],
                "error": f"Failed to parse recommendations: {str(e)}"
            }