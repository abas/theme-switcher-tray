killall theme-switcher-tray
rm -f /usr/share/icons/hicolor/scalable/apps/theme-switcher-tray.svg
cp ./theme-switcher-tray/usr/share/icons/hicolor/scalable/apps/theme-switcher-tray.svg /usr/share/icons/hicolor/scalable/apps/
echo "logo updated~"
theme-switcher-tray
echo "realaunch.."