"""
Math Quiz - Интерактивная математическая викторина
"""

import json
import time
import random
from typing import Dict, List
from datetime import datetime
from colorama import Fore, Style

from src.ui import (
    display_title,
    display_main_menu,
    display_game_modes,
    display_difficulty_selection,
    display_high_scores,
    display_info,
    clear_screen
)
from src.generators import (
    generate_arithmetic_question,
    generate_equation_question,
    generate_word_problem,
    generate_sequence_question,
    generate_geometry_question
)
from src.config import (
    DIFFICULTY_LEVELS,
    HIGH_SCORES_FILE,
    DEFAULT_HIGH_SCORES
)

VERSION = "2.0"

class MathQuiz:
    def __init__(self):
        self.high_scores = self.load_high_scores()
        self.current_score = 0
        self.streak = 0
        self.questions_answered = 0
        self.correct_answers = 0
        
    def load_high_scores(self) -> Dict:
        """Загружает таблицу рекордов из файла"""
        try:
            with open(HIGH_SCORES_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return DEFAULT_HIGH_SCORES.copy()
    
    def save_high_scores(self) -> None:
        """Сохраняет таблицу рекордов в файл"""
        with open(HIGH_SCORES_FILE, 'w') as f:
            json.dump(self.high_scores, f)
    
    def add_high_score(self, difficulty: str) -> None:
        """Добавляет новый рекорд в таблицу"""
        accuracy = (self.correct_answers / self.questions_answered * 100) if self.questions_answered > 0 else 0
        score_data = {
            'score': self.current_score,
            'accuracy': round(accuracy, 1),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        self.high_scores[difficulty].append(score_data)
        self.high_scores[difficulty].sort(key=lambda x: (-x['score'], x['accuracy']))
        self.high_scores[difficulty] = self.high_scores[difficulty][:10]
        self.save_high_scores()
    
    def play_game(self, difficulty: str, practice_mode: bool) -> None:
        """Запускает игровую сессию"""
        clear_screen()
        level_info = DIFFICULTY_LEVELS[difficulty]
        time_limit = float('inf') if practice_mode else level_info['time']
        start_time = time.time()
        
        # Показываем инструкции перед началом игры
        print(f"\n{Fore.CYAN}Управление во время игры:{Style.RESET_ALL}")
        print(f"• Введите {Fore.GREEN}число{Style.RESET_ALL} для ответа на вопрос")
        print(f"• Нажмите {Fore.YELLOW}q{Style.RESET_ALL} для выхода в главное меню")
        print(f"\n{Fore.CYAN}Нажмите Enter, чтобы начать...{Style.RESET_ALL}")
        input()
        clear_screen()
        
        question_generators = {
            'arithmetic': generate_arithmetic_question,
            'equation': generate_equation_question,
            'word_problem': generate_word_problem,
            'sequence': generate_sequence_question,
            'geometry': generate_geometry_question
        }
        
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= time_limit:
                break
                
            # Выбор случайного типа задачи из доступных для текущего уровня
            available_types = level_info['question_types']
            q_type = random.choice(available_types)
            question, correct_answer = question_generators[q_type](difficulty)
            
            # Отображение статуса игры
            remaining_time = max(0, time_limit - elapsed_time) if not practice_mode else float('inf')
            print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Время: {'∞' if practice_mode else round(remaining_time)}с")
            print(f"Счёт: {self.current_score} (Серия: {self.streak}){Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
            print(f"\n{question}")
            print(f"\n{Fore.GREEN}[Ответ/q для выхода]{Style.RESET_ALL} > ", end='')
            
            user_answer = input().strip()
            
            if user_answer.lower() == 'q':
                print(f"\n{Fore.YELLOW}Игра завершена пользователем{Style.RESET_ALL}")
                time.sleep(1)
                return
            
            try:
                user_answer = float(user_answer)
                is_correct = abs(user_answer - correct_answer) < 0.01
                
                self.questions_answered += 1
                if is_correct:
                    self.correct_answers += 1
                    self.streak += 1
                    bonus = max(1, self.streak // 3)
                    self.current_score += 10 * bonus
                    print(f"\n{Fore.GREEN}Правильно! +{10 * bonus} очков{Style.RESET_ALL}")
                else:
                    self.streak = 0
                    print(f"\n{Fore.RED}Неправильно. Правильный ответ: {correct_answer}{Style.RESET_ALL}")
                
                time.sleep(1)
                clear_screen()
                
            except ValueError:
                print(f"\n{Fore.RED}Пожалуйста, введите число{Style.RESET_ALL}")
                time.sleep(1)
                clear_screen()
        
        if not practice_mode:
            self.add_high_score(difficulty)
            print(f"\n{Fore.YELLOW}Игра окончена!{Style.RESET_ALL}")
            print(f"Итоговый счёт: {self.current_score}")
            print(f"Правильных ответов: {self.correct_answers}/{self.questions_answered}")
            input("\nНажмите Enter для продолжения...")
    
    def run(self) -> None:
        """Запускает главный цикл приложения"""
        while True:
            display_title(VERSION)
            choice = display_main_menu()
            
            if choice == '1':  # Начать игру
                practice_mode = display_game_modes()
                difficulty = display_difficulty_selection()
                self.current_score = 0
                self.streak = 0
                self.questions_answered = 0
                self.correct_answers = 0
                self.play_game(difficulty, practice_mode)
            
            elif choice == '2':  # Таблица рекордов
                display_high_scores(self.high_scores)
            
            elif choice == '3':  # Информация
                display_info()
            
            else:  # Выход
                clear_screen()
                print("\nСпасибо за игру! До свидания!")
                break

if __name__ == '__main__':
    quiz = MathQuiz()
    quiz.run()