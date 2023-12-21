import os
from openai import OpenAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel



app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Only do this if not in debug mode
if os.getenv("DEBUG") != "true":
    # Get the API key from the environment variable
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    if not client.api_key:
        raise ValueError("No OpenAI API key found")

# be sure to delete or comment out. for debug only
# print(client.api_key) 

async def generate_cocktail_recipe(prompt):
    try:
        response = client.completions.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )
        return response.choices[0].text
    except Exception as e:
        print(f"An error occurred generating recipe: {e}")
        return None

async def generate_image(description):
    try:
        # Generate an image using DALL-E based on the description
        response = client.images.generate(
            model="dall-e-3",
            prompt=description,
            n=1,  # Number of images to generate
            size="1024x1024",  # Image size
            quality="standard"
        )

        # Assuming the response contains a URL to the generated image
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"An error occurred generating image: {e}")
        return None

# Define a request model
class RecipePrompt(BaseModel):
    prompt: str

@app.get("/")
async def usage():
    return {"message": "See /docs for API usage"}


@app.post("/generate-recipe/")
async def generate_recipe(request: RecipePrompt):

    # If environment variable DEBUG=true call a mock API fo testing
    if os.getenv("DEBUG") == "true":
        recipe = "\nMocktail\n1. Add Water\n2. Add Ice\n3. Add a twist of this and that\n4. Enjoy your "+ request.prompt
        image_url = "https://www.cupofzest.com/wp-content/uploads/2022/03/Blue-Lagoon-Mocktail-Thumbnail-2-Web.jpg.jpg"
    else:
        recipe = await generate_cocktail_recipe("Generate a cocktail recipe called the "+request.prompt)
        image_url = await generate_image("An image of a cocktail: " + request.prompt + "which is made from the following recipe: " + recipe)

    return {"recipe_name": request.prompt, "recipe": recipe, "image_url": image_url} 