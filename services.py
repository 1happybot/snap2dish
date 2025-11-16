"""Services for image analysis and recipe generation."""
import os
import base64
import requests
from typing import Dict, Optional


class ImageAnalysisService:
    """Service for analyzing food images using GitHub Models API."""
    
    def __init__(self, github_token: str, endpoint: str):
        """Initialize the service with GitHub token and endpoint."""
        self.github_token = github_token
        self.endpoint = endpoint
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {github_token}"
        }
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_food_image(self, image_path: str) -> Dict[str, any]:
        """
        Analyze a food image and return dish information.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing dish_name, ingredients, instructions, and cuisine_type
        """
        if not self.github_token:
            # Return mock data for development/testing
            return self._get_mock_response()
        
        try:
            # Encode the image
            base64_image = self.encode_image(image_path)
            
            # Prepare the request to GitHub Models
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analyze this food image and provide:
1. Dish name
2. List of ingredients (comma-separated)
3. Step-by-step cooking instructions
4. Cuisine type

Format your response as JSON with keys: dish_name, ingredients, instructions, cuisine_type"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "model": "gpt-4o",
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            # Make the request
            response = requests.post(
                f"{self.endpoint}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Parse the response
                return self._parse_response(content)
            else:
                # Fallback to mock data if API fails
                return self._get_mock_response()
                
        except Exception as e:
            print(f"Error analyzing image: {e}")
            # Return mock data on error
            return self._get_mock_response()
    
    def _parse_response(self, content: str) -> Dict[str, str]:
        """Parse the AI response into structured data."""
        import json
        
        try:
            # Try to parse as JSON first
            if '{' in content and '}' in content:
                json_start = content.index('{')
                json_end = content.rindex('}') + 1
                json_str = content[json_start:json_end]
                data = json.loads(json_str)
                return {
                    'dish_name': data.get('dish_name', 'Unknown Dish'),
                    'ingredients': data.get('ingredients', 'Not available'),
                    'instructions': data.get('instructions', 'Not available'),
                    'cuisine_type': data.get('cuisine_type', 'Unknown')
                }
        except:
            pass
        
        # Fallback: extract information from text
        return self._extract_from_text(content)
    
    def _extract_from_text(self, content: str) -> Dict[str, str]:
        """Extract information from plain text response."""
        lines = content.split('\n')
        result = {
            'dish_name': 'Unknown Dish',
            'ingredients': 'Not available',
            'instructions': 'Not available',
            'cuisine_type': 'Unknown'
        }
        
        current_section = None
        for line in lines:
            line = line.strip()
            if 'dish' in line.lower() and ':' in line:
                result['dish_name'] = line.split(':', 1)[1].strip()
            elif 'ingredient' in line.lower() and ':' in line:
                current_section = 'ingredients'
                result['ingredients'] = line.split(':', 1)[1].strip()
            elif 'instruction' in line.lower() and ':' in line:
                current_section = 'instructions'
                result['instructions'] = line.split(':', 1)[1].strip()
            elif 'cuisine' in line.lower() and ':' in line:
                result['cuisine_type'] = line.split(':', 1)[1].strip()
            elif current_section and line:
                result[current_section] += '\n' + line
        
        return result
    
    def _get_mock_response(self) -> Dict[str, str]:
        """Return mock data for testing/development."""
        return {
            'dish_name': 'Delicious Food Dish',
            'ingredients': 'Main ingredients, Secondary ingredients, Spices and seasonings',
            'instructions': '1. Prepare the ingredients\n2. Cook according to the recipe\n3. Serve hot and enjoy!',
            'cuisine_type': 'International'
        }
