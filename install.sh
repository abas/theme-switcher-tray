echo "|---------------------------------|"
echo "|---Theme Switcher Installation---|"
echo "|---------------------------------|"

echo ""
echo ""

echo "defining var for execute"
XDG=./etc/xdg
USR=./usr
USR_BIN=$USR/bin
USR_SHARE=$USR/share
USR_ICONS=$USR/icons
XDG_ROOT=/etc/xdg
USR_ROOT=/usr
USR_BIN_ROOT=$USR_ROOT/bin
USR_SHARE_ROOT=$USR_ROOT/share
USR_ICONS_ROOT=$USR_ROOT/icons

echo ""
echo ""

echo "deploying autostart"
# XDG ################################################
cp $XDG/autostart/theme-switcher-tray.desktop $XDG_ROOT/autostart/
cp $XDG/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/tealinux.xml $XDG_ROOT/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/

echo ""
echo ""

echo "copying binary file"
# BIN ################################################
cp $USR/bin/theme-switcher-tray $USR_ROOT/bin/

echo ""
echo ""

echo "making documentation"
# SHARE ##############################################
cp $USR/share/doc/theme-switcher-tray $USR_ROOT/share/doc/

echo ""
echo ""

echo "installing icons"
# ICONS ##############################################
cp $USR/share/icons/hicolor/scalable/apps/theme-switcher-tray.svg $USR_ROOT/share/icons/hicolor/scalable/apps/

echo ""
echo ""

echo "finishing install"
# THEME-SWITCHER-TRAY ################################
cp $USR/share/theme-switcher $USR_ROOT/share

echo ""
echo ""
echo "done~"

echo "|---------------------------------|"
echo "|------INSTALLATION COMPLETE0-----|"
echo "|---------------------------------|"
