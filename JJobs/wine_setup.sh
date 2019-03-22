#!/bin/bash
# wi https://tecadmin.net/steps-install-wine-centos-rhel-fedora-systems/

Kernel=$(uname -s)
echo
echo "Operating System Kernel : $Kernel"
echo



yum clean all
yum update


yum groupinstall 'Development Tools'
yum install libX11-devel freetype-devel zlib-devel libxcb-devel \
      libxslt-devel libgcrypt-devel libxml2-devel gnutls-devel \
      libpng-devel libjpeg-turbo-devel libtiff-devel gstreamer-devel \
      dbus-devel fontconfig-devel


cd /usr/src
wget http://dl.winehq.org/wine/source/3.0/wine-3.0.tar.xz
tar -Jxf wine-3.0.tar.xz
cd wine-3.0

ARCH=$(uname -m)

echo
echo "Operating System Architecture : $ARCH"
echo

if [$ARCH = "i386"];then
  #For 32-Bit Systems:
  echo "32-Bit System"
  ./configure
  make
  make install
  #On 32-Bit Systems:
  wine --version

  elif [ $ARCH = "x86_64" ]; then
    #For 64-Bit Systems:
    ./configure  --enable-win64
    make
    make install
    #On 64-Bit Systems:
    wine64 --version
fi




wget http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html

wine putty.exe
