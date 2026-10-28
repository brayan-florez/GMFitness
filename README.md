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
- `membresias/`: planes por sede, beneficios, precios por periodo e historial de membresías.
- `pagos/`: pagos y recibos internos asociados a una membresía.
- `citas/`: disponibilidades de fisioterapia y reservas de clientes.
- Las apps separan los dominios; las entidades nuevas quedan gestionables desde el administrador de Django y sus modelos/migraciones viven en la app correspondiente.
- `gimnasios/templates/base.html` contiene la estructura y navegación compartidas por las páginas.

Las dietas y rutinas oficiales se guardan en la base de datos. Las propuestas personales que el cliente cree en su navegador no se guardan en el servidor por ahora. La aprobación de pagos disponible en el administrador es una simulación interna y emite un recibo; no integra una pasarela bancaria.

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
