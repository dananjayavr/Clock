# Literature Clock

A Raspberry Pi kiosk that displays literary quotes matching the current time, built with Flask and Alpine.js.

## How It Works

Every minute, the app reads a JSON file matching the current time (e.g. `14_35.json`) from the `literature-clock/docs/times/` submodule, picks a random quote, and displays it in the browser in kiosk mode. Dark/light mode switches automatically based on the time of day.

---

## Setup

### 1. Clone the repo with submodule

```bash
git clone --recurse-submodules <your-repo-url>
cd Clock
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
User=dananjaya
Group=dananjaya
WorkingDirectory=/home/dananjaya/Clock
ExecStart=/home/dananjaya/Clock/venv/bin/python app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start it:

```bash
sudo systemctl enable literature-clock
sudo systemctl start literature-clock
```

> **Note:** Use the venv Python path directly in `ExecStart` — no need to activate the virtualenv.

### 4. Set up Chromium autostart via labwc

Raspberry Pi OS uses **labwc** as its compositor. Create the autostart file:

```bash
mkdir -p ~/.config/labwc
nano ~/.config/labwc/autostart
```

Add this line:

```bash
bash -c "until curl -s http://127.0.0.1:5000 > /dev/null; do sleep 1; done; chromium-browser http://127.0.0.1:5000 --noerrdialogs --disable-infobars --no-first-run --ozone-platform=wayland --enable-features=OverlayScrollbar --start-maximized --kiosk --password-store=basic" &
```

Make it executable:

```bash
chmod +x ~/.config/labwc/autostart
```

> **Note:** The `&` at the end is required for labwc autostart. The `until curl` loop waits until Flask is ready before launching Chromium, avoiding connection refused errors.

> **Note:** `--password-store=basic` prevents the keyring password popup on boot.

### 5. Boot to desktop

The Pi must boot to desktop (not CLI) for the autostart to work:

```bash
sudo raspi-config
# System Options → Boot / Auto Login → Desktop Autologin
```

### 6. Remove any conflicting autostart entries

Check for and remove any old autostart scripts that might launch a different page:

```bash
# Check for old .desktop files
ls ~/.config/autostart/

# Check for old scripts in home folder
ls ~/

# Search for any other chromium references
grep -r "chromium" ~/.config/

# Remove anything that shouldn't be there
rm ~/.config/autostart/<old-entry>.desktop
rm ~/<old-script>.sh
```

---

## Verifying After a Reboot

```bash
# Check Flask is running
sudo systemctl status literature-clock

# View Flask logs
journalctl -u literature-clock -n 50

# Check labwc autostart is correct
cat ~/.config/labwc/autostart
```

---

## Troubleshooting

**Flask keeps restarting (status 217/USER)**
Make sure the `User=` in the service file matches your actual username:
```bash
whoami
```

**Connection refused in Chromium**
Flask isn't ready yet. The `until curl` loop handles this automatically — if it still fails, check Flask logs:
```bash
journalctl -u literature-clock -n 50
```

**Chromium opens the wrong page**
Another autostart script is conflicting. Search for it:
```bash
grep -r "chromium" ~/.config/
ls ~/
```

**Autostart not firing**
Make sure you're editing files in the correct terminal session and home directory:
```bash
whoami
echo $HOME
```

---

## Project Structure

```
Clock/
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
- **labwc** — Wayland compositor on Raspberry Pi OS that handles autostart
- **systemd** — keeps the Flask server running and restarts it on failure
