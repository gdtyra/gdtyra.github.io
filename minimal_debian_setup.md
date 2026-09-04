# Essential steps when setting up a minimal Debian environment

### Setup sudo

```sh
su -
apt install sudo
usermod -aG sudo <user>
```

### Install minimal components

- Install xorg
- Install openbox, obconf, lxappearance
- Install picom
- Install tint2
- Install network-manager, network-manager-gnome
- Install pipewire, wireplumber, pavucontrol

### Install laptop essentials if needed

- Install lxqt-powermanagement
- install xsct to modify screen brightness and color temperature

### Install desktop essentials

- install xsel for clipboard access
- Install Thunar or PCManFM
- Install xscreensaver for lock screen


### Non-essentials

- Install a font for emoji, like `fonts-noto-color-emoji` or `fonts-symbola`, then run `fc-cache -f -v`
- Install flameshot

### Add non-free package sources

- Modify `/etc/apt/sources.list` to include `contrib` and `non-free` in each line

### Setup firewall for VPN-only traffic plus DNS

```
ufw reset
ufw default deny outgoing
ufw default deny incoming
ufw allow out to any port 53
ufw allow out to <vpn-endpoint> 1194 proto udp
ufw allow out on tun0 from any to any
ufw enable

OPENSSL_CONF=/dev/null /usr/sbin/openvpn --config client.ovpn --tls-version-min 1.0 --tls-cipher "DEFAULT:@SECLEVEL=0" --data-ciphers "AES-256-GCM:AES-128-GCM:AES-256-CBC" --block-ipv6
```