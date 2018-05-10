killall theme-switcher-tray
rm -f /usr/share/icons/theme-switcher-tray.svg
cp ./theme-switcher-tray/usr/share/icons/theme-switcher-tray.svg /usr/share/icons/
echo "logo updated~"
theme-switcher-tray
echo "realaunch.."