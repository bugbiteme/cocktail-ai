import os
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()

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
    recipe = await generate_cocktail_recipe("Generate a cocktail recipe called the "+request.prompt)
    image_url = "placeholder.url"
    image_url = await generate_image("An image of a cocktail: " + request.prompt + "which is made from the following recipe: " + recipe)
    return {"recipe_name": request.prompt, "recipe": recipe, "image_url": image_url} 