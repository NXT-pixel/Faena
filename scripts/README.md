# 🛠️ Scripts del harness

Utilidades de mantenimiento, gestión multi-tenant y un dashboard visual en vivo. **Ninguna hace falta para trabajar un ticket**: el flujo por chat no ejecuta scripts.

```powershell
.\scripts\doctor.cmd           # ¿está bien mi entorno? (con el arreglo de cada aviso)
.\scripts\validate.cmd         # ¿está íntegro el harness?
.\scripts\rebuild-skills.cmd   # regenera el catálogo de skills
.\scripts\index-tasks.cmd      # estado de los tickets en tasks/INDEX.md (local)
.\scripts\dashboard.cmd        # lanza el dashboard web acompañante en vivo
.\scripts\create-tenant.cmd    # inicializa un nuevo tenant aislado en tenants/
.\scripts\switch-tenant.cmd    # consulta o cambia el tenant activo (.active-tenant)
.\scripts\export-tenants.cmd    # exporta contexto, reglas y preferencias a tenants.local.json
.\scripts\import-tenants.cmd    # restaura todos los tenants desde tenants.local.json
```

Los `.cmd` son wrappers de una línea sobre los `.ps1`: **no pasan por la política de ejecución de Windows**, así que son la forma recomendada en Windows. En macOS/Linux, `pwsh ./scripts/<script>.ps1`.

---

## `doctor.ps1`

Diagnóstico del entorno. No modifica nada: mira y aconseja. Diez comprobaciones:

| Comprobación | Qué mira |
| :--- | :--- |
| `repo-root` | Que estés ejecutando desde un clon de Faena (`PROTOCOL.md` presente) |
| `powershell` | Versión (7 recomendado; 5.1 funciona) |
| `git` | Instalado y versión ≥ 2.30 |
| `exec-policy` | Política **efectiva** de ejecución; avisa si bloquea `.ps1` |
| `hooks` | Si `core.hooksPath` apunta a `.githooks` |
| `skills-catalog` | Si `skills/README.md` está al día |
| `proyecto` | Repositorios clonados en `Proyecto/` |
| `team-context` | Si `tasks/context/team-context.md` sigue con marcadores de plantilla |
| `ecc` | Si `faena.local.json` define `eccPath`, que esa carpeta exista y tenga `skills/` |
| `tls-backend` | Backend TLS de git (avisa si es `schannel`) |

Con `-Network` añade una prueba real de acceso al remoto (`git ls-remote --heads origin`).

Sale con código 1 solo si algo es `FAIL`; los avisos (`WARN`) no rompen nada.

## `validate-faena.ps1`

Ocho chequeos, pensados para local y para CI:

| Chequeo | Qué verifica |
| :--- | :--- |
| `skill-location` | Todo `SKILL.md` vive en `skills/<nombre>/` o `skills/project/<nombre>/`, con mayúsculas exactas |
| `skill-metadata` | Cada skill tiene `name` y `description`, y `name` coincide con su carpeta |
| `skills-catalog` | `skills/README.md` está al día respecto a los `SKILL.md` |
| `rules-extension` | No queda ningún `.mdc` fuera de `.cursor/rules/` |
| `protocol-adapters` | `PROTOCOL.md` existe y los cinco adaptadores lo referencian |
| `proyecto-visibility` | Cada repositorio presente en `Proyecto/` aparece documentado en `tasks/context/project-structure.md` |
| `path-references` | Toda ruta `skills/`, `rules/`, `agents/`, `commands/`, `scripts/` o `tasks/context/` citada en la documentación existe, con mayúsculas exactas |
| `template-metadata` | Los campos de cabecera que lee el dashboard (`Branch`, `Ticket Origen`, `Location`, `Base Commit`…) usan el formato `**Campo**:` en las plantillas del flujo |

Sale con código 1 si algo falla, así que sirve tal cual en un pre-commit o en CI.

**Qué no revisa**: referencias a carpetas (indistinguibles de prosa como "agents/commands"), rutas absolutas de la máquina, ni los documentos bajo `skills/` que hablan del repo del cliente.

## `build-skills-index.ps1`

Regenera la tabla de `skills/README.md` a partir del front matter de cada `SKILL.md`. El catálogo es derivado: no se edita a mano.

```powershell
.\scripts\rebuild-skills.cmd -Check   # no escribe; falla si está desactualizado
```

`-Check` es lo que usa la validación y el CI. Añadir o renombrar una skill sin regenerar rompe el chequeo a propósito.

## `build-tasks-index.ps1`

Genera `tasks/INDEX.md` con una fila por `tasks/task-<nombre>/`: qué artefactos tiene (design, TRD, test-spec, tareas), checkboxes hechos/total y fecha de última modificación.

```powershell
.\scripts\index-tasks.cmd
```

El índice **no se versiona** (está en `.gitignore`): el estado difiere por rama y por máquina, y commitearlo solo produce conflictos. Por eso la validación no lo exige y el CI nunca lo ve.

## `dashboard.cmd` / `Faena-Dashboard.cmd`

Lanza el dashboard web acompañante en vivo (`http://localhost:3333`) para monitorear el progreso de las tareas, los Quality Gates y los logs de ejecución en tiempo real mientras cualquier IA (Claude Code, Codex, Antigravity) trabaja en el repositorio. Ejecutable directamente con doble clic en Windows. Implementado en `scripts/dashboard/server.py`.

## `faena-known-refs.txt`
Lista de referencias históricamente rotas que la validación tolera. No es un mecanismo para silenciar errores nuevos: cualquier ruta rota que no esté aquí hace fallar `path-references`. Cuando arregles una, borra su línea. Hoy está vacía a propósito.

## `common/SkillsCatalog.ps1`

Lógica compartida entre los scripts (lectura de front matter, render del catálogo). No se ejecuta por sí sola.

---

## El hook de pre-commit

`.githooks/pre-commit` hace dos cosas, en este orden:

1. **Regenera** `skills/README.md` y, si cambió, lo añade al commit. Así un catálogo desactualizado no llega a CI: se repara en el camino.
2. **Valida** el harness completo y bloquea el commit si algo está roto.

Actívalo una vez por clon con `git config core.hooksPath .githooks`. En CI no hay hooks: allí un catálogo desactualizado sí falla, que es exactamente lo que se quiere.
