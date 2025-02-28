import requests

url = "http://127.0.0.1:8000/generate"

# Define the prompt
prompt_text = "A snowy winter landscape, with a man in warm clothing, holding a cup of tea and smiling"

# Open the image file
with open("data\images\Kirill.jpg", "rb") as image_file:
    files = {"image": image_file}  # File upload
    data = {"prompt": prompt_text}  # Form data
    
    # Send POST request
    response = requests.post(url, files=files, data=data)

# Save the generated image
if response.status_code == 200:
    with open("retrived_image.png", "wb") as output_file:
        output_file.write(response.content)
else:
    print(response.text)
