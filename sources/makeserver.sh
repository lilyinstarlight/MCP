#!/bin/sh
homedir="/home/armagetron"
prefixdir="$homedir/servers"
sourcedir="$homedir/sources"

if [ -z "$1" ] || [ -z "$2" ]; then
	echo -e "Usage:\t$0 <server> <source>"
	exit 1
fi

green="\e[32;1m"
red="\e[31;1m"
normal="\e[00m"

cd "$sourcedir/$2"

echo -e "Bootstrapping..."
./bootstrap.sh > /dev/null
if [ $? -ne 0 ]; then
	echo -e "${red}Error while bootstrapping.${normal}"
	exit 1
fi

echo -e "Configuring..."
CXXFLAGS="-march=native -pipe" ./configure --enable-dedicated --enable-armathentication --disable-automakedefaults --disable-sysinstall --disable-useradd --disable-etc --disable-desktop --disable-initscripts --disable-uninstall --disable-games --prefix="$prefixdir/$1" --localstatedir="$prefixdir/$1/var" > /dev/null
if [ $? -ne 0 ]; then
	echo -e "${red}Error while configuring.${normal}"
	exit 1
fi

echo -e "Compiling..."
make -j3 > /dev/null
if [ $? -ne 0 ]; then
	echo -e "${red}Error while compiling.${normal}"
	exit 1
fi

echo -e "Installing..."
make install > /dev/null
if [ $? -ne 0 ]; then
	echo -e "${red}Error while installing.${normal}"
	exit 1
fi

echo -e "Setting up directories..."
cd "$prefixdir/$1/"
mkdir -p config
cp -nR etc/armagetronad-dedicated/* config/
rm -rf etc
cp -nR "$sourcedir"/config/* config/
mkdir -p data
cp -nR share/armagetronad-dedicated/* data/
rm -rf share
mkdir -p var
touch var/ladderlog.txt
touch var/input.txt
mkdir -p scripts
cp -nR "$sourcedir"/scripts/* scripts/
mkdir -p user

echo -e "Done!"
