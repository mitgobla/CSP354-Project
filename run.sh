# Run script on startup inside /etc/rc.local before exit 0
# Ensure it is executable: chmod +x /etc/rc.local
# Include ampersand at end of command to run in background

# Update git repo
git pull

# Install dependencies
python3.7 -m pip install -r requirements.txt

# Run python script
libcamerify python3.7 -m main.run
