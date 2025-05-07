from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Optional
from pydantic import BaseModel, Field
import getpass
import os
from dotenv import load_dotenv
load_dotenv()

# store api key in environment variable
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

# initialize the chat models
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")
image_llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-exp-image-generation")

# create a pydantic class to structure the llm output
class Campaign(BaseModel):
    """Create different creative material for ad copy."""

    headline: str = Field(description="A catchy one-liner headline")
    description: str = Field(description="Short paragraph creatively describing the product or offer")
    image_prompt: str = Field(description="A image prompt to generate a visual element for ad")
    call_to_action: str = Field(description="A direct action the viewer should take")


structured_llm = llm.with_structured_output(Campaign)

# prompt for ad copy generation
prompt = ChatPromptTemplate([

    ("system", "You are a online ads marketing expert."),

    ("user", 
     """
    Generate a compelling digital ad copy using the details below. Structure the output into four clear sections: Headline, Ad Description, Creative Idea, and Call to Action. The ad should be short, engaging, and match the desired tone.

    #Brand Information
    - Brand Name: {brand_name}
    - Product Name: {product_name}
    - Description: {brand_description}

    # Target Audience
    - Age Category: {age_category}
    - Gender: {gender}

    # Campaign Objective
    - Goal: {campaign_goal}

    # Style
    - Tone: {tone}

    # Format Your Output Like This:
    ---
    **Headline:** <A catchy one-liner headline>

    **Ad Description:** <Short paragraph creatively describing the product or offer>

    **Creative Idea:** <An image generation prompt to create an creative image for the ad>

    **Call to Action:** <Direct action the viewer should take, like “Download now” or “Visit our store”>
    ---
    Make sure the ad reflects the tone and suits the audience profile.  
    """)
])

# chain for llm ad copy generation
ad_chain = prompt | structured_llm


