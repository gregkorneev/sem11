find . -name "*.csv" -type f -delete && \
find . -name "*.png" -type f -delete && \
rm -rf build && \
cmake -B build && \
cmake --build build && \
./build/app && \
cd build && \
./benchmark && \
python3 ../plot_timings.py
