import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep


# Function to open a display images based on a given prompt
def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    
    # Generate the File name for the image
    Files = [f"{prompt}{i}.jpg" for i in range(1, 6)]
    
    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        
        try:
            # Try to open and display the image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1) # Pause fo 1 second to display the next image
            
        except IOError:
            print(f"Failed to open image: {image_path}")
            
        
# API details for the Hugging Face Stable Diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Async function to generate images based on a given prompt
async def generate_images(prompt):
    tasks = []
    
    # Create 4 Image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality = 4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}", 
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)
        
    # Wait for all task to complete
    image_bytes_list = await asyncio.gather(*tasks)
    
    # Save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ', '_')}{i+1}.jpg", "wb") as f:
            f.write(image_bytes)
            
# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt)) # Run the async image generation
    open_images(prompt)
    
while True:
    
    try:
        # Read teh status and prompt from the data file
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()
            
        Prompt, Status = Data.split(",")
        
        # If the status indicates an image generation request
        if Status == "True":   
            print("Generating Images")
            ImageStatus = GenerateImages(prompt=Prompt)
            
            # Reset the status in the data file after generating the images
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False, False")
                break # Exits the loop after processing the request
            
        else:
            sleep(1) # Wait for 1 second before checking again
            
    except :
        pass