# Tractor

Tractor is core app which lets user to setup a proxy with Onion Routing via TOR and optionally obfs4proxy in their user space. The goal is to ease the proccess of connecting to TOR and prevent messing up with system files.

## Install
In Debian-based distros, make sure that you have `software-properties-common` package installed an then do as following:

    sudo add-apt-repository ppa:tractor-team/tractor
    sudo apt update
    sudo apt install tractor

If you are using a distro other than Ubuntu, please check if the release name in the relevant file located in `/etc/apt/sources.list.d/` is a supported one (e.g. bionic).

In Arch-based distros, you can install [Tractor package from AUR](https://aur.archlinux.org/packages/tractor-git/).

If you are any other distribution or OS, Tractor team welcomes you to make build recepie of yours.

## Run
you can run Tractor by command line or use one of the graphical interfaces which are packaged separately. For command line interface, read manual which is provided in installed package or available [here](https://gitlab.com/tractor-team/tractor/blob/master/man/tractor.1).
