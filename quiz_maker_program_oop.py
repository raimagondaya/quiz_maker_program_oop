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

file_path = r"C:\\OOP\\simple-number-programs\\quiz_maker\\saved_quiz_data.txt"
question_bank = QuestionBank(file_path)



random.shuffle(quiz_data)

root = tk.Tk()
root.title("Quiz Game")
root.geometry("800x600")
root.configure(bg="black")

question_label = tk.Label(root, text="", fg="white", bg="black", font=("Arial", 20), wraplength=700)
question_label.pack(pady=50)

buttons = []
for _ in range(4):
    button = tk.Button(root, text="", font=("Arial", 16), width=30)
    button.pack(pady=10)
    buttons.append(button)

score = 0
current = 0

def next_question():
    global current
    if current >= len(quiz_data):
        question_label.config(text=f"Quiz Over! Score: {score}/{len(quiz_data)}")
        for button in buttons:
            button.pack_forget()
        return
    question_text, answer_options, correct_answer = quiz_data[current]
    question_label.config(text=question_text)
    for index, button in enumerate(buttons):
        button.config(text=answer_options[index], command=lambda user_choice=chr(65+index): check_answer(user_choice))
    root.configure(bg="black")

def check_answer(user_choice):
    global score, current
    correct = quiz_data[current][2]
    if user_choice == correct:
        root.configure(bg="green")
        score += 1
    else:
        root.configure(bg="red")
    current += 1
    root.after(1000, next_question)

next_question()
root.mainloop()
