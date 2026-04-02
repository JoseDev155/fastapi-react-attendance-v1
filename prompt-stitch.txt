# ROLE & CONTEXT
Actúa como un Senior Product Designer. Crea el diseño de alta fidelidad para una aplicación web (Desktop) de gestión de asistencias para UBBJ, de México. El diseño debe ser responsive y profesional.

# DATA CONTEXT
1. Usa el archivo .json adjunto para mapear formularios y tablas de los endpoints reales.
2. Usa el archivo .md de arquitectura de backend para INFERIR y diseñar las pantallas de los módulos marcados con (*), basándote en la lógica de carpetas (ej. metrics, reports).

# LAYOUT & NAVIGATION
- FLOW: La primera pantalla es un Login elegante. Tras autenticarse, la página index `/` será un Dashboard modular que muestre opciones según el rol (asume rol de Administrador para el diseño inicial).
- NAVBAR: Basado en el bosquejo de Excalidraw adjunto. Iconos de navegación centrados.
- STATUS BAR (Abajo del Navbar): Muestra el "Nombre del usuario activo" y "Rol" en la esquina superior derecha. 
- NAVEGACIÓN: Incluye un botón de "Regresar" (Página anterior) visible y accesible (preferiblemente en la parte superior izquierda del contenido o como elemento flotante/sticky).
- FOOTER: Estático, con enlaces institucionales.

# VISUAL VIBE (BANKING-EDUCATION HYBRID)
- IDIOMA: Ya que la institución es de México, TODO el contenido de las pantallas debe ser en ESPAÑOL.
- ESTILO: Elegante, minimalista (estética de Banca Digital de alta gama).
- COLORES: Fondo general en Modo Oscuro (Dark Mode). Navbar en color [ROJO/OCRE INSTITUCIONAL]. Contenido central en tonos gris frío y blanco para máxima legibilidad.
- TIPOGRAFÍA: 'Instrument Sans' para títulos y 'Inter' para datos/tablas.
- ICONOGRAFÍA: Librería Lucide con esquinas redondeadas.
- IMÁGENES: Usa el crawling de Google para generar fondos con texturas académicas o fotos de la arquitectura real de la institución.

# SPECIFIC COMPONENTS
- Tablas de asistencia con 'Zebra Striping' sutil y espaciado amplio (high padding).
- Widgets de métricas (KPIs) para el dashboard basados en la carpeta /metrics del .md.