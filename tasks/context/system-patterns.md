# System Patterns & Architecture
**Created**: 2026-10-25T03:19:55.675128+00:00
**Last Updated**: 2026-10-26T22:30:00Z

## Core Design Principles
1. **Persona vs Procedure**: Agents define WHO; Commands define HOW TO; Faena runs THE FLOW.
2. **TDD Discipline**: Tests written first (RED), code implemented (GREEN), quality gates verified (VERIFY).
3. **Multi-Provider Agnostic**: Code execution works identically with Claude, ChatGPT, Gemini, Ollama, etc.
4. **Clean Artifact Lifecycle**: Transient task files drive autonomous execution; results are committed cleanly.

---

## 🏗️ Patrones de Arquitectura Implementados en `Proyecto/growthhacking.PrototypeZero`

### 1. Pipeline de Importación y Extracción de Catálogos con IA
- **Flujo de Procesamiento**:
  1. Subida de PDF/Catálogo a Azure Blob Storage (`store-catalog`) vía `PrototypeZero.CoreService`.
  2. Extracción y segmentación asistida por OpenAI en `PrototypeZero.AiService`.
  3. Creación de borradores de productos (`CatalogProductDraft`) en base de datos.
  4. Revisión por operador humano en el portal Angular (`/store/products/import-catalog`).
  5. Publicación final hacia catálogo oficial (`CatalogProduct` y `CatalogVariant`).

### 2. Sincronización y Expansión Exacta de Variantes (`Preserve Approved Price Pattern`)
- **Regla de Integridad Monetaria**:
  - Los textos extraídos por OCR/IA pueden contener discrepancias menores en burbujas o variantes hijas (`VariantsJson`).
  - El precio aprobado explícitamente por el operador (`draft.PriceAmount`) es la fuente de verdad inmutable.
- **Implementación**:
  - **`CatalogDraftVariantResolver.SyncVariantPrices`**: Sincroniza en tiempo real `VariantsJson` con el precio padre aprobado durante la actualización (`UpdateDraftAsync`), aprobación (`MarkDraftReviewedAsync`) y publicación (`PublishDraftsAsync`).
  - **`CatalogDraftVariantResolver.ExpandVariants`**: Al descomponer un borrador en productos individuales para publicación, hereda `draft.PriceAmount` para todas las variantes que compartan el precio base, garantizando que ninguna lectura errónea o desfasada sobreescriba la decisión humana.
  - **Frontend Angular Reactivo**: `(change)="onPriceAmountChange()"` y `syncVariantPrices()` en `create-update-catalog-draft.component.ts` aseguran que la interfaz mantenga consistencia antes del envío del DTO HTTP.

### 3. Handoff de Archivos Multimedia para WhatsApp / Meta
- WhatsApp no acepta payloads crudos en base64 para multimedia en WABA.
- `PrototypeZero.FileManagementService` genera tokens públicos temporales `{PublicShareBaseUrl}/api/file-management/standard-storage/share/{token}`.
- Meta realiza `HTTP GET` para descargar los blobs; requiere que el API Gateway exponga un túnel público (`Public` en DevTunnels).
