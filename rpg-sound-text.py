import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import pygame
import time
import threading
import os

DND_SUPPORT = False
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_SUPPORT = True
except ImportError:
    print("tkinterdnd2 не найден. Перетаскивание файлов будет недоступно.")
    print("Для установки: pip install tkinterdnd2")

class RPGTextSoundApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("RPG Text Sound Player")
        # Попробуем уменьшить начальную высоту окна для тестера
        self.root.geometry("700x550") # Было 700x600

        try:
            pygame.mixer.init()
        except pygame.error as e:
            messagebox.showerror("Ошибка Pygame", f"Не удалось инициализировать Pygame Mixer: {e}\nУбедитесь, что у вас установлены звуковые драйверы.")
            self.root.quit()
            return

        self.sound_path = None
        self.current_sound = None
        self.is_playing = False
        self.playback_thread = None

        style = ttk.Style()
        style.theme_use('clam')

        controls_frame = ttk.LabelFrame(self.root, text="Управление", padding=(10, 5))
        controls_frame.pack(padx=10, pady=10, fill="x")

        ttk.Button(controls_frame, text="Выбрать звук (.wav)", command=self.select_sound_file).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.sound_label = ttk.Label(controls_frame, text="Звук не выбран")
        self.sound_label.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        ttk.Label(controls_frame, text="Интервал (мс):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.speed_var = tk.IntVar(value=100)
        self.speed_scale = ttk.Scale(controls_frame, from_=10, to=500, orient="horizontal", variable=self.speed_var, command=lambda s: self.speed_var.set(int(float(s))))
        self.speed_scale.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.speed_entry = ttk.Entry(controls_frame, textvariable=self.speed_var, width=5)
        self.speed_entry.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(controls_frame, text="Громкость:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.volume_var = tk.DoubleVar(value=0.8)
        self.volume_scale = ttk.Scale(controls_frame, from_=0.0, to=1.0, orient="horizontal", variable=self.volume_var, command=lambda v: self.volume_var.set(float(v)))
        self.volume_scale.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.volume_entry = ttk.Entry(controls_frame, textvariable=self.volume_var, width=5)
        self.volume_entry.grid(row=2, column=2, padx=5, pady=5)
        
        controls_frame.columnconfigure(1, weight=1)

        input_frame_text = "Введите текст или перетащите .txt файл сюда" if DND_SUPPORT else "Введите текст"
        input_frame = ttk.LabelFrame(self.root, text=input_frame_text, padding=(10, 5))
        input_frame.pack(padx=10, pady=5, fill="both", expand=True) # expand=True важен

        self.input_text_area = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10, font=("Arial", 10))
        self.input_text_area.pack(padx=5, pady=5, fill="both", expand=True)

        if DND_SUPPORT:
            self.input_text_area.drop_target_register(DND_FILES)
            self.input_text_area.dnd_bind('<<Drop>>', self.handle_drop)
            self.input_text_area.dnd_bind('<<DragEnter>>', self.drag_enter)
            self.input_text_area.dnd_bind('<<DragLeave>>', self.drag_leave)
        else:
            ttk.Button(input_frame, text="Загрузить текст из файла (.txt)", command=self.load_text_from_file).pack(pady=5, side="bottom")


        output_frame = ttk.LabelFrame(self.root, text="Результат", padding=(10, 5))
        output_frame.pack(padx=10, pady=5, fill="both", expand=True) # expand=True важен

        self.output_text_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10, state="disabled", font=("Arial", 12, "bold"))
        self.output_text_area.pack(padx=5, pady=5, fill="both", expand=True)

        action_buttons_frame = ttk.Frame(self.root, padding=(10,5))
        action_buttons_frame.pack(fill="x", padx=10, pady=(5,10)) # Немного отступ снизу

        self.play_button = ttk.Button(action_buttons_frame, text="Воспроизвести", command=self.start_playback)
        self.play_button.pack(side="left", padx=5, expand=True, fill="x")

        self.stop_button = ttk.Button(action_buttons_frame, text="Остановить", command=self.stop_playback, state="disabled")
        self.stop_button.pack(side="left", padx=5, expand=True, fill="x")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def select_sound_file(self):
        path = filedialog.askopenfilename(
            title="Выберите звуковой файл",
            filetypes=(("Audio Files", "*.wav *.ogg *.mp3"),("WAV files", "*.wav"), ("OGG files", "*.ogg"), ("MP3 files", "*.mp3"), ("All files", "*.*"))
        )
        if path:
            try:
                self.current_sound = pygame.mixer.Sound(path)
                self.sound_path = path
                self.sound_label.config(text=os.path.basename(path))
            except pygame.error as e:
                messagebox.showerror("Ошибка звука", f"Не удалось загрузить звук: {e}\nУбедитесь, что это поддерживаемый аудиофайл.")
                self.current_sound = None
                self.sound_path = None
                self.sound_label.config(text="Ошибка загрузки звука")

    def load_text_from_file(self, filepath=None):
        if not filepath:
            filepath = filedialog.askopenfilename(
                title="Выберите текстовый файл",
                filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
            )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.input_text_area.delete('1.0', tk.END)
                    self.input_text_area.insert('1.0', f.read())
            except Exception as e:
                messagebox.showerror("Ошибка файла", f"Не удалось прочитать файл: {e}")

    if DND_SUPPORT:
        def drag_enter(self, event):
            event.widget.focus_force()
            return event.action

        def drag_leave(self, event):
            pass

        def handle_drop(self, event):
            if event.data:
                filepaths = self.root.tk.splitlist(event.data)
                if filepaths and filepaths[0].lower().endswith(".txt"):
                    self.load_text_from_file(filepaths[0])
                elif filepaths:
                     messagebox.showwarning("Неверный файл", f"Пожалуйста, перетащите .txt файл. Вы перетащили: {os.path.basename(filepaths[0])}")
            return event.action

    def start_playback(self):
        if self.is_playing:
            return
        if not self.current_sound:
            messagebox.showwarning("Нет звука", "Пожалуйста, выберите звуковой файл.")
            return

        text_to_play = self.input_text_area.get("1.0", tk.END).strip()
        if not text_to_play:
            messagebox.showwarning("Нет текста", "Пожалуйста, введите текст для воспроизведения.")
            return

        self.is_playing = True # Устанавливаем флаг в начале
        
        # Обновляем GUI перед запуском потока
        self.play_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.input_text_area.config(state="disabled")
        
        self.output_text_area.config(state="normal") # Разрешаем изменения
        self.output_text_area.delete("1.0", tk.END) # Очищаем
        # self.output_text_area.config(state="disabled") # Пока не отключаем, текст будет добавляться

        self.playback_thread = threading.Thread(target=self._playback_logic, args=(text_to_play,), daemon=True)
        self.playback_thread.start()

    def _playback_logic(self, text_to_play):
        char_interval_ms = self.speed_var.get()
        volume = self.volume_var.get()
        self.current_sound.set_volume(volume)

        try:
            for char_to_display in text_to_play:
                if not self.is_playing: # Проверяем флаг перед каждой операцией
                    break
                
                # Безопасное обновление текстового поля из основного потока
                self.root.after(0, self._insert_char_in_output, char_to_display)

                if char_to_display.strip():
                    try:
                        self.current_sound.play()
                    except pygame.error as e:
                        print(f"Ошибка воспроизведения звука: {e}") # Логируем
                
                # Точное ожидание с проверкой флага
                start_wait = time.time()
                while (time.time() - start_wait) * 1000 < char_interval_ms:
                    if not self.is_playing:
                        break
                    time.sleep(0.001) 
                if not self.is_playing: # Еще одна проверка после цикла ожидания
                    break
        finally:
            # Гарантированный сброс UI по завершении или прерывании потока,
            # выполненный в основном потоке.
            self.root.after(0, self._finalize_playback_ui)

    def _insert_char_in_output(self, char_to_insert):
        # Эта функция вызывается через root.after, поэтому она в основном потоке
        # output_text_area должна быть 'normal' для вставки
        original_state = self.output_text_area.cget("state")
        self.output_text_area.config(state="normal")
        self.output_text_area.insert(tk.END, char_to_insert)
        self.output_text_area.see(tk.END)
        self.output_text_area.config(state=original_state) # Возвращаем исходное состояние (обычно 'disabled' для пользователя)

    def _finalize_playback_ui(self):
        # Эта функция вызывается через root.after, поэтому она в основном потоке
        self.is_playing = False # КРИТИЧНО: сбрасываем флаг для возможности нового запуска
        
        self.output_text_area.config(state="disabled") # Отключаем редактирование результата
        self.play_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.input_text_area.config(state="normal")

    def stop_playback(self):
        if self.is_playing:
            self.is_playing = False # Сигнализируем потоку остановиться
            # Поток сам вызовет _finalize_playback_ui при завершении.
            # Можно добавить немедленное обновление состояния кнопок для отзывчивости,
            # но финальное состояние все равно установит _finalize_playback_ui.
            self.stop_button.config(state="disabled") 
            # self.play_button.config(state="normal") # Можно включить, но _finalize_playback_ui это сделает надежнее

    def on_closing(self):
        if self.is_playing:
            self.is_playing = False # Сигнал потоку
            if self.playback_thread and self.playback_thread.is_alive():
                self.playback_thread.join(0.2) # Дать немного времени на завершение
        pygame.mixer.quit()
        self.root.destroy()

if __name__ == "__main__":
    if DND_SUPPORT:
        main_window = TkinterDnD.Tk()
    else:
        main_window = tk.Tk()
    
    app = RPGTextSoundApp(main_window)
    main_window.mainloop()
