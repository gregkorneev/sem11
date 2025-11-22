rm -rf data && rm -rf build && cmake -B build && cmake --build build && ./build/app && ./build/benchmark && python3 .py/benchmark_numpy.py && python3 .py/plot_timings.py && python3 .py/generate_report.py && python3 .py/plot_comparison_table.py && python3 .py/plot_asymptotic_analysis.py


ёёёёёё
