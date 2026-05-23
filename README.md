# pymonomatrix

Python Application to manage the Monoprice Blackbird 8x8 matrix using the RESTful interface and MQTT.

This application consists of two main components:
1. **MQTT Publisher (`mqttPublish.py`)**: Polls the matrix for its current status and publishes changes to MQTT.
2. **MQTT Subscriber (`mqttSubscribe.py`)**: Subscribes to MQTT topics and controls the matrix based on incoming commands.

## Prerequisites
- Podman (for running the containerized applications)
- systemd (for managing the podman containers as background services)
- An MQTT broker

## Installation and Setup

### 1. Configuration (`config.yaml`)

Device names for inputs, video outputs, and audio outputs can be configured via a `config.yaml` file in the root directory.

Example `config.yaml`:
```yaml
input_labels: ["PC", "Apple TV", "Roku", "Input 4", "Input 5", "Input 6", "Input 7", "Input 8"]
output_video_labels: ["TV 1", "TV 2", "Projector", "Output 4", "Output 5", "Output 6", "Output 7", "Output 8"]
output_audio_labels: ["Receiver", "Soundbar", "Output 3", "Output 4", "Output 5", "Output 6", "Output 7", "Output 8"]
```

By default, the application looks for `config.yaml` in the project root. You can override this location using the `PYMONOMATRIX_CONFIG` environment variable. The matrix IP can be configured via the `MONOPRICE_MATRIX_IP` environment variable (defaults to `192.168.0.178`).

### 2. Running via Systemd (Recommended)

To install the services using Podman and systemd, run the provided `install.sh` script:

```bash
./install.sh
```

The script will interactively prompt you for:
- MQTT Username
- MQTT Password
- MQTT Broker IP/Hostname
- Monoprice Matrix IP
- Container Image (Defaults to `ghcr.io/randylevensalor/pymonomatrix:main`)

Once installed, it will automatically enable and start `container-pymatrix-pub.service` and `container-pymatrix-sub.service`.

To view logs for the services:
```bash
# If installed as root:
journalctl -u container-pymatrix-pub.service -f
journalctl -u container-pymatrix-sub.service -f

# If installed as user:
journalctl --user -u container-pymatrix-pub.service -f
journalctl --user -u container-pymatrix-sub.service -f
```

### 3. Running Manually

If you want to run the scripts manually without Docker/Podman:

1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
2. Run Publisher:
   ```bash
   MONOPRICE_MATRIX_IP=192.168.0.178 python3 -u pymonomatrix/mqttPublish.py <mqtt_user> <mqtt_password> <mqtt_broker_ip>
   ```
3. Run Subscriber:
   ```bash
   MONOPRICE_MATRIX_IP=192.168.0.178 python3 -u pymonomatrix/mqttSubscribe.py <mqtt_user> <mqtt_password> <mqtt_broker_ip>
   ```
4. Control Matrix via CLI:
   ```bash
   MONOPRICE_MATRIX_IP=192.168.0.178 python3 pymonomatrix/main.py <type> <index> <value>
   # example: python3 pymonomatrix/main.py volume 1 20
   ```