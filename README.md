rm -rf data && rm -rf build && cmake -B build && cmake --build build && ./build/benchmark && python3 benchmark_numpy.py && python3 plot_timings.py
