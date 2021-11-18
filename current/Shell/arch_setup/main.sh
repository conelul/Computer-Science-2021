#!/bin/bash

# Redirect pacman stdout to /dev/null
function pacman_silent() {
    echo -e "Installing $1..."
    sudo pacman -Sq --noconfirm "$1" > /dev/null 
}

# Exports (for building)
echo -e "Environment variables..."
export MAKEFLAGS="-j$(nproc)" # Number of cores to use for building (all of them)
export RUSTFLAGS="-C opt-level=2 -C target-cpu=native" # Rust optimizations

# Installing with pacman
pacman_silent base-devel # Install base-devel, VERY IMPORTANT
pacman_silent Firefox
pacman_silent Discord

# Installing paru
echo -e "Installing Paru..."
git clone https://aur.archlinux.org/paru-bin.git # Get paru source
cd paru-bin # Enter the directory
makepkg -si --noconfirm # Build the package
rm -rf paru # Remove source files

echo "Done!"