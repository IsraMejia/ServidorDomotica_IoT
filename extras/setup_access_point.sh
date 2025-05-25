#!/usr/bin/env bash
# setup_access_point.sh — RPi 5 + Bookworm listo-para-usar
set -euo pipefail
say(){ echo -e "\e[32m[SETUP-AP]\e[0m $*"; }
die(){ echo -e "\e[31m[SETUP-AP-ERROR]\e[0m $*" >&2; exit 1; }

[[ $EUID -eq 0 ]] || die "Ejecuta con sudo"
ip link show wlan0 &>/dev/null || die "No existe wlan0"

say "🔧 Instalando dependencias..."
apt update -y
DEBIAN_FRONTEND=noninteractive apt install -y hostapd dnsmasq

say "🛑 Deteniendo servicios..."
systemctl stop hostapd || true
systemctl stop dnsmasq || true

# ── Evitar choques con NetworkManager ───────────────────────────
say "🚦 Indicando a NetworkManager que ignore wlan0..."
mkdir -p /etc/NetworkManager/conf.d
cat > /etc/NetworkManager/conf.d/ignore-wlan0.conf <<'EOF'
[keyfile]
unmanaged-devices=interface-name:wlan0
EOF
systemctl reload NetworkManager

# ── IP estática via dhcpcd ───────────────────────────────────────
if ! grep -q "RedDomotica setup" /etc/dhcpcd.conf; then
  say "⚙️  Ajustando /etc/dhcpcd.conf..."
  cat >> /etc/dhcpcd.conf <<'EOF'
# RedDomotica setup
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
EOF
fi
systemctl restart dhcpcd

# ── hostapd ──────────────────────────────────────────────────────
say "📡 Configurando hostapd..."
cat > /etc/hostapd/hostapd.conf <<'EOF'
interface=wlan0
driver=nl80211
ssid=RedDomotica
hw_mode=g
channel=7
ieee80211n=1
wmm_enabled=1
auth_algs=1
wpa=2
wpa_passphrase=clave1234
rsn_pairwise=CCMP
EOF
sed -i 's|^#\?DAEMON_CONF=.*|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd

# ── dnsmasq ─────────────────────────────────────────────────────
say "🧠 Configurando dnsmasq..."
mv -f /etc/dnsmasq.conf /etc/dnsmasq.conf.orig || true
cat > /etc/dnsmasq.conf <<'EOF'
interface=wlan0
dhcp-range=192.168.4.10,192.168.4.40,255.255.255.0,24h
EOF

systemctl unmask hostapd
systemctl enable hostapd dnsmasq

# ── Script de información ───────────────────────────────────────
say "🗒️  Creando /usr/local/bin/ap-info.sh..."
cat > /usr/local/bin/ap-info.sh <<'EOF'
#!/usr/bin/env bash
ip=$(ip -4 addr show wlan0 | awk '/inet /{print $2}' | cut -d/ -f1)
mac=$(cat /sys/class/net/wlan0/address)
clients=$(iw dev wlan0 station dump 2>/dev/null | grep -c '^Station' || echo 0)
leases=$(grep -cv '^#' /var/lib/misc/dnsmasq.leases 2>/dev/null || echo 0)
echo -e "\e[34m[AP-STATUS]\e[0m 🚀 Access Point RedDomotica activo"
echo "    📶 SSID   : RedDomotica"
echo "    🔑 Pass   : clave1234"
echo "    🌐 IP     : ${ip:-192.168.4.1}"
echo "    🔗 MAC    : $mac"
echo "    👥 Clientes: $clients"
echo "    📜 Leases : $leases"
echo "    🐳 Backend : http://${ip:-192.168.4.1}:8000/"
echo "    🕒 Hora    : $(date '+%F %T')"
EOF
chmod +x /usr/local/bin/ap-info.sh

# ── Servicio systemd ─────────────────────────────────────────────
say "🔨 Configurando ap-status.service..."
cat > /etc/systemd/system/ap-status.service <<'EOF'
[Unit]
Description=Mostrar estado de RedDomotica al arrancar
After=hostapd.service dnsmasq.service
Wants=hostapd.service dnsmasq.service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/ap-info.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable ap-status.service

# ── Arranque inmediato ──────────────────────────────────────────
say "🔄 Levantando servicios..."
systemctl restart hostapd
systemctl restart dnsmasq

say "✅ Access Point configurado correctamente."
say "    📶 SSID : RedDomotica"
say "    🔑 Pass : clave1234"
say "    🌐 IP   : 192.168.4.1"
say "🔃 Reinicio en 5 s para aplicar todo (Ctrl-C para abortar)…"
sleep 5
reboot
