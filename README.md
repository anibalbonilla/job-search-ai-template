# 🧳 Job Search Assistant — starter template

Un sistema de búsqueda de empleo diseñado para operarse junto a un asistente de IA con acceso a herramientas de archivos (y opcionalmente navegador/búsqueda web) — Claude Code, ChatGPT con Code Interpreter/archivos, Gemini CLI, Cursor, opencode, etc. `AGENTS.md` es la convención de archivo que varias de estas herramientas (opencode, Amp, Codex, Claude Code) leen automáticamente al abrir el proyecto.

## ✅ Qué hace

- Mantiene un **CV maestro** (`profile/cv_master.md`) con toda tu experiencia real, y genera versiones **ajustadas por vacante** (nunca inventadas) en `applications/<empresa>-<puesto>/`.
- Convierte esas versiones a **PDF ATS-friendly** con un script propio (sin depender de Word/Canva).
- Chequea la **cobertura de keywords ATS** de tu CV contra el texto real de cada vacante.
- Busca vacantes automáticamente en 4 agregadores remotos con API pública, y ayuda a investigar/revisar manualmente el resto de fuentes que definas en `profile/job_sources.md` (LinkedIn, portales locales, staffing, empresas objetivo) — ver esa lista para el detalle completo de fuentes actuales y cómo agregar una nueva.
- **Escribe cada CV y carta en el mismo idioma en que está escrita la vacante** (lo infiere solo, no hace falta pedirlo cada vez — podés pedir la otra versión cuando quieras). Esto es independiente del idioma en el que estén escritos estos documentos del proyecto.
- Lleva un **log de aplicaciones** y un registro de contacto con reclutadores.
- Investiga un **rango salarial de referencia** por vacante y lo deja en las notas de cada aplicación; busca **preguntas frecuentes de entrevista** y arma un **guion de preparación** (presentación, respuestas sugeridas, preguntas para el entrevistador) cuando ya tenés una agendada con una empresa puntual (no automático en cada aplicación); y verifica la **legitimidad de la fuente/empresa** cuando hay señales de duda (agregador desconocido, salario desalineado, sin nombre de empresa visible).
- Todo el criterio operativo (cuándo evaluar un gap como real, cuándo declinar un turno, cómo manejar formularios de compensación, cómo agregar fuentes nuevas, etc.) vive en `AGENTS.md` — es lo que el asistente lee para saber cómo comportarse.

## 🌐 Idioma de este proyecto

Todo el contenido de este template (`README.md`, `AGENTS.md`, los `.example.md`) está escrito en **español** — es una limitación de acceso conocida, no un accidente: si no leés español no vas a poder auto-servirte el setup, aunque el asistente de IA sí entiende las instrucciones en español sin problema y puede escribir tus CVs/cartas en inglés igual (ver punto anterior). Una versión en inglés queda pendiente para un fork futuro.

## 🚫 Qué NO hace

- No aplica por vos. Nunca envía formularios ni sube archivos a un portal sin tu confirmación explícita.
- No inventa experiencia. El principio central de todo el sistema es: si no está en tu CV maestro, no aparece en ningún CV ajustado hasta que lo confirmes como real.

## ⚙️ Setup

1. Clona o copia esta carpeta.
2. `pip install fpdf2` (única dependencia externa, usada por `scripts/md_to_pdf.py`).
3. Copia `profile/cv_master.example.md` → `profile/cv_master.md` y llénalo con tu experiencia real.
   - **¿Ya tenés un CV armado en otro formato** (Word, PDF, export de LinkedIn)? No lo reescribas a mano — compártelo con tu asistente de IA y pídele que lo reestructure al formato de `cv_master.md`. Es mucho más rápido que empezar de cero, y así el asistente ya conoce tu experiencia real desde el primer mensaje.
4. Copia `profile/ats_keywords.example.md` → `profile/ats_keywords.md`. **No lo llenes a mano de una** — con `cv_master.md` ya listo, pídele a tu asistente que lo lea y te proponga las categorías/keywords reales de tu campo. No es una sincronización automática (si más adelante actualizás tu CV, hay que pedirle que revise `ats_keywords.md` de nuevo), pero es mucho más rápido y preciso que armarlo desde cero vos mismo.
5. Copia `profile/job_sources.example.md` → `profile/job_sources.md`. Los 4 agregadores con API pública (RemoteOK, Remotive, Jobicy, Arbeitnow) ya vienen con su URL real y funcionan igual para cualquier campo — no hay que tocarlos. Todo lo demás (nicho de tu industria, staffing, portales locales, empresas objetivo) depende de tu campo/país específico: pídele a tu asistente que investigue y te proponga opciones concretas para tu caso en vez de dejarlo en blanco.
6. Copia `profile/interview_review.example.md` → `profile/interview_review.md` (opcional, se usa después de tu primera entrevista).
7. Copia `PENDING.example.md` → `PENDING.md` (opcional, lista viva de pendientes/decisiones — ayuda a que el asistente retome el contexto entre sesiones).
8. Abre una conversación con tu asistente de IA en esta carpeta y dile que lea `AGENTS.md` para entender el flujo. (Con Claude Code, opencode, Cursor, y herramientas similares esto suele pasar automático al detectar `AGENTS.md` en la raíz del proyecto.)
9. Empieza a pegarle vacantes.

## 🚀 Cómo usarlo día a día

### La primera vez (justo después del setup)

1. Abre una conversación nueva con tu asistente de IA **en esta misma carpeta** (que la vea como directorio de trabajo).
2. Si tu herramienta no lee `AGENTS.md` automáticamente al abrir el proyecto (Claude Code, opencode y similares sí lo hacen solos), dile explícitamente: *"lee AGENTS.md antes de empezar"*.
3. Pega el texto completo de una vacante real (o el link, si tu asistente puede leerlo directo) en el chat.
4. El asistente va a comparar la vacante contra tu `profile/cv_master.md` y decirte honestamente qué tan buen fit es y qué vacíos reales tiene — antes de escribir nada. Si le contás experiencia real que falta en tu CV maestro, la agrega ahí primero.
5. Si el fit tiene sentido, el asistente crea `applications/<empresa>-<puesto>/` con `cv.md` y `cover_letter.md` ajustados a esa vacante (nunca inventa experiencia), agrega notas de la vacante y un rango salarial de referencia, y exporta a PDF.
6. Revisa los `.md` y los PDF generados. Vos sos quien sube el PDF al portal/LinkedIn — el asistente nunca aplica en tu nombre.
7. Avísale cuando la envíes, para que actualice el estado en `applications/00-log.md`.

No hace falta ningún comando especial para "arrancar" el sistema — el paso 3 (pegar una vacante) es lo que dispara todo el flujo.

### A partir de la segunda vacante en adelante

- **No hay nada que resetear ni reconfigurar.** Simplemente abre una conversación nueva en la carpeta y repite el paso 3 de arriba (pegar la siguiente vacante) — cada una crea su propia carpeta en `applications/`, no pisa las anteriores.
- **¿Quieres ver en qué estado quedó todo?** Pídele al asistente que resuma `applications/00-log.md`, o ábrelo vos mismo — el archivo explica sus propias columnas y los valores válidos de "Estado" (Preparado / Aplicado / En proceso / Rechazado / Oferta / Descartado) en el encabezado.
- **¿Quieres que retome contexto de sesiones anteriores** (barridos ya hechos, decisiones tomadas, cosas pendientes)? Llevá `PENDING.md` actualizado (ver Setup, paso 7) y pídele al asistente que lo lea al empezar — así no repite trabajo ni te vuelve a preguntar algo que ya decidiste.
- **¿Quieres buscar vacantes de forma proactiva** (sin tener ya un posting pegado)? Corré `python3 scripts/search_jobs.py` vos mismo (ver comandos en `AGENTS.md`), o pídele al asistente que haga un "barrido" por las fuentes de `profile/job_sources.md` (LinkedIn, portales locales, empresas objetivo, etc.).
- **¿Tuviste una entrevista o examen?** Contale al asistente qué te costó — lo agrega a `profile/interview_review.md` como referencia para la próxima vez.
- **¿Cambió tu CV o ganaste una skill nueva?** Editá `profile/cv_master.md` directamente, o pedíselo al asistente en la conversación — así queda disponible para todas las vacantes futuras.
- Todo el detalle operativo (qué preguntar en la llamada, cómo manejar un Talent Network, seguimiento a reclutadores, etc.) vive en `AGENTS.md` — el asistente lo consulta solo, pero también podés leerlo vos si querés entender el criterio completo.

## 🗂️ Estructura

```
.
├── AGENTS.md                          Instrucciones de flujo para el asistente de IA (y para vos)
├── README.md
├── PENDING.example.md                 → copiar a PENDING.md (opcional): lista viva de pendientes/decisiones
├── profile/
│   ├── cv_master.example.md           → copiar a cv_master.md: toda tu experiencia real, sin editar por vacante
│   ├── cover_letter_template.md       Plantilla base de carta de presentación
│   ├── job_sources.example.md         → copiar a job_sources.md: plataformas donde buscar
│   ├── ats_keywords.example.md        → copiar a ats_keywords.md: vocabulario ATS de tu campo
│   └── interview_review.example.md    → copiar a interview_review.md: log de temas fallados en entrevistas
├── scripts/
│   ├── search_jobs.py                 Busca en RemoteOK, Remotive, Jobicy y Arbeitnow por keywords
│   ├── md_to_pdf.py                   Convierte un .md (CV o carta) a PDF ATS-friendly
│   └── ats_check.py                   Compara un CV contra una vacante y marca keywords que faltan
└── applications/
    ├── 00-log.md                      Índice de todas las vacantes vistas/aplicadas (prefijo "00-" para que ordene primero)
    └── <empresa>-<puesto>/            Una carpeta por vacante a la que aplicás
        ├── cv.md                          CV ajustado a esa vacante (editable en Markdown)
        ├── cover_letter.md                Carta ajustada a esa vacante
        ├── notes.md                       Descripción original + notas de fit + rango salarial
        ├── <Tu Nombre> CV.pdf             PDF final, listo para subir
        └── <Tu Nombre> Cover Letter.pdf   PDF final, listo para subir
```

Cada carpeta `applications/<empresa>-<puesto>/` se crea de cero por vacante — el nombre de la carpeta y los `.md` de adentro los genera el asistente siguiendo el flujo de `AGENTS.md`, no hace falta crearlos a mano.

## 🔒 Si vas a subir tu copia (con tus datos reales) a un repo público

Este template está pensado para compartirse vacío. Si lo convertís en tu copia de trabajo con tus datos reales, **no lo subas tal cual a un repo público** — agregá algo como esto a `.gitignore` antes de tu primer commit:

```
profile/cv_master.md
profile/job_sources.md
profile/ats_keywords.md
profile/interview_review.md
applications/*/
applications/00-log.md
PENDING.md
```

Y dejá solo los `.example.md` y `AGENTS.md` visibles — que es exactamente lo que tiene esta carpeta template.
