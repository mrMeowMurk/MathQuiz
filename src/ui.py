"""Функции пользовательского интерфейса"""

import os
from typing import Dict
from colorama import Fore, Style
from art import text2art
from .config import DIFFICULTY_LEVELS, QUESTION_TYPE_DESCRIPTIONS

def clear_screen() -> None:
    """Очищает экран терминала"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_title(version: str) -> None:
    """Отображает заголовок приложения"""
    clear_screen()
    title = text2art("Math Quiz", font="block")
    print(Fore.CYAN + title + Style.RESET_ALL)
    print(f"{Fore.YELLOW}Версия: {version}{Style.RESET_ALL}")

def display_main_menu() -> str:
    """Отображает главное меню и возвращает выбор пользователя"""
    print("\nГлавное меню:")
    print("1. Начать игру")
    print("2. Посмотреть рекорды")
    print("3. Информация о программе")
    print("4. Выход")
    
    while True:
        choice = input("\nВыберите действие (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print(f"{Fore.RED}Пожалуйста, выберите 1, 2, 3 или 4{Style.RESET_ALL}")

def display_game_modes() -> bool:
    """Отображает выбор режима игры. Возвращает True для режима практики"""
    print("\nРежимы игры:")
    print("1. Стандартный режим - решайте примеры на время")
    print("2. Режим практики - без ограничения по времени")
    
    while True:
        mode = input("\nВыберите режим (1/2): ").strip()
        if mode in ['1', '2']:
            return mode == '2'
        print(f"{Fore.RED}Пожалуйста, выберите 1 или 2{Style.RESET_ALL}")

def display_difficulty_selection() -> str:
    """Отображает выбор уровня сложности"""
    print("\nВыберите уровень сложности:")
    for level, info in DIFFICULTY_LEVELS.items():
        print(f"\n{info['name']}:")
        print(f"• Диапазон чисел: {info['range'][0]}-{info['range'][1]}")
        print(f"• Время: {info['time']} секунд")
        print(f"• Доступные типы задач:")
        for q_type in info['question_types']:
            print(f"  - {QUESTION_TYPE_DESCRIPTIONS[q_type]}")
    
    while True:
        choice = input("\nВаш выбор (1-3): ")
        if choice in DIFFICULTY_LEVELS:
            return choice
        print(f"{Fore.RED}Пожалуйста, выберите 1, 2 или 3{Style.RESET_ALL}")

def display_high_scores(high_scores: Dict, difficulty: str = None) -> None:
    """Отображает таблицу рекордов"""
    clear_screen()
    print(f"\n{Fore.YELLOW}Таблица рекордов{Style.RESET_ALL}")
    
    difficulties = [difficulty] if difficulty else DIFFICULTY_LEVELS.keys()
    
    for diff in difficulties:
        print(f"\n{Fore.CYAN}{DIFFICULTY_LEVELS[diff]['name']} уровень:{Style.RESET_ALL}")
        scores = sorted(high_scores[diff], key=lambda x: (-x['score'], x['accuracy']))[:5]
        if scores:
            for i, score in enumerate(scores, 1):
                print(f"{i}. Счёт: {score['score']}, "
                      f"Точность: {score['accuracy']}%, "
                      f"Дата: {score['date']}")
        else:
            print("Пока нет рекордов!")
    
    input("\nНажмите Enter, чтобы продолжить...")

def display_info() -> None:
    """Отображает информацию о программе"""
    clear_screen()
    print("\nО программе:")
    print("Math Quiz - это интерактивная математическая викторина,")
    print("которая поможет вам улучшить ваши математические навыки.")
    
    print("\nТипы задач:")
    for q_type, desc in QUESTION_TYPE_DESCRIPTIONS.items():
        print(f"• {desc}")
    
    print("\nУровни сложности:")
    for level, info in DIFFICULTY_LEVELS.items():
        print(f"\n{info['name']}:")
        print(f"• Диапазон чисел: {info['range'][0]}-{info['range'][1]}")
        print(f"• Время: {info['time']} секунд")
    
    input("\nНажмите Enter, чтобы вернуться в главное меню...") 