from pathlib import Path
import json
from manim import *

FONDO = '#101827'
BLANCO = '#EDF3FC'
GRIS = '#A9B8CF'
VERDE = '#40D9C0'
AMARILLO = '#FFCC66'
#color del fondo del video
config.background_color = FONDO
RUTA_INDICE = Path(__file__).with_name('media') / 'indice_textos.json'
if RUTA_INDICE.exists():
    INDICE_TEXTOS = json.loads(RUTA_INDICE.read_text())
else:
    INDICE_TEXTOS = {}


class TextoGuardado(Text):

    #busca los textos que ya guardamos con nombre
    def _text2svg(self, color):
        nombre_original = self._text2hash(color) + '.svg'
        registro = INDICE_TEXTOS.get(nombre_original)
        if registro is None:
            return super()._text2svg(color)
        destino = config.get_dir('text_dir') / registro['archivo']
        if not destino.exists():
            archivo_generado = Path(super()._text2svg(color))
            archivo_generado.rename(destino)
        return str(destino.resolve())


#crea los textos con la misma fuente
def texto(text, size=28, color=BLANCO):
    return TextoGuardado(text, font='DejaVu Sans', font_size=size, color=color)


class LinkedListLesson(Scene):

    #dibuja un nodo con su dato y su referencia
    def crear_nodo(self, valor, x, y=0):
        caja = RoundedRectangle(width=1.65,
            height=0.85,
            corner_radius=0.12,
            stroke_color=VERDE,
            fill_color='#1E3448',
            fill_opacity=1)
        division = Line([0.28, -0.425, 0], [0.28, 0.425, 0], color=VERDE)
        numero = texto(str(valor), 30).move_to([-0.28, 0, 0])
        punto = Dot([0.57, 0, 0], radius=0.055, color=VERDE)
        return VGroup(caja, division, numero, punto).move_to([x, y, 0])

    #une dos nodos con una flecha
    def crear_flecha(self, izquierda, derecha, color=VERDE):
        return Arrow(izquierda.get_right(),
            derecha.get_left(),
            buff=0.12,
            color=color,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.18)

    #etiqueta de la cabeza
    def cabeza(self, nodo):
        nombre = texto('cabeza', 24, AMARILLO).move_to(nodo.get_top() + UP * 0.9)
        flecha = Arrow(nombre.get_bottom(), nodo.get_top(), buff=0.1, color=AMARILLO)
        return VGroup(nombre, flecha)

    #cambia el título de la sección
    def cambiar_titulo(self, num, titulo):
        if hasattr(self, 'titulo_actual'):
            self.play(FadeOut(self.titulo_actual), run_time=0.25)
        self.titulo_actual = VGroup(texto(f'{num:02} / 09', 20, VERDE), texto(titulo, 36))
        self.titulo_actual.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UL, buff=0.55)
        self.play(FadeIn(self.titulo_actual, shift=RIGHT * 0.15), run_time=0.4)

    #repoduce y completa los movimientos 
    def mostrar_parte(self, duracion, *animaciones, secuencia=()):
        inicio = self.time
        if animaciones:
            self.play(*animaciones, run_time=1.1)
        else:
            self.wait(1.1)
        for animacion in secuencia:
            self.play(animacion, run_time=0.7)
        # Ajusta las pausas a fotogramas completos para mantener los 2:30.
        fps = config.frame_rate
        fotogramas_restantes = round(duracion * fps) - round((self.time - inicio) * fps)
        self.wait(max(round(0.8 * fps), fotogramas_restantes) / fps - 1e-8)

    # Esta función mueve un punto por la lista de este video.
    def animar_recorrido(self, nodos, fin):
        punto = Dot(nodos[0].get_center(), radius=0.1, color=AMARILLO)
        self.play(FadeIn(punto), run_time=0.3)
        for i in range(len(nodos)):
            self.play(punto.animate.move_to(nodos[i].get_right()), run_time=0.3)
            if i < len(nodos) - 1:
                destino = nodos[i + 1].get_center()
            else:
                destino = fin.get_center()
            self.play(punto.animate.move_to(destino), run_time=0.6)
        self.play(Indicate(fin, color=AMARILLO), run_time=0.6)
        self.play(FadeOut(punto), run_time=0.3)

    #une las partes del video
    def construct(self):
        titulo = VGroup(texto('LISTA ENLAZADA', 66, VERDE),
            texto('Linked list', 34),
            texto('Nodos · referencias · operaciones', 24, GRIS)).arrange(DOWN,
            buff=0.45)
        self.add(titulo)
        self.wait(5)
        self.remove(titulo)

        #quita los dibujos anteriores para pasar al siguente punto
        def limpiar_escena(num, titulo):
            objetos = [o for o in self.mobjects if o is not getattr(self, 'titulo_actual', None)]
            if objetos:
                self.play(*[FadeOut(o) for o in objetos], run_time=0.4)
            self.cambiar_titulo(num, titulo)

        #crea una lista xd
        def crear_lista():
            nodos = [self.crear_nodo(v, x) for v, x in zip([10, 20, 30], [-3.8, -0.5, 2.8])]
            fin = texto('null', 28, GRIS).move_to([5.3, 0, 0])
            flechas = [self.crear_flecha(nodos[0], nodos[1]),
                self.crear_flecha(nodos[1], nodos[2]),
                self.crear_flecha(nodos[2], fin)]
            cabeza = self.cabeza(nodos[0])
            self.add(*nodos, *flechas, fin, cabeza)
            return (nodos, flechas, fin, cabeza)

        #el nodo que revisamos
        def marcar(obj):
            return SurroundingRectangle(obj, color=AMARILLO, buff=0.12, corner_radius=0.12)

        self.cambiar_titulo(1, 'Una secuencia de nodos')
        nodos, flechas, fin, cabeza = crear_lista()
        a, b, c = nodos
        self.mostrar_parte(110 / 30, *[Indicate(n, color=VERDE) for n in nodos])
        etiquetas = VGroup(texto('dato', 22, GRIS).move_to([-4.1, -0.9, 0]),
            texto('referencia', 22, VERDE).move_to([-2.1, -0.9, 0]))
        self.mostrar_parte(89 / 30, FadeIn(etiquetas), Indicate(a))
        self.play(FadeOut(etiquetas), run_time=0.3)
        self.mostrar_parte(82 / 30, Indicate(cabeza))
        cursor = marcar(a)
        self.mostrar_parte(136 / 30,
            Create(cursor),
            secuencia=[Transform(cursor, marcar(b)), Transform(cursor, marcar(c)), Transform(cursor, marcar(fin))])
        self.play(FadeOut(cursor), run_time=0.3)
        self.mostrar_parte(82 / 30, *[Indicate(n[2]) for n in nodos])
        self.mostrar_parte(165 / 30, secuencia=[Indicate(cabeza), Indicate(flechas[0]), Indicate(flechas[1])])
        self.mostrar_parte(82 / 30, Indicate(fin))
        self.remove(*flechas, cabeza)
        flechas_moviles = [always_redraw(lambda: self.crear_flecha(a, b)),
            always_redraw(lambda: self.crear_flecha(b, c)),
            always_redraw(lambda: self.crear_flecha(c, fin))]
        self.add(*flechas_moviles)
        self.mostrar_parte(110 / 30, a.animate.shift(UP * 0.55), b.animate.shift(DOWN * 0.6), c.animate.shift(UP * 0.35))
        for flecha in flechas_moviles:
            flecha.clear_updaters()

        limpiar_escena(2, 'Recorrer y buscar')
        nodos, flechas, fin, cabeza = crear_lista()
        a, b, c = nodos
        self.mostrar_parte(82 / 30, Indicate(cabeza))
        cursor = marcar(a)
        self.animar_recorrido(nodos, fin)
        self.wait(1)
        destino = texto('Buscar 30: comparar cada dato', 27, AMARILLO).move_to([0, -1.25, 0])
        self.mostrar_parte(149 / 30,
            FadeIn(destino),
            Create(cursor),
            secuencia=[Transform(cursor, marcar(b)), Transform(cursor, marcar(c)), Indicate(c, color=AMARILLO)])
        costo = texto('Búsqueda: O(n) en el peor caso', 27, AMARILLO).move_to(destino)
        self.mostrar_parte(102 / 30, ReplacementTransform(destino, costo))

        limpiar_escena(3, 'Insertar: conectar sin perder la lista')
        a, b, c = [self.crear_nodo(v, x) for v, x in zip([10, 20, 30], [-1.5, 1.3, 4.1])]
        ab, bc = (self.crear_flecha(a, b), self.crear_flecha(b, c))
        cabeza = self.cabeza(a)
        fin = texto('null', 24, GRIS).move_to([6, 0, 0])
        self.add(a, b, c, ab, bc, cabeza, fin, self.crear_flecha(c, fin))
        self.mostrar_parte(82 / 30, Indicate(cabeza))
        nuevo = self.crear_nodo(5, -4.3)
        na = self.crear_flecha(nuevo, a)
        self.mostrar_parte(157 / 30, FadeIn(nuevo), secuencia=[Create(na), Transform(cabeza, self.cabeza(nuevo))])
        intermedio = self.crear_nodo(15, -0.1, -1.3)
        mb = Arrow(intermedio.get_right(), b.get_bottom(), buff=0.12, color=VERDE)
        am = Arrow(a.get_bottom(), intermedio.get_left(), buff=0.12, color=AMARILLO)
        self.mostrar_parte(195 / 30,
            Indicate(a, color=AMARILLO),
            secuencia=[FadeIn(intermedio), Create(mb), AnimationGroup(FadeOut(ab), Create(am))])

        limpiar_escena(4, 'Eliminar: localizar y reconectar')
        nodos, flechas, fin, cabeza = crear_lista()
        a, b, c = nodos
        cursor = marcar(a)
        puente = CurvedArrow(a.get_bottom() + DOWN * 0.08,
            c.get_bottom() + DOWN * 0.08,
            angle=PI / 3,
            color=AMARILLO)
        self.mostrar_parte(161 / 30,
            Create(cursor),
            secuencia=[Transform(cursor, marcar(b)), AnimationGroup(Create(puente), FadeOut(flechas[0]), FadeOut(flechas[1])), AnimationGroup(FadeOut(b), FadeOut(cursor))])
        self.mostrar_parte(94 / 30,
            Transform(cabeza, self.cabeza(c)),
            secuencia=[AnimationGroup(FadeOut(a), FadeOut(puente))])
        nota = VGroup(texto('Reconectar: O(1), con el anterior localizado', 25, VERDE),
            texto('Localizar: O(n) en el peor caso', 25, AMARILLO)).arrange(DOWN,
            buff=0.25).move_to([0, -1.25, 0])
        self.mostrar_parte(127 / 30, FadeIn(nota))

        limpiar_escena(5, 'Simple y doblemente enlazada')
        nodos, flechas, fin, cabeza = crear_lista()
        a, b, c = nodos
        self.mostrar_parte(93 / 30, *[Indicate(l) for l in flechas])
        self.play(FadeOut(cabeza), run_time=0.3)
        flechas_atras = [Arrow(derecha.get_left() + DOWN * 0.23, izquierda.get_right() + DOWN * 0.23, buff=0.12, color=AMARILLO) for izquierda,
            derecha in zip(nodos, nodos[1:])]
        self.play(*[l.animate.shift(UP * 0.2) for l in flechas[:2]], run_time=0.4)
        referencias_extra = VGroup(*[Dot(n.get_left() + RIGHT * 0.18 + DOWN * 0.22, radius=0.055, color=AMARILLO) for n in nodos])
        nulo_anterior = texto('null', 22, GRIS).move_to([-5.9, 0, 0])
        extremo = VGroup(Arrow(a.get_left(), nulo_anterior.get_right(), buff=0.12, color=AMARILLO), nulo_anterior)
        self.mostrar_parte(119 / 30, *[Create(l) for l in flechas_atras], FadeIn(referencias_extra), FadeIn(extremo))
        nota = texto('siguiente + anterior = una referencia extra por nodo', 25, AMARILLO).move_to([0, -1.35, 0])
        cursor = marcar(a)
        self.mostrar_parte(166 / 30,
            FadeIn(nota),
            Create(cursor),
            secuencia=[Transform(cursor, marcar(b)), Transform(cursor, marcar(c)), Transform(cursor, marcar(b)), Transform(cursor, marcar(a))])

        limpiar_escena(6, 'Circular: el último vuelve al primero')
        nodos, flechas, fin, cabeza = crear_lista()
        a, b, c = nodos
        self.mostrar_parte(82 / 30, Indicate(VGroup(*nodos)))
        vuelta = CurvedArrow(c.get_bottom() + DOWN * 0.1,
            a.get_bottom() + DOWN * 0.1,
            angle=-PI / 3,
            color=AMARILLO)
        self.mostrar_parte(82 / 30, FadeOut(fin), FadeOut(flechas[2]), Create(vuelta))
        nota = texto('Puede ser simple o doble', 27, VERDE).move_to([0, 1.4, 0])
        self.mostrar_parte(82 / 30, FadeIn(nota))
        parada = texto('Parar al volver al nodo inicial', 27, AMARILLO).move_to(nota)
        cursor = marcar(a)
        self.mostrar_parte(149 / 30,
            ReplacementTransform(nota, parada),
            Create(cursor),
            secuencia=[Transform(cursor, marcar(b)), Transform(cursor, marcar(c)), Transform(cursor, marcar(a))])

        limpiar_escena(7, 'Aplicaciones: pila y cola')
        pregunta = texto('¿Cómo necesitamos acceder a los datos?', 35, VERDE)
        self.mostrar_parte(82 / 30, FadeIn(pregunta))
        self.play(FadeOut(pregunta), run_time=0.3)
        nodos, flechas, fin, cabeza = crear_lista()
        a, b, c = nodos
        etiqueta = texto('PILA · insertar y retirar por el inicio', 29, AMARILLO).move_to([0, -1.25, 0])
        self.mostrar_parte(123 / 30, FadeIn(etiqueta), Indicate(cabeza), secuencia=[Indicate(a, color=AMARILLO)])
        final = texto('final', 24, AMARILLO).move_to(c.get_top() + UP * 0.9)
        flecha_final = Arrow(final.get_bottom(), c.get_top(), buff=0.1, color=AMARILLO)
        etiqueta_cola = texto('COLA · retirar al inicio / agregar al final', 29, VERDE).move_to(etiqueta)
        self.mostrar_parte(123 / 30,
            ReplacementTransform(etiqueta, etiqueta_cola),
            FadeIn(final),
            Create(flecha_final),
            secuencia=[Indicate(a), Indicate(c)])

        limpiar_escena(8, 'Aplicaciones: historial y turnos')
        paginas = VGroup(*[RoundedRectangle(width=3, height=1.05, corner_radius=0.12, color=VERDE) for _ in range(3)]).arrange(RIGHT,
            buff=1)
        nombres = VGroup(*[texto(t, 27).move_to(p) for t, p in zip(['Inicio', 'Artículo', 'Perfil'], paginas)])
        flechas = VGroup(*[DoubleArrow(paginas[i].get_right(), paginas[i + 1].get_left(), buff=0.1, color=AMARILLO) for i in range(2)])
        cursor = marcar(paginas[1])
        self.mostrar_parte(136 / 30,
            FadeIn(paginas),
            FadeIn(nombres),
            Create(flechas),
            Create(cursor),
            secuencia=[Transform(cursor, marcar(paginas[0])), Transform(cursor, marcar(paginas[1]))])
        self.play(FadeOut(paginas), FadeOut(nombres), FadeOut(flechas), FadeOut(cursor), run_time=0.4)
        jugadores = [self.crear_nodo(v, x) for v, x in zip(['A', 'B', 'C'], [-3.8, 0, 3.8])]
        flechas_turnos = VGroup(self.crear_flecha(jugadores[0], jugadores[1]),
            self.crear_flecha(jugadores[1], jugadores[2]),
            CurvedArrow(jugadores[2].get_bottom() + DOWN * 0.1, jugadores[0].get_bottom() + DOWN * 0.1, angle=-PI / 3, color=AMARILLO))
        cursor = marcar(jugadores[0])
        self.mostrar_parte(149 / 30,
            *[FadeIn(p) for p in jugadores],
            Create(flechas_turnos),
            Create(cursor),
            secuencia=[Transform(cursor, marcar(jugadores[1])), Transform(cursor, marcar(jugadores[2])), Transform(cursor, marcar(jugadores[0]))])

        limpiar_escena(9, 'Elegir según el recorrido y los cambios')
        nodos, flechas, fin, cabeza = crear_lista()
        self.mostrar_parte(85 / 30, *[Indicate(n) for n in nodos])
        nota = texto('Ventaja: ajustar conexiones en un lugar conocido', 26, VERDE).move_to([0, -1.25, 0])
        self.mostrar_parte(110 / 30, FadeIn(nota))
        limite = texto('Límite: acceder a una posición requiere recorrer', 26, AMARILLO).move_to(nota)
        self.mostrar_parte(149 / 30, ReplacementTransform(nota, limite), secuencia=[Indicate(n) for n in nodos])
        self.play(*[FadeOut(o) for o in [*nodos, *flechas, fin, cabeza, limite]], run_time=0.4)
        tipos = VGroup(texto('SIMPLE', 34, VERDE),
            texto('DOBLE', 34, AMARILLO),
            texto('CIRCULAR', 34, VERDE)).arrange(RIGHT,
            buff=1.25)
        resumen = texto('Dirección del recorrido · inserciones · eliminaciones', 26, GRIS).move_to([0, -1.1, 0])
        self.mostrar_parte(106 / 30, FadeIn(tipos), FadeIn(resumen))
        self.wait(55 / 30)
