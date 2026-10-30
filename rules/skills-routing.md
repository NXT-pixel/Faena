---
description: Enrutamiento obligatorio a la skill de dominio correcta antes de escribir o revisar código.
alwaysApply: true
---

# Skills Routing

Las skills son lectura obligatoria antes de tocar un dominio, no material de consulta opcional.

## Dónde viven

- Ubicación canónica: `skills/<nombre>/SKILL.md`.
- Catálogo (generado, siempre actual): `skills/README.md`.
- Un `SKILL.md` fuera de `skills/` es un bug: las skills no se duplican en `agents/`, `commands/` ni `rules/`.

## Cómo usar una skill

1. Abre `skills/README.md` y ubica la skill cuyo "cuándo usar" coincida con la tarea.
2. Lee `skills/<nombre>/SKILL.md` **antes** de escribir código, tests o una revisión en ese dominio.
3. Abre los `references/` o `assets/` que `SKILL.md` indique **solo** para la tarea en curso.
4. Lee cada skill una vez por tarea; no releas el mismo archivo en la misma sesión.

## Si ninguna skill aplica

Dilo explícitamente — por ejemplo: *"ninguna skill cubre X; procedo con `rules/project/` y el TRD"* — en lugar de inventar convenciones que el repositorio no define.

## Agregar una skill

Crea `skills/<nombre>/SKILL.md` con `name` (igual a la carpeta) y `description`, y regenera el catálogo con `scripts/build-skills-index.ps1`. `scripts/validate-faena.ps1` falla si el catálogo queda desactualizado o si el `name` no coincide con la carpeta.
