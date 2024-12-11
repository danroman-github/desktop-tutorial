# Функция создания сортированного списка
def sorted_files(list_files):
    file_date = []

    for file_name in list_files:

        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
            len_content = len(content.splitlines())
            file_date.append((file_name, len_content, content))

    file_date.sort(key=lambda x: x[1])
    return file_date


# Функция создания сортированного списка
def merging_files(list_files, merge_file):
    file_date = sorted_files(list_files)

    with open(merge_file, 'w', encoding='utf-8') as f:

        for file_name, len_content, content in file_date:
            f.write(f'{file_name}\n')
            f.write(f'{len_content}\n')
            f.write(f'{content}\n')

    return file_date


list_files = ['1.txt', '2.txt', '3.txt']
merge_file = 'sorted.txt'
merging_files(list_files, merge_file)
print(f'Файлы успешно объединены в {merge_file}')
