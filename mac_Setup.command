#! /usr/bin/env sh
cd `dirname $0`
sudo easy_install pip
sudo pip3 install pip requests autobahn beautifulsoup4 configobj pytz prettytable --upgrade
