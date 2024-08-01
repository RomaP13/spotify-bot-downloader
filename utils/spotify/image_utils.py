import requests


def download_cover_image(url: str, output_path: str) -> str | None:
    """
    Download the cover image from a given URL and
    save it to the specified output path.

    Args:
        url (str): URL of the cover image.
        output_path (str): Path where the image will be saved.

    Returns:
        str | None: Path to the saved image or None if an error occurred.
    """
    try:
        response = requests.get(url)
        with open(output_path, "wb") as file:
            file.write(response.content)
        return output_path
    except requests.RequestException as e:
        print(f"ERROR: {e}")

    return None
