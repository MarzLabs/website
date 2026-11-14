# marzlabs.tech

Sitio web corporativo de **MARZ LABS, S.A.S.** — un sitio institucional, estático y sobrio
que identifica a la empresa como entidad legal y enlaza a sus productos (actualmente
[Fiscaliza.me](https://fiscaliza.me) y [Cuadra](https://marzlabs.gumroad.com/l/cuadra)).

El contenido está en español; los nombres de archivo y las rutas están en inglés por convención.

## Estructura

```
/
├── index.html          → /            (landing)
├── products.html       → /products    (índice de productos)
├── fiscaliza.html      → /fiscaliza   (página de producto: Fiscaliza.me)
├── cuadra.html         → /cuadra      (página de producto: Cuadra)
├── company.html        → /company     (empresa)
├── contact.html        → /contact     (contacto)
├── privacy.html        → /privacy     (política de privacidad)
├── terms.html          → /terms       (términos de uso)
├── sitemap.xml
├── robots.txt
├── favicon.ico         (16/32/48 px, derivado de la marca circular)
├── apple-touch-icon.png (180×180)
├── README.md
└── assets/
    ├── logo.png        (logo horizontal de marca: marca circular + "MARZ LABS")
    ├── styles.css      (hoja de estilos única)
    ├── menu.js         (menú móvil, mejora progresiva)
    ├── og-image.png    (1200×630, tarjeta social)
    └── fonts/
        └── inter-latin.woff2  (Inter variable, subconjunto latin, auto-alojada)
```

## Stack y decisiones técnicas

- **HTML estático + CSS plano, sin dependencias en runtime.** No hay framework de JS ni backend.
  El único JavaScript es `assets/menu.js` (~1 KB): activa el menú hamburguesa en móvil como
  *mejora progresiva*. Sin JS, la navegación sigue siendo visible y funcional.
- **Sin Tailwind por CDN.** La especificación sugería Tailwind vía CDN «para empezar», pero el
  *Play CDN* de Tailwind inyecta un compilador en el navegador (mucho JS, render en cliente) y es
  incompatible con el objetivo de Lighthouse 100/100 en Performance. Para un puñado de páginas simples se optó
  por CSS plano con tokens (variables CSS) en `assets/styles.css`: cero build, cero dependencias,
  rendimiento máximo. Si en el futuro se prefiere Tailwind, conviene un build local con purga
  (`tailwindcss -o assets/styles.css --minify`) en vez del CDN.
- **Tipografía Inter auto-alojada.** Un único `.woff2` (subconjunto *latin*, eje de peso variable
  400–700) servido desde el mismo dominio, con `preload` y `font-display: swap`. No hay peticiones a
  Google Fonts ni a terceros, lo que mantiene la privacidad y el rendimiento. El subconjunto *latin*
  (U+0000–00FF) cubre todos los caracteres del español (á, é, í, ó, ú, ñ, ü, ¿, ¡).
- **Color de acento: terracota de marca `#db7851`** (tomado del logo). Por accesibilidad, el
  terracota brillante solo se usa en gráficos/decorativo (`--accent`); para texto y enlaces se usa
  un terracota más oscuro `#b5532f` (`--accent-ink`, contraste AA ≈ 4.7:1 sobre el fondo) y `#8f3f22`
  para hover (`--accent-strong`). Las tres variables están en `assets/styles.css`. Si se cambia la
  identidad de marca, edítelas y regenere los assets (ver más abajo).
- **Sin analítica ni cookies.** El sitio no instala cookies ni carga scripts de seguimiento.

## Agregar un producto

Cada producto tiene su propia página en la raíz y una tarjeta resumida en el índice:

1. Cree `<producto>.html` en la raíz copiando `fiscaliza.html` y ajuste el `<head>` (título,
   descripción, canonical, Open Graph, Twitter y JSON-LD), la miga de pan y el contenido.
2. Agregue la tarjeta del producto en `products.html` y en `index.html`, con un enlace a la nueva
   página.
3. Agregue la URL a `sitemap.xml`.

Los precios de Cuadra están escritos a mano en `cuadra.html` (tabla de precios y JSON-LD): si
cambian en Gumroad, actualícelos ahí.

## Vista previa local

No requiere build. Cualquier servidor estático sirve. Con Python:

```bash
cd marzlabs.tech
python3 -m http.server 8080
# abrir http://localhost:8080
```

> Nota: las rutas usan barras iniciales (`/products.html`, `/assets/...`), por lo que conviene
> servir desde la raíz del proyecto y no abrir los `.html` con `file://`.

## Despliegue

El sitio es completamente estático: súbalo a cualquier hosting de archivos estáticos.

- **Cloudflare Pages / Netlify / Vercel:** conecte el repositorio o arrastre la carpeta. Sin comando
  de build; el directorio de salida es la raíz del proyecto.
- **GitHub Pages:** publique la rama desde la raíz (`/`). Funciona tal cual.
- **Amazon S3 + CloudFront / Bucket estático:** suba todos los archivos respetando la estructura;
  documento índice `index.html`.

Apunte el dominio `marzlabs.tech` (y `www`, con redirección a la raíz) al proveedor elegido.
Sirva todo por **HTTPS**. Todas las URL canónicas y los metadatos Open Graph ya apuntan a
`https://marzlabs.tech`.

### Cabeceras recomendadas (opcional)

Si el proveedor permite cabeceras personalizadas:

```
# Caché larga para assets versionables
/assets/*    Cache-Control: public, max-age=31536000, immutable
# HTML siempre revalidado
/*.html      Cache-Control: public, max-age=0, must-revalidate
```

## Regenerar iconos y la imagen Open Graph

Los binarios (`favicon.ico`, `apple-touch-icon.png`, `assets/og-image.png`) se derivan de
`assets/logo.png` con un script de Python + Pillow. El favicon y el apple-touch-icon usan la marca
circular (recortada del logo) y la imagen Open Graph usa el logo completo. Si se reemplaza el logo o
se cambia el color de acento, edite los valores al inicio del script y vuelva a ejecutarlo:

```bash
python3 scripts/gen_assets.py
```

> El script de generación se incluye en `scripts/gen_assets.py`. Requiere `Pillow`
> (`pip install Pillow`).

## Accesibilidad y SEO

- Landmarks semánticos (`<header>`, `<nav>`, `<main>`, `<footer>`), enlace «Saltar al contenido»,
  jerarquía de encabezados coherente (un solo `<h1>` por página) y foco visible por teclado.
- Contraste de color verificado contra WCAG 2.1 AA (texto principal ~17:1, acento ~10:1 sobre el
  fondo).
- Cada página tiene `<title>` y `meta description` únicos, etiquetas Open Graph y Twitter Card,
  `<link rel="canonical">`, favicons y `theme-color`.
- `sitemap.xml` y `robots.txt` permiten la indexación completa. La home incluye datos estructurados
  `Organization` (JSON-LD) para apoyar la verificación de la organización ante terceros.

## Qué no incluye (por diseño)

Blog, carreras, casos de estudio, newsletter, formularios de contacto (solo correo directo),
chat/widget de soporte, multilenguaje y modo oscuro. Ver la especificación funcional.
