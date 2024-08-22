import pandas as pd
import json
import os


def get_date_from_excel():
    # Путь к файлу Excel
    file_path = 'REGULAR_SCHEDULE.xlsx'

    # Директория для сохранения файлов
    output_dir = 'output_data'
    os.makedirs(output_dir, exist_ok=True)

    # 1. Преобразование данных из листа Models
    models_df = pd.read_excel(file_path, sheet_name='Models')
    models_data = []
    for _, row in models_df.iterrows():
        models_data.append({
            'Model': row.iloc[0],  # Имя модели
            'Category': row.iloc[1]  # Категория модели
        })

    # Сохранение данных в отдельный файл
    with open(os.path.join(output_dir, 'models_data.json'), 'w') as f:
        json.dump(models_data, f, indent=4)

    # 2. Преобразование данных из листа Boost
    boost_df = pd.read_excel(file_path, sheet_name='Boost')
    boost_data = []
    for _, row in boost_df.iterrows():
        for day in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']:
            boost_data.append({
                'Day': day,
                'Model': row['MODEL'],
                'Boost Count': row[day]
            })

    # Сохранение данных в отдельный файл
    with open(os.path.join(output_dir, 'boost_data.json'), 'w') as f:
        json.dump(boost_data, f, indent=4)

    # 2.1 Преобразование данных из листа PRIORITY_BOOST
    priority_df = pd.read_excel(file_path, sheet_name='PRIORITY')
    priority_data = []
    for _, row in priority_df.iterrows():
        for day in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']:
            priority_data.append({
                'Day': day,
                'Model': row['MODEL'],
                'Boost Count': row[day]
            })

    # Сохранение данных в отдельный файл
    with open(os.path.join(output_dir, 'priority_boost_data.json'), 'w') as f:
        json.dump(priority_data, f, indent=4)

    # 3. Преобразование данных из листа BlackList
    blacklist_df = pd.read_excel(file_path, sheet_name='BlackList')
    blocked_models = {}
    for _, row in blacklist_df.iterrows():
        model_a = row['Model']
        model_b = row['Blocked']

        if model_a in blocked_models:
            blocked_models[model_a].append(model_b)
        else:
            blocked_models[model_a] = [model_b]

        if model_b in blocked_models:
            blocked_models[model_b].append(model_a)
        else:
            blocked_models[model_b] = [model_a]

    blacklist_data = [{'Model': model, 'Blocked': blocked} for model, blocked in blocked_models.items()]

    # Сохранение данных в отдельный файл
    with open(os.path.join(output_dir, 'blacklist_data.json'), 'w') as f:
        json.dump(blacklist_data, f, indent=4)

    # 4. Преобразование данных из листа Template
    template_df = pd.read_excel(file_path, sheet_name='Template')
    days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
    models = template_df.columns[3::2]  # Начинаем с колонки D и берем через одну

    all_models_data = []
    for model in models:
        model_name = model.split('.')[0]
        model_data = {'Model': model_name, 'Days': []}

        for day in days:
            day_index = template_df[template_df['MODEL LINE'] == day].index[0]
            day_data = template_df.iloc[day_index:day_index + 7][model]
            model_data['Days'].append({
                'Day': day,
                'Filled Tasks': day_data.tolist()
            })

        all_models_data.append(model_data)

    # Сохранение данных в отдельный файл
    with open(os.path.join(output_dir, 'template_data.json'), 'w') as f:
        json.dump(all_models_data, f, indent=4)

    # Сохранение всех данных в один общий JSON файл
    all_data = {
        'Models': models_data,
        'Boost': boost_data,
        'BlackList': blacklist_data,
        'Template': all_models_data
    }

    with open(os.path.join(output_dir, 'all_data.json'), 'w') as f:
        json.dump(all_data, f, indent=4)

    print(f"Все данные успешно сохранены в директорию: {output_dir}")
