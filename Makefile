# Define directories
TRACKS_DIR = media/tracks
IMG_DIR = media/img
PLAYLISTS_DIR = media/playlists

# Create necessary directories
.PHONY: setup
setup:
	mkdir -p $(TRACKS_DIR)
	mkdir -p $(IMG_DIR)
	mkdir -p $(PLAYLISTS_DIR)

# Clean target
.PHONY: clean
clean:
	@echo "Cleaning directories..."
	@rm -rf $(TRACKS_DIR) $(IMG_DIR)
	@echo "Directories cleaned."

# Run the Python script to start the bot
.PHONY: app
app:
	@echo "Starting the bot..."
	@python3 app.py
