# Proyecto AED: listas enlazadas

En este proyecto usamos Python y Manim para crear una animación sobre las listas enlazadas. El video muestra qué ocurre con los nodos y sus referencias al recorrer, insertar y eliminar elementos.

El ejemplo principal usa los valores 10, 20 y 30. Los nodos se representan con rectángulos, las referencias con flechas y un punto amarillo indica el recorrido.

## Contenido del video

Primero se presenta la estructura de una lista enlazada: sus nodos, la cabeza y el final indicado con `null`. Después se explican las operaciones de recorrido, búsqueda, inserción y eliminación.

También se muestran las listas doblemente enlazadas y las listas circulares. Para los ejemplos se mencionan casos como el historial de navegación y los turnos de una partida.

El resultado principal es `LinkedListLesson_2K.mp4`, con una resolución de **2560 × 1440 píxeles** y **30 fps**. También se incluye una versión en formato MPEG, `LinkedListLesson.mpg`.

## Animación del recorrido

La función `animar_recorrido(nodos, fin)` se usa para explicar cómo se recorre la lista.

Un punto amarillo aparece en el primer nodo. Primero se mueve hacia la referencia de ese nodo y después sigue la flecha hasta el siguiente. Hace lo mismo con los valores 10, 20 y 30. Cuando llega a `null`, se resalta ese texto y el punto desaparece.

Para esta parte usamos `Dot`, un ciclo `for` y `animate.move_to()`. `FadeIn` y `FadeOut` controlan la aparición y desaparición del punto. Toda la animación se genera desde el código; no se utiliza un video externo.

## Organización del código

El código del video está en `linked_list.py`, dentro de la escena `LinkedListLesson`. La función `construct()` organiza las distintas partes de la animación.

Las funciones principales son:

- `crear_nodo()`: crea un nodo con su valor y su referencia.
- `crear_flecha()`: conecta dos elementos con una flecha.
- `cabeza()`: coloca la etiqueta de la cabeza de la lista.
- `cambiar_titulo()`: cambia el título de cada sección.
- `mostrar_parte()`: reproduce una sección durante el tiempo indicado.
- `animar_recorrido()`: mueve el punto amarillo por la lista.

Además, `crear_lista()`, `limpiar_escena()` y `marcar()` ayudan a preparar cada ejemplo, limpiar la escena y resaltar nodos.

La clase `TextoGuardado` permite reutilizar los textos SVG guardados en `media/texts/`.

La duración y el orden de las animaciones están definidos directamente en `linked_list.py`. Por ejemplo, `mostrar_parte(4, ...)` reserva aproximadamente cuatro segundos para una sección. Este programa está hecho para generar el video del proyecto, no para recibir listas introducidas por el usuario.

## Conceptos utilizados

Cada nodo almacena un dato y una referencia al siguiente nodo. La cabeza señala el inicio de la lista y, en una lista simple, el último nodo apunta a `null`.

Buscar un elemento puede costar O(n), porque en el peor caso hay que revisar todos los nodos. Insertar al principio cuesta O(1). Eliminar un nodo también puede hacerse en O(1) si ya conocemos el nodo anterior, aunque encontrar su posición puede costar O(n).

En una lista doble se puede avanzar y retroceder porque cada nodo tiene dos referencias. En una lista circular, el último nodo apunta al primero, por lo que el recorrido necesita una condición de parada distinta de `null`.

## Archivos principales

- `linked_list.py`: código de la animación.
- `manim.cfg`: configuración de la resolución, los fps y la carpeta de salida.
- `requirements.txt`: versión de Manim utilizada.
- `media/texts/`: archivos SVG con los textos de la animación.
- `media/indice_textos.json`: relaciona los nombres de los textos con sus archivos SVG.
- `linked_list.srt`: subtítulos de una versión anterior; no son necesarios para ejecutar el programa.
- `LinkedListLesson_2K.mp4` y `LinkedListLesson.mpg`: videos finales.

## Ejecución

Se necesita Python, Manim 0.21.0 y FFmpeg. Manim también utiliza Cairo y Pango. El proyecto usa la fuente DejaVu Sans, así que no hace falta instalar LaTeX.

Los siguientes comandos se ejecutan desde la carpeta `ProyectoAED1` en Linux. Primero se crea un entorno virtual y se instalan las dependencias. Si el entorno ya existe, se puede reutilizar.

```bash
python -m venv ../.venv
../.venv/bin/python -m pip install -r requirements.txt
```

Para generar el video principal:

```bash
../.venv/bin/python -m manim linked_list.py LinkedListLesson
```

El resultado queda en `media/videos/linked_list/1440p30/LinkedListLesson.mp4`. Para preparar los dos archivos finales:

```bash
ffmpeg -y -i media/videos/linked_list/1440p30/LinkedListLesson.mp4 \
  -c copy -movflags +faststart LinkedListLesson_2K.mp4

ffmpeg -y -i media/videos/linked_list/1440p30/LinkedListLesson.mp4 \
  -c:v mpeg2video -q:v 3 -pix_fmt yuv420p -f mpeg LinkedListLesson.mpg
```

Para revisar un cambio rápidamente se puede agregar `-ql` al comando de Manim. Esta opción genera una vista previa de menor calidad. Para el video final se debe usar el comando sin `-ql`.
