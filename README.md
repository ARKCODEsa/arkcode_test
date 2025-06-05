``` markdown
# Aplicación Speed Test

Una aplicación de prueba de velocidad de Internet desarrollada en Python con interfaz gráfica. Esta aplicación mide la velocidad de descarga, subida y ping a varios servidores en Ecuador y regiones cercanas.

## Características

- **Pruebas de Velocidad en Tiempo Real**: Mide velocidades de descarga y subida en Mbps
- **Pruebas de Ping**: Verifica la latencia a múltiples servidores
- **Selección de Servidor**: Selecciona automáticamente el mejor servidor basado en ping y fiabilidad
- **Retroalimentación Visual**: 
  - Indicadores de velocidad por colores
  - Barra de progreso durante las pruebas
  - Actualizaciones de estado en tiempo real
- **Controles de Usuario**: 
  - Funcionalidad de Inicio/Detención
  - Visualización clara de resultados

## Requisitos

- Python 3.x
- Paquetes Python requeridos:
  - `tkinter`
  - `requests`
  - `urllib3`
  - `threading`
  - `statistics`

## Instalación

1. Clona este repositorio o descarga el código fuente
2. Instala los paquetes requeridos:
```
bash pip install requests urllib3
``` 

## Uso

Ejecuta la aplicación usando Python:
```
bash python speedtest.py
``` 

### Cómo Usar la Aplicación

1. Inicia la aplicación
2. Haz clic en "INICIAR TEST" para comenzar la prueba
3. La aplicación:
   - Encontrará el mejor servidor
   - Probará el ping
   - Medirá la velocidad de descarga
   - Medirá la velocidad de subida
4. Los resultados se mostrarán en tiempo real
5. Usa el botón "DETENER" para parar la prueba en cualquier momento

## Umbrales de Velocidad

La aplicación utiliza los siguientes umbrales de velocidad:
- Bajo (Rojo): < 10 Mbps
- Medio (Amarillo): 10-50 Mbps
- Alto (Verde): > 50 Mbps

## Cobertura de Servidores

Incluye servidores de múltiples proveedores en Ecuador:
- Netlife Ecuador
- CNT Ecuador
- PuntoNet
- Telconet
- Claro Ecuador
Y servidores de respaldo en:
- Perú (Lima)
- EE.UU. (Miami)

## Detalles Técnicos

- Utiliza múltiples tamaños de archivo de prueba para mediciones precisas
- Implementa manejo de errores y gestión de tiempos de espera
- Soporta conexiones seguras y no seguras
- Tamaños de fragmentos configurables para un rendimiento óptimo
- Implementación segura para hilos con respuesta UI fluida

## Licencia

[Agregar información de licencia aquí]

## Contribuir

[Agregar pautas de contribución si aplica]
```
