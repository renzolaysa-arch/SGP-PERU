# Correcciones de SGP de octubre de 2026

La rama contiene seis correcciones independientes sobre `main` (`2d1210b`). No incluye la rama local de registro de sesiones ni cambios locales previos. Cada commit identifica un caso del documento de bugs del usuario.

| Caso | Comportamiento corregido |
| --- | --- |
| SGP-01 | Palabra clave busca en título o nombre de entidad proveedora, conservando el queryset y filtros originales. |
| SGP-02 | Preparación cuenta entregas únicas, explica cuáles faltan y no retrocede al consultar pantallas. Se pueden evaluar entregas preparadas mientras otras quedan pendientes. |
| SGP-03 | El registro guarda la cuenta antes del envío, comprueba el resultado y muestra el error de correo. Hay reenvío por POST, limitado a la sesión que creó la cuenta y a un intento por minuto. Incluye el trabajo revisado de la rama local de correo. |
| SGP-04 | Cada reemplazo de archivo conserva la versión anterior y registra autor y fecha de la nueva. El proveedor propietario, Unidad Central y funcionarios con acceso vigente pueden consultar el historial. |
| SGP-05 | Los cinco iframes de YouTube envían el origen mediante referrerpolicy, incluidos los modales. |
| SGP-06 | Vistas del tablero comprueban sesión y rol; una sesión vencida devuelve 401 al AJAX y provoca ingreso de la ventana completa. El estado de sección se guarda por usuario y se valida contra el menú vigente. |

## Validación realizada

Desde `sgp-peru/nginx/peru`, con las dependencias de la aplicación instaladas:

```sh
python -m pytest tests/regression users/tests notifications/tests --ds=cepal.settings.regression -q
```

La configuración `cepal.settings.regression` usa SQLite temporal y correo en memoria; no conecta con bases de producción. Se ejecutaron las pruebas también en un PostgreSQL local desechable, usando el esquema actual con `--nomigrations`: 40 pruebas pasaron. La suite incluye autenticación y rol del tablero, sesión invalidada, registro y reenvío, fallos SMTP simulados, entregas pendientes, preparaciones duplicadas, conservación y descarga de versiones y restricciones de acceso.

Se restauró además el respaldo local de 2025 en otra base PostgreSQL desechable y se ejecutó `migrate`: la actualización pasó y generó versiones iniciales para sus 35 archivos vigentes. Las bases de negocio no se modificaron. La nueva migración se comprueba además con una prueba de preservación idempotente.

La reconstrucción de todo el historial antiguo desde una base PostgreSQL vacía falla antes de las nuevas migraciones por un valor demasiado largo para varchar(25). También hay diferencias previas entre modelos y migraciones heredadas. Esta rama no reescribe ese historial: la actualización sobre el respaldo existente sí se validó. No ejecutar `makemigrations` ni usar `--fake` para eludir errores durante el despliegue.

La compilación de producción del frontend pasó con Webpack 4 y las dependencias locales existentes. Los archivos de `dist` siguen ignorados: se deben reconstruir en despliegue. La búsqueda por MINEDU y la consulta del historial con dos versiones se revisaron además en un navegador sobre una base local independiente.

## Actualización del servidor

1. Comparar la rama con el código realmente desplegado y probarla primero en una copia de preproducción. Este repositorio ya tenía correcciones anteriores a esta entrega.
2. Respaldar la base y el directorio de archivos cargados. Conservar la configuración privada del servidor fuera de Git.
3. Instalar las dependencias del proyecto en su entorno Python existente. No reemplazar las credenciales o el dominio del servidor con valores locales.
4. Revisar el plan de migración con los ajustes reales de Perú:

```sh
cd sgp-peru/nginx/peru
python manage.py migrate --plan --settings=cepal.settings.cepal_pe
```

Las migraciones nuevas son `providers.0003_alter_providerentity_domain` (validación de formulario, sin SQL de estructura) e `inventory.0028_inventoryfileversion` (tabla de versiones y referencias iniciales). Si aparecen operaciones inesperadas, revisar antes de continuar. La migración del historial conserva las rutas de los archivos existentes y deja desconocidos autor y fecha históricos.

5. En la copia verificada, aplicar las migraciones:

```sh
python manage.py migrate --settings=cepal.settings.cepal_pe
```

6. Construir los estáticos con el entorno Node compatible con Webpack 4 del servidor:

```sh
cd cepal/static/cepal
npm ci
npm run build -- --watch=false
cd ../../..
python manage.py collectstatic --noinput --settings=cepal.settings.cepal_pe
```

Reiniciar los procesos de la aplicación según la operación del proveedor. El historial solo existe después de migrar y los cambios JavaScript solo se ven con el bundle reconstruido y publicado.

## Comprobaciones del proveedor

- Buscar MINEDU sin que figure en el título y combinar la búsqueda con otros filtros.
- En una solicitud con varias entregas, abrir evidencias y volver sin cambiar su avance. Comprobar la lista pendiente. Si se completan dos de tres, 66% sigue siendo correcto; solo tres de tres deben dar 100%.
- Revisar el caso histórico de la solicitud 275 sin marcar preparaciones automáticamente como finalizadas.
- Configurar remitente y SMTP. `EMAIL_USE_SSL` y `EMAIL_USE_TLS` son configurables y no deben activarse simultáneamente. El envío tiene el timeout configurado y el resto de notificaciones continúa en segundo plano. Un envío aceptado por SMTP no garantiza llegada a la bandeja; revisar también filtros y servicio de correo.
- Registrar un proveedor de dominio reconocido y otro pendiente de aprobación. Probar activación, un error SMTP y reenvío. La prueba SMTP real requiere un destinatario de prueba acordado.
- Ejecutar `python manage.py corregir_dominios --settings=cepal.settings.cepal_pe` para obtener solo un diagnóstico. La opción `--aplicar` cambia datos y no es necesaria para desplegar: debe revisarse por separado.
- Reemplazar un archivo de prueba y descargar ambas versiones. Revisar accesos entre proveedores y funcionarios. Los archivos desconectados antes de esta migración no se recuperan automáticamente.
- Probar YouTube en inicio, testimonios, noticias, contenido educativo y proyectos desde HTTPS. Revisar Referer y políticas del proxy, navegador y servidor. Disponibilidad del video y permisos de inserción en YouTube son verificaciones adicionales.
- Salir, volver, cambiar de cuenta, usar dos pestañas e invalidar una sesión de prueba. Un error 500 debe conservar su tratamiento de error y no ocultarse como sesión vencida.

## Reversión

Revertir un cambio de código es distinto de eliminar el historial. Si se revierte la aplicación, conservar la tabla de versiones y los archivos hasta revisar la operación. Revertir la migración que crea la tabla elimina sus registros de versiones. No borrar archivos antiguos ni ejecutar scripts de reparación de datos como parte de esta entrega.

El servidor de producción no fue modificado. La recepción real del correo, reproducción de YouTube en el dominio final y validación de usuarios en preproducción quedan a cargo de la revisión de despliegue antes de publicar los cambios allí.
