# Requerimientos y Diseño: Optimización de Eliminación de Catálogo y Desbloqueo de Borradores Incompletos

**Fecha:** 2026-11-04  
**Ticket Origen:** `[Catalog Import] Timeout 504 al borrar catálogo y bloqueo de selección en incompletos`  
**Repositorio Afectado:** `Proyecto/growthhacking.PrototypeZero/`  

---

## 1. Resumen Ejecutivo y Objetivos

El módulo de importación de catálogos mediante extracción asistida por IA presenta dos fallas críticas que degradan la experiencia del usuario e impiden la operación normal de la tienda:

1. **Timeout 504 y Rollback al eliminar catálogo activo**: Al intentar eliminar un catálogo con volumen medio/alto de productos (ej. 200 borradores y ~180 imágenes asociadas), la petición `DELETE /api/core/store/catalog-import/active-catalog` tarda más de 100 segundos. El API Gateway corta la conexión respondiendo `504 Gateway Timeout`. Dado que la operación en el backend corre en un `UnitOfWork` transaccional de ABP Framework, la transacción se cancela y revierte (`rollback`), dejando la base de datos intacta (no se borra ningún borrador ni se reinicia el catálogo).
2. **Imposibilidad de seleccionar o eliminar borradores incompletos**: En la tabla de revisión de borradores (`catalog-import.component.html`), el checkbox de selección de cada fila tiene la directiva `[disabled]="!canPublish(row)"`. Cuando un producto extraído está en estado `Incomplete` (por falta de datos obligatorios), el checkbox queda deshabilitado. Debido a que en la grilla no existe un botón individual de eliminación en la columna de acciones (solo existe "Editar"), los borradores incompletos quedan atrapados indefinidamente sin posibilidad de borrarse individualmente ni en lote.

El objetivo de este ticket es:
- Optimizar la rutina de eliminación de blobs y descuento de cuota en el backend para que la eliminación de un catálogo con más de 200 productos e imágenes se ejecute en pocos segundos sin superar los timeouts del gateway.
- Liberar el selector de selección en la interfaz de Angular para permitir que cualquier borrador pueda ser seleccionado y eliminado, restringiendo la validación de `canPublish` exclusivamente al botón de publicación.

---

## 2. Personas y Actores

- **Usuario Final / Rol**: Administrador de Tienda / Operador de Catálogo (importa catálogos PDF/imágenes, revisa borradores y descarta productos no deseados o incompletos).
- **Equipo Interno**:
  - **Tech Lead**: Santiago (Pevaar) / David
  - **QA Asignado**: Laura (QA Engineer)
  - **DevOps**: Sofía (Cloud/DevOps)

---

## 3. Criterios de Aceptación (Gherkin / Given-When-Then)

### Escenario 1: Eliminación rápida y exitosa del catálogo activo con muchas imágenes
- **Dado** un catálogo activo con 200+ borradores y 180+ imágenes almacenadas en Azure Blob Storage.
- **Cuando** el usuario solicita eliminar el catálogo activo (`DELETE /api/core/store/catalog-import/active-catalog`).
- **Entonces** la operación se completa en menos de 10 segundos sin producir error 504 Gateway Timeout.
- **Y** todos los borradores asociados se eliminan de la base de datos (`Store.CatalogProductDrafts`).
- **Y** los blobs de imágenes correspondientes se eliminan en Azure Blob Storage.
- **Y** la cuota de almacenamiento se actualiza consistentemente.
- **Y** el estado del catálogo en `Store.CatalogImports` pasa a `Idle`.

### Escenario 2: Selección y eliminación de borradores incompletos en la tabla
- **Dado** uno o más borradores en la tabla con estado `Incomplete`.
- **Cuando** el usuario visualiza la tabla de revisión de catálogo.
- **Entonces** las casillas de verificación (checkbox) de los borradores incompletos están habilitadas e interactivas.
- **Y** el usuario puede marcar la casilla individual de un borrador incompleto o usar "Seleccionar todos".
- **Y** al pulsar "Eliminar seleccionados", los borradores seleccionados (incluyendo los incompletos) se eliminan exitosamente de la base de datos y de la grilla.

### Escenario 3: Protección del botón de publicación contra borradores incompletos
- **Dado** que el usuario selecciona uno o más borradores donde al menos uno tiene estado `Incomplete`.
- **Cuando** se actualiza la selección en la tabla.
- **Entonces** el botón "Publicar seleccionados" permanece deshabilitado (o muestra advertencia impidiendo la acción).
- **Y** el botón "Eliminar seleccionados" permanece habilitado permitiendo descartarlos.

---

## 4. Alcance Técnico

### En Alcance (In Scope):
1. **Backend (`services/core/PrototypeZero.CoreService`)**:
   - `Store/CatalogImport/StoreCatalogBlobService.cs`:
     - Implementar método para eliminación en paralelo de blobs (`DeleteManyAsync` / `DeleteBlobsAsync`) con `Parallel.ForEachAsync` y concurrencia controlada (`MaxDegreeOfParallelism`).
     - Optimizar la consulta de tamaño y llamada a `quotaService.RemoveUsedAsync`: acumular el total de bytes eliminados y ejecutar una única llamada consolidada al servicio de cuota, o evitar llamadas redundantes de `Exists` y `GetProperties` antes de `DeleteIfExistsAsync`.
   - `Store/CatalogImport/CatalogImportAppService.cs`:
     - Refactorizar `DeleteActiveCatalogAsync` para utilizar la eliminación paralela de blobs de imágenes.
     - Refactorizar `DeleteDraftsAsync` para optimizar la verificación de referencias y la eliminación masiva concurrente de blobs asociados a borradores eliminados.
   - Pruebas unitarias y de integración en `services/core/PrototypeZero.CoreService.Tests`.

2. **Frontend (`apps/angular`)**:
   - `apps/angular/src/app/store/catalog-import/catalog-import.component.html`:
     - Quitar `[disabled]="!canPublish(row)"` del `<input type="checkbox">` de fila.
     - Ajustar el checkbox de cabecera ("Seleccionar todos") para permitir seleccionar todos los borradores visibles.
     - Condicionar la habilitación de "Publicar seleccionados" para que solo esté activo si todos los elementos seleccionados son publicables (`canPublish`).
   - `apps/angular/src/app/store/catalog-import/catalog-import.component.ts`:
     - Actualizar `toggleSelectAll(checked)` para seleccionar o deseleccionar todos los borradores de la página.
     - Crear señal computada `canPublishSelected` o actualizar `allPublishableSelected` para gobernar el botón de publicación.
     - Pruebas unitarias en `catalog-import.component.spec.ts`.

### Fuera de Alcance (Out of Scope):
- Modificaciones en la arquitectura del microservicio `FileManagementService` (el contrato de integración existente `ICatalogStorageQuotaIntegrationService` se conserva intacto).
- Modificaciones al pipeline de extracción con IA en `AiService`.

---

## 5. Coordinación de Equipo y Delegaciones

- **Handoff a QA (Laura)**:
  - Cargar un catálogo de prueba con 200+ productos e imágenes.
  - Verificar que al presionar "Eliminar catálogo activo", la respuesta HTTP sea 200/204 en pocos segundos y la pantalla regrese a estado inicial `Idle`.
  - Probar un catálogo con productos en estado `Incomplete` (sin precio o sin categoría).
  - Verificar que las casillas de los incompletos puedan marcarse individualmente y con "Seleccionar todos".
  - Verificar que al seleccionar un incompleto, el botón "Eliminar seleccionados" esté activo y los borre correctamente, mientras que el botón "Publicar seleccionados" permanezca deshabilitado.

- **Handoff a DevOps (Sofía)**:
  - Sin cambios en variables de entorno, Azure Key Vault ni configuración de infraestructura.
  - La mejora reduce la carga sobre Azure Blob Storage y evita colapsar los límites de timeout en el API Gateway (YARP / Reverse Proxy).

---

## 6. Próximo Paso

Para generar el TRD (Documento de Requerimientos Técnicos) y la especificación de pruebas:
Arrastra al chat:
`@commands/2-create-trd.md tasks/task-catalog-import-delete-fix/design-catalog-import-delete-fix.md`
