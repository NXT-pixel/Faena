# Requerimientos y Diseño: Rediseño Responsive Móvil del Catálogo Storefront

**Fecha:** 2026-11-04  
**Ticket Origen:** "el responsive en celulares esta completamente mal, haz que sea como esta pagina" (Referencia visual: Catálogo Móvil estilo Kyte - María Isabel Accesorios)  
**Repositorio Afectado:** `Proyecto/growthhacking.PrototypeZero/apps/angular/`  
**Ubicación de Componente:** `apps/angular/src/app/public/storefront/storefront-catalog.component.{ts,html,scss}`  

---

## 1. Resumen Ejecutivo y Objetivos

El catálogo público actual (`StorefrontCatalogComponent`) en pantallas móviles presenta problemas críticos de usabilidad y jerarquía visual:
1. En pantallas pequeñas, la barra lateral de categorías, opciones de ordenamiento y contacto se apilaba en el flujo vertical principal antes de los productos, obligando al usuario a desplazarse extensamente antes de ver el primer artículo.
2. La cuadrícula de productos en móviles utilizaba tarjetas verticales con imágenes cuadradas masivas de ancho completo (`100% viewport width`), en lugar del formato moderno de tarjeta horizontal compacta estándar en comercio electrónico móvil (estilo Kyte / Instagram shopping).
3. La barra de navegación superior resultaba sobrecargada al incluir selector de idioma, botón de tema, búsqueda expandida y botón de WhatsApp simultáneamente en pantallas estrechas.

**Objetivo:** Rediseñar la experiencia móvil (`viewport <= 768px`) inspirándose fielmente en el estándar de la referencia proporcionada (`maria-isabel-accesorios.catalog.kyte.site`), ofreciendo:
- **Header móvil ultra limpio:** Menú hamburguesa (`☰`) a la izquierda para acceder a info y contacto, logo centrado/izquierdo y carrito a la derecha.
- **Navegación por categorías en carrusel horizontal:** Icono de búsqueda + pestañas de categorías en mayúsculas (`TODO`, `ACCESORIOS`, etc.) con scroll horizontal y subrayado activo.
- **Barra de acción / filtro compacta:** Pill de categoría activa + botón `ORDENAR POR` con modal/bottom-sheet limpio en lugar de botones dispersos.
- **Tarjetas de producto horizontales en móviles:** Imagen cuadrada con bordes redondeados a la izquierda (~38% ancho), y a la derecha: Título en negrita, categoría/subtítulo en gris tenue y precio destacado en color corporativo.
- **Preservación total de la vista Desktop:** En pantallas de escritorio (`> 768px`), el catálogo conserva su cuadrícula multi-columna y barra lateral sin regresiones.

---

## 2. Personas y Actores

- **Usuario Final (Comprador Móvil):** Cliente que ingresa desde Instagram, WhatsApp o navegador móvil y necesita explorar productos de forma rápida, ver precios claros y agregar al carrito sin scrolls innecesarios.
- **Comerciante / Tenant:** Propietario de la tienda que requiere una presentación estética, profesional y competitiva de sus productos similar a plataformas de catálogo reconocidas.
- **Equipo Interno:**
  - **Tech Lead:** Santiago / David (Alineación de arquitectura y diseño responsive sin regresión en desktop).
  - **QA Asignado:** Laura (Certificación de visualización en Chrome Mobile DevTools, iOS Safari y Android).
  - **DevOps:** Sofía (Sin impacto en infraestructura o secretos).

---

## 3. Criterios de Aceptación (Given-When-Then)

### Escenario 1: Header móvil compacto con menú hamburguesa
- **Dado** un usuario que visita el catálogo en un dispositivo móvil (`viewport width <= 768px`).
- **Cuando** carga la página.
- **Entonces** la cabecera muestra el botón hamburguesa `☰` a la izquierda, el logo del tenant limpio y proporcionado, y el botón de carrito a la derecha; las acciones secundarias (contacto, tema, idioma) quedan consolidadas dentro del menú lateral deslizable accesible vía `☰`.

### Escenario 2: Carrusel horizontal de categorías tipo pestañas (Kyte style)
- **Dado** un catálogo con múltiples categorías activas en móvil.
- **When** se observa la barra sub-header bajo el banner o navegación.
- **Entonces** se visualiza un icono de búsqueda y un listado deslizable horizontalmente con las categorías en mayúsculas (`TODO`, `CATEGORÍA 1`, `CATEGORÍA 2`), sin barra de scroll visible, con la categoría seleccionada destacada mediante subrayado inferior.
- **Cuando** el usuario hace clic o tap en una categoría.
- **Entonces** el catálogo filtra reactivamente los productos correspondientes sin recargar la página.

### Escenario 3: Barra de ordenamiento móvil (Botón "ORDENAR POR")
- **Dado** el listado de productos en móvil.
- **Cuando** se visualiza la sección previa a los productos.
- **Entonces** se muestra una barra compacta con la etiqueta de la categoría actual y un botón discreto `ORDENAR POR` con icono de lista.
- **Cuando** el usuario presiona `ORDENAR POR`.
- **Entonces** se despliega un selector limpio (bottom sheet o menú modal) para elegir el criterio de ordenamiento (`Categoría`, `Menor precio`, `Mayor precio`, `Nombre`), cerrándose al seleccionar y aplicando el orden inmediato.

### Escenario 4: Tarjetas de producto en disposición horizontal móvil
- **Dado** el listado de productos en pantalla móvil (`<= 768px`).
- **Cuando** se renderizan los productos del catálogo.
- **Entonces** cada tarjeta se despliega horizontalmente:
  - Lado izquierdo: Imagen del producto cuadrada (aprox. 120px de ancho) con esquinas redondeadas (`border-radius: 14px` o `16px`).
  - Lado derecho: Nombre del producto destacado en tipografía negrita, categoría o resumen corto en tono gris atenuado, y precio en formato grande y visible con el color de acento corporativo.
  - El clic en la tarjeta continúa abriendo el modal de detalle del producto con zoom disponible.

### Escenario 5: No regresión en vista Desktop
- **Dado** un usuario que navega en escritorio (`viewport > 768px`).
- **Cuando** consulta el catálogo.
- **Entonces** la barra lateral de categorías, la búsqueda completa, las opciones de visualización (grid / list) y la cuadrícula de 3 o 4 columnas se mantienen operativas exactamente como fueron diseñadas.

---

## 4. Alcance Técnico

### En Alcance (In Scope)
1. **Componente `storefront-catalog.component.html`**:
   - Integrar botón de menú hamburguesa móvil en el header.
   - Implementar drawer deslizable lateral para navegación móvil (info, contacto, idioma, tema).
   - Crear barra de navegación horizontal de categorías con estilo pestañas + icono de búsqueda.
   - Crear barra de herramientas móvil con botón `ORDENAR POR` y modal/sheet de selección de orden.
   - Adaptar el marcado de tarjetas para renderizar la estructura horizontal en móvil (`store-card mobile-optimized`).
2. **Componente `storefront-catalog.component.ts`**:
   - Señal reactiva `isMobileDrawerOpen = signal<boolean>(false)`.
   - Señal reactiva `isSortSheetOpen = signal<boolean>(false)`.
   - Métodos `toggleMobileDrawer()`, `closeMobileDrawer()`, `openSortSheet()`, `closeSortSheet()`.
   - Bloqueo de scroll cuando el drawer móvil o el sheet de ordenamiento están abiertos.
3. **Estilos `storefront-catalog.component.scss`**:
   - Media queries específicos para `<= 768px` y `<= 480px`.
   - Reglas de flexbox horizontal para `.store-card` en móvil con proporciones de imagen 1:1 (~120px) y contenido lateral.
   - Estilos para carrusel horizontal con scroll táctil suave (`-webkit-overflow-scrolling: touch; scrollbar-width: none;`).
   - Drawer móvil con diseño glassmorphism y botón de cierre.
   - Soporte completo para temas Claro y Oscuro.
4. **Pruebas Automatizadas `storefront-catalog.component.spec.ts`**:
   - Pruebas unitarias para las señales `isMobileDrawerOpen` y `isSortSheetOpen`.
   - Pruebas de selección de categoría y ordenamiento desde los controles móviles.

### Fuera de Alcance (Out of Scope)
- Modificación de contratos backend o microservicios (.NET).
- Cambios en las pasarelas de pago o en la lógica de checkout de WhatsApp.

---

## 5. Coordinación de Equipo y Delegaciones

- **Handoff a QA (Laura):**
  - **Dispositivos de Prueba:** Validar en Chrome DevTools con emulación de iPhone 12/14/15 (390x844), Samsung Galaxy S20 (360x800) y iPad/Tablet (768px).
  - **Puntos Clave a Verificar:**
    1. Desplazamiento horizontal fluido de categorías.
    2. Visualización correcta de tarjetas horizontales (imagen a la izquierda, título, categoría y precio a la derecha).
    3. Apertura y cierre del drawer móvil `☰` y del selector `ORDENAR POR`.
    4. Que en desktop (`> 900px`) la página continúe viéndose con cuadrícula multi-columna tradicional.
- **Handoff a DevOps (Sofía):**
  - Ninguno requerido. Todos los cambios son a nivel de cliente Angular (`apps/angular`).

---

## 6. Próximo Paso

Para generar el Documento de Requerimientos Técnicos (TRD) y la especificación de pruebas unitarias:
> 👉 **Siguiente paso:** Arrastra al chat `@commands/2-create-trd.md tasks/task-mobile-storefront-responsive/design-mobile-storefront-responsive.md`
