# cepal

## Correos de notificaciones de inventario

La edición de inventarios crea primero las notificaciones internas y envía sus
correos en segundo plano, sin hacer esperar al formulario. El envío utiliza el
timeout configurado mediante `EMAIL_TIMEOUT` y no se reintenta si falla.
