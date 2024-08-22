import json
import os


def combine_all_days():
    # Пути к основным файлам
    template_file_path = 'output_data/template_data.json'
    schedule_dir = 'output_data/days_split'

    # Загрузка данных из шаблона
    with open(template_file_path, 'r') as f:
        template_data = json.load(f)

    # Цикл по дням недели
    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    for day in days_of_week:
        # Загрузка расписания для текущего дня
        schedule_file = os.path.join(schedule_dir, f'{day}_schedule.json')
        with open(schedule_file, 'r') as f:
            day_schedule = json.load(f)

        # Проходим по всем моделям в шаблоне
        for model_data in template_data:
            model_name = model_data['Model']

            # Ищем соответствующую модель в расписании для текущего дня
            for day_entry in model_data['Days']:
                if day_entry['Day'].lower() == day:
                    # Находим запись для этой модели в расписании
                    for schedule_entry in day_schedule:
                        if schedule_entry['Model'] == model_name:
                            # Обновляем задачи для текущего дня
                            day_entry['Filled Tasks'] = schedule_entry['Tasks']
                            break

    # Сохранение обновленного шаблона в файл
    output_file_path = 'output_data/filled_template.json'
    with open(output_file_path, 'w') as f:
        json.dump(template_data, f, indent=4)

    print(f"Обновленный шаблон сохранен в файл: {output_file_path}")
