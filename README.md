### Flask systemd service

- Create the file at /etc/systemd/system/literature-clock.service
- Run to enable:

`
sudo systemctl enable literature-clock
sudo systemctl start literature-clock
`

### Chromium autostart

- Create ~/.config/autostart/literature-clock.desktop
