import tkinter as tk
from tkinter import ttk
import random
import timeit
from loguru import logger
logger.remove()

class SortingComparisonApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Сравнение сортировки")
        self.root.geometry("800x800")
        self.root.resizable(False, False)
        self.my_list = []

        self.create_list_button = ttk.Button(self.root, text="Создать список", command=self.create_random_list)
        self.create_list_button.pack(pady=10)

        self.data_text = tk.Text(self.root, wrap=tk.WORD)
        self.data_text.pack(pady=5)
        self.data_text.bind("<Key>", self.on_text_edit)

        self.bubble_label = ttk.Label(self.root, text="Bubble Sort:")
        self.bubble_label.pack(pady=5)
        self.quick_label = ttk.Label(self.root, text="Quick Sort:")
        self.quick_label.pack(pady=5)

        self.run_button = ttk.Button(self.root, text="Запустить сравнение", command=self.run_sorting)
        self.run_button.pack(pady=10)

        self.bubble_final_label = ttk.Label(self.root, text="Bubble Sort:")
        self.bubble_final_label.pack(pady=5)

        self.bubble_final_text = tk.Text(self.root, wrap=tk.WORD, height=2)
        self.bubble_final_text.pack(pady=5)

        self.quick_final_label = ttk.Label(self.root, text="Quick Sort:")
        self.quick_final_label.pack(pady=5)

        self.quick_final_text = tk.Text(self.root, wrap=tk.WORD, height=2)
        self.quick_final_text.pack(pady=5)


    def create_random_list(self):
        self.my_list = [random.randint(1, 1000) for _ in range(1000)]
        self.data_text.insert("1.0", ",".join(map(str, self.my_list)))
        logger.info("Создан новый случайный список.")

    @logger.catch
    def bubble_sort(self, data):
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    t = data[j]
                    data[j] = data[j + 1]
                    data[j + 1] = t
        return data

    @logger.catch
    def quick_sort(self, data):
        if len(data) > 1:
            x = data[random.randint(0, len(data) - 1)]
            low = [u for u in data if u < x]
            eq = [u for u in data if u == x]
            hi = [u for u in data if u > x]
            data = self.quick_sort(low) + eq + self.quick_sort(hi)
        return data

    @logger.catch
    def run_sorting(self):
        # Измерьте время выполнения сортировки пузырьком
        bubble_start_time = timeit.default_timer()
        bf = self.bubble_sort(self.my_list[:])
        bubble_time = timeit.default_timer() - bubble_start_time

        # Измерьте время выполнения быстрой сортировки
        quick_start_time = timeit.default_timer()
        qf = self.quick_sort(self.my_list[:])
        quick_time = timeit.default_timer() - quick_start_time

        self.bubble_label.config(text=f"Bubble Sort: {bubble_time:.6f} sec")
        self.quick_label.config(text=f"Quick Sort: {quick_time:.6f} sec")

        self.bubble_final_text.delete("1.0", "end")
        self.bubble_final_text.insert("1.0", bf)

        self.quick_final_text.delete("1.0", "end")
        self.quick_final_text.insert("1.0", qf)

        logger.success("Сравнение сортировки завершено.")

    @logger.catch
    def on_text_edit(self, event):
        data = self.data_text.get("1.0", "end")
        data = list(map(float, data.split(",")))
        a = sum(data) - int(sum(data))
        self.my_list = list(map(int if a == 0 else float, data))
        logger.debug("Значение обновлено!")
        logger.debug(self.my_list)


if __name__ == "__main__":
    logger.add("sorting_log.log", rotation="10 MB")
    app = SortingComparisonApp()
    app.root.mainloop()
