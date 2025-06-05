import urllib3

urllib3.disable_warnings()

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import time
import statistics


class SpeedTest(tk.Frame):  # Cambiar de tk.Tk a tk.Frame
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        # Configuraciones básicas
        self.PING_TIMEOUT = 3.0
        self.MAX_RETRIES = 3
        self.PING_SAMPLES = 3
        self.is_testing = False

        # Configuración de la sesión HTTP
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*'
        })

        self.stop_test = False
        self.create_widgets()
        self.pack(expand=True, fill='both')

    def create_widgets(self):
        main_frame = tk.Frame(self, bg='#141526')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Título
        title = tk.Label(main_frame, text="SPEED TEST",
                         font=("Arial", 24, "bold"),
                         bg='#141526', fg='white')
        title.pack(pady=20)

        # Status
        self.status_label = tk.Label(main_frame,
                                     text="Listo para iniciar",
                                     font=("Arial", 12),
                                     bg='#141526', fg='#00ff00')
        self.status_label.pack(pady=10)

        # Resultado principal
        results_frame = tk.Frame(main_frame, bg='#141526')
        results_frame.pack(pady=20)

        self.speed_label = tk.Label(results_frame,
                                    text="0",
                                    font=("Arial", 48, "bold"),
                                    bg='#141526', fg='white')
        self.speed_label.pack()

        tk.Label(results_frame, text="Mbps",
                 font=("Arial", 14),
                 bg='#141526', fg='#888888').pack()

        # Detalles
        details_frame = tk.Frame(main_frame, bg='#141526')
        details_frame.pack(fill='x', pady=20)

        self.ping_label = tk.Label(details_frame,
                                   text="--",
                                   font=("Arial", 16, "bold"),
                                   bg='#141526', fg='white')
        self.ping_label.pack(side='left', expand=True)

        self.download_label = tk.Label(details_frame,
                                       text="--",
                                       font=("Arial", 16, "bold"),
                                       bg='#141526', fg='white')
        self.download_label.pack(side='left', expand=True)

        self.upload_label = tk.Label(details_frame,
                                     text="--",
                                     font=("Arial", 16, "bold"),
                                     bg='#141526', fg='white')
        self.upload_label.pack(side='left', expand=True)

        # Etiquetas
        labels_frame = tk.Frame(main_frame, bg='#141526')
        labels_frame.pack(fill='x')

        tk.Label(labels_frame, text="PING (ms)",
                 font=("Arial", 10),
                 bg='#141526', fg='#888888').pack(side='left', expand=True)
        tk.Label(labels_frame, text="DESCARGA",
                 font=("Arial", 10),
                 bg='#141526', fg='#888888').pack(side='left', expand=True)
        tk.Label(labels_frame, text="SUBIDA",
                 font=("Arial", 10),
                 bg='#141526', fg='#888888').pack(side='left', expand=True)

        # Botones
        button_frame = tk.Frame(main_frame, bg='#141526')
        button_frame.pack(pady=30)

        # Frame para botones lado a lado
        buttons_container = tk.Frame(button_frame, bg='#141526')
        buttons_container.pack()

        self.start_button = ttk.Button(
            buttons_container,
            text="INICIAR TEST",
            command=self.start_test,
            width=15
        )
        self.start_button.pack(side='left', padx=5)

        self.stop_button = ttk.Button(
            buttons_container,
            text="DETENER",
            command=self.stop_current_test,
            width=15,
            state='disabled'
        )
        self.stop_button.pack(side='left', padx=5)

        # Barra de progreso
        self.progress = ttk.Progressbar(button_frame,
                                        length=200,
                                        mode='determinate')
        self.progress.pack(pady=5)

    def create_widgets(self):
        # [El resto del código de la interfaz permanece igual...]
        main_frame = tk.Frame(self.root, bg='#141526')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Título
        title = tk.Label(main_frame, text="SPEED TEST",
                         font=("Arial", 24, "bold"),
                         bg='#141526', fg='white')
        title.pack(pady=20)

        # Status
        self.status_label = tk.Label(main_frame,
                                     text="Listo para iniciar",
                                     font=("Arial", 12),
                                     bg='#141526', fg='#00ff00')
        self.status_label.pack(pady=10)

        # Resultado principal
        results_frame = tk.Frame(main_frame, bg='#141526')
        results_frame.pack(pady=20)

        self.speed_label = tk.Label(results_frame,
                                    text="0",
                                    font=("Arial", 48, "bold"),
                                    bg='#141526', fg='white')
        self.speed_label.pack()

        tk.Label(results_frame, text="Mbps",
                 font=("Arial", 14),
                 bg='#141526', fg='#888888').pack()

        # Detalles
        details_frame = tk.Frame(main_frame, bg='#141526')
        details_frame.pack(fill='x', pady=20)

        self.ping_label = tk.Label(details_frame,
                                   text="--",
                                   font=("Arial", 16, "bold"),
                                   bg='#141526', fg='white')
        self.ping_label.pack(side='left', expand=True)

        self.download_label = tk.Label(details_frame,
                                       text="--",
                                       font=("Arial", 16, "bold"),
                                       bg='#141526', fg='white')
        self.download_label.pack(side='left', expand=True)

        self.upload_label = tk.Label(details_frame,
                                     text="--",
                                     font=("Arial", 16, "bold"),
                                     bg='#141526', fg='white')
        self.upload_label.pack(side='left', expand=True)

        # Etiquetas
        labels_frame = tk.Frame(main_frame, bg='#141526')
        labels_frame.pack(fill='x')

        tk.Label(labels_frame, text="PING (ms)",
                 font=("Arial", 10),
                 bg='#141526', fg='#888888').pack(side='left', expand=True)
        tk.Label(labels_frame, text="DESCARGA",
                 font=("Arial", 10),
                 bg='#141526', fg='#888888').pack(side='left', expand=True)
        tk.Label(labels_frame, text="SUBIDA",
                 font=("Arial", 10),
                 bg='#141526', fg='#888888').pack(side='left', expand=True)

        # Botones
        button_frame = tk.Frame(main_frame, bg='#141526')
        button_frame.pack(pady=30)
    
        # Frame para botones lado a lado
        buttons_container = tk.Frame(button_frame, bg='#141526')
        buttons_container.pack()
    
        self.start_button = ttk.Button(
            buttons_container,
            text="INICIAR TEST",
            command=self.start_test,
            width=15
        )
        self.start_button.pack(side='left', padx=5)
    
        self.stop_button = ttk.Button(
            buttons_container,
            text="DETENER",
            command=self.stop_current_test,
            width=15,
            state='disabled'
        )
        self.stop_button.pack(side='left', padx=5)

        # Barra de progreso
        self.progress = ttk.Progressbar(button_frame,
                                        length=200,
                                        mode='determinate')
        self.progress.pack(pady=5)

    def get_best_server(self):
        """Encuentra el servidor más rápido con mejor manejo de errores"""
        best_server = None
        best_score = float('inf')

        # Servidores para Ecuador
        self.servers = [
            {
                "url": "http://speedtest.netlife.ec",
                "name": "Netlife Ecuador",
                "location": "Quito"
            },
            {
                "url": "http://speedtest.cnt-grms.com.ec",
                "name": "CNT Ecuador",
                "location": "Guayaquil"
            },
            {
                "url": "http://speedtest.claro.com.ec",
                "name": "Claro Ecuador",
                "location": "Quito"
            },
            {
                "url": "http://speedtest.movistar.com.ec",
                "name": "Movistar Ecuador",
                "location": "Guayaquil"
            },
            {
                "url": "http://mia1.speedtest.telefonica.com",
                "name": "Telefónica Miami",
                "location": "Miami"
            }
        ]

        self.session.timeout = (5, 10)

        for server in self.servers:
            try:
                self.update_status(f"Probando {server['name']}...")
                ping_times = []
                failed_attempts = 0
                connected = False

                # Prueba de conectividad
                test_paths = ["/", "/speedtest/", "/test/", "/100MB.test", "/1MB.test"]

                for path in test_paths:
                    try:
                        test_response = self.session.head(
                            f"{server['url']}{path}",
                            timeout=3,
                            verify=False,
                            allow_redirects=True
                        )
                        if test_response.status_code in [200, 301, 302]:
                            connected = True
                            break
                    except:
                        continue

                if not connected:
                    print(f"No se puede conectar a {server['name']}")
                    continue

                # Pruebas de ping
                for i in range(self.PING_SAMPLES):
                    try:
                        if self.stop_test:
                            return None, None

                        start_time = time.time()
                        response = self.session.get(
                            f"{server['url']}/1MB.test",
                            stream=True,
                            timeout=self.PING_TIMEOUT,
                            verify=False
                        )

                        if response.status_code == 200:
                            next(response.iter_content(1024))
                            ping_time = (time.time() - start_time) * 1000

                            if ping_time < 1000:
                                ping_times.append(ping_time)
                                print(f"Ping {i + 1} a {server['name']}: {ping_time:.0f}ms")

                        response.close()

                    except Exception as e:
                        print(f"Error en ping {i + 1} a {server['name']}: {str(e)}")
                        failed_attempts += 1

                # Calcular score
                if ping_times:
                    avg_ping = statistics.mean(ping_times)
                    reliability = 1 - (failed_attempts / self.PING_SAMPLES)
                    score = avg_ping * (2 - reliability)

                    print(f"\nServidor: {server['name']}")
                    print(f"Ping promedio: {avg_ping:.0f}ms")
                    print(f"Confiabilidad: {reliability * 100:.1f}%")
                    print(f"Score: {score:.0f}\n")

                    if score < best_score:
                        best_score = score
                        best_server = server
                        self.update_status(
                            f"Mejor servidor: {server['name']}\n"
                            f"Ping: {avg_ping:.0f}ms | "
                            f"Confiabilidad: {reliability * 100:.1f}%"
                        )

            except Exception as e:
                print(f"Error completo con {server['name']}: {str(e)}")
                continue

        if not best_server:
            self.update_status("No se encontró ningún servidor disponible", '#ff0000')
            return None, None

        return best_server, best_score

    def update_progress(self, current, total):
        """Actualiza la barra de progreso"""
        progress = (current / total) * 100
        self.progress['value'] = progress
        self.root.update_idletasks()

    def measure_speed(self, server, mode='download'):
        """Mide la velocidad de descarga o subida"""
        speeds = []
        total_files = len(self.test_files if mode == 'download' else [1, 2, 5])
        current_file = 0
        chunk_size = 8192  # Definir el tamaño del chunk aquí
        
        try:
            if mode == 'download':
                for test_file in self.test_files:
                    if self.stop_test:
                        break
                        
                    current_file += 1
                    self.update_progress(current_file, total_files)
                    
                    try:
                        response = self.session.get(
                            f"{server['url']}/{test_file}",
                            stream=True,
                            timeout=10
                        )

                        file_start_time = time.time()
                        file_bytes = 0

                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                file_bytes += len(chunk)
                                duration = time.time() - file_start_time
                                if duration > 0:
                                    speed = (file_bytes * 8) / (1_000_000 * duration)  # Mbps
                                    speeds.append(speed)
                                    self.update_speed(speed, mode)

                            if time.time() - file_start_time > 5:  # Máximo 5 segundos por archivo
                                break

                        response.close()

                    except Exception as e:
                        print(f"Error descargando {test_file}: {str(e)}")
                        continue

            else:  # upload
                data_sizes = [1024*1024, 2*1024*1024, 5*1024*1024]
                for size in data_sizes:
                    if self.stop_test:
                        break
                        
                    current_file += 1
                    self.update_progress(current_file, total_files)
                    
                    try:
                        data = b'0' * size
                        start_chunk = time.time()

                        # Simular upload enviando datos al servidor
                        response = self.session.post(
                            f"{server['url']}/upload",
                            data=data,
                            timeout=10
                        )

                        duration = time.time() - start_chunk
                        if duration > 0:
                            speed = (size * 8) / (1_000_000 * duration)
                            speeds.append(speed)
                            self.update_speed(speed, mode)

                    except Exception as e:
                        print(f"Error en upload de {size} bytes: {str(e)}")
                        continue

            # Calcular velocidad promedio
            if speeds:
                return statistics.mean(speeds[-5:])  # Promedio de las últimas 5 mediciones
            return 0

        except Exception as e:
            print(f"Error en medición de {mode}: {str(e)}")
            return 0

    def test_speed(self):
        """Ejecuta la prueba de velocidad completa"""
        try:
            self.stop_button.config(state='normal')
            
            # Encontrar mejor servidor
            server, ping = self.get_best_server()
            if not server or self.stop_test:
                if not self.stop_test:  # Solo mostrar error si no fue detenido manualmente
                    self.update_status("No se encontró servidor", '#ff0000')
                return
            
            self.ping_label.config(text=f"{ping:.0f}")
            
            # Test de descarga
            if not self.stop_test:
                self.update_status("Midiendo velocidad de descarga...")
                self.progress['value'] = 0
                download_speed = self.measure_speed(server, 'download')
                if download_speed > 0:
                    self.download_label.config(text=f"{download_speed:.1f}")
            
            # Test de subida
            if not self.stop_test:
                self.update_status("Midiendo velocidad de subida...")
                self.progress['value'] = 0
                upload_speed = self.measure_speed(server, 'upload')
                if upload_speed > 0:
                    self.upload_label.config(text=f"{upload_speed:.1f}")
            
            if not self.stop_test:
                self.update_status("Test completado", '#00ff00')
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", '#ff0000')
            print(f"Error en test_speed: {str(e)}")
        finally:
            self.is_testing = False
            self.stop_test = False
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            self.progress['value'] = 0

    def start_test(self):
        if not self.is_testing:
            self.is_testing = True
            self.stop_test = False
            self.start_button.config(state='disabled')  # Solo cambiar el estado
            self.stop_button.config(state='normal')
            self.reset_display()
            threading.Thread(target=self.test_speed, daemon=True).start()

    def stop_current_test(self):
        """Detiene la prueba actual de manera segura"""
        self.stop_test = True
        self.update_status("Deteniendo prueba...", '#ffff00')
        self.stop_button.config(state='disabled')

    def reset_display(self):
        self.speed_label.config(text="0")
        self.ping_label.config(text="--")
        self.download_label.config(text="--")
        self.upload_label.config(text="--")
        self.progress['value'] = 0
        self.update_status("Iniciando test...")

    def update_status(self, message, color='#00ff00'):
        self.status_label.config(text=message, fg=color)
        self.root.update()

    def update_speed(self, speed, mode):
        """Actualiza las etiquetas de velocidad"""
        # Limitar la velocidad máxima mostrada a 1000 Mbps
        speed = min(speed, 1000)

        if mode == 'download':
            self.download_label.config(text=f"{speed:.1f}")
        else:
            self.upload_label.config(text=f"{speed:.1f}")
        self.speed_label.config(text=f"{speed:.1f}")

        # Actualizar color según la velocidad
        if speed < 10:
            color = '#ff0000'  # Rojo para velocidades bajas
        elif speed < 50:
            color = '#ffff00'  # Amarillo para velocidades medias
        else:
            color = '#00ff00'  # Verde para velocidades altas
        self.speed_label.config(fg=color)

    def update_speed_display(self, speed):
        """Actualizar display de velocidad"""
        if speed < 1:
            self.speed_label.configure(text=f"{speed*1000:.1f} Kbps")
        else:
            self.speed_label.configure(text=f"{speed:.1f} Mbps")

    def measure_speed(self, url, size_mb):
        """Medir velocidad de descarga con mayor precisión"""
        try:
            start_time = time.time()
            received_size = 0
            
            response = self.session.get(
                url,
                stream=True,
                timeout=self.PING_TIMEOUT
            )
            
            if response.status_code != 200:
                return 0
            
            for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                if self.stop_test:
                    return 0
                
                if chunk:
                    received_size += len(chunk)
                    elapsed_time = time.time() - start_time
                    
                    if elapsed_time > 0:
                        # Calcular velocidad en Mbps
                        current_speed = (received_size * 8) / (elapsed_time * 1000000)
                        self.update_speed_display(current_speed)
                    
                    # Actualizar barra de progreso
                    progress = (received_size / (size_mb * 1024 * 1024)) * 100
                    self.progress['value'] = min(progress, 100)
                
            total_time = time.time() - start_time
            if total_time > 0:
                return (received_size * 8) / (total_time * 1000000)
            return 0
        
        except Exception as e:
            print(f"Error en medición: {str(e)}")
            return 0

    def setup_servers(self):
        """Configurar lista de servidores optimizada para Ecuador"""
        self.servers = [
            {
                "url": "https://speedtest-gye.netlife.ec",  # Servidor principal Netlife [[1]](https://www.ookla.com/research/reports/ecuador-speedtest-connectivity-report-h2-2024)
                "name": "Netlife Ecuador",
                "location": "Guayaquil"
            },
            {
                "url": "https://speedtest-uio.netlife.ec",
                "name": "Netlife Ecuador",
                "location": "Quito"
            },
            {
                "url": "https://speedtest.cnt.net.ec",
                "name": "CNT Ecuador",
                "location": "Quito"
            },
            {
                "url": "https://speedtest-gye.puntonet.ec",
                "name": "PuntoNet",
                "location": "Guayaquil"
            },
            {
                "url": "https://speedtest.telconet.ec",
                "name": "Telconet",
                "location": "Guayaquil"
            },
            {
                "url": "https://speedtest-quito.claro.com.ec",
                "name": "Claro Ecuador",
                "location": "Quito"
            },
            {
                "url": "https://speedtest-lima.claro.com.pe",
                "name": "Claro Perú",
                "location": "Lima"
            },
            {
                "url": "https://mia.speedtest.net",
                "name": "Speedtest.net",
                "location": "Miami"
            }
        ]
        
        # Test files estandarizados de Ookla
        self.test_files = [
            "random350x350.jpg",    # ~100KB
            "random500x500.jpg",    # ~200KB
            "random1500x1500.jpg",  # ~1MB
            "random2000x2000.jpg",  # ~2MB
            "random4000x4000.jpg"   # ~8MB
        ]

        # Configuración de timeouts
        self.session.timeout = (3, 10)  # (connect timeout, read timeout)

    def __init__(self, root):
        super().__init__(root)
        self.root = root

        # Configuraciones básicas
        self.PING_TIMEOUT = 3.0
        self.MAX_RETRIES = 3
        self.PING_SAMPLES = 3
        self.is_testing = False

        # Configuración de la sesión HTTP
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*'
        })

        self.stop_test = False
        self.create_widgets()
        self.pack(expand=True, fill='both')
    
    # Configuraciones optimizadas basadas en datos de 2024
        self.PING_TIMEOUT = 2.0  # Reducido para mejor respuesta
        self.MAX_RETRIES = 3
        self.PING_SAMPLES = 5  # Aumentado para mayor precisión
        self.CHUNK_SIZE = 16384  # Optimizado para conexiones más rápidas (16KB)
    
    # Umbrales de velocidad actualizados para Ecuador
        self.SPEED_THRESHOLDS = {
            'low': 10,    # Mbps - Rojo
            'medium': 50,  # Mbps - Amarillo
            'high': 100   # Mbps - Verde
        }


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Speed Test")
    root.configure(bg='#141526')
    root.minsize(400, 600)
    app = SpeedTest(root)
    root.mainloop()