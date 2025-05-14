"""Генераторы различных типов задач"""

import random
from typing import Tuple, Dict, Any
from .config import OPERATIONS, DIFFICULTY_LEVELS

def generate_arithmetic_question(difficulty: str) -> Tuple[str, float]:
    """Генерирует арифметический пример"""
    diff_info = DIFFICULTY_LEVELS[difficulty]
    num_range = diff_info['range']
    operation = random.choice(diff_info['operations'])
    
    if operation == '√':
        num1 = random.randint(1, 100)
        num2 = random.randint(2, 3)
        question = f"∛{num1} = ?" if num2 == 3 else f"√{num1} = ?"
    elif operation == '**':
        num1 = random.randint(2, 5)
        num2 = random.randint(2, 3)
        question = f"{num1} ^ {num2} = ?"
    else:
        num1 = random.randint(*num_range)
        num2 = random.randint(*num_range)
        question = f"{num1} {operation} {num2} = ?"
    
    answer = OPERATIONS[operation][0](num1, num2)
    return question, answer

def generate_equation_question(difficulty: str) -> Tuple[str, float]:
    """Генерирует линейное уравнение"""
    diff_info = DIFFICULTY_LEVELS[difficulty]
    num_range = diff_info['range']
    
    a = random.randint(2, 5)
    x = random.randint(*num_range)
    b = random.randint(-10, 10)
    c = a * x + b
    
    question = f"{a}x {'+' if b >= 0 else '-'} {abs(b)} = {c}\nНайдите x:"
    return question, x

def generate_word_problem(difficulty: str) -> Tuple[str, float]:
    """Генерирует текстовую задачу"""
    templates = [
        {
            "text": "В магазине было {total} яблок. {sold} яблок продали. Сколько яблок осталось?",
            "generate": lambda r: {
                "total": random.randint(*r),
                "sold": random.randint(1, r[1]//2)
            },
            "solve": lambda params: params["total"] - params["sold"]
        },
        {
            "text": "У Пети было {initial} рублей. Он купил {items} конфет по {price} рублей. Сколько денег у него осталось?",
            "generate": lambda r: {
                "initial": random.randint(50, 200),
                "items": random.randint(2, 5),
                "price": random.randint(5, 20)
            },
            "solve": lambda params: params["initial"] - (params["items"] * params["price"])
        },
        {
            "text": "Расстояние между городами {distance} км. Велосипедист проезжает {speed} км в час. За сколько часов он доедет?",
            "generate": lambda r: {
                "distance": random.randint(20, 100),
                "speed": random.randint(5, 20)
            },
            "solve": lambda params: params["distance"] / params["speed"]
        }
    ]
    
    template = random.choice(templates)
    values = template["generate"](DIFFICULTY_LEVELS[difficulty]["range"])
    question = template["text"].format(**values)
    answer = round(template["solve"](values), 2)
    return question, answer

def generate_sequence_question(difficulty: str) -> Tuple[str, float]:
    """Генерирует задачу на последовательности"""
    types = [
        # Арифметическая прогрессия
        lambda r: (
            random.randint(1, 5),  # шаг
            random.randint(0, 10),  # начальное число
            "арифметическую последовательность"
        ),
        # Геометрическая прогрессия
        lambda r: (
            random.randint(2, 3),  # множитель
            random.randint(1, 5),  # начальное число
            "геометрическую последовательность"
        )
    ]
    
    seq_type, start, desc = random.choice(types)(DIFFICULTY_LEVELS[difficulty]["range"])
    sequence = []
    
    if "арифметическую" in desc:
        for i in range(5):
            sequence.append(start + seq_type * i)
        next_num = start + seq_type * 5
    else:
        for i in range(5):
            sequence.append(start * (seq_type ** i))
        next_num = start * (seq_type ** 5)
    
    question = f"Продолжите {desc}:\n{', '.join(map(str, sequence))}, ..."
    return question, next_num

def generate_geometry_question(difficulty: str) -> Tuple[str, float]:
    """Генерирует геометрическую задачу"""
    templates = [
        {
            "text": "Найдите площадь прямоугольника со сторонами {a} и {b}:",
            "generate": lambda r: {"a": random.randint(2, 10), "b": random.randint(2, 10)},
            "solve": lambda params: params["a"] * params["b"]
        },
        {
            "text": "Найдите периметр квадрата со стороной {a}:",
            "generate": lambda r: {"a": random.randint(2, 15)},
            "solve": lambda params: 4 * params["a"]
        },
        {
            "text": "Найдите площадь треугольника с основанием {a} и высотой {h}:",
            "generate": lambda r: {"a": random.randint(2, 10), "h": random.randint(2, 10)},
            "solve": lambda params: (params["a"] * params["h"]) / 2
        }
    ]
    
    template = random.choice(templates)
    values = template["generate"](DIFFICULTY_LEVELS[difficulty]["range"])
    question = template["text"].format(**values)
    answer = round(template["solve"](values), 2)
    return question, answer

# Словарь с функциями-генераторами
QUESTION_GENERATORS = {
    'arithmetic': generate_arithmetic_question,
    'equation': generate_equation_question,
    'word_problem': generate_word_problem,
    'sequence': generate_sequence_question,
    'geometry': generate_geometry_question
} 