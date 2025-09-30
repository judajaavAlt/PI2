# Manual de Usuario

## Introducción

Esta aplicación de gestión de hábitos te ayuda a crear, seguir y mejorar tus hábitos diarios de forma sencilla. Está diseñada para que cualquier persona pueda usarla, sin importar si tiene conocimientos técnicos o no.

## Requisitos previos

- **Sistema operativo:** Windows, macOS o Linux.
- **Python 3** instalado en tu computadora.
- **Conexión a internet** para descargar la aplicación y sus dependencias.

## Instalación

1. Descarga el proyecto desde GitHub.
2. Abre la carpeta del proyecto en tu computadora.
3. Instala las dependencias necesarias:
   - Abre una terminal y ejecuta:
     ```powershell
     pip install -r requirements.txt
     ```

## Ejecución

1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta el siguiente comando:
   ```powershell
   python main.py
   ```
3. Se abrirá la ventana principal de la aplicación.

## Uso básico

### Registrar un nuevo hábito
- Haz clic en el botón "Agregar hábito".
- Escribe el nombre y la descripción del hábito.
- Selecciona la frecuencia y guarda.

### Marcar hábito como realizado
- Busca el hábito en la lista principal.
- Haz clic en el botón para marcarlo como hecho ese día.

### Ver progreso y rachas
- En la pantalla principal, puedes ver cuántos días seguidos has cumplido cada hábito.

### Editar o eliminar hábitos
- Selecciona el hábito que deseas modificar.
- Haz clic en "Editar" para cambiar los detalles o en "Eliminar" para borrarlo.

### Personalizar preferencias
- Accede al menú de configuración para ajustar tus preferencias de usuario.

## Resolución de problemas comunes

- **No se abre la aplicación:**
  - Verifica que tienes Python 3 instalado.
  - Asegúrate de haber instalado las dependencias con `pip install -r requirements.txt`.

- **Error al instalar dependencias:**
  - Revisa que tienes conexión a internet.
  - Intenta ejecutar el comando como administrador.

- **La interfaz no se muestra correctamente:**
  - Verifica que PySide6 está instalado correctamente.
  - Reinstala las dependencias si es necesario.

---

Si tienes dudas o problemas que no aparecen aquí, puedes consultar la sección de Issues en GitHub o contactar al equipo de desarrollo.

¡Esperamos que disfrutes usando la aplicación y que te ayude a mejorar tus hábitos!
