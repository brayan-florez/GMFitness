# GMFitness

Aplicación web de gestión para un gimnasio, desarrollada con Django.

## Estructura

- `config/`: configuración general del proyecto y rutas principales.
- `gimnasios/`: sedes y página de inicio.
- `usuarios/`: usuarios y datos de acceso.
- `clientes/`: clientes, objetivos y mediciones.
- `profesionales/`: entrenadores, nutricionistas y fisioterapeutas.
- `entrenamientos/`: ejercicios y rutinas.
- `nutricion/`: alimentos y planes de alimentación.
- Cada app mantiene juntos los componentes que ya están implementados para su dominio: modelos, formularios, vistas, rutas, administración, migraciones y plantillas.
- `gimnasios/templates/base.html` contiene la estructura y navegación compartidas por las páginas.

Las apps se mantienen separadas por responsabilidad del dominio; las rutas principales las reúne `config/urls.py`, siguiendo el esquema de entrada de `sena`.

## Ejecución local

Activa el entorno virtual, instala las dependencias y ejecuta las migraciones y el servidor:

```bash
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` para entrar a la página principal.
