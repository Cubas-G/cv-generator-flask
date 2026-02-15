# CV Generator Flask

Este proyecto es una aplicación web construida con Flask que permite a los usuarios registrarse, iniciar sesión y generar Curriculums Vitae (CVs) de manera sencilla. Los usuarios pueden crear, ver, editar y eliminar sus CVs desde un panel de control.

## Características

*   **Autenticación de Usuarios**: Registro, inicio de sesión y cierre de sesión seguros.
*   **Panel de Control (Dashboard)**: Vista principal para usuarios autenticados.
*   **Gestión de CVs**:
    *   **Crear**: Formulario completo para ingresar datos personales, experiencia, educación, habilidades, etc.
    *   **Listar**: Ver todos los CVs creados por el usuario.
    *   **Ver**: Visualizar un CV específico en un formato de plantilla.
    *   **Editar**: Modificar la información de un CV existente.
    *   **Eliminar**: Borrar CVs que ya no se necesiten.
*   **Base de Datos**: Utiliza SQLite para almacenar usuarios y CVs.

## Estructura del Proyecto

*   `app.py`: Archivo principal de la aplicación Flask. Contiene la configuración, modelos de base de datos y rutas.
*   `init_db.py`: Script para inicializar la base de datos (crear tablas).
*   `requirements.txt`: Lista de dependencias del proyecto.
*   `templates/`: Directorio que contiene las plantillas HTML (vistas).
    *   `register.html`, `login.html`: Vistas de autenticación.
    *   `dashboard.html`: Panel principal.
    *   `form.html`: Formulario para crear CV (y página de inicio).
    *   `cv_template.html`: Plantilla para visualizar el CV generado.
    *   `mis_cvs.html`: Lista de CVs del usuario.
    *   `editar_cv.html`: Formulario para editar CV.
*   `static/`: Directorio para archivos estáticos (CSS, JS, imágenes).
*   `instance/`: Directorio donde se almacena la base de datos SQLite (`database.db`).

## Requisitos Previos

*   Python 3.x instalado.
*   pip (gestor de paquetes de Python).

## Instalación y Ejecución

Sigue estos pasos para levantar el proyecto en tu máquina local:

1.  **Clonar o descargar el proyecto**: Asegúrate de tener los archivos en tu equipo.

2.  **Crear un entorno virtual (Opcional pero recomendado)**:
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicializar la base de datos**:
    Ejecuta el script de inicialización para crear el archivo `database.db` y las tablas necesarias.
    ```bash
    python init_db.py
    ```

5.  **Ejecutar la aplicación**:
    ```bash
    python app.py
    ```

6.  **Acceder a la aplicación**:
    Abre tu navegador web y ve a `http://127.0.0.1:5000`.

## Uso

1.  **Registro**: Crea una cuenta nueva en la página de registro.
2.  **Login**: Inicia sesión con tus credenciales.
3.  **Dashboard**: Desde aquí puedes navegar a "Mis CVs" o crear uno nuevo.
4.  **Generar CV**: Rellena el formulario con tus datos y guarda.
5.  **Gestionar CVs**: En "Mis CVs" puedes ver, editar o eliminar tus creaciones.

## Tecnologías Utilizadas

*   **Flask**: Framework web ligero para Python.
*   **Flask-SQLAlchemy**: ORM para interactuar con la base de datos.
*   **Flask-Login**: Gestión de sesiones de usuario.
*   **SQLite**: Base de datos ligera basada en archivos.
*   **HTML/CSS**: Frontend (plantillas y estilos).
