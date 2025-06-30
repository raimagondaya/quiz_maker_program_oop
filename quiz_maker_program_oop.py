import tkinter as tk
import random

class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def write_question_to_file(self, question_text, option_list, correct_answer):
        with open(self.file_path, "a", encoding="utf-8") as file_writer:
            file_writer.write(question_text.strip() + "\n")
            for option in option_list:
                file_writer.write(option.strip() + "\n")
            file_writer.write(correct_answer.strip() + "\n")

    def read_quiz_data(self):
        with open(self.file_path, "r", encoding="utf-8") as file_reader:
            lines = [line.strip() for line in file_reader if line.strip()]
        return lines

class QuestionBank(FileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.quiz_items = []

    def collect_questions(self):
        while True:
            print("Welcome to quiz maker! The quiz will start after...")
            question_text = input("Enter your question: ")
            option_a = input("A. ")
            option_b = input("B. ")
            option_c = input("C. ")
            option_d = input("D. ")
            correct_answer = input("Enter the correct answer (A, B, C, or D): ").upper()

            while correct_answer not in ['A', 'B', 'C', 'D']:
                correct_answer = input("Enter the correct answer (A, B, C, or D): ").upper()

            self.write_question_to_file(
                question_text,
                [option_a, option_b, option_c, option_d],
                correct_answer
            )

            continue_prompt = input("Add another question? (yes/no): ").lower()
            if continue_prompt != 'yes':
                break

    def load_questions(self):
        raw_lines = self.read_quiz_data()
        index = 0
        while index + 5 < len(raw_lines):
            question_text = raw_lines[index]
            options = [raw_lines[index+1], raw_lines[index+2], raw_lines[index+3], raw_lines[index+4]]
            correct_option = raw_lines[index+5]
            self.quiz_items.append((question_text, options, correct_option))
            index += 6

class QuizProgram:
    def __init__(self, quiz_data):
        self.quiz_data = quiz_data
        self.current_index = 0
        self.score = 0

        self.window = tk.Tk()
        self.window.title("Quiz Game")
        self.window.geometry("800x600")
        self.window.configure(bg="black")

        self.question_label = tk.Label(self.window, text="", fg="white", bg="black", font=("Arial", 20), wraplength=700)
        self.question_label.pack(pady=50)

        self.option_buttons = []
        for _ in range(4):
            button = tk.Button(self.window, text="", font=("Arial", 16), width=30)
            button.pack(pady=10)
            self.option_buttons.append(button)

        self.display_next_question()
        self.window.mainloop()

    def display_next_question(self):
        if self.current_index >= len(self.quiz_data):
            self.question_label.config(text=f"Quiz Over! Score: {self.score}/{len(self.quiz_data)}")
            for button in self.option_buttons:
                button.pack_forget()
            return

        question_text, options, _ = self.quiz_data[self.current_index]
        self.question_label.config(text=question_text)

        for index, button in enumerate(self.option_buttons):
            button.config(
                text=options[index],
                command=lambda selected_option=chr(65 + index): self.check_answer(selected_option)
            )

        self.window.configure(bg="black")

    def check_answer(self, selected_option):
        correct_answer = self.quiz_data[self.current_index][2]
        if selected_option == correct_answer:
            self.window.configure(bg="green")
            self.score += 1
        else:
            self.window.configure(bg="red")

        self.current_index += 1
        self.window.after(1000, self.display_next_question)
