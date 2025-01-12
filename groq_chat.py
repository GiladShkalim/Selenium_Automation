from dotenv import load_dotenv
import os
from groq import Groq
import json
import logging

TITLE = """FLASH50: Half-Price Frenzy!"""
DESCRIPTION = """Grab your favorite items at unbeatable prices! For the next 24 hours, enjoy a whopping 50% off on all products storewide. Whether you're eyeing that stylish jacket or the latest tech gadget, now's your chance to snag it for half the price. But hurry, this offer vanishes at midnight! Use code FLASH50 at checkout to unlock your savings. Don't miss out on this lightning-fast deal – shop now before time runs out!"""    
CATEGORIES = """["Home & Furniture","Electronics & Gadgets","Fashion & Apparel","Beauty & Personal Care","Groceries & Food","Health & Wellness","Sports & Outdoors","Toys & Games","Books & Media","Automotive & Tools","Pet Supplies","Office & School Supplies","Jewelry & Accessories","Baby & Kids","Garden & Outdoor Living"]"""
CONSUMER_STATUS = """["Student","Parent","Retiree","Professional","Homeowner","Renter","Newlywed","Single","Military/Veteran","Entrepreneur","Unemployed","Caregiver","Digital Nomad","First-time Buyer","Empty Nester"]"""
MESSAGE_TO_SEND = f"""Analyze the provided coupon offer title and description. Then, perform the following tasks:
1. Select all appropriate categories from the given list of categories.
2. Choose all relevant consumer statuses from the provided list of consumer statuses.
3. Create a JSON response with the following structure:
   {{
     "labels": ["Category1", "Category2", ...],
     "consumer_statuses": ["Status1", "Status2", ...],
     "title": "{TITLE}",
     "description": "{DESCRIPTION}"
   }}
Ensure that:
- The "labels" field contains as many relevant categories as possible, using exact names from the provided list.
- The "consumer_statuses" field includes all applicable consumer statuses, using exact names from the given list.
- The "title" and "description" fields contain the original offer title and description.

Offer Title: "{TITLE}"
Offer Description: "{DESCRIPTION}"
List of Categories: {CATEGORIES}
List of Consumer Statuses: {CONSUMER_STATUS}
"""



# Load environment variables
load_dotenv()


def send_chat_message(message: str) -> dict | None:
    """
    Send a message to Groq API and receive JSON response.

    Args:
        message (str): The message to send to the AI

    Returns:
        dict | None: Parsed JSON response from the API, or None if error occurs
    """
    try:
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": message
            }],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        return json.loads(completion.choices[0].message.content)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    response = send_chat_message(MESSAGE_TO_SEND)
    if response:
        print("\nAI's API Response:")
        print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main() 