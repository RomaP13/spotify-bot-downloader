import os

import eyed3


def add_metadata_to_track(
    file_path: str, track_info: dict, cover_path: str
) -> None:
    """
    Adds metadata to an audio track file.

    Args:
        file_path (str): The path to the audio file to update.
        track_info (dict): A dictionary containing track information.
        cover_path (str): The path to the cover image file to
        embed in the audio file.

    Raises:
        AssertionError: If the audio file or its tag is not found.
    """
    eyed3.log.setLevel("ERROR")  # Set the log level to only show errors

    audiofile = eyed3.load(file_path)
    assert audiofile is not None, "Audio file could not be loaded."
    assert audiofile.tag is not None, "Audio file does not have a tag."

    audiofile.tag.title = track_info["title"]
    audiofile.tag.artist = track_info["artists"]
    audiofile.tag.album = track_info["album"]
    audiofile.tag.release_date = track_info["release_date"]
    audiofile.tag.genre = track_info["genres"]

    track_number_str = str(track_info["track_number"])
    total_tracks_str = str(track_info["total_tracks"])

    track_number = int(track_number_str) if track_number_str.isdigit() else 0
    total_tracks = int(total_tracks_str) if total_tracks_str.isdigit() else 0

    audiofile.tag.track_num = (track_number, total_tracks)

    if cover_path and os.path.exists(cover_path):
        with open(cover_path, "rb") as image_file:
            imagedata = image_file.read()
        audiofile.tag.images.set(3, imagedata, "image/jpeg", "cover")

    audiofile.tag.save()
