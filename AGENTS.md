# 🧭 Cómo funciona este sistema de búsqueda de empleo

Guía de referencia para operar todo el flujo: perfil, búsqueda de vacantes, generación de CV/carta, y seguimiento de aplicaciones. Está escrita para que la siga un asistente de IA (Claude Code, ChatGPT, Gemini, o cualquier otro con acceso a herramientas de archivos/navegador), pero también sirve para que un humano entienda el sistema.

## ⚙️ Antes de empezar (setup)

Si estás leyendo esto como asistente de IA en una sesión de setup inicial con un usuario nuevo, esta sección es tu checklist — guía al usuario paso a paso, no asumas que ya lo hizo todo.

1. Instala las dependencias de los scripts: `pip install fpdf2` (para `md_to_pdf.py`).
2. Copia `profile/cv_master.example.md` → `profile/cv_master.md`. **Si el usuario ya tiene un CV en otro formato** (Word, PDF, texto pegado, export de LinkedIn), no le pidas que lo reescriba a mano — pídeselo directamente y reestructúralo vos al formato de `cv_master.md`, sin inventar ni omitir nada de lo que compartió.
3. Con `cv_master.md` ya lleno, léelo y proponle al usuario las categorías/keywords para `profile/ats_keywords.md` (copiado desde `ats_keywords.example.md`) y también los `DEFAULT_KEYWORDS` de `scripts/search_jobs.py` — no es una sincronización automática, es un paso que hacés vos como asistente cada vez que el CV cambia significativamente.
4. Copia `profile/job_sources.example.md` → `profile/job_sources.md`. Los 4 agregadores con API pública (RemoteOK, Remotive, Jobicy, Arbeitnow) ya tienen URL real fija y sirven para cualquier campo, no hace falta tocarlos. Para el resto de categorías (nicho de industria, staffing, portales locales, empresas objetivo), investiga opciones concretas para el campo/país del usuario en vez de dejar los placeholders sin completar.
5. Copia `profile/interview_review.example.md` → `profile/interview_review.md` (opcional, se usa después de la primera entrevista real).
6. Nunca subas datos reales del usuario (`cv_master.md`, `applications/`, `PENDING.md` con contenido real) a un repositorio público si este proyecto nació como copia de un repo compartido — agrégalos a `.gitignore`.

## 🗂️ Estructura del proyecto

```
.
├── AGENTS.md                          Esta guía — instrucciones de flujo para el asistente de IA (y para vos)
├── profile/
│   ├── cv_master.md                   CV maestro — toda tu experiencia real, sin editar por vacante (copia cv_master.example.md)
│   ├── cover_letter_template.md       Plantilla base de carta de presentación (placeholders {{ASI}})
│   ├── job_sources.md                 Lista editable de plataformas donde buscar — agrega/quita libremente
│   ├── ats_keywords.md                Vocabulario de keywords para el chequeo ATS — específico a tu campo
│   └── interview_review.md            Log de temas que fallaste en entrevistas reales — revísalo antes de la siguiente
├── scripts/
│   ├── md_to_pdf.py                   Convierte un .md (CV o carta) a PDF ATS-friendly
│   ├── search_jobs.py                 Busca en agregadores remotos con API pública por palabras clave
│   └── ats_check.py                   Compara un CV contra una vacante usando profile/ats_keywords.md
└── applications/
    ├── log.md                         Índice de todas las vacantes vistas/aplicadas
    └── <empresa>-<puesto>/            Una carpeta por vacante a la que aplicás
        ├── cv.md                          CV ajustado a esa vacante (editable en Markdown)
        ├── cover_letter.md                Carta ajustada a esa vacante
        ├── notes.md                       Descripción original de la vacante + notas de fit + rango salarial
        ├── <Tu Nombre> CV.pdf             PDF final para subir
        └── <Tu Nombre> Cover Letter.pdf   PDF final para subir
```

Cada carpeta `applications/<empresa>-<puesto>/` se crea de cero por vacante siguiendo el flujo de abajo — no hace falta crearla a mano.

## 🔄 Flujo estándar para una vacante nueva

1. **Pega el texto de la vacante** (o el link, si se puede leer directo) en la conversación.
2. El asistente evalúa el match contra `profile/cv_master.md` de forma honesta — avisa de vacíos reales antes de escribir nada. Si mencionas experiencia real que falta en el CV maestro, se agrega ahí primero (así queda disponible para futuras vacantes). El match no es solo técnico: si la vacante exige un turno/horario específico o algo incompatible con tu vida, eso también se marca como punto a confirmar antes de avanzar — nunca se asume que lo aceptás solo porque el resto del fit es fuerte. **Si hay señales de duda** (agregador desconocido, salario desalineado con el mercado, sin nombre de empresa visible, o cualquier otra bandera roja) — el asistente verifica la legitimidad de la fuente/empresa antes de seguir, en vez de invertir tiempo preparando CV/carta para algo que podría no ser real. Esto no es un paso automático para toda vacante — solo cuando hay algo que no cuadra.
3. Se crea la carpeta `applications/<empresa>-<puesto>/` con `cv.md` y `cover_letter.md` ajustados — nunca se inventa experiencia. Idioma: se infiere del idioma en que está escrita la vacante, no se pregunta cada vez — pero puedes pedir la otra versión cuando quieras.
4. Se investiga un rango salarial de referencia y se agrega a `notes.md`, junto con la descripción original de la vacante y las notas de fit para tu entrevista.
5. Se corre `ats_check.py` (CV vs. la vacante) y se ajusta la redacción del CV si hay coincidencias de fondo que quedaron con distinta palabra — sin inventar nada, solo alineando el wording a lo que ya es cierto.
6. Se exporta a PDF (ver comando abajo).
7. Se agrega la fila correspondiente a `applications/log.md`, guardando siempre el **link directo a la vacante** en `notes.md` — necesario para poder ubicar después a quién la publicó.
8. Tú subes el PDF al portal y avisas cuando la envíes, para actualizar el estado en el log.
9. **Contacto con reclutador (opcional):** cuando aplicás a una vacante nueva, se puede revisar quién la publicó y redactar un mensaje corto de conexión/seguimiento para que lo envíes tú mismo (nunca lo envía el asistente sin que lo confirmes).

## 🔕 Seguimiento de aplicaciones en silencio

- Si una vacante lleva 1-2 semanas en estado "Aplicado" sin respuesta, no asumas que hay que buscar más vacantes — primero revisa si vale la pena un mensaje de seguimiento al reclutador. Buscar más solo genera más aplicaciones en silencio si el problema real es de conversión, no de volumen.
- Antes de invertir tiempo en un seguimiento, confirma que la vacante sigue activa.

## 📣 Outreach proactivo a reclutadores (sin vacante publicada)

Para empresas con demanda recurrente confirmada para tu perfil, vale la pena identificar reclutadores técnicos vía LinkedIn (búsqueda de personas dentro de la página de la empresa, filtrando por "recruiter"/"talent acquisition") y enviar un mensaje de presentación general, sin esperar a que se abra un req específico. Prioriza contactos de 2º grado (con conexión en común) sobre contactos fríos de 3er+ grado — la tasa de aceptación es mucho más alta.

## 💻 Comandos que puedes correr tú mismo

**Convertir un Markdown a PDF:**
```bash
python3 scripts/md_to_pdf.py "applications/<carpeta>/cv.md" "applications/<carpeta>/<Tu Nombre> CV.pdf"
```

**Buscar vacantes en agregadores con API pública con tus keywords por defecto:**
```bash
python3 scripts/search_jobs.py
```

**Buscar con keywords personalizadas:**
```bash
python3 scripts/search_jobs.py --keywords "keyword1,keyword2,keyword3"
```

**Chequear cobertura ATS de un CV contra una vacante:**
```bash
python3 scripts/ats_check.py --cv "applications/<carpeta>/cv.md" --jd "applications/<carpeta>/notes.md"
```
Compara tu CV contra el texto de la vacante usando el vocabulario de `profile/ats_keywords.md` y dice qué términos coinciden y cuáles faltan — útil para afinar la redacción antes de exportar a PDF. Nota: solo detecta coincidencias de texto exacto (como hace un ATS real), así que un "falta X" puede ser un vacío real o solo una diferencia de redacción — revisa ambos casos.

## 🏢 Portales propios de reclutadoras (Talent Network / ATS del reclutador)

Es común que, después de aplicar, la reclutadora pida un paso adicional: unirte a su "Talent Network" o registrarte en el ATS propio de su agencia. Suele venir con la aclaración de que "no compromete a nada" — es solo para que tengan tu perfil cargado en su sistema.

Cuando pase esto:

- **Con tu permiso explícito, el asistente puede conectarse por navegador y llenar el formulario/perfil directamente** (bio, experiencia, educación, certificaciones, work preferences, self assessment, subir el CV en PDF ya preparado) usando lo que ya está en `profile/cv_master.md` y en la carpeta de esa aplicación específica.
- **Preguntas de nivel de expertise/años por tecnología o área:** se responden con criterio conservador y honesto — nunca se sube el nivel de un gap ya identificado solo para parecer mejor candidato, y se mantiene consistencia con los números que ya usa tu CV.
- **Preguntas de "con qué te gustaría trabajar" (interés) vs. "qué dominás mejor" (dominio):** son preguntas distintas — en la de interés sí se puede incluir herramientas que son gaps reales pero que estás estudiando activamente; en la de dominio, no.
- **Campos de compensación (Current/Expected):** si el formulario da la opción de no revelarlos, mejor declinar — especialmente el salario actual, que puede anclar la oferta hacia abajo. Si el campo es obligatorio, usar un rango (no una cifra fija) para el expected compensation.
- **No se toca el toggle de "looking for a job" / visibilidad del perfil sin que lo decidas vos.**
- **No se hace clic en "Submit"/envío final de un formulario sin haber repasado antes contigo lo que se va a mandar**, salvo que ya se haya acordado el contenido exacto en la conversación.

## ✏️ Editar tu perfil o fuentes de búsqueda

- **Agregar una skill/certificación nueva:** edita `profile/cv_master.md` directamente, o pídeselo al asistente en la conversación.
- **Agregar o quitar una plataforma de búsqueda:** edita `profile/job_sources.md` — es una tabla en Markdown, agrega o borra filas libremente.

## 🔌 Qué es automatizable y qué no

- `profile/job_sources.md` es un documento de **referencia**, no una configuración que el script lea. Las 4 fuentes marcadas `method: api` (RemoteOK, Remotive, Jobicy, Arbeitnow) están consultadas con sus URLs escritas directo dentro de `scripts/search_jobs.py` — agregar una fila nueva marcada `api` en `job_sources.md` no hace que `search_jobs.py` la consulte sola; hay que editar el script y agregar la función correspondiente.
- LinkedIn, Indeed, y la mayoría de portales locales/de staffing no tienen API pública y algunos bloquean lectura automática (403 o requieren JavaScript) → estas se revisan por búsqueda asistida (WebSearch, o navegador si el asistente tiene esa herramienta) en la conversación, no por script.
- **Aplicar/enviar el formulario** siempre lo haces tú manualmente, salvo que le des permiso explícito al asistente para llenar un formulario específico (ver sección de Talent Networks arriba) — nunca tiene acceso a tu sesión de ningún portal por su cuenta.

## 🎓 Después de una entrevista o examen

Cuéntale al asistente qué preguntas te costaron o qué temas no recordaste — se agrega a `profile/interview_review.md` con un repaso rápido, para que quede como referencia antes de tu siguiente entrevista.

Si ya tenés una entrevista agendada con una empresa específica, decíselo al asistente y puede buscar qué tipo de preguntas suelen hacer ahí (Glassdoor, reseñas de entrevistas, etc.) — esto **no se hace automático en cada aplicación**, solo cuando ya hay una entrevista real programada. Junto con esa investigación, puede armar un documento de preparación (guion de presentación, respuestas sugeridas a las preguntas esperadas de esa etapa, y preguntas para que le hagas vos al entrevistador) ajustado al tipo de etapa — screening de RRHH vs. técnica — para no sobre-preparar contenido técnico en una llamada de encaje o viceversa.

## 📊 Estado actual

Consulta `applications/log.md` para ver el estado de cada vacante — el archivo mismo explica sus columnas y los valores válidos de "Estado" en su encabezado. Si querés llevar una lista viva de pendientes/decisiones (barridos recientes, ideas a futuro, notas sueltas), crea un `PENDING.md` siguiendo el mismo espíritu — es opcional, pero ayuda a que el asistente retome el contexto entre sesiones.
