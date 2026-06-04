# Commits rapidos para Jhon Polo

Esta guia es para que Jhon pueda hacer commits propios desde VS Code aunque no tenga mucho tiempo. No requiere tocar backend, Docker ni archivos secretos.

## Configurar su identidad de Git en este repo

Solo Jhon debe ejecutar esto si el commit sera suyo:

```powershell
git config user.name "Jhon Polo"
git config user.email "roasebastian0714@gmail.com"
```

Verificar:

```powershell
git config user.name
git config user.email
```

Importante: GitHub no usa la password normal para hacer push. Si VS Code ya esta logueado con GitHub, normalmente basta con hacer **Sync Changes** o **Push** desde el panel Source Control.

## Rutina para cada commit

1. Hacer una tarea pequena.
2. Correr:

```powershell
cd frontend
npm run build
```

3. Volver a la raiz:

```powershell
cd ..
git status
```

4. Commit:

```powershell
git add frontend
git commit -m "mensaje del commit"
```

5. Subir:

```powershell
git push
```

## 10 tareas pequenas que Jhon puede hacer

### 1. Mejorar texto vacio del inventario

Archivo sugerido:

- `frontend/src/components/InventoryPanel.vue`

Cambio pequeno:

- Ajustar el texto cuando no hay ingredientes.
- No cambiar endpoints.

Commit:

```txt
style(frontend): improve inventory empty copy
```

### 2. Revisar responsive del header

Archivo sugerido:

- `frontend/src/styles/shell.css`

Cambio pequeno:

- Probar ancho 360px.
- Ajustar paddings si algun boton se ve apretado.

Commit:

```txt
style(frontend): tune mobile header spacing
```

### 3. Pulir skeleton del historial

Archivo sugerido:

- `frontend/src/components/RecipeHistoryPanel.vue`
- `frontend/src/styles/recipe.css`

Cambio pequeno:

- Hacer que los skeletons se vean como tarjetas reales.

Commit:

```txt
style(frontend): polish recipe history skeletons
```

### 4. Mejorar mensaje de receta generada

Archivo sugerido:

- `frontend/src/components/RecipeGenerator.vue`

Cambio pequeno:

- Ajustar el mensaje de exito cuando aparece una receta.

Commit:

```txt
style(frontend): refine generated recipe feedback
```

### 5. Agregar estado hover a tarjetas

Archivo sugerido:

- `frontend/src/styles/inventory.css`
- `frontend/src/styles/recipe.css`

Cambio pequeno:

- Hover solo dentro de `@media (hover: hover) and (pointer: fine)`.

Commit:

```txt
style(frontend): add card hover polish
```

### 6. Mejorar modal de ingrediente

Archivo sugerido:

- `frontend/src/components/InventoryPanel.vue`
- `frontend/src/styles/modal.css`

Cambio pequeno:

- Revisar labels, espaciado y botones del modal.

Commit:

```txt
style(frontend): polish ingredient modal
```

### 7. Mejorar pagina de perfil

Archivo sugerido:

- `frontend/src/pages/ProfilePage.vue`

Cambio pequeno:

- Hacer mas clara la tarjeta de perfil.
- No mostrar token completo.

Commit:

```txt
style(frontend): improve profile card readability
```

### 8. Mejorar pagina 404

Archivo sugerido:

- `frontend/src/pages/NotFoundPage.vue`

Cambio pequeno:

- Ajustar texto y boton de regreso.

Commit:

```txt
style(frontend): polish not found page
```

### 9. Revisar textos rotos

Archivos sugeridos:

- `frontend/src/**/*.vue`

Cambio pequeno:

- Buscar textos con caracteres raros de encoding.
- Cambiarlos por texto ASCII simple: `sesion`, `esta`, `atras`.

Commit:

```txt
chore(frontend): clean visible copy encoding
```

### 10. Documentar capturas para PDF

Archivo sugerido:

- `frontend/README.md`

Cambio pequeno:

- Agregar seccion con capturas necesarias: login, inventario, receta generada, historial, detalle, perfil y mobile.

Commit:

```txt
docs(frontend): list screenshots for final report
```

## Si algo falla

Si `npm run build` falla, copiar el error exacto a la IA y pedir:

```txt
Corrige este error de build sin cambiar funcionalidades no relacionadas.
```
