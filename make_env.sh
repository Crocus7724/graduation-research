#!/bin/bash -e
name=""
while getopts n: OPT
do
  case $OPT in
    n) name="$OPTARG"
      ;;
  esac
done

base_dir=$(dirname $(readlink -f $0))
env_dir=$base_dir/env/$name
mkdir $env_dir
echo $env_dir
cd $env_dir

simulator_dir=$base_dir/simulator/cmake-build-release
learning_dir=$base_dir/learning
cp $simulator_dir/simulator .
cp -r $simulator_dir/textures .
cp $learning_dir/*.py .

mkdir data
cd data
mkdir history model weight tensorboard
