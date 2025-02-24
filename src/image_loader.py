import requests

class ImageLoader:
    def __init__(self):
        pass

    @staticmethod
    def download_image(url: str, file_path: str):
        response = requests.get(url)

        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
        else:
            print("Failed to download image. Status code:", response.status_code)