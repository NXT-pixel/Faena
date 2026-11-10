# Rediseño Responsive Móvil del Catálogo Storefront - Task Index

**Location:** `Proyecto/growthhacking.PrototypeZero/apps/angular/src/app/public/storefront/`  
**Total Tasks:** 3 (1 Setup + 1 RED + 1 GREEN+VERIFY)  
**Estimated Effort:** ~3.5 horas  

---

## Quick Start

### Prerequisites
1. Leer [`trd-mobile-storefront-responsive.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-mobile-storefront-responsive/trd-mobile-storefront-responsive.md) para el contexto técnico y arquitectónico.
2. Revisar [`test-spec-mobile-storefront-responsive.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-mobile-storefront-responsive/test-spec-mobile-storefront-responsive.md) para los escenarios de prueba Given-When-Then.
3. Asegurar que Node.js y Yarn estén disponibles para el proyecto Angular.

### Execution Order
Las tareas deben ejecutarse en orden estricto de TDD:
- **Task 01 (Setup)**: Estructura de señales reactivas y métodos en `storefront-catalog.component.ts`.
- **Task 02 (RED)**: Escribir las pruebas unitarias que definen el contrato y comprobar que fallen inicialmente.
- **Task 03 (GREEN + VERIFY)**: Implementar la plantilla HTML, los estilos SCSS responsive (Kyte style), verificar que pasen los tests y compilar con `yarn build`.

---

## Task Overview

| Task | Name | Phase | Size | Est. Hours | Dependencies | Agent |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | Setup & Signals Architecture | Setup | S | 0.5h | None | angular-developer |
| **02** | Unit Tests Specification (RED) | RED | M | 1.0h | Task 01 | angular-developer |
| **03** | Mobile Layout & SCSS (GREEN+VERIFY) | GREEN+VERIFY | M | 2.0h | Task 02 | angular-developer |

---

## Progress Tracking

- [x] **Task 01**: Setup & Signals Architecture (`task01-setup.md`)
- [x] **Task 02**: Especificación y Escritura de Pruebas Unitarias RED (`task02-red.md`)
- [x] **Task 03**: Implementación de UI Móvil y Estilos SCSS GREEN + VERIFY (`task03-green.md`)
- [x] **Task 04 (Extension)**: Vistas Duales (Cuadrícula / Lista), Modo Claro por defecto & Drawer de Contacto

---

## Quality Gates

### 1. verify:quick (< 15s)
```bash
cd Proyecto/growthhacking.PrototypeZero/apps/angular && npx ng test --watch=false --browsers=ChromeHeadless --include="**/storefront-catalog.component.spec.ts"
```

### 2. verify:build (< 20s)
```bash
cd Proyecto/growthhacking.PrototypeZero/apps/angular && yarn build
```

---

## References

- **TRD:** [`trd-mobile-storefront-responsive.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-mobile-storefront-responsive/trd-mobile-storefront-responsive.md)
- **Test Spec:** [`test-spec-mobile-storefront-responsive.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-mobile-storefront-responsive/test-spec-mobile-storefront-responsive.md)
- **Design:** [`design-mobile-storefront-responsive.md`](file:///C:/Users/santi/Documents/GitHub/Growth-Hacking/tasks/task-mobile-storefront-responsive/design-mobile-storefront-responsive.md)
