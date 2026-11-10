# Zoom de Imagen en Detalle de Producto del Catálogo - Task Index

**Location**: `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/`  
**Total Tasks**: 3 (1 Setup + 1 RED + 1 GREEN+VERIFY)  
**Estimated Effort**: ~4 horas  

---

## Quick Start

### Prerequisites
1. Leer [`trd-product-image-zoom.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-product-image-zoom/trd-product-image-zoom.md) para el contexto técnico y arquitectónico.
2. Revisar [`test-spec-product-image-zoom.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-product-image-zoom/test-spec-product-image-zoom.md) para los escenarios de prueba Given-When-Then.
3. Asegurar que Node.js y Yarn estén listos para el proyecto Angular.

### Execution Order
Las tareas deben ejecutarse en orden estricto de TDD:
- **Task 01 (Setup)**: Verificación del entorno y archivos base.
- **Task 02 (RED)**: Escribir las pruebas unitarias que definen el contrato y comprobar que fallen inicialmente.
- **Task 03 (GREEN + VERIFY)**: Implementar la lógica, plantilla y estilos hasta que todas las pruebas pasen y la compilación sea limpia.

---

## Task Overview

| Task | Name | Phase | Size | Est. Hours | Dependencies | Agent |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | Scaffolding & Setup | Setup | S | 0.5h | None | angular-developer |
| **02** | Unit Tests Specification (RED) | RED | M | 1.5h | Task 01 | angular-developer |
| **03** | Zoom Implementation & Styles (GREEN) | GREEN+VERIFY | M | 2.0h | Task 02 | angular-developer |

---

## Progress Tracking

- [x] **Task 01**: Scaffolding & Setup de Entorno (`task01-setup.md`)
- [x] **Task 02**: Especificación y Escritura de Pruebas Unitarias RED (`task02-red.md`)
- [x] **Task 03**: Implementación y Estilos de Zoom GREEN + VERIFY (`task03-green.md`)

---

## Quality Gates

### 1. verify:quick (< 30s)
```bash
yarn --cwd Proyecto/growthhacking.PrototypeZero/apps/angular build
```

### 2. verify:tests (< 1m)
```bash
yarn --cwd Proyecto/growthhacking.PrototypeZero/apps/angular test --watch=false
```

---

## References

- **TRD:** [`trd-product-image-zoom.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-product-image-zoom/trd-product-image-zoom.md)
- **Test Spec:** [`test-spec-product-image-zoom.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-product-image-zoom/test-spec-product-image-zoom.md)
- **Design:** [`design-product-image-zoom.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-product-image-zoom/design-product-image-zoom.md)
