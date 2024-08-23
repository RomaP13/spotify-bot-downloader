# Define directories
IMG_DIR = media/img
TRACKS_DIR = media/tracks
PLAYLISTS_DIR = media/playlists
ALBUMS_DIR = media/albums

# Create necessary directories
.PHONY: setup
setup:
	mkdir -p $(IMG_DIR)
	mkdir -p $(TRACKS_DIR)
	mkdir -p $(PLAYLISTS_DIR)
	mkdir -p $(ALBUMS_DIR)

# Clean target
.PHONY: clean
clean:
	@echo "Cleaning directories..."
	@rm -rf $(TRACKS_DIR) $(IMG_DIR) ${PLAYLISTS_DIR}
	@echo "Directories cleaned."

# Run the Python script to start the bot
.PHONY: app
app:
	@echo "Starting the bot..."
	@python3 app.py
