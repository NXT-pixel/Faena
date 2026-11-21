# 🏢 Faena Tenants (Multi-Tenant Architecture)

Esta carpeta contiene los diferentes **tenants** (empresas, clientes o proyectos independientes) gestionados por este hub de Faena.

El motor de Faena (`skills/`, `agents/`, `commands/`, `scripts/`, `dashboard`) es único y compartido, mientras que el código, contexto, reglas corporativas y tickets están aislados por tenant.

---

## 📁 Estructura de un Tenant

Cada carpeta dentro de `tenants/<nombre-del-tenant>/` tiene la siguiente estructura:

```
tenants/<nombre-del-tenant>/
├── context/
│   ├── team-context.md        # Organigrama (Tech Lead, QA, DevOps) e identidad Git corporativa
│   ├── tech-context.md        # Stack técnico y versiones reales
│   ├── project-structure.md   # Documentación de repositorios clonados
│   ├── learnings.md           # Memoria viva y gotchas aprendidos en este tenant
│   ├── progress.md            # Progreso global del tenant
│   └── system-patterns.md     # Patrones de arquitectura y diseño aplicables
├── rules/
│   └── company-standards.md   # Estándares corporativos y de código del cliente
├── tasks/                     # Carpetas de tickets (task-<slug>/) de este tenant
└── Proyecto/                  # Código fuente real del cliente (ignorado por Git)
```

---

## 🚀 Comandos Rápidos

### Crear un nuevo Tenant
```powershell
# Windows
.\scripts\create-tenant.cmd <nombre-del-tenant>

# Linux / macOS
./scripts/create-tenant.sh <nombre-del-tenant>
```

### Cambiar de Tenant Activo
```powershell
# Windows
.\scripts\switch-tenant.cmd <nombre-del-tenant>

# Linux / macOS
./scripts/switch-tenant.sh <nombre-del-tenant>
```

---

## 📊 Monitoreo Multi-Tenant

El Dashboard Companion (`Faena-Dashboard.cmd` o `./dashboard.sh`) detecta automáticamente todos los tenants creados en esta carpeta y te permite alternar entre ellos o monitorear el progreso simultáneo de varios desarrollos en tiempo real desde `http://localhost:3333`.
