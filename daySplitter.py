import json
import os


def split_days():
    # Путь к JSON файлу с заполненными данными
    input_file_path = 'output_data/template_data.json '

    # Директория для сохранения файлов
    output_dir = 'output_data/days_split'
    os.makedirs(output_dir, exist_ok=True)

    # Загрузка данных из JSON файла
    with open(input_file_path, 'r') as f:
        filled_schedule = json.load(f)

    # Проход по каждому дню недели
    days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']

    # Структура данных для каждого дня
    days_data = {day: [] for day in days}

    for model_data in filled_schedule:
        model_name = model_data['Model']
        for day_data in model_data['Days']:
            day_name = day_data['Day']
            tasks = day_data['Filled Tasks']
            # Добавляем данные для текущего дня
            days_data[day_name].append({
                'Model': model_name,
                'Tasks': tasks
            })

    # Сохранение данных по дням в отдельные JSON файлы
    for day, data in days_data.items():
        output_file_path = os.path.join(output_dir, f'{day.lower()}_schedule.json')
        with open(output_file_path, 'w') as f:
            json.dump(data, f, indent=4)

    print(f"Данные успешно разделены и сохранены по дням в директорию: {output_dir}")

