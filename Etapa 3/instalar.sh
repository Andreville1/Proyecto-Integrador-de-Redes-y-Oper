sudo apt-get install cmake
sudo apt-get install python3-dev
sudo apt-get install python-dev
sudo apt-get install build-essential
cd Oper
git clone https://github.com/pybind/pybind11.git
mkdir build
cd build 
cmake ..
make 