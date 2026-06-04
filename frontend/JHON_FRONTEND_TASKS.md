# Tareas sugeridas para Jhon Polo

Cada tarea está pensada para un commit descriptivo y pequeño dentro de `frontend/`.

1. En `frontend`, mejora el empty state del inventario con un bloque visual claro, sin cambiar el API client. Debe mostrar una llamada a agregar ingrediente y verse bien en mobile.
2. Crea componentes reutilizables `BaseButton`, `BaseInput` y `BaseCard` siguiendo los estilos existentes. No cambies lógica, solo reemplaza duplicación visual.
3. Agrega filtros visuales al historial de recetas por dificultad y búsqueda por nombre, todo en frontend sobre los datos ya cargados.
4. Mejora el modal de detalle de receta con secciones para ingredientes, pasos, tiempo y dificultad. Debe usar el modal existente.
5. Agrega skeleton loaders para inventario, generación de receta e historial, sin usar spinners genéricos.
6. Agrega toasts o mensajes inline para éxito/error en crear, editar, eliminar y calificar.
7. Pule responsive mobile: header, formularios, cards de recetas y modales no deben desbordarse en 360px.
8. Agrega una pantalla o sección de perfil simple que muestre nombre/email si están disponibles y botón de cerrar sesión.
9. Agrega microinteracciones de botón: active scale, hover solo en desktop y reduced motion.
10. Prepara capturas de frontend para el PDF: inventario, receta generada, historial y login. Deja una lista en README con qué capturar.
