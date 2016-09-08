#!/usr/bin/env bash

platform='unknown'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   platform='linux'
elif [[ "$unamestr" == 'Darwin' ]]; then
   platform='darwin'
fi



if [[ "$platform" == "darwin" ]]; then
    echo 'Checking Brew Package Manager . . .' && command -v brew >/dev/null 2>&1 ||
    {
        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    }
    echo 'Checking Kubectl Package . . .' && command -v kubectl >/dev/null 2>&1 ||
    {
        curl -O https://storage.googleapis.com/kubernetes-release/release/v1.2.4/bin/darwin/amd64/kubectl; chmod +x kubectl; mv kubectl /usr/local/bin/kubectl
    }
    echo 'Checking Vagrant Package . . .' && command -v vagrant >/dev/null 2>&1 ||
    {
        wget https://releases.hashicorp.com/vagrant/1.8.5/vagrant_1.8.5.dmg
        echo "Vagrant DMG File downloaded. Please install and run this script again"
    }
    echo 'Checking Docker Package . . .' && command -v docker >/dev/null 2>&1 ||
    {
        brew install docker
    }
elif [[ "$platform" == "linux" ]]; then
    echo 'Checking Kubectl Package . . .' && command -v kubectl >/dev/null 2>&1 ||
    {
        curl -O https://storage.googleapis.com/kubernetes-release/release/v1.2.4/bin/linux/amd64/kubectl
    }
    echo 'Checking Vagrant Package . . .' && command -v vagrant >/dev/null 2>&1 ||
    {
        wget https://releases.hashicorp.com/vagrant/1.8.5/vagrant_1.8.5_x86_64.deb
        sudo dpkg -i vagrant_1.8.5_x86_64.deb
        sudo rm -rf vagrant_1.8.5_x86_64.deb
    }
    echo 'Checking Docker Package . . .' && command -v docker >/dev/null 2>&1 ||
    {
        sudo apt-get install docker
    }
else
    echo "Operating System not supported"
    exit 1
fi


echo 'Checking Tensorflow Installation . . .'
c_out="$(python3 -c 'import tensorflow')"
if [[ "$c_out" != "" ]]; then
   echo 'Installing Tensorflow . . .' && sudo pip3 install tensorflow
fi

exit 0

