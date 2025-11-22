#!/usr/bin/env python3
"""
plot_comparison_table.py
Сравнительная таблица стандартного алгоритма умножения матриц и алгоритма Штрассена.

Создаёт файл:
  data/png/comparison_table.png
"""

from pathlib import Path
import matplotlib.pyplot as plt

# Пути относительно структуры проекта sem11
PY_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PY_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
PNG_DIR = DATA_DIR / "png"


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)

    # Заголовки и данные таблицы
    col_labels = [
        "Характеристика",
        "Стандартный алгоритм",
        "Алгоритм Штрассена",
    ]

    table_data = [
        [
            "Вычислительная\nсложность",
            r"$O(n^3)$",
            r"$O(n^{\log_2 7}) \approx O(n^{2.807})$",
        ],
        [
            "Асимптотическое\nповедение",
            "Кубический рост",
            "Субкубический рост",
        ],
        [
            "Константный\nмножитель",
            "Малый (~1)",
            "Большой (~7 рекурсивных\nвычислений)",
        ],
        [
            "Требования\nк памяти",
            r"$O(n^2)$",
            r"$O(n^2) + O(\log n)$\n(рекурсивный стек)",
        ],
        [
            "Простота\nреализации",
            "Высокая",
            "Средняя",
        ],
        [
            "Практическая\nэффективность",
            "Лучше для\nмалых матриц",
            "Лучше для\nбольших матриц",
        ],
        [
            "Параллелизация",
            "Хорошая",
            "Отличная (7 независимых\nподзадач)",
        ],
    ]

    # Создаём фигуру
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.axis("off")

    # Заголовок блока
    fig.suptitle(
        "Сравнительная таблица алгоритмов умножения матриц",
        fontsize=14,
        fontweight="bold",
        y=0.97,
    )

    # Рисуем таблицу
    table = ax.table(
        cellText=table_data,
        colLabels=col_labels,
        loc="center",
        cellLoc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.1, 1.6)

    # Немного стиля: выделим заголовок столбцов
    header_color = "#e0eafc"
    header_row = 0
    for col in range(len(col_labels)):
        cell = table[header_row, col]
        cell.set_facecolor(header_color)
        cell.set_fontsize(10)
        cell.set_text_props(weight="bold")

    # Выравнивание первой колонки по левому краю
    for row in range(1, len(table_data) + 1):
        cell = table[row, 0]
        cell._loc = "left"  # слегка «хак», но работает
        cell.set_text_props(ha="left")

    out_path = PNG_DIR / "comparison_table.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print("Сравнительная таблица сохранена в:", out_path)


if __name__ == "__main__":
    main()
