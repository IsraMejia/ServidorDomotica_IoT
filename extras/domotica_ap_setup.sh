#!/usr/bin/env bash
set -e

# --- CONFIGURACIÓN ---
CON_NAME="domotica_ap"
SSID="RedDomotica"
PASS="clave1234"
IP4="192.168.4.1/24"
CHAN="11"

# --- DETECTAR INTERFAZ Wi-Fi ---
IFACE=$(nmcli device status | grep wifi | grep -w "disconnected\|connected" | awk '{print $1}')

if [ -z "$IFACE" ]; then
    echo "❌ No se encontró una interfaz Wi-Fi disponible."
    exit 1
fi

echo "📡 Usando interfaz Wi-Fi: $IFACE"

# --- VERIFICAR QUE SOPORTA MODO AP ---
if ! iw list | grep -A 10 "Supported interface modes" | grep -q "AP"; then
    echo "❌ Tu adaptador Wi-Fi no soporta modo AP."
    exit 1
fi

# --- CREAR CONEXIÓN SI NO EXISTE ---
if ! nmcli -t -f NAME con show | grep -qx "$CON_NAME"; then
    echo "🔧 Creando conexión '$CON_NAME'..."
    nmcli con add type wifi ifname "$IFACE" con-name "$CON_NAME" autoconnect yes ssid "$SSID"
    nmcli con mod "$CON_NAME" \
         802-11-wireless.mode ap \
         802-11-wireless.band bg \
         802-11-wireless.channel "$CHAN" \
         wifi-sec.key-mgmt wpa-psk \
         wifi-sec.psk "$PASS" \
         ipv4.addresses "$IP4" \
         ipv4.method shared
fi

# --- MEJORAS DE ESTABILIDAD ---
iw dev "$IFACE" set power_save off || true
iw phy0 set txpower fixed 1000 || true

# --- ACTIVAR CONEXIÓN ---
echo "🚀 Activando AP '$SSID'..."
nmcli con up "$CON_NAME"

echo "✅ AP '$SSID' activo con IP $IP4 y clave '$PASS'" 