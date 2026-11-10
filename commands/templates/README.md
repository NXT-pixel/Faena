# 📄 Plantillas de comandos

Plantillas que un comando carga **solo cuando las necesita**, para no pagar su coste en tokens al arrastrar el comando completo.

## Por qué existe esta carpeta

Un comando de 1.200 líneas cuesta lo mismo que un ticket: el agente lo lee entero antes de empezar. La mayor parte de ese volumen suele ser *plantillas de salida* (el esqueleto del TRD, el formato de un archivo de tarea, ejemplos largos) que solo hacen falta al generar esa sección.

Regla: el comando contiene el **procedimiento**; esta carpeta contiene el **formato**. El comando deja un puntero como:

```markdown
> Plantilla completa: [`commands/templates/<comando>/<plantilla>.md`](templates/<comando>/<plantilla>.md) - ábrela antes de generar esta sección.
```

## Cómo se usa

1. El usuario arrastra el comando.
2. El agente lee el procedimiento y, cuando llega al puntero, abre **solo** esa plantilla.
3. Si el agente se salta el puntero, la salida sale sin formato: el puntero es una instrucción, no una sugerencia.

## Estado actual

| Comando | Plantillas | Nota |
| :--- | :--- | :--- |
| `create-gherkins.md` | [1](create-gherkins/) | Refactorizado y verificado |
| el resto | — | Pendiente: sus documentos tienen fences de Markdown mal cerrados (ver abajo) y extraer bloques movería contenido incorrecto |

## Bloqueante conocido

Cinco comandos (`make-agent.md`, `design-ux-ui.md`, `2-create-trd.md`, `3-create-tasks.md`, `1c-decompose.md`) tienen bloques de código mal cerrados: usan un fence **con etiqueta** (` ```mermaid `, ` ```json `, ` ```typescript `) como cierre de un bloque abierto sin etiqueta. El resultado es que se renderizan como un único bloque gigante y cualquier extracción automática empareja mal los fences.

Antes de trocearlos hay que arreglar su estructura: convertir el fence exterior de esas plantillas a cuatro backticks (```` ```` ````) para que los ejemplos anidados queden literales. Hasta entonces, esos comandos se dejan como están a propósito.
