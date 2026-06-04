# Guia de trabajo para Jhon Polo

Esta guia esta pensada para que Jhon pueda trabajar con Claude o ChatGPT web copiando prompts. La idea es que haga 10 commits reales de frontend, sin tocar secretos, backend ni despliegue.

## Antes de empezar

1. Abrir el proyecto en el IDE.
2. Cambiar a la rama de frontend o crear una rama propia desde ella:

```powershell
git checkout develop-frontend-design
git checkout -b jhon-frontend-polish
```

3. Entrar al frontend:

```powershell
cd frontend
npm install
npm run dev
```

4. Abrir:

```txt
http://127.0.0.1:5173
```

5. Antes de cada prompt, copiarle a la IA estos archivos si los pide:

- `frontend/src/App.vue`
- `frontend/src/components/AppShell.vue`
- `frontend/src/components/AppHeader.vue`
- `frontend/src/components/AuthPanel.vue`
- `frontend/src/components/InventoryPanel.vue`
- `frontend/src/components/RecipeGenerator.vue`
- `frontend/src/components/RecipeHistoryPanel.vue`
- `frontend/src/components/BaseModal.vue`
- `frontend/src/services/api.ts`
- `frontend/src/styles/main.css`
- `frontend/src/styles/shell.css`
- `frontend/src/styles/auth.css`
- `frontend/src/styles/inventory.css`
- `frontend/src/styles/recipe.css`
- `frontend/src/styles/modal.css`

Regla importante: no modificar `.env`, `.env.example`, backend, Docker ni carpetas `.agents`.

## Commit 1: empty state del inventario

Nombre del commit:

```txt
feat(frontend): improve inventory empty state
```

Prompt para copiar:

```txt
Estoy trabajando en un frontend Vue + Vite + TypeScript para una app de recetas con inventario. Necesito mejorar solamente el empty state del inventario.

Objetivo:
- Cuando no haya ingredientes, mostrar un bloque visual claro y bonito.
- Debe tener titulo corto, texto de ayuda y boton para agregar ingrediente.
- Debe verse bien en mobile de 360px.
- No cambies el API client.
- No cambies endpoints.
- No cambies la logica de autenticacion.
- Mantener el estilo existente: culinario premium, botones redondos, UI limpia.

Archivos permitidos:
- frontend/src/components/InventoryPanel.vue
- frontend/src/styles/inventory.css

Entregame el codigo completo de los archivos que cambies.
```

Criterios para revisar:

- Si la lista esta vacia se ve un bloque agradable.
- El boton abre el modal de agregar ingrediente.
- No hay texto desbordado en mobile.

## Commit 2: componentes base visuales

Nombre del commit:

```txt
feat(frontend): add reusable base UI components
```

Prompt para copiar:

```txt
Necesito crear componentes reutilizables visuales para el frontend Vue + Vite.

Objetivo:
- Crear BaseButton, BaseInput y BaseCard.
- Usarlos para reemplazar duplicacion visual evidente.
- No cambiar logica de negocio.
- No cambiar llamadas al API.
- Mantener TypeScript y estilo actual.
- Los botones deben conservar apariencia redonda y estados hover/active.

Archivos permitidos:
- frontend/src/components/BaseButton.vue
- frontend/src/components/BaseInput.vue
- frontend/src/components/BaseCard.vue
- componentes existentes solo si hace falta reemplazar markup visual
- archivos CSS existentes o uno nuevo si es necesario

Entregame codigo completo de cada archivo creado o editado.
```

Criterios para revisar:

- La app compila.
- Los formularios siguen funcionando.
- Los componentes son simples y reutilizables.

## Commit 3: filtros de historial

Nombre del commit:

```txt
feat(frontend): add recipe history filters
```

Prompt para copiar:

```txt
Quiero agregar filtros visuales al historial de recetas en Vue.

Objetivo:
- Agregar busqueda por nombre de receta.
- Agregar filtro por dificultad: todas, facil, media, dificil.
- El filtrado debe ser solo frontend sobre las recetas ya cargadas.
- No crear endpoints.
- No tocar API client.
- Mantener la UI responsive y limpia.

Archivos permitidos:
- frontend/src/components/RecipeHistoryPanel.vue
- frontend/src/styles/recipe.css

Entregame codigo completo de los archivos modificados.
```

Criterios para revisar:

- Buscar por texto filtra tarjetas.
- Cambiar dificultad filtra sin pedir datos al backend.
- Si no hay resultados, aparece mensaje claro.

## Commit 4: modal de detalle de receta

Nombre del commit:

```txt
feat(frontend): improve recipe detail modal
```

Prompt para copiar:

```txt
Necesito mejorar el modal de detalle de receta usando el modal existente.

Objetivo:
- Al abrir una receta, mostrar secciones claras: ingredientes, pasos, tiempo y dificultad.
- Usar el componente BaseModal existente.
- No instalar librerias nuevas.
- No cambiar endpoints.
- Debe verse bien en desktop y mobile.
- El contenido largo no debe desbordar el modal.

Archivos permitidos:
- frontend/src/components/RecipeHistoryPanel.vue
- frontend/src/components/BaseModal.vue solo si es estrictamente necesario
- frontend/src/styles/recipe.css
- frontend/src/styles/modal.css

Entregame codigo completo de los archivos editados.
```

Criterios para revisar:

- Se puede abrir y cerrar el modal.
- Escape/click afuera siguen funcionando si ya existian.
- Los pasos se leen ordenados.

## Commit 5: skeleton loaders

Nombre del commit:

```txt
feat(frontend): add skeleton loading states
```

Prompt para copiar:

```txt
Quiero agregar skeleton loaders al frontend.

Objetivo:
- Skeleton para inventario mientras carga.
- Skeleton para historial mientras carga.
- Estado visual especial mientras se genera receta.
- No usar spinners genericos.
- Respetar prefers-reduced-motion.
- No cambiar endpoints ni API client.

Archivos permitidos:
- frontend/src/components/InventoryPanel.vue
- frontend/src/components/RecipeGenerator.vue
- frontend/src/components/RecipeHistoryPanel.vue
- frontend/src/styles/inventory.css
- frontend/src/styles/recipe.css
- frontend/src/styles/main.css si hace falta

Entregame codigo completo de los archivos modificados.
```

Criterios para revisar:

- Se ven placeholders antes de los datos.
- La generacion de receta comunica progreso.
- No hay saltos bruscos de layout.

## Commit 6: mensajes de exito/error

Nombre del commit:

```txt
feat(frontend): add inline feedback messages
```

Prompt para copiar:

```txt
Necesito mejorar mensajes de exito y error en el frontend.

Objetivo:
- Mostrar mensajes claros al crear, editar, eliminar y calificar.
- Pueden ser mensajes inline o toasts simples.
- No agregar una libreria pesada.
- Los mensajes deben desaparecer o poder cerrarse.
- No cambiar endpoints.
- Mantener accesibilidad basica con aria-live cuando aplique.

Archivos permitidos:
- componentes donde ocurren acciones
- frontend/src/styles/main.css
- frontend/src/styles/inventory.css
- frontend/src/styles/recipe.css

Entregame codigo completo de los archivos modificados.
```

Criterios para revisar:

- Si una accion sale bien, se entiende.
- Si falla, se muestra el error.
- El mensaje no tapa botones importantes.

## Commit 7: responsive mobile

Nombre del commit:

```txt
style(frontend): polish mobile responsive layout
```

Prompt para copiar:

```txt
Necesito pulir el responsive mobile del frontend Vue.

Objetivo:
- Revisar header, formularios, cards de recetas y modales.
- Debe funcionar sin desbordes a 360px de ancho.
- No cambiar logica.
- No cambiar endpoints.
- Ajustar CSS con media queries donde haga falta.
- Mantener botones legibles y comodos.

Archivos permitidos:
- frontend/src/styles/*.css
- componentes Vue solo si el markup actual impide responsive correcto

Entregame codigo completo de los archivos editados.
```

Criterios para revisar:

- Probar ancho 360px.
- No hay scroll horizontal.
- Modales caben en pantalla.

## Commit 8: perfil simple

Nombre del commit:

```txt
feat(frontend): add simple profile section
```

Prompt para copiar:

```txt
Quiero agregar una seccion simple de perfil.

Objetivo:
- Mostrar nombre/email si estan disponibles en la sesion o token.
- Mostrar boton de cerrar sesion.
- No crear endpoints nuevos.
- Si no hay datos del usuario, mostrar estado simple tipo "Sesion activa".
- Mantener diseno consistente.

Archivos permitidos:
- frontend/src/components/AppShell.vue
- frontend/src/components/AppHeader.vue
- frontend/src/composables/useAuthSession.ts si hace falta
- frontend/src/styles/shell.css

Entregame codigo completo de los archivos modificados.
```

Criterios para revisar:

- El usuario puede ver una seccion de perfil.
- El logout sigue funcionando.
- No rompe login ni registro.

## Commit 9: microinteracciones de botones

Nombre del commit:

```txt
style(frontend): add button microinteractions
```

Prompt para copiar:

```txt
Necesito agregar microinteracciones a los botones.

Objetivo:
- Hover solo en dispositivos con hover real.
- Active scale suave.
- Transiciones de 100ms a 160ms.
- Respetar prefers-reduced-motion.
- No cambiar logica ni textos.
- No exagerar animaciones.

Archivos permitidos:
- frontend/src/styles/main.css
- frontend/src/styles/shell.css
- frontend/src/styles/auth.css
- frontend/src/styles/inventory.css
- frontend/src/styles/recipe.css
- frontend/src/styles/modal.css

Entregame codigo completo de los archivos editados.
```

Criterios para revisar:

- Botones se sienten mas vivos.
- Reduced motion elimina movimiento innecesario.
- No hay cambios de layout al hover.

## Commit 10: lista de capturas para PDF

Nombre del commit:

```txt
docs(frontend): document screenshots for final report
```

Prompt para copiar:

```txt
Necesito preparar una lista clara de capturas para el PDF final.

Objetivo:
- Agregar en frontend/README.md una seccion llamada "Capturas para el PDF".
- Incluir capturas necesarias: login, registro, inventario, modal de ingrediente, receta generada, historial, calificacion y responsive mobile.
- Para cada captura, decir que debe mostrarse.
- No cambiar codigo funcional.

Archivo permitido:
- frontend/README.md

Entregame el README completo actualizado.
```

Criterios para revisar:

- El README explica exactamente que capturar.
- Sirve para armar el PDF final.

## Despues de cada tarea

Ejecutar:

```powershell
npm run build
git status
git add frontend
git commit -m "mensaje-del-commit"
```

Si `npm run build` falla, copiar el error completo a la IA y pedirle:

```txt
Este error salio al correr npm run build. Corrige solo lo necesario, no cambies funcionalidades no relacionadas.
```
