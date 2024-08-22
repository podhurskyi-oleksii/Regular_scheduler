import json
import os


def split_boost_schedule():
    # Путь к JSON файлу с данными boost
    input_file_path = 'output_data/boost_data.json'

    # Директория для сохранения файлов
    output_dir = 'output_data/boost_days_split'
    os.makedirs(output_dir, exist_ok=True)

    # Загрузка данных из JSON файла
    with open(input_file_path, 'r') as f:
        boost_data = json.load(f)

    # Структура данных для каждого дня
    days_data = {day: [] for day in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']}

    # Проход по данным boost и распределение их по дням
    for entry in boost_data:
        day_name = entry['Day']
        days_data[day_name].append({
            'Model': entry['Model'],
            'Boost Count': entry['Boost Count']
        })

    # Сохранение данных по дням в отдельные JSON файлы
    for day, data in days_data.items():
        output_file_path = os.path.join(output_dir, f'{day.lower()}_boost.json')
        with open(output_file_path, 'w') as f:
            json.dump(data, f, indent=4)

    print(f"Данные boost успешно разделены и сохранены по дням в директорию: {output_dir}")
