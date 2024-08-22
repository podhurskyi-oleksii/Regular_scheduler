import os
import random
import json


def fill_regular_content():
    # Директория для сохранения файлов
    output_dir = 'output_data'
    os.makedirs(output_dir, exist_ok=True)

    # Загрузка данных из JSON-файлов для заполнения
    with open(os.path.join(output_dir, 'models_data.json'), 'r') as f:
        models_data = json.load(f)

    with open(os.path.join(output_dir, 'blacklist_data.json'), 'r') as f:
        blacklist_data = json.load(f)

    with open(os.path.join(output_dir, 'filled_template.json'), 'r') as f:
        template_data = json.load(f)

    # Преобразование блокировок для удобства поиска
    blocked_dict = {item['Model']: item['Blocked'] for item in blacklist_data}

    def is_blocked(model, target_model, blocked_dict):
        blocked_models_for_target = blocked_dict.get(target_model, [])
        return model in blocked_models_for_target

    # TODO
    # Не позорся клоун
    def is_costyl(candidate, filled_tasks):
        # Проверяем, есть ли кандидат в задачах текущего дня
        for task in filled_tasks:
            if task == f"{candidate}_priority" or task == f"{candidate}_boost" or task == candidate:
                return True
        return False

    def fill_regular_content(models_data, template_data, blocked_dict):
        filled_schedule = []
        for model_data in template_data:
            model_name = model_data['Model']
            filled_days = []

            for day_data in model_data['Days']:
                filled_tasks = day_data['Filled Tasks'][:]
                used_models = set()  # Следим за тем, какие модели уже использованы для текущей модели в этот день

                for i, task in enumerate(day_data['Filled Tasks']):
                    if task in ['VANILA', 'COSPLAY', 'BDSM', 'EBONY']:
                        # Выбираем случайную модель из любой категории
                        all_models = [item['Model'] for item in models_data]
                        random.shuffle(all_models)

                        for candidate in all_models:
                            if candidate != model_name and not is_blocked(candidate, model_name,
                                                                          blocked_dict) and candidate not in used_models and not is_costyl(candidate, filled_tasks):
                                print(f"Assigning model {candidate} to slot {i} for model {model_name}")
                                candidate_category = next((item['Category'] for item in models_data if item['Model'] == candidate), None)

                                # Определить окончание в зависимости от категории
                                if candidate_category == 'VANILA':
                                    suffix = '_vanila'
                                elif candidate_category == 'BDSM':
                                    suffix = '_bdsm'
                                elif candidate_category == 'COSPLAY':
                                    suffix = '_cosplay'
                                elif candidate_category == 'EBONY':
                                    suffix = '_ebony'
                                else:
                                    suffix = ''

                                filled_tasks[i] = f"{candidate}{suffix}"
                                used_models.add(candidate)
                                break
                            else:
                                print(
                                    f"Skipping model {candidate} for model {model_name} due to blocking or duplication")

                    elif task == 'BOOST':
                        # Пропускаем обработку для слотов BOOST
                        continue

                    elif task == 'ANY MODEL':
                        # Выбираем случайную модель из любой категории
                        all_models = [item['Model'] for item in models_data]
                        random.shuffle(all_models)

                        for candidate in all_models:
                            if candidate != model_name and not is_blocked(candidate, model_name,
                                                                          blocked_dict) and candidate not in used_models and not is_costyl(candidate, filled_tasks):
                                print(f"Assigning model {candidate} to slot {i} for model {model_name}")
                                filled_tasks[i] = candidate
                                used_models.add(candidate)
                                break
                            else:
                                print(
                                    f"Skipping model {candidate} for model {model_name} due to blocking or duplication")

                filled_days.append({
                    'Day': day_data['Day'],
                    'Filled Tasks': filled_tasks
                })

            filled_schedule.append({
                'Model': model_name,
                'Days': filled_days
            })

        return filled_schedule

    # Используем функцию из внешнего файла для заполнения слотов
    filled_schedule = fill_regular_content(models_data, template_data, blocked_dict)

    # Сохранение заполненного расписания в JSON файл
    output_file_path = 'output_data/filled_template.json'
    with open(output_file_path, 'w') as f:
        json.dump(filled_schedule, f, indent=4)

    print(f"Заполненное расписание сохранено в файл: {output_file_path}")