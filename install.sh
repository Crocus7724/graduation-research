#!/bin/bash
ODE_VERSION=0.13
ANACONDA_VERSION=3-5.0.1
BASE_DIR=$(dirname $(readlink -f $0))

printf "password: "
read -s PASSWORD

cd $BASE_DIR/libs

tar -jxvf "ode-$ODE_VERSION.tar.bz2"

# install dependencies ODE
echo $PASSWORD | sudo -S apt-get install automake libtool freeglut3-dev
cd "ode-$ODE_VERSION"

# install ODE
./boostrap
./configure --with-trimesh=opcode --enable-new-trimesh --enable-shared  --enable-release --with-x --enable-double-precision --with-libccd

make && echo $PASSWORD | sudo -S make install

# install drawstuff
echo $PASSWORD | sudo -S cp -r include/drawstuff /usr/local/include/
echo $PASSWORD | sudo -S cp drawstuff/src/.libs/libdrawstuff.* /usr/local/lib
echo $PASSWORD | sudo -S ldconfig

cd ../

# install gRPC for C++
echo $PASSWORD | sudo -S apt-get install build-essential autoconf libtool clang libc++-dev

which git || echo $PASSWORD | sudo -S apt-get install git
cd grpc
git submodule update --init
make
echo $PASSWORD | sudo -S make install

 # install protobuf
echo $PASSWORD | sudo -S apt-get install autoconf automake curl make g++ unzip 
cd third_party/protobuf
./autogen.sh
./configure
make
make check
echo $PASSWORD | sudo -S make install
echo $PASSWORD | sudo -S ldconfig 

# build Simulator
cd $BASE_DIR/simulator
mkdir cmake-build-release
cd cmake-build-release
cp -r $BASE_DIR/libs/ode-$ODE_VERSION/drawstuff/textures .
cmake -DCMAKE_BUILD_TYPE=Release ..
make

# install python(use pyenv)
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc

echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc

exec "$SHELL"
pyenv install anaconda3-5.0.1
cd $BASE_DIR/learning

pyenv local anaconda3-5.0.1

# install machine learning tools
pip install tensorflow gym keras-rl h5py

# install and generate gRPC for Python
pip install grpcio-tools
python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/simulator.proto

mkdir $BASE_DIR/env

echo "Install finished!"
echo "You can start learning after 'sh make_env.sh -n ENV_NAME'"
