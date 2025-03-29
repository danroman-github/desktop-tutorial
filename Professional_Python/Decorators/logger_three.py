import os
from datetime import datetime

def logger(old_function):
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    def new_function(*args, **kwargs):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        arguments = f"args: {args}, kwargs: {kwargs}"
        result = old_function(*args, **kwargs)

        log_string = (
            f"{current_datetime}\n" 
            f"Функция: {old_function.__name__}\n"
            f"Аргументы: {arguments}\n"
            f"Возвращает: {result}\n\n"
        )

        with open('log_three.log', 'a') as log_file:
            log_file.write(log_string)

        return result

    return new_function

@logger
def vote(votes):
    max_count = 0
    result = None
    for i in votes:
        current_count = votes.count(i)
        if current_count > max_count:
            max_count = current_count
            result = i
    return result


if __name__ == '__main__':
    votes = [1, 2, 3, 2, 2, 3, 4, 2, 1, 2, 3]
    vote(votes)
