# Reglas del Proyecto - OculusLab Grafos

Para asegurar la escalabilidad, mantenibilidad y calidad del código, todos los contribuidores deben seguir estas reglas estrictamente:

## 1. Enfoque Modular y Estructurado
El proyecto se basa en una arquitectura modular.
- **División por Secciones:** Cada página (`/pages`) no debe contener lógica de renderizado compleja directamente. Debe dividirse en **secciones** ubicadas en archivos separados dentro de `/sections/[nombre-de-pagina]/`.
- **Layouts:** Se debe utilizar un sistema de layouts manejable para envolver las páginas y asegurar la consistencia visual.
- **Escalabilidad:** Esta estructura es obligatoria para facilitar el debug y la expansión de la terminal.

## 2. Gestión de Deuda Técnica
No se permiten "cabos sueltos" sin documentar.
- **TODO.md:** Siempre que se implementen mocks, botones sin funcionalidad, o apartados inconclusos, es **OBLIGATORIO** registrarlo en el archivo `TODO.md` de la raíz.
- **Transparencia:** Esto permite que el equipo sepa exactamente qué falta por conectar o pulir.

## 3. Garantía de Build
La estabilidad de la rama principal es prioridad.
- **Verificación:** Cada vez que se implemente, modifique o manipule cualquier parte del proyecto, se debe ejecutar el comando de build (`npm run build` o `yarn build`).
- **Éxito Obligatorio:** No se considera terminada una tarea hasta que la build sea exitosa y libre de errores de linting o tipos.

## 4. Flujo de Commits
El historial de cambios debe ser reflejo de estados estables.
- **Timing:** Solo se realizarán commits después de que la build haya sido exitosa y los cambios hayan sido verificados visualmente.
- **Integridad:** Un commit debe representar una pieza de funcionalidad que no rompa el sistema.

## 5. Uso de Componentes y Estilos 
Priorizamos la velocidad de desarrollo y la coherencia visual.
- **ShadCN Primero:** SIEMPRE usa componentes de ShadCN. Si un componente necesario no está instalado, instálalo usando el CLI (`npx shadcn@latest add ...`) antes de considerar crear uno desde cero.
- **Sin Hardcoding:** Nunca "postconfigures" componentes con colores hardcodeados en los `classNames`.
- **Uso del Tema:** Todas las variaciones visuales deben hacerse utilizando las variables del tema por defecto (`primary`, `muted`, `accent`, etc.) para asegurar que el modo oscuro y los cambios de tema funcionen automáticamente.
- **Prohibido el uso de Emojis:** El uso de emojis SIEMPRE está prohibido, cada vez que encuentres un emoji en el código o insertes uno, reemplazalo por un icono de PhosphorIcons
- **Manipulación de CSS:** Está terminantemente prohibido la modificación sin autorización del CSS del proyecto, siempre usar los colores establecidos desde un inicio en el proyecto.

---
*Estas reglas están diseñadas para que OculusLab Grafos sea un producto de ingeniería de clase mundial.*
