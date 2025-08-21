import asyncio
from random import randint
from PIL import Image
import requests
import os
from time import sleep


# Function to open and display images based on the given prompt
def open_images(prompt):
    folder_path = r"Data\Images"
    prompt = prompt.replace(" ", "_")
    # Generate the filenames for the images
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")


# Free Pollinations API (no key required)
API_URL = "https://image.pollinations.ai/prompt/"


# Async function to send query to Pollinations API
async def query(payload):
    prompt = payload["text"]
    url = API_URL + prompt.replace(" ", "%20")
    response = await asyncio.to_thread(requests.get, url)
    return response.content


# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {
            "text": f"{prompt}, ultra realistic, 4K, high detail, seed={randint(0,1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    folder_path = r"Data\Images"
    os.makedirs(folder_path, exist_ok=True)
    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            with open(os.path.join(folder_path, f"{prompt.replace(' ', '_')}{i + 1}.jpg"), "wb") as f:
                f.write(image_bytes)


def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)


# Main monitoring loop for image generation requests
while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()
        Prompt, Status = Data.split(",")

        if Status == "True":
            print("Generating Images...")
            GenerateImages(prompt=Prompt)

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break
        else:
            sleep(1)
    except Exception as e:
        print(e)
