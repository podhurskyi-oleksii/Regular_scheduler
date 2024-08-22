import shutil
import tkinter as tk
from tkinter import messagebox

import allDaysCombiner
import boostFiller
import boostScheduleSplitter
import daySplitter
import excelDataGetter
import exporter
import priorityBoostFiller
import priorityBoostScheduleSplitter
import regularContenFiller


def main():
    excelDataGetter.get_date_from_excel()
    daySplitter.split_days()
    priorityBoostScheduleSplitter.split_priority_boost_schedule()
    boostScheduleSplitter.split_boost_schedule()
    priorityBoostFiller.fill_priority_boost()
    boostFiller.fill_boost()
    allDaysCombiner.combine_all_days()
    regularContenFiller.fill_regular_content()
    exporter.export_from_json_to_excel()

    #shutil.rmtree("output_data")

    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно
    messagebox.showinfo("Завершено", "Готово")


if __name__ == "__main__":
    main()
