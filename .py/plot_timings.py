#!/usr/bin/env python3
"""
plot_timings.py
Строит все графики времени и теоретических асимптот для ЛР по умножению матриц.

Читает:
  data/csv/timings.csv         — стандартный C++ и Штрассен
  data/csv/timings_numpy.csv   — NumPy

Сохраняет:
  data/png/timings_standard.png
  data/png/timings_strassen.png
  data/png/timings_numpy.png
  data/png/timings_all.png
  data/png/timings_all_loglog.png
  data/png/complexity_theory.png
  data/png/complexity_theory_loglog.png
  data/png/complexity_saving_bar.png
  data/png/complexity_ratio.png
"""

from pathlib import Path
import csv
import math

import matplotlib.pyplot as plt


# --- Пути к проекту и папкам data/csv и data/png ---

PY_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PY_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
CSV_DIR = DATA_DIR / "csv"
PNG_DIR = DATA_DIR / "png"


def read_timings():
    """Читает timings.csv и timings_numpy.csv, возвращает общие данные."""
    standard_n = []
    standard_ms = []
    strassen_ms = []

    # Основные замеры C++: стандартный и Штрассен
    with (CSV_DIR / "timings.csv").open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n = int(row["n"])
            standard_n.append(n)
            standard_ms.append(float(row["standard_ms"]))
            strassen_ms.append(float(row["strassen_ms"]))

    # Замеры NumPy (могут отсутствовать)
    numpy_n = []
    numpy_ms = []
    numpy_path = CSV_DIR / "timings_numpy.csv"
    if numpy_path.exists():
        with numpy_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                numpy_n.append(int(row["n"]))
                numpy_ms.append(float(row["numpy_ms"]))

    # На всякий случай сортируем по n
    zipped_std = sorted(
        zip(standard_n, standard_ms, strassen_ms), key=lambda x: x[0]
    )
    standard_n = [z[0] for z in zipped_std]
    standard_ms = [z[1] for z in zipped_std]
    strassen_ms = [z[2] for z in zipped_std]

    zipped_np = sorted(zip(numpy_n, numpy_ms), key=lambda x: x[0])
    numpy_n = [z[0] for z in zipped_np]
    numpy_ms = [z[1] for z in zipped_np]

    return standard_n, standard_ms, strassen_ms, numpy_n, numpy_ms


# --- Построение практических графиков времени ---


def plot_single(n_list, ms_list, title, filename, ylabel="Время, мс"):
    """Простой график: n по оси X, время по оси Y."""
    plt.figure()
    plt.plot(n_list, ms_list, marker="o")
    plt.xlabel("Размер матрицы n")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PNG_DIR / filename
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()


def plot_all_linear(n, standard_ms, strassen_ms, numpy_n, numpy_ms):
    """Сравнение всех трёх алгоритмов в линейном масштабе."""
    plt.figure()
    plt.plot(n, standard_ms, marker="o", label="Стандартный C++")
    plt.plot(n, strassen_ms, marker="o", label="Штрассен C++")

    # Для NumPy возможны немного другие n, поэтому строим отдельно
    if numpy_n and numpy_ms:
        plt.plot(numpy_n, numpy_ms, marker="o", label="NumPy (Python)")

    plt.xlabel("Размер матрицы n")
    plt.ylabel("Время, мс")
    plt.title("Сравнение времени работы алгоритмов (линейный масштаб)")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(PNG_DIR / "timings_all.png", bbox_inches="tight")
    plt.close()


def plot_all_loglog(n, standard_ms, strassen_ms, numpy_n, numpy_ms):
    """Сравнение всех трёх алгоритмов в логарифмическом масштабе (log–log)."""
    plt.figure()

    # Логарифмический масштаб остаётся, просто используем базу по умолчанию
    plt.loglog(n, standard_ms, marker="o", label="Стандартный C++")
    plt.loglog(n, strassen_ms, marker="o", label="Штрассен C++")

    if numpy_n and numpy_ms:
        plt.loglog(numpy_n, numpy_ms, marker="o", label="NumPy (Python)")

    plt.xlabel("log n")
    plt.ylabel("log времени, мс")
    plt.title("Сравнение времени работы алгоритмов (log–log)")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(PNG_DIR / "timings_all_loglog.png", bbox_inches="tight")
    plt.close()


# --- Теоретические графики асимптот ---


def build_theoretical_sequences(n_list):
    """
    Возвращает:
      values_n3      — n^3,
      values_str     — n^{log2 7},
      ratio          — n^3 / n^{log2 7},
      saving_percent — теоретическая экономия операций Штрассена, %
    """
    values_n3 = []
    values_str = []
    ratio = []
    saving_percent = []

    alpha = math.log(7, 2)  # ≈ 2.807

    for n in n_list:
        v3 = n ** 3
        vs = n ** alpha
        values_n3.append(v3)
        values_str.append(vs)
        ratio.append(v3 / vs)
        saving_percent.append((1 - vs / v3) * 100.0)

    return values_n3, values_str, ratio, saving_percent


def plot_complexity_theory(n_list):
    """
    Строит теоретический график:
    - n^3 и n^{log2 7} (нормированные),
    - теоретическую экономию операций (в процентах) на второй оси Y.
    """
    values_n3, values_str, ratio, saving_percent = build_theoretical_sequences(n_list)

    # Нормируем кривые, чтобы они занимали сравнимый диапазон по Y
    max_n3 = max(values_n3)
    max_str = max(values_str)
    norm_n3 = [v / max_n3 for v in values_n3]
    norm_str = [v / max_str for v in values_str]

    fig, ax1 = plt.subplots()

    ax1.plot(n_list, norm_n3, marker="o", label="O(n³) (норм.)")
    ax1.plot(n_list, norm_str, marker="o", label="O(n^{log₂7}) (норм.)")
    ax1.set_xlabel("Размер матрицы n")
    ax1.set_ylabel("Нормированная сложность")
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

    # Вторая ось Y — теоретическая экономия операций
    ax2 = ax1.twinx()
    ax2.plot(
        n_list,
        saving_percent,
        marker="s",
        linestyle=":",
        label="Экономия Штрассена, %",
    )
    ax2.set_ylabel("Экономия операций, %")

    # Общая легенда
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    fig.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    plt.title("Теоретическая сложность: стандартный алгоритм vs Штрассена")
    plt.savefig(PNG_DIR / "complexity_theory.png", bbox_inches="tight")
    plt.close(fig)


def plot_complexity_theory_loglog(n_list):
    """Строит теоретические O(n³) и O(n^{log2 7}) в логарифмическом масштабе."""
    values_n3, values_str, ratio, _ = build_theoretical_sequences(n_list)

    plt.figure()
    plt.loglog(n_list, values_n3, marker="o", label="O(n³)")
    plt.loglog(n_list, values_str, marker="o", label="O(n^{log₂7})")
    plt.xlabel("log n")
    plt.ylabel("log числа операций (условно)")
    plt.title("Теоретические асимптотики (log–log)")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(PNG_DIR / "complexity_theory_loglog.png", bbox_inches="tight")
    plt.close()


def plot_complexity_saving_bar(n_list):
    """Строит столбчатую диаграмму теоретической экономии операций Штрассена."""
    _, _, _, saving_percent = build_theoretical_sequences(n_list)

    plt.figure()
    plt.bar([str(n) for n in n_list], saving_percent)
    plt.xlabel("Размер матрицы n")
    plt.ylabel("Экономия операций, %")
    plt.title("Теоретическая экономия операций алгоритма Штрассена")
    plt.grid(axis="y", linestyle="--", linewidth=0.5)

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(PNG_DIR / "complexity_saving_bar.png", bbox_inches="tight")
    plt.close()


def plot_complexity_ratio(n_list):
    """
    Отношение теоретических сложностей: n^3 / n^{log2 7}.
    Показывает, во сколько раз стандартный алгоритм асимптотически медленнее Штрассена.
    """
    _, _, ratio, _ = build_theoretical_sequences(n_list)

    plt.figure()
    plt.plot(n_list, ratio, marker="o")
    plt.xlabel("Размер матрицы n")
    plt.ylabel("Отношение n^3 / n^{log₂7}")
    plt.title("Отношение теоретических сложностей алгоритмов")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(PNG_DIR / "complexity_ratio.png", bbox_inches="tight")
    plt.close()


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)

    n, standard_ms, strassen_ms, numpy_n, numpy_ms = read_timings()

    # Практические графики
    plot_single(
        n,
        standard_ms,
        "Время работы стандартного алгоритма (C++)",
        "timings_standard.png",
    )
    plot_single(
        n,
        strassen_ms,
        "Время работы алгоритма Штрассена (C++)",
        "timings_strassen.png",
    )
    if numpy_n and numpy_ms:
        plot_single(
            numpy_n,
            numpy_ms,
            "Время работы NumPy (Python)",
            "timings_numpy.png",
        )

    # Сравнение практических данных
    plot_all_linear(n, standard_ms, strassen_ms, numpy_n, numpy_ms)
    plot_all_loglog(n, standard_ms, strassen_ms, numpy_n, numpy_ms)

    # Теоретические графики асимптот (используем те же n, что и в timings.csv)
    plot_complexity_theory(n)
    plot_complexity_theory_loglog(n)
    plot_complexity_saving_bar(n)
    plot_complexity_ratio(n)

    print("Графики сохранены в", PNG_DIR)


if __name__ == "__main__":
    main()
