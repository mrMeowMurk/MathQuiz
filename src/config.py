"""Конфигурация приложения"""

from typing import Dict, List, Tuple, Callable

# Настройки уровней сложности
DIFFICULTY_LEVELS: Dict[str, Dict] = {
    '1': {
        "range": (1, 10),
        "name": "Легкий",
        "time": 60,
        "operations": ['+', '-', '*'],
        "question_types": ['arithmetic', 'sequence']
    },
    '2': {
        "range": (1, 50),
        "name": "Средний",
        "time": 90,
        "operations": ['+', '-', '*', '**'],
        "question_types": ['arithmetic', 'equation', 'sequence', 'geometry']
    },
    '3': {
        "range": (1, 100),
        "name": "Сложный",
        "time": 120,
        "operations": ['+', '-', '*', '**', '√'],
        "question_types": ['arithmetic', 'equation', 'word_problem', 'sequence', 'geometry']
    }
}

# Математические операции
OPERATIONS: Dict[str, Tuple[Callable, str]] = {
    '+': (lambda x, y: x + y, "сложение"),
    '-': (lambda x, y: x - y, "вычитание"),
    '*': (lambda x, y: x * y, "умножение"),
    '**': (lambda x, y: x ** y, "возведение в степень"),
    '√': (lambda x, y: round(x ** (1/y), 2), "корень")
}

# Описания типов задач
QUESTION_TYPE_DESCRIPTIONS: Dict[str, str] = {
    'arithmetic': "Арифметические примеры",
    'equation': "Уравнения",
    'word_problem': "Текстовые задачи",
    'sequence': "Последовательности",
    'geometry': "Геометрические задачи"
}

# Настройки сохранения
HIGH_SCORES_FILE = 'high_scores.json'
DEFAULT_HIGH_SCORES = {'1': [], '2': [], '3': []} 