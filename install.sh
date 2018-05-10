echo "|---------------------------------|"
echo "|---Theme Switcher Installation---|"
echo "|---------------------------------|"

echo ""
echo ""

echo "defining var for execute"
XDG=./theme-switcher-tray/etc/xdg
USR=./theme-switcher-tray/usr
USR_BIN=$USR/bin
USR_SHARE=$USR/share
USR_ICONS=$USR/icons
XDG_ROOT=/etc/xdg
USR_ROOT=/usr
USR_BIN_ROOT=$USR_ROOT/bin
USR_SHARE_ROOT=$USR_ROOT/share
USR_ICONS_ROOT=$USR_ROOT/icons

echo "deploying autostart"
# XDG ################################################
cp $XDG/autostart/theme-switcher-tray.desktop $XDG_ROOT/autostart/
cp $XDG/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/tealinux.xml $XDG_ROOT/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/

echo "copying binary file"
# BIN ################################################
cp $USR/bin/theme-switcher-tray $USR_ROOT/bin/

echo "making documentation"
# SHARE ##############################################
cp -r $USR/share/doc/theme-switcher-tray $USR_ROOT/share/doc/

echo "installing icons"
# ICONS ##############################################
cp $USR/share/icons/hicolor/scalable/apps/theme-switcher-tray.svg $USR_ROOT/share/icons/hicolor/scalable/apps/

echo "finishing install"
# THEME-SWITCHER-TRAY ################################
cp -r $USR/share/theme-switcher $USR_ROOT/share/

echo "done~"

echo "|---------------------------------|"
echo "|------INSTALLATION COMPLETE0-----|"
echo "|---------------------------------|"
