#!/usr/bin/env python3
"""
plot_asymptotic_analysis.py

Генерирует текстовый PNG с кратким анализом асимптотической сложности
стандартного алгоритма умножения матриц и алгоритма Штрассена.

Использует практические данные из:
  data/csv/timings.csv

Сохраняет результат в:
  data/png/asymptotic_analysis.png
"""

from pathlib import Path
import csv
import math

import matplotlib.pyplot as plt

# Пути относительно корня проекта
PY_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PY_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
CSV_DIR = DATA_DIR / "csv"
PNG_DIR = DATA_DIR / "png"


def load_timings():
    """
    Читает data/csv/timings.csv и возвращает список кортежей:
    (n, standard_ms, strassen_ms)
    """
    path = CSV_DIR / "timings.csv"
    rows = []
    if not path.exists():
        return rows

    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n = int(row["n"])
            standard_ms = float(row["standard_ms"])
            strassen_ms = float(row["strassen_ms"])
            rows.append((n, standard_ms, strassen_ms))

    # сортируем по n на всякий случай
    rows.sort(key=lambda x: x[0])
    return rows


def build_practical_summary(rows):
    """
    На основе экспериментальных данных формирует короткий текстовый вывод
    о практическом поведении алгоритмов.
    """
    if not rows:
        return (
            "Практические данные бенчмарка недоступны "
            "(файл data/csv/timings.csv не найден)."
        )

    max_n = rows[-1][0]

    # Считаем отношение времен стандарт / Штрассен
    ratios = []
    for n, standard_ms, strassen_ms in rows:
        if strassen_ms > 0:
            ratios.append((n, standard_ms / strassen_ms))

    # Проверяем, есть ли области, где Штрассен быстрее
    strassen_better_ns = [n for n, r in ratios if r > 1.0]  # standard/strassen > 1
    standard_better_ns = [n for n, r in ratios if r < 1.0]

    if not strassen_better_ns:
        # во всех точках стандартный быстрее или примерно равен
        return (
            "По результатам бенчмарка в исследованном диапазоне размеров "
            f"матриц (n ≤ {max_n}) стандартный алгоритм работает быстрее "
            "или сравнимо с алгоритмом Штрассена. Асимптотическое "
            "преимущество Штрассена в этом диапазоне не проявляется из-за "
            "больших константных накладных расходов рекурсивного алгоритма."
        )

    # Если вдруг есть n, где Штрассен выиграл — находим минимальное
    threshold_n = min(strassen_better_ns)
    return (
        "По результатам бенчмарка алгоритм Штрассена начинает выигрывать "
        f"по времени у стандартного алгоритма при n ≳ {threshold_n}, "
        "что согласуется с теоретическим предположением о его "
        "асимптотическом преимуществе на больших размерах матриц."
    )


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)

    rows = load_timings()
    practical_text = build_practical_summary(rows)

    # Формулы для теоретической части
    alpha = math.log(7, 2)  # ≈ 2.807...
    alpha_str = f"{alpha:.3f}"

    # Создаём фигуру под текст
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")

    y = 0.94
    dy = 0.075

    # Заголовок
    fig.text(
        0.03,
        y,
        "Критический анализ асимптотической сложности",
        fontsize=16,
        fontweight="bold",
    )
    y -= dy

    # Блок 1: асимптотическое поведение
    fig.text(0.03, y, "Асимптотическое поведение алгоритмов:", fontsize=12, fontweight="bold")
    y -= dy

    theory_lines = [
        r"• Стандартный алгоритм умножения матриц имеет сложность $O(n^3)$ (три вложенных цикла).",
        rf"• Алгоритм Штрассена имеет сложность $O(n^{{\log_2 7}}) \approx O(n^{{{alpha_str}}})$.",
        r"• Отношение сложностей даётся выражением "
        r"$\dfrac{n^3}{n^{\log_2 7}} = n^{3 - \log_2 7}$, "
        r"поэтому при $n \to \infty$ оно неограниченно растёт, "
        r"что теоретически подтверждает асимптотическое преимущество алгоритма Штрассена.",
    ]

    for line in theory_lines:
        fig.text(0.05, y, line, fontsize=10)
        y -= dy * 0.9

    y -= dy * 0.3

    # Блок 2: практическое поведение на экспериментальных данных
    fig.text(
        0.03,
        y,
        "Практическое поведение по данным бенчмарка:",
        fontsize=12,
        fontweight="bold",
    )
    y -= dy

    fig.text(0.05, y, f"• {practical_text}", fontsize=10)
    y -= dy * 1.4

    # Блок 3: краткий вывод
    fig.text(0.03, y, "Вывод:", fontsize=12, fontweight="bold")
    y -= dy

    conclusion = (
        "• Теоретически алгоритм Штрассена обладает более выгодной асимптотической "
        "оценкой по времени по сравнению со стандартным алгоритмом умножения матриц.\n"
        "• На малых размерах матриц стандартный алгоритм на практике оказывается "
        "эффективнее за счёт меньших констант и отсутствия накладных расходов "
        "на рекурсивное разбиение.\n"
        "• Использование алгоритма Штрассена оправдано при достаточно больших n, "
        "когда асимптотическое снижение степени роста компенсирует дополнительные накладные расходы."
    )

    # Разбиваем вывод по строкам вручную, чтобы не городить разметку:
    for line in conclusion.split("\n"):
        fig.text(0.05, y, line, fontsize=10)
        y -= dy * 0.9

    out_path = PNG_DIR / "asymptotic_analysis.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print("Анализ асимптотической сложности сохранён в:", out_path)


if __name__ == "__main__":
    main()
