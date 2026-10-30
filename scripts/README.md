# 🛠️ Scripts del harness

Dos utilidades de mantenimiento. **Ninguna hace falta para trabajar un ticket**: el flujo por chat no ejecuta scripts.

```powershell
.\scripts\validate-faena.ps1          # ¿está el harness íntegro?
.\scripts\build-skills-index.ps1      # regenera el catálogo de skills
```

> En Windows, si la política de ejecución bloquea los scripts:
> `powershell -ExecutionPolicy Bypass -File .\scripts\validate-faena.ps1`

---

## `validate-faena.ps1`

Seis chequeos, pensados para local y para CI:

| Chequeo | Qué verifica |
| :--- | :--- |
| `skill-location` | Todo `SKILL.md` vive en `skills/<nombre>/` o `skills/project/<nombre>/`, con mayúsculas exactas |
| `skill-metadata` | Cada skill tiene `name` y `description`, y `name` coincide con su carpeta |
| `skills-catalog` | `skills/README.md` está al día respecto a los `SKILL.md` |
| `rules-extension` | No queda ningún `.mdc` fuera de `.cursor/rules/` |
| `protocol-adapters` | `PROTOCOL.md` existe y los cinco adaptadores lo referencian |
| `path-references` | Toda ruta `skills/`, `rules/`, `agents/`, `commands/`, `scripts/` o `tasks/context/` citada en la documentación existe, con mayúsculas exactas |

Sale con código 1 si algo falla, así que sirve tal cual en un pre-commit o en CI.

**Qué no revisa**: referencias a carpetas (indistinguibles de prosa como "agents/commands"), rutas absolutas de la máquina, ni los documentos bajo `skills/` que hablan del repo del cliente.

## `build-skills-index.ps1`

Regenera la tabla de `skills/README.md` a partir del front matter de cada `SKILL.md`. El catálogo es derivado: no se edita a mano.

```powershell
.\scripts\build-skills-index.ps1 -Check   # no escribe; falla si está desactualizado
```

`-Check` es lo que usa la validación y el CI. Añadir o renombrar una skill sin regenerar rompe el chequeo a propósito.

## `faena-known-refs.txt`

Lista de referencias históricamente rotas que la validación tolera. No es un mecanismo para silenciar errores nuevos: cualquier ruta rota que no esté aquí hace fallar `path-references`. Cuando arregles una, borra su línea.

## `common/SkillsCatalog.ps1`

Lógica compartida entre los dos scripts (lectura de front matter, render del catálogo). No se ejecuta por sí sola.
