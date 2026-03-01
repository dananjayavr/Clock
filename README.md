# Literature Clock

A Raspberry Pi kiosk that displays literary quotes matching the current time, built with Flask and Alpine.js.

## How It Works

Every minute, the app reads a JSON file matching the current time (e.g. `14_35.json`) from the `literature-clock/docs/times/` submodule, picks a random quote, and displays it in the browser in kiosk mode.

---

## Setup

### 1. Clone the repo with submodule

```bash
git clone --recurse-submodules <your-repo-url>
cd literature-clock
```

If you already cloned without the submodule:

```bash
git submodule update --init --recursive
```

### 2. Create a virtualenv and install Flask

```bash
python3 -m venv venv
venv/bin/pip install flask
```

### 3. Set up the systemd service

Create `/etc/systemd/system/literature-clock.service`:

```ini
[Unit]
Description=Literature Clock Flask App
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/literature-clock
ExecStart=/home/pi/literature-clock/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start it:

```bash
sudo systemctl enable literature-clock
sudo systemctl start literature-clock
```

### 4. Set up Chromium autostart

Create `~/.config/autostart/literature-clock.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Literature Clock
Exec=bash -c "sleep 5 && chromium-browser http://127.0.0.1:5000 --noerrdialogs --disable-infobars --no-first-run --ozone-platform=wayland --enable-features=OverlayScrollbar --start-maximized --kiosk"
```

### 5. Boot to desktop

The Pi must boot to desktop (not CLI) for the autostart to work:

```bash
sudo raspi-config
# System Options → Boot / Auto Login → Desktop Autologin
```

---

## After a Reboot

Everything runs automatically. To verify:

```bash
# Check Flask is running
sudo systemctl status literature-clock

# View logs if something is wrong
journalctl -u literature-clock -f
```

---

## Project Structure

```
literature-clock/
├── app.py                  # Flask backend
├── templates/
│   └── index.html          # Alpine.js + Tailwind CSS frontend
├── venv/                   # Python virtualenv (not committed)
└── literature-clock/docs/  # Git submodule with quote JSON files
    └── times/
        └── HH_MM.json
```

---

## Tech Stack

- **Flask** — serves the app and picks a random quote for the current minute
- **Alpine.js** — reactive frontend, refreshes the quote in sync with the clock
- **Tailwind CSS** — styling with automatic dark/light mode based on time of day
- **Playfair Display** — elegant serif font via Google Fonts
- **Raspberry Pi** — runs in kiosk mode via Chromium
