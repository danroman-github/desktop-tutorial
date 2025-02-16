import os


# Функция создания сортированного списка
def merging_files(list_files, merge_file):
    """Объединяет содержимое файлов, отсортированных по количеству строк."""
    file_data = []
    for file_name in list_files:
        if not os.path.exists(file_name):
            print(f"Файл {file_name} не найден. Пропускаем.")
            continue

        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.readlines()
            file_data.append((file_name, len(content), ''.join(content)))

    file_data.sort(key=lambda x: x[1])

    with open(merge_file, 'w', encoding='utf-8') as f:
        for file_name, len_content, content in file_data:
            f.write(f'{file_name}\n{len_content}\n{content}\n')
    print(f'Файлы успешно объединены в {merge_file}')


list_files = ['1.txt', '2.txt', '3.txt']
merge_file = 'sorted.txt'
merging_files(list_files, merge_file)

