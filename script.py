import requests
import os

# Enter your Flickr API keys
FLICKR_API_KEY = "FLICKR_API_KEY"
FLICKR_USER_ID = "FLICKR_USER_ID@N07"

SAVE_DIRECTORY = "img"
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

def get_user_photos():
    photos = []
    page = 1
    while True:
        url = f"https://api.flickr.com/services/rest/?method=flickr.people.getPublicPhotos&api_key={FLICKR_API_KEY}&user_id={FLICKR_USER_ID}&format=json&nojsoncallback=1&page={page}"
        response = requests.get(url)
        data = response.json()
        if data["stat"] == "ok":
            photos += data["photos"]["photo"]
            page += 1
            if page > data["photos"]["pages"]:
                break
        else:
            print("Failed to retrieve photos from Flickr.")
            break
    return photos

def download_photo(photo, index, total_photos):
    photo_url = f"https://farm{photo['farm']}.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_b.jpg"
    file_path = os.path.join(SAVE_DIRECTORY, f"{photo['id']}.jpg")
    try:
        response = requests.get(photo_url)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded photo {index+1}/{total_photos} - 100% complete")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download photo {index+1}/{total_photos}: {str(e)}")

def main():
    photos = get_user_photos()
    total_photos = len(photos)
    print(f"Found {total_photos} photos.")

    for i, photo in enumerate(photos):
        download_photo(photo, i, total_photos)

    print("All photos downloaded successfully.")

if __name__ == "__main__":
    main()