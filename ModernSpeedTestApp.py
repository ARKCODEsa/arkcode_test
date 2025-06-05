
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from PIL import Image, ImageTk
import speedtest
import os

class ModernSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Test")
        self.root.geometry("600x700")
        self.root.configure(bg='#141526')
        self.root.attributes('-alpha', 0.95)

        # Configurar estilos
        self.style = ttk.Style()
        self.style.configure(
            "Custom.TLabel",
            background='#141526',
            foreground='white',
            font=("Arial", 12)
        )
        self.style.configure(
            "Title.TLabel",
            background='#141526',
            foreground='white',
            font=("Arial", 24, "bold")
        )
        self.style.configure(
            "Result.TLabel",
            background='#141526',
            foreground='white',
            font=("Arial", 40, "bold")
        )
        self.style.configure(
            "Unit.TLabel",
            background='#141526',
            foreground='#888888',
            font=("Arial", 16)
        )
        
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(expand=True, fill='both')
        main_frame.configure(style="Main.TFrame")

        # Logo y título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=20)
        
        title = ttk.Label(
            title_frame,
            text="SPEEDTEST",
            style="Title.TLabel"
        )
        title.pack()

        # Frame para el círculo central
        self.gauge_frame = tk.Frame(main_frame, bg='#141526')
        self.gauge_frame.pack(expand=True, fill='both', padx=20)

        # Canvas para el medidor circular
        self.canvas = tk.Canvas(
            self.gauge_frame,
            width=400,
            height=400,
            bg='#141526',
            highlightthickness=0
        )
        self.canvas.pack(expand=True)

        # Crear círculos base
        self.outer_circle = self.canvas.create_oval(
            50, 50, 350, 350,
            outline='#1a1b2e',
            width=40
        )

        # Arco de progreso
        self.progress_arc = self.canvas.create_arc(
            50, 50, 350, 350,
            start=90,
            extent=0,
            fill='',
            outline='#00ff00',
            width=40,
            style=tk.ARC
        )

        # Texto central
        self.speed_text = self.canvas.create_text(
            200, 180,
            text="0",
            fill="white",
            font=("Arial", 60, "bold")
        )
        
        self.mbps_text = self.canvas.create_text(
            200, 240,
            text="Mbps",
            fill="#888888",
            font=("Arial", 20)
        )

        # Frame para resultados
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill='x', pady=20)

        # Resultados detallados
        self.ping_frame = self.create_result_widget(results_frame, "PING", "ms")
        self.ping_frame.pack(side='left', expand=True)
        
        self.download_frame = self.create_result_widget(results_frame, "DESCARGA", "Mbps")
        self.download_frame.pack(side='left', expand=True)
        
        self.upload_frame = self.create_result_widget(results_frame, "SUBIDA", "Mbps")
        self.upload_frame.pack(side='left', expand=True)

        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30)

        # Estilo para botones
        self.style.configure(
            "Action.TButton",
            background="#141526",
            foreground="white",
            padding=10,
            font=("Arial", 12)
        )

        self.start_button = ttk.Button(
            button_frame,
            text="INICIAR TEST",
            style="Action.TButton",
            command=self.start_test
        )
        self.start_button.pack(side='left', padx=10)

        self.web_button = ttk.Button(
            button_frame,
            text="IR A SPEEDTEST.NET",
            style="Action.TButton",
            command=self.open_speedtest_web
        )
        self.web_button.pack(side='left', padx=10)

    def create_result_widget(self, parent, title, unit):
        frame = ttk.Frame(parent)
        
        title_label = ttk.Label(
            frame,
            text=title,
            style="Custom.TLabel"
        )
        title_label.pack()
        
        value_label = ttk.Label(
            frame,
            text="0",
            style="Result.TLabel"
        )
        value_label.pack()
        
        unit_label = ttk.Label(
            frame,
            text=unit,
            style="Unit.TLabel"
        )
        unit_label.pack()
        
        frame.value_label = value_label
        return frame

    def update_progress(self, value, speed=0):
        # Actualizar arco de progreso
        extent = int(360 * (value / 100))
        self.canvas.itemconfig(self.progress_arc, extent=extent)
        
        # Actualizar texto de velocidad
        self.canvas.itemconfig(self.speed_text, text=f"{speed:.1f}")
        
        # Actualizar color según la velocidad
        if speed > 100:
            color = '#00ff00'  # Verde para velocidad alta
        elif speed > 50:
            color = '#ffaa00'  # Naranja para velocidad media
        else:
            color = '#ff0000'  # Rojo para velocidad baja
            
        self.canvas.itemconfig(self.progress_arc, outline=color)
        self.root.update()

    def start_test(self):
        self.start_button.config(state='disabled')
        self.reset_values()
        thread = threading.Thread(target=self.run_speedtest, daemon=True)
        thread.start()

    def reset_values(self):
        self.ping_frame.value_label.config(text="0")
        self.download_frame.value_label.config(text="0")
        self.upload_frame.value_label.config(text="0")
        self.update_progress(0, 0)

    def run_speedtest(self):
        try:
            st = speedtest.Speedtest()
            
            # Servidor
            self.update_progress(10, 0)
            st.get_best_server()
            
            # Ping
            self.update_progress(20, 0)
            ping = st.results.ping
            self.ping_frame.value_label.config(text=f"{ping:.1f}")
            
            # Descarga
            def download_progress(speed, _):
                speed_mbps = speed / 1_000_000
                self.update_progress(50, speed_mbps)
                
            st.download(callback=download_progress)
            download_speed = st.results.download / 1_000_000
            self.download_frame.value_label.config(text=f"{download_speed:.1f}")
            
            # Subida
            def upload_progress(speed, _):
                speed_mbps = speed / 1_000_000
                self.update_progress(80, speed_mbps)
                
            st.upload(callback=upload_progress)
            upload_speed = st.results.upload / 1_000_000
            self.upload_frame.value_label.config(text=f"{upload_speed:.1f}")
            
            # Completado
            self.update_progress(100, upload_speed)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el test: {str(e)}")
            self.update_progress(0, 0)
        finally:
            self.start_button.config(state='normal')

    def open_speedtest_web(self):
        webbrowser.open('https://www.speedtest.net/')

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernSpeedTest(root)
    root.mainloop()