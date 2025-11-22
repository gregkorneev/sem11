rm -rf data && rm -rf build && cmake -B build && cmake --build build \
&& ./build/benchmark && python3 .py/benchmark_numpy.py && python3 .py/plot_timings.py && python3 .py/generate_report.py
