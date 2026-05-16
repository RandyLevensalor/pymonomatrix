#!/bin/bash
set -e

# Default configuration values
MQTT_USER="${MQTT_USER:-hauser}"
MQTT_PASSWORD="${MQTT_PASSWORD:-hapassword}"
MQTT_BROKER="${MQTT_BROKER:-192.168.0.136}"
MATRIX_IP="${MATRIX_IP:-192.168.0.178}"
IMAGE="${IMAGE:-ghcr.io/randylevensalor/pymonomatrix:main}"

# Determine systemd directory (user vs root)
if [ "$EUID" -ne 0 ]; then
    SERVICE_DIR="$HOME/.config/systemd/user"
    mkdir -p "$SERVICE_DIR"
    SYSTEMCTL_CMD="systemctl --user"
else
    SERVICE_DIR="/etc/systemd/system"
    SYSTEMCTL_CMD="systemctl"
fi

CONFIG_MOUNT=""
if [ -f "$(pwd)/config.yaml" ]; then
    CONFIG_MOUNT="-v $(pwd)/config.yaml:/app/config.yaml:ro"
fi

echo "Installing systemd services to $SERVICE_DIR..."

# Generate pub service
cat <<SERVICE > "$SERVICE_DIR/container-pymatrix-pub.service"
[Unit]
Description=Podman container-pymatrix-pub.service
Documentation=man:podman-generate-systemd(1)
Wants=network-online.target
After=network-online.target
RequiresMountsFor=%t/containers

[Service]
Environment=PODMAN_SYSTEMD_UNIT=%n
Restart=always
RestartSec=10s
TimeoutStopSec=70
ExecStartPre=/bin/rm -f %t/%n.ctr-id
ExecStart=/usr/bin/podman run --cidfile=%t/%n.ctr-id --cgroups=no-conmon --rm --sdnotify=conmon --replace --name pymatrix-pub -e MONOPRICE_MATRIX_IP=${MATRIX_IP} ${CONFIG_MOUNT} ${IMAGE} python -u pymonomatrix/mqttPublish.py ${MQTT_USER} ${MQTT_PASSWORD} ${MQTT_BROKER}
ExecStop=/usr/bin/podman stop --ignore --cidfile=%t/%n.ctr-id
ExecStopPost=/usr/bin/podman rm -f --ignore --cidfile=%t/%n.ctr-id
Type=notify
NotifyAccess=all

[Install]
WantedBy=default.target
SERVICE

# Generate sub service
cat <<SERVICE > "$SERVICE_DIR/container-pymatrix-sub.service"
[Unit]
Description=Podman container-pymatrix-sub.service
Documentation=man:podman-generate-systemd(1)
Wants=network-online.target
After=network-online.target
RequiresMountsFor=%t/containers

[Service]
Environment=PODMAN_SYSTEMD_UNIT=%n
Restart=always
RestartSec=10s
TimeoutStopSec=70
ExecStartPre=/bin/rm -f %t/%n.ctr-id
ExecStart=/usr/bin/podman run --cidfile=%t/%n.ctr-id --cgroups=no-conmon --rm --sdnotify=conmon --replace --name pymatrix-sub -e MONOPRICE_MATRIX_IP=${MATRIX_IP} ${CONFIG_MOUNT} ${IMAGE} python -u pymonomatrix/mqttSubscribe.py ${MQTT_USER} ${MQTT_PASSWORD} ${MQTT_BROKER}
ExecStop=/usr/bin/podman stop --ignore --cidfile=%t/%n.ctr-id
ExecStopPost=/usr/bin/podman rm -f --ignore --cidfile=%t/%n.ctr-id
Type=notify
NotifyAccess=all

[Install]
WantedBy=default.target
SERVICE

echo "Reloading systemd daemon..."
$SYSTEMCTL_CMD daemon-reload

echo "Enabling and starting services..."
$SYSTEMCTL_CMD enable --now container-pymatrix-pub.service
$SYSTEMCTL_CMD enable --now container-pymatrix-sub.service

echo "Installation complete!"
