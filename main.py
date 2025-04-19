import argparse
from datetime import datetime
from random import shuffle
import sys


class DataFormatError(Exception):
    pass


def parse_terminal(questions):
    parser = argparse.ArgumentParser()
    parser.add_argument("index", nargs=1, type=int, help="Выберите правильный вариант ответа")
    correct_answers = 0
    cur_pos = 0
    is_first = True
    while cur_pos < len(questions):
        print(f"{questions[cur_pos][0]}")
        for i in range(1, 6):
            print(f"{i}. {questions[cur_pos][i]}")

        ind = int(input("Номер: "))
        if ind < 1 or ind > 5:
            print("Неправильный индекс. Попробуйте снова\n")
        elif questions[cur_pos][ind] != questions[cur_pos][6]:
            print("Неправильный ответ. Следующий вопрос\n")
            cur_pos += 1
        else:
            print("Правильно!\n")
            correct_answers += 1
            cur_pos += 1
    print("Вы ответили на все вопросы")
    return correct_answers


def logging_question(text):
    try:
        with open("results.txt", "a") as file:
            file.write(text + "\n")
    except OSError:
        print("Could not open/read file")
        sys.exit()


def shuffle_elements(lst):
    for i in range(len(lst)):
        el = lst[i][1:-1]
        shuffle(el)
        lst[i] = [lst[i][0], *el, lst[i][-1]]
    shuffle(lst)
    return lst


def main():
    try:
        with open("data.txt", "r", encoding="utf-8") as file:
            data = file.readlines()
            questions = list(map(lambda x: x.rstrip().split("|"), data))
            if all(list(map(lambda x: len(x) != 7, questions))):
                raise DataFormatError
    except OSError:
        print("Could not open/read file")
        sys.exit()
    except DataFormatError:
        print("Incorrect questions format")
        sys.exit()
    logging_question(f"Время начала теста: {datetime.now()}")
    questions = shuffle_elements(questions)
    correct_answers = parse_terminal(questions)
    logging_question(f"Время окончания теста: {datetime.now()}")
    logging_question(f"Общее количество вопросов: {len(questions)}\n"
                     f"Количество правильных ответов: {correct_answers}\n"
                     f"Процент правильных ответов: {((correct_answers / len(questions)) * 100):.2f}%\n")


if __name__ == "__main__":
    main()
