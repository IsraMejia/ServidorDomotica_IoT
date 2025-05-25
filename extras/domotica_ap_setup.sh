#!/usr/bin/env bash
set -e

CON_NAME="domotica_ap"
SSID="RedDomotica"
PASS="clave1234"
IP4="192.168.4.1/24"
CHAN="11"

# -- si la conexión no existe, créala
if ! nmcli -t -f NAME con show | grep -qx "$CON_NAME"; then
    nmcli con add type wifi ifname wlan0 con-name "$CON_NAME" autoconnect yes ssid "$SSID"
    nmcli con mod "$CON_NAME" \
         802-11-wireless.mode ap \
         802-11-wireless.band bg \
         802-11-wireless.channel "$CHAN" \
         wifi-sec.key-mgmt wpa-psk \
         wifi-sec.psk "$PASS" \
         ipv4.addresses "$IP4" \
         ipv4.method shared          # NM levanta DHCP/NAT automáticamente 
fi

# -- desactiva power-save (evita congelones brcmfmac) 
iw dev wlan0 set power_save off

# -- limita potencia a 10 dBm para mayor estabilidad (opcional) 
iw phy0 set txpower fixed 1000 || true

# -- activa la conexión (si ya está up no pasa nada)
nmcli con up "$CON_NAME"

exit 0
