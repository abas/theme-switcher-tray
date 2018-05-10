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
USR_ICONS=$USR_SHARE/icons
XDG_ROOT=/etc/xdg
USR_ROOT=/usr
USR_BIN_ROOT=$USR_ROOT/bin
USR_SHARE_ROOT=$USR_ROOT/share
USR_ICONS_ROOT=$USR_SHARE_ROOT/icons

echo "deploying autostart"
# XDG ################################################
cp $XDG/autostart/theme-switcher-tray.desktop $XDG_ROOT/autostart/
cp $XDG/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/tealinux.xml $XDG_ROOT/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/

echo "copying binary file"
# BIN ################################################
cp $USR_BIN/theme-switcher-tray $USR_BIN_ROOT/

echo "making documentation"
# SHARE ##############################################
cp -r $USR_SHARE/doc/theme-switcher-tray $USR_SHARE_ROOT/doc/

echo "installing icons"
# ICONS ##############################################
cp $USR_ICONS/theme-switcher-tray.svg $USR_ICONS_ROOT/

echo "finishing install"
# THEME-SWITCHER-TRAY ################################
cp -r $USR_SHARE/theme-switcher $USR_SHARE_ROOT/

echo "done~"

echo "|---------------------------------|"
echo "|------INSTALLATION COMPLETE0-----|"
echo "|---------------------------------|"
