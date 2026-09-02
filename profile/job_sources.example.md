# Fuentes de búsqueda de empleo

Esta es la lista completa de dónde se busca — automatizable y manual. Edítala libremente: agrega o quita filas para ajustar dónde se busca. `method` indica cómo se consulta cada fuente:
- `api` → tiene API pública consultada por `scripts/search_jobs.py`. **Importante:** este archivo es solo referencia, no una configuración que el script lea — las 4 fuentes `api` de abajo ya están conectadas directo en el código de `search_jobs.py`. Agregar una fila nueva con `method: api` acá NO hace que el script la consulte automáticamente; hace falta editar `search_jobs.py` para agregar esa fuente.
- `search` → sin API pública; se consulta por búsqueda asistida (WebSearch o navegador) cada vez
- `manual` → sitio de una sola empresa; se revisa directamente su página de carreras

**Las filas de abajo son solo ejemplos de arranque, no una lista completa ni neutral de industria.** Los 4 agregadores con API (RemoteOK, Remotive, Jobicy, Arbeitnow) están sesgados hacia roles de tecnología — si tu campo no es tech, probablemente no te sirvan y conviene reemplazarlos por agregadores relevantes a tu industria. Edita las categorías, agrega tu país/ciudad en la sección Local, y agrega las empresas específicas que te interesan en "Empresas objetivo".

## Remoto — agregadores con API pública

| Plataforma | URL | Method | Notas |
|---|---|---|---|
| RemoteOK | https://remoteok.com | api | Orientado a tech; buen volumen de roles remoto |
| Remotive | https://remotive.com | api | Orientado a tech |
| Jobicy | https://jobicy.com | api | Filtra por tag; parcialmente orientado a tech pero con categorías más amplias |
| Arbeitnow | https://www.arbeitnow.com | api | Agregador remoto/Europa, buen volumen |

## Remoto — nicho de tu industria (reemplazar)

| Plataforma | URL | Method | Notas |
|---|---|---|---|
| {{Board especializado en tu campo}} | {{URL}} | search | {{Notas}} |

## Agencias de staffing remoto

| Plataforma | URL | Method | Notas |
|---|---|---|---|
| {{Agencia de staffing relevante para tu región/campo}} | {{URL}} | search | {{Notas}} |

## Local — {{tu país/ciudad}}

| Plataforma | URL | Method | Notas |
|---|---|---|---|
| {{Portal de empleo local}} | {{URL}} | search | {{Notas}} |

## General grande (cubre remoto + local + relocation)

| Plataforma | URL | Method | Notas |
|---|---|---|---|
| LinkedIn Jobs | https://www.linkedin.com/jobs | search | Sin API pública gratuita confiable — mejor fuente para muchos campos, requiere sesión logueada |
| Indeed | https://www.indeed.com | search | Sin API pública gratuita confiable |

## Empresas objetivo (páginas directas de carreras)

| Empresa | URL | Method | Notas |
|---|---|---|---|
| {{Empresa donde te interesa trabajar}} | {{URL de careers}} | manual | {{Por qué te interesa / qué roles buscar ahí}} |
