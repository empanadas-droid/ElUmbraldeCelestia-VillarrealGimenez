import pygame
import sys
import random

# ==========================================
# 1. INICIALIZACIÓN Y CONFIGURACIÓN BASE
# ==========================================
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
ANCHO, ALTO = 1600, 720

pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN | pygame.SCALED) 
pygame.display.set_caption("El Umbral de Celestia - MVP")
reloj = pygame.time.Clock()

canal_pasos_jugador = pygame.mixer.Channel(0)
canal_pasos_ente = pygame.mixer.Channel(1)
canal_efectos = pygame.mixer.Channel(2) 
canal_tension = pygame.mixer.Channel(3) 

# Paleta de colores
NEGRO_FONDO = (10, 10, 18)
BLANCO_TEXTO = (240, 240, 255)
VIOLETA_UI = (35, 20, 55)
VIOLETA_CLARO = (75, 45, 110)
ROJO_SANGRE = (160, 35, 35)
VERDE_OK = (45, 190, 110)
GRIS_MUEBLES = (90, 90, 105)
MARRON_ARMARIO = (110, 70, 45)
PASILLO_OSCURO = (15, 8, 8)  
ORO_CAJA = (210, 165, 60)
GRIS_DISPLAY = (30, 40, 30)  

# Fuentes tipográficas
fuente_titulos = pygame.font.SysFont("Arial", 54, bold=True)
fuente_subtitulos = pygame.font.SysFont("Arial", 28)
fuente_pixel = pygame.font.SysFont("Courier New", 36, bold=True)
fuente_documento = pygame.font.SysFont("Courier New", 22, bold=False)

# Cooldowns de audio
ULTIMO_PASO_JUGADOR = 0
COOLDOWN_PASO_JUGADOR = 450  
ULTIMO_PASO_ENTE = 0
COOLDOWN_PASO_ENTE = 600     

inventario = []
codigo_recogido = False   
ficha_recogida = False    
nota_camilla_recogida = False
puzzle_fusibles_resuelto = False
item_inspeccionando = None 

# Configuración botones menú de inicio
ancho_btn, alto_btn = 235, 72
pos_y_botones = 615
btn_jugar_rect = pygame.Rect(392, pos_y_botones, ancho_btn, alto_btn)
btn_registros_rect = pygame.Rect(680, pos_y_botones, ancho_btn, alto_btn)
btn_salir_rect = pygame.Rect(970, pos_y_botones, ancho_btn, alto_btn)

# ==========================================
# NUEVA CONFIGURACIÓN DE INVENTARIO (PEGADO ABAJO)
# ==========================================
ANCHO_BARRA_INV = 460
ALTO_BARRA_INV = 120
X_BARRA_INV = (ANCHO // 2) - (ANCHO_BARRA_INV // 2)
Y_BARRA_INV = ALTO - ALTO_BARRA_INV - 5

# Slots interactivos recalculados automáticamente en base a la nueva Y_BARRA_INV
slot_codigo_rect = pygame.Rect(X_BARRA_INV + 20, Y_BARRA_INV + 10, 100, 100)
slot_ficha_rect = pygame.Rect(X_BARRA_INV + 170, Y_BARRA_INV + 10, 100, 100)
slot_nota_rect = pygame.Rect(X_BARRA_INV + 320, Y_BARRA_INV + 10, 100, 100)

intensidad_distorsion = 0

# Parpadeos de luces
ultimo_parpadeo = 0
durante_parpadeo = False
fin_parpadeo = 0

# Variables cinematica
tiempo_inicio_cinematica = 0
fase_cinematica = 1

# --- DECLARACIÓN DE AUDIOS ---
sonido_puerta = sonido_reja_abrir = sonido_armario = pasos_recepcionista = pasos_investigadora = sonido_tension = mostrar_ficha1 = None
pasos_exterior = golpe_seco = portazo = None
sonido_abrir_archivador = sonido_cerrar_archivador = sonido_abrir_caja = None



try: 
    musica_inicio= pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\musica_inicio.MPEG")
except Exception: musica_inicio = None

try: sonido_puerta = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\puerta_armario2.MPEG")
except Exception: sonido_puerta = None
try: sonido_reja_abrir = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\abrir_reja2.MPEG")
except Exception: sonido_reja_abrir = None
try: sonido_armario = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\puerta_armario2.MPEG")
except Exception: sonido_armario = None
try: pasos_recepcionista = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\pasos_recepcionista2.MPEG")
except Exception: pasos_recepcionista = None
try: pasos_investigadora = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\pasos_investigadora2.MPEG")
except Exception: pasos_investigadora = None
try: mostrar_ficha1 = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\muestro_ficha1.MPEG")
except Exception: mostrar_ficha1 = None
try: sonido_tension = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\musica_tension.MPEG")
except Exception: sonido_tension = None
try: pasos_exterior = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\pasos_exterior.MP3")
except Exception: pasos_exterior = None
try: golpe_seco = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\golpe_seco.MPEG")
except Exception: golpe_seco = None
# Carga de la secuencia de sonidos para la entrada al hospital
try: portazo = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\portazo.MPEG")
except Exception: portazo = None
try: snd_forcejeo = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\forzar_puerta.MPEG")
except Exception: snd_forcejeo = None
try: snd_rechinar = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\rechinido_puerta.MPEG")
except Exception: snd_rechinar = None

# Variable global de control de la secuencia de audio
paso_secuencia_puerta = 0

# NUEVOS EFECTOS DE SONIDO SOLICITADOS
try: sonido_abrir_archivador = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\abrir_archivador.MPEG")
except Exception: sonido_abrir_archivador = None
try: sonido_cerrar_archivador = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\cerrar_archivador.MPEG")
except Exception: sonido_cerrar_archivador = None
try: sonido_abrir_caja = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\abrir_caja.MPEG")
except Exception: sonido_abrir_caja = None

try:
    sonido_ok = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\sonido_ok.MPEG")
except:
    sonido_ok = None

try:
    sonido_error = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\sonido_error.MPEG")
except:
    sonido_error = None

# ==========================================
# 2. FUNCIONES AUXILIARES Y CLASES
# ==========================================
def cargar_animacion_sheet(ruta_archivo, filas, columnas, ancho_cuadro_orig, alto_cuadro_orig, escala_ancho, escala_alto):
    sheet = pygame.image.load(ruta_archivo).convert_alpha()
    animaciones = []
    for fila in range(filas):
        lista_fila = []
        for col in range(columnas):
            superficie_cuadro = pygame.Surface((ancho_cuadro_orig, alto_cuadro_orig), pygame.SRCALPHA)
            superficie_cuadro.fill((0, 0, 0, 0))
            superficie_cuadro.blit(sheet, (0, 0), (col * ancho_cuadro_orig, fila * alto_cuadro_orig, ancho_cuadro_orig, alto_cuadro_orig))
            lista_fila.append(pygame.transform.scale(superficie_cuadro, (escala_ancho, escala_alto)))
        animaciones.append(lista_fila)
    return animaciones

def aplicar_parpadeo_luces(superficie):
    global ultimo_parpadeo, durante_parpadeo, fin_parpadeo
    tiempo_actual = pygame.time.get_ticks()
    
    if not durante_parpadeo:
        if tiempo_actual - ultimo_parpadeo > random.randint(3000, 7000):
            durante_parpadeo = True
            fin_parpadeo = tiempo_actual + random.randint(80, 250)
    else:
        if tiempo_actual < fin_parpadeo:
            filtro_oscuro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            filtro_oscuro.fill((5, 5, 10, random.randint(120, 210)))
            superficie.blit(filtro_oscuro, (0, 0))
        else:
            durante_parpadeo = False
            ultimo_parpadeo = tiempo_actual

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x_inicio, y_inicio):
        super().__init__()
        self.ancho, self.alto = 130, 195
        self.velocidad = 6  
        self.esta_escondido = False
        
        try:
            cuadros_base = cargar_animacion_sheet("C:\\Users\\sofia\\Downloads\\videojuego\\investigadora\\spritesheet_investigadora3.png", 2, 3, 800, 800, self.ancho, self.alto)
            self.anim_derecha = [cuadros_base[1][2], cuadros_base[0][2], cuadros_base[1][0]]
            self.anim_izquierda = [cuadros_base[0][0], cuadros_base[0][1], cuadros_base[1][1]]
            self.usando_sprites_reales = True
        except Exception:
            self.usando_sprites_reales = False
            self.image = pygame.Surface((self.ancho, self.alto)); self.image.fill((60, 110, 240))

        self.lista_actual = self.anim_derecha if self.usando_sprites_reales else None
        self.indice_cuadro = self.contador_tiempo = 0
        if self.usando_sprites_reales: self.image = self.lista_actual[self.indice_cuadro]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_inicio, y_inicio

    def controlar_movimiento(self, ancho_limite):
        global ULTIMO_PASO_JUGADOR
        if self.esta_escondido: return

        teclas = pygame.key.get_pressed()
        moviendose = False

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            if self.rect.x > 0:
                self.rect.x -= self.velocidad
                if self.usando_sprites_reales: self.lista_actual = self.anim_izquierda
                moviendose = True
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            if self.rect.x < ancho_limite - self.ancho:
                self.rect.x += self.velocidad
                if self.usando_sprites_reales: self.lista_actual = self.anim_derecha
                moviendose = True

        if moviendose:
            if self.usando_sprites_reales:
                self.contador_tiempo += 1
                if self.contador_tiempo > 5: 
                    self.indice_cuadro = (self.indice_cuadro + 1) % len(self.lista_actual)
                    self.image = self.lista_actual[self.indice_cuadro]
                    self.contador_tiempo = 0
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - ULTIMO_PASO_JUGADOR > COOLDOWN_PASO_JUGADOR:
                if pasos_investigadora:
                    canal_pasos_jugador.set_volume(0.35)
                    canal_pasos_jugador.play(pasos_investigadora)
                ULTIMO_PASO_JUGADOR = tiempo_actual
        elif not moviendose and self.usando_sprites_reales:
            self.indice_cuadro = 0 
            self.image = self.lista_actual[self.indice_cuadro]

    def dibujar(self, superficie, camara_x=0):
        superficie.blit(self.image, (self.rect.x - camara_x, self.rect.y))

class Entidad(pygame.sprite.Sprite):
    def __init__(self, x_inicio, y_inicio, x_limite_izq, x_limite_der):
        super().__init__()
        self.ancho, self.alto = 130, 250
        self.velocidad = 3
        self.limite_izq, self.limite_der = x_limite_izq, x_limite_der
        self.direccion = 1 

        try:
            self.hojas_recortadas = cargar_animacion_sheet("C:\\Users\\sofia\\Downloads\\videojuego\\recepcionista\\spritesheet_recepcionista3.png", 2, 2, 1200, 1200, self.ancho, self.alto)
            self.anim_derecha, self.anim_izquierda = self.hojas_recortadas[0], self.hojas_recortadas[1]
            self.usando_sprites_reales = True
        except Exception:
            self.usando_sprites_reales = False
            self.image = pygame.Surface((self.ancho, self.alto)); self.image.fill((140, 30, 30))

        self.indice_cuadro = self.contador_tiempo = 0
        self.lista_actual = self.anim_derecha if self.usando_sprites_reales else None
        if self.usando_sprites_reales: self.image = self.lista_actual[self.indice_cuadro]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_inicio, y_inicio

    def actualizar_patrulla(self, jugador_x, cuarto_actual):
        global ULTIMO_PASO_ENTE, intensidad_distorsion
        self.rect.x += self.velocidad * self.direccion

        if self.rect.x >= self.limite_der:
            self.direccion = -1
            if self.usando_sprites_reales: self.lista_actual = self.anim_izquierda
        elif self.rect.x <= self.limite_izq:
            self.direccion = 1
            if self.usando_sprites_reales: self.lista_actual = self.anim_derecha

        if self.usando_sprites_reales:
            self.contador_tiempo += 1
            if self.contador_tiempo > 10:
                self.indice_cuadro = (self.indice_cuadro + 1) % len(self.lista_actual)
                self.image = self.lista_actual[self.indice_cuadro]
                self.contador_tiempo = 0
                
        distancia = abs(self.rect.x - jugador_x)
        tiempo_actual = pygame.time.get_ticks()

        if cuarto_actual == "PASILLO":
            # Aumentamos el rango a 600 para que la tensión comience desde más lejos
            if distancia < 600:
                intensidad_distorsion = int((1.0 - (distancia / 600)) * 10) 
                
                volumen = max(0.1, 1.0 - (distancia / 600))
                if sonido_tension and not canal_tension.get_busy():
                    canal_tension.play(sonido_tension, loops=-1)
                canal_tension.set_volume(volumen * 0.6)

                if pasos_recepcionista and (tiempo_actual - ULTIMO_PASO_ENTE > COOLDOWN_PASO_ENTE):
                    canal_pasos_ente.set_volume(volumen * 0.5)
                    canal_pasos_ente.play(pasos_recepcionista)
                    ULTIMO_PASO_ENTE = tiempo_actual
            else:
                intensidad_distorsion = 0
                canal_tension.stop()
        else:
            intensidad_distorsion = 0
            canal_tension.stop()

# ==========================================
# 3. CONFIGURACIÓN DEL ESCENARIO Y OBJETOS
# ==========================================
investigador = Jugador(100, 330)
recepcionista = Entidad(1400, 285, 200, 2000)
# Lista / Grupo de los Ecos (Sombras)
ecos_grupo = []

def cargar_img(ruta, dims, alpha=False):
    try:
        img = pygame.image.load(ruta)
        return pygame.transform.scale(img.convert_alpha() if alpha else img.convert(), dims), True
    except Exception: return None, False

# 1. Función para crear el círculo de luz sobre la investigadora
def dibujar_circulo_vision(superficie, pos_jugador, radio=170):
    sombra = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 248)) # Oscuridad casi total
    
    # Recortar el círculo de luz sobre el personaje (transparente)
    pygame.draw.circle(sombra, (0, 0, 0, 0), pos_jugador, radio)
    # Borde difuminado
    pygame.draw.circle(sombra, (0, 0, 0, 120), pos_jugador, radio + 15, width=15)
    
    superficie.blit(sombra, (0, 0))

# 2. Función para dibujar/animar la sombra del Eco por el techo dinámicamente
def crear_sprite_eco(ancho=70, alto=70):
    eco_surf = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    centro = (ancho // 2, alto // 2)
    
    # Núcleo latente oscuro
    radio_cuerpo = 22 + random.randint(-3, 3) # Efecto de palpitar
    pygame.draw.circle(eco_surf, (15, 15, 20, 230), centro, radio_cuerpo)
    
    # Halo transparente (Aura)
    pygame.draw.circle(eco_surf, (0, 0, 0, 90), centro, radio_cuerpo + 8)
    
    # Ojos brillantes
    pygame.draw.circle(eco_surf, (220, 40, 40, 250), (centro[0] - 8, centro[1] + 4), 3)
    pygame.draw.circle(eco_surf, (220, 40, 40, 250), (centro[0] + 8, centro[1] + 4), 3)
    
    return eco_surf

# Clase para controlar a la sombra corriendo en el techo
class EcoTecho:
    def __init__(self, x, y_techo=100):
        self.x = x
        self.y = y_techo
        self.velocidad = random.randint(4, 7)
        self.image = crear_sprite_eco()

    def actualizar(self):
        self.x += self.velocidad
        # Si sale por la derecha, reaparece por la izquierda
        if self.x > ANCHO + 100:
            self.x = -100
        # Regenera la forma para que 'palpite' mientras camina
        self.image = crear_sprite_eco()

    def dibujar(self, superficie):
        superficie.blit(self.image, (self.x, self.y))

imagen_pabellon, usar_pabellon_real = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\ala_dormitorios.png", (ANCHO, ALTO))
imagen_inicio, usar_inicio_real = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\INICIO2.png", (ANCHO, ALTO))
imagen_ficha, usar_ficha_real = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\ingresos-egresos.png", (750, 500), True)
imagen_sala_interior, usar_sala_interior_real = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\sala_registros2.png", (1600, 720))

imagen_pad_reja, usar_pad_reja = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\pad_numeros.png", (500, 600), True)
imagen_pad_caja, usar_pad_caja = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\pad_numeros.png", (500, 600), True)
imagen_interior_caja, usar_interior_caja = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\interior_cajafuerte.png", (800, 600), True)
imagen_interior_archivador, usar_interior_archivador = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\interior_archivador.png", (800, 500), True)
# --- NUEVAS IMÁGENES PARA EL NIVEL 2 ---
# --- LISTA DE IMÁGENES PROGRESIVAS PARA LA CAJA DE FUSIBLES ---
imagenes_fusibles = []
usar_fusibles_animados = True

for i in range(1, 6):  # Carga cajafusibles_1.png, cajafusibles_2.png, ..., cajafusibles_5.png
    ruta_img = f"C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\cajafusibles_{i}.png"
    img, exito = cargar_img(ruta_img, (600, 450), True)
    if exito:
        imagenes_fusibles.append(img)
    else:
        usar_fusibles_animados = False
imagen_nota_camilla, usar_nota_camilla = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\nota_camilla.png", (500, 650), True)
# Crear versión pequeña para el inventario
mini_nota_camilla = pygame.transform.scale(imagen_nota_camilla, (80, 80)) if usar_nota_camilla else None
# Crear versión grande para vista de examen
grande_nota_camilla = pygame.transform.scale(imagen_nota_camilla, (600, 780)) if usar_nota_camilla else None
# -------------------------------------------------------------
# 1. CARGA DE IMÁGENES EN ALTA RESOLUCIÓN (Para que no se pixele al agrandar)
# -------------------------------------------------------------
imagen_codigo_sprite, usar_codigo_sprite = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\sprite_codigo.png", (500, 500), True)
imagen_ficha_celestia, usar_ficha_celestia = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\ficha_celestia.png", (1500, 1000), True)

# -------------------------------------------------------------
# 2. VERSIONES PEQUEÑAS PARA EL INVENTARIO (80x80)
# -------------------------------------------------------------
mini_codigo_sprite = pygame.transform.scale(imagen_codigo_sprite, (80, 80)) if usar_codigo_sprite else None
mini_ficha_celestia = pygame.transform.scale(imagen_ficha_celestia, (80, 80)) if usar_ficha_celestia else None

# -------------------------------------------------------------
# 3. VERSIONES MEDIANAS PARA DENTRO DEL ARCHIVADOR Y LA CAJA FUERTE (200x200)
# -------------------------------------------------------------
sprite_codigo_caja = pygame.transform.scale(imagen_codigo_sprite, (200, 250)) if usar_codigo_sprite else None
sprite_ficha_caja = pygame.transform.scale(imagen_ficha_celestia, (250, 300)) if usar_ficha_celestia else None

# -------------------------------------------------------------
# 4. VERSIONES GRANDES Y NÍTIDAS PARA VISTA EXAMEN
# -------------------------------------------------------------
grande_codigo_sprite = pygame.transform.scale(imagen_codigo_sprite, (450, 450)) if usar_codigo_sprite else None
grande_ficha_celestia = pygame.transform.scale(imagen_ficha_celestia, (750, 600)) if usar_ficha_celestia else None

# Rectángulos de interacción dentro de los contenedores emergentes
rect_codigo_clickeable = pygame.Rect(700, 260, 200, 200)
# REAJUSTADO: Ubicación del sprite de la ficha en el centro inferior del contenedor interior de la caja fuerte
rect_ficha_clickeable = pygame.Rect(700, 230, 200, 200)

# ==========================================
# IMÁGENES DE LA CINEMÁTICA (3 ESCENAS)
# ==========================================
escena1, _ = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\escena1.png", (ANCHO, ALTO))
escena2, _ = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\escena2.png", (ANCHO, ALTO))
escena3, _ = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\escena3.png", (ANCHO, ALTO))

# Configuración de las 3 escenas de la historia
escenas_cinematica = [
    {
        "imagen": escena1,
        "texto": "1995. Tenía solo 8 años cuando escuché los susurros sobre el hospital Monte de los Olivos y las extrañas desapariciones.",
        "duracion": 10000 # Duración en milisegundos (10 segundos)
    },
    {
        "imagen": escena2,
        "texto": "Pasé mi adolescencia buscando respuestas, uniendo pistas y notas sobre la internación de mi madre...",
        "duracion": 10000 # Duración en milisegundos (10 segundos)  
    },
    {
        "imagen": escena3,
        "texto": "Hoy, años después, vine a buscar la verdad por mi propia cuenta. No hay vuelta atrás.",
        "duracion": 10000 # Duración en milisegundos (10 segundos)
    }
]

# Variables de control de la cinemática
indice_escena_actual = 0
tiempo_inicio_escena = 0

try:
    imagen_fondo_original = pygame.image.load("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\hospital_admision_fondo.png").convert()
    ANCHO_MUNDO_ESCALADO = int(imagen_fondo_original.get_width() * (ALTO / imagen_fondo_original.get_height()))
    imagen_fondo = pygame.transform.scale(imagen_fondo_original, (ANCHO_MUNDO_ESCALADO, ALTO))
    ANCHO_NIVEL_REAL = ANCHO_MUNDO_ESCALADO
    usar_fondo_real = True
except Exception:
    ANCHO_NIVEL_REAL = 3200; usar_fondo_real = False

mostrar_ficha = False

escritorio_rect = pygame.Rect(1050, 480, 160, 100)  
armario1_rect = pygame.Rect(300, 350, 100, 230) 
armario2_rect = pygame.Rect(800, 350, 100, 230)
armario3_rect = pygame.Rect(1500, 350, 100, 230)    
reja_rect = pygame.Rect(2100, 260, 160, 200) 
puerta_1b_rect = pygame.Rect(1200, 290, 120, 210) 
cajafusibles_rect = pygame.Rect(300, 350, 500, 230) 
camilla_rect = pygame.Rect(1050, 480, 160, 100) 
ANCHO_SALA_INTERIOR = 1600 

# REAJUSTADO: Rectángulo de la Caja Fuerte hecho notablemente más grande para que se aprecie mejor la animación
caja_fuerte_interior_rect = pygame.Rect(1000, 250, 150, 250) 

archivador_interior_rect = pygame.Rect(300, 400, 130, 230)
puerta_salida_interior_rect = pygame.Rect(40, 290, 100, 200) 

cuarto_actual = "PASILLO" 
pasillo_guardado_x = 100   
camara_x = 0 

ancho_apertura_reja = 0 
ancho_apertura_caja = 0
reja_abierta = False
caja_fuerte_abierta = False
texto_codigo_ingresado = ""
tiempo_espera_cambio = 0

# --- NUEVAS VARIABLES PARA EL NIVEL 2 ---
# 1. Transición con Zoom
escala_zoom = 1.0
tiempo_inicio_zoom = 0
duracion_zoom = 1500  # 1.5 segundos en milisegundos

# 2. Luz UV y Parpadeo
luz_uv_activa = False
tiempo_inicio_uv = 0
puzzle_fusibles_resuelto = False

# 3. Datos del Puzzle de Fusibles
texto_codigo_fusibles = ""
respuesta_correcta_fusibles = "26"  # Ejemplo de cálculo: (4 * 5) + 6
estado_visual_fusibles = "NORMAL"  # NORMAL, ERROR, CORRECTO
tiempo_cambio_visual_fusibles = 0

INICIO, REGISTROS, CINEMATICA, TRANSICION_PUERTA, JUEGO, PAD_REJA, PAD_CAJA, ANIM_REJA, ANIM_CAJA, INTERIOR_ARCHIVADOR, INTERIOR_CAJA, VISTA_EXAMEN, VICTORIA, GAMEOVER, TRANSICION_ZOOM, PUZZLE_FUSIBLES, PUZZLE_COFRE = (
    "Bienvenida", "Registros", "Cinematica", "TRANSICION_PUERTA", "Juego", "PadReja", "PadCaja", "AnimReja", "AnimCaja", "InteriorArchivador", "InteriorCaja", "VistaExamen", "Ganaste", "Perdiste", "TRANSICION_ZOOM", "PuzzleFusibles", "PuzzleCofre"
)
estado_actual = INICIO

lienzo_juego = pygame.Surface((ANCHO, ALTO))

def dibujar_inventario_roblox(superficie):
    """Renderiza el HUD del inventario flotante centrado con alineación calibrada de miniaturas."""
    barra_surf = pygame.Surface((ANCHO_BARRA_INV, ALTO_BARRA_INV), pygame.SRCALPHA)
    barra_surf.fill((20, 20, 20, 160))
    superficie.blit(barra_surf, (X_BARRA_INV, Y_BARRA_INV))
    pygame.draw.rect(superficie, (100, 100, 100), (X_BARRA_INV, Y_BARRA_INV, ANCHO_BARRA_INV, ALTO_BARRA_INV), 2, border_radius=4)
    
    if len(inventario) == 0:
        texto_vac = fuente_subtitulos.render("Inventario Vacío", True, (150, 150, 150))
        superficie.blit(texto_vac, (X_BARRA_INV + (ANCHO_BARRA_INV // 2) - (texto_vac.get_width() // 2), Y_BARRA_INV + 45))
    else:
        if "Código Caja Fuerte" in inventario:
            pygame.draw.rect(superficie, VIOLETA_CLARO, slot_codigo_rect, border_radius=5)
            pygame.draw.rect(superficie, ORO_CAJA, slot_codigo_rect, 2, border_radius=5)
            if mini_codigo_sprite:
                # Centrado perfecto del sprite de 80x80 dentro del slot de 100x100
                superficie.blit(mini_codigo_sprite, (slot_codigo_rect.x + 10, slot_codigo_rect.y + 10))
            else:
                superficie.blit(fuente_pixel.render("CODE", True, ORO_CAJA), (slot_codigo_rect.x + 10, slot_codigo_rect.y + 30))
            
        if "Ficha Celestia" in inventario:
            pygame.draw.rect(superficie, VIOLETA_CLARO, slot_ficha_rect, border_radius=5)
            pygame.draw.rect(superficie, ORO_CAJA, slot_ficha_rect, 2, border_radius=5)
            if mini_ficha_celestia:
                # Centrado perfecto del sprite de 80x80 dentro del slot de 100x100
                superficie.blit(mini_ficha_celestia, (slot_ficha_rect.x + 10, slot_ficha_rect.y + 10))
            else:
                superficie.blit(fuente_pixel.render("DOC", True, ORO_CAJA), (slot_ficha_rect.x + 15, slot_ficha_rect.y + 30))
        
        if "Nota Camilla" in inventario:
            pygame.draw.rect(superficie, VIOLETA_CLARO, slot_nota_rect, border_radius=5)
            pygame.draw.rect(superficie, ORO_CAJA, slot_nota_rect, 2, border_radius=5)
            if mini_nota_camilla:
                # Centrado perfecto del sprite de 80x80 dentro del slot de 100x100
                superficie.blit(mini_nota_camilla, (slot_nota_rect.x + 10, slot_nota_rect.y + 10))
            else:
                superficie.blit(fuente_pixel.render("NOTA", True, ORO_CAJA), (slot_nota_rect.x + 15, slot_nota_rect.y + 30))

def obtener_objetivo_actual():
    # Objetivos del Nivel 2 (Dormitorios)
    if cuarto_actual == "DORMITORIOS":
        if not luz_uv_activa:
            return "Objetivo: Resuelve el puzzle de la caja de fusibles para activar la luz UV."
        elif not nota_camilla_recogida:
            return "Objetivo: Busca la nota en la camilla."
        else:
            return "Objetivo: Explora los dormitorios y busca más pistas."
    
    # Objetivos del Nivel 1 (Pasillo y Sala de Registros)
    # 1. Si no ha abierto la reja pero ya tiene el código o la ficha
    if not reja_abierta:
        if not caja_fuerte_abierta:
            if not codigo_recogido:
                return "Objetivo: Explora la Sala de Registros y busca el código."
            else:
                return "Objetivo: Abre la caja fuerte en la Sala de Registros."
        else:
            if not ficha_recogida:
                return "Objetivo: Inspecciona la caja fuerte para recoger la Ficha."
            else:
                return "Objetivo: Usa el código en el teclado de la Reja Principal."
    else:
        return "Objetivo: ¡Escapa de la Recepcionista por el pasillo!"

def dibujar_barra_objetivos(superficie):
    texto_obj = obtener_objetivo_actual()
    
    # Renderizamos el texto
    surf_texto = fuente_documento.render(texto_obj, True, (240, 240, 240))
    
    ancho_caja = surf_texto.get_width() + 30
    alto_caja = 40
    x, y = 20, 20  # Posición superior izquierda
    
    # Fondo semi-transparente estilo UI
    caja_ui = pygame.Surface((ancho_caja, alto_caja), pygame.SRCALPHA)
    caja_ui.fill((15, 15, 25, 200)) # Fondo oscuro transparente
    
    # Borde violeta/gris
    pygame.draw.rect(caja_ui, (80, 60, 110), caja_ui.get_rect(), 2, border_radius=6)
    
    # Dibujamos en la pantalla
    superficie.blit(caja_ui, (x, y))
    superficie.blit(surf_texto, (x + 15, y + 8))


# ==========================================
# 4. BUCLE PRINCIPAL DE JUEGO
# ==========================================
jugando = True
while jugando:
    pos_mouse = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        
        # -------------------------------------------------------------
        # EVENTOS DE TECLADO (KEYDOWN)
        # -------------------------------------------------------------
        elif evento.type == pygame.KEYDOWN:
            # 1. Salir o regresar con ESC
            if evento.key == pygame.K_ESCAPE:
                if estado_actual in [PAD_REJA, PAD_CAJA, INTERIOR_ARCHIVADOR, INTERIOR_CAJA, VISTA_EXAMEN, PUZZLE_FUSIBLES]: 
                    estado_actual = JUEGO
                else: 
                    jugando = False
            
            # 2. Avanzar la cinemática con ESPACIO o ENTER
            elif estado_actual == CINEMATICA:
                if evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                    indice_escena_actual += 1
                    tiempo_inicio_escena = pygame.time.get_ticks()
                    
                    if indice_escena_actual >= len(escenas_cinematica):
                        # Transición hacia la puerta
                        estado_actual = "TRANSICION_PUERTA"
                        paso_secuencia_puerta = 0
                        if snd_forcejeo:
                            canal_efectos.play(snd_forcejeo)

            # 3. Volver desde la pantalla de registros
            elif estado_actual == REGISTROS: 
                estado_actual = INICIO
            
            # 4. Teclado numérico de Reja y Caja Fuerte
            elif estado_actual in [PAD_REJA, PAD_CAJA]:
                if evento.key == pygame.K_BACKSPACE: 
                    texto_codigo_ingresado = texto_codigo_ingresado[:-1]
                elif evento.key == pygame.K_RETURN:
                    if estado_actual == PAD_REJA:
                        if texto_codigo_ingresado == "12":
                            reja_abierta = True
                            texto_codigo_ingresado = ""
                            if sonido_reja_abrir: canal_efectos.play(sonido_reja_abrir)
                            estado_actual = ANIM_REJA
                            tiempo_espera_cambio = pygame.time.get_ticks()
                        else: 
                            texto_codigo_ingresado = ""
                    
                    elif estado_actual == PAD_CAJA:
                        if texto_codigo_ingresado == "170695":
                            caja_fuerte_abierta = True
                            if sonido_abrir_caja: canal_efectos.play(sonido_abrir_caja)
                            estado_actual = ANIM_CAJA
                            tiempo_espera_cambio = pygame.time.get_ticks()
                        else: 
                            texto_codigo_ingresado = ""
                else:
                    if evento.unicode.isdigit() and len(texto_codigo_ingresado) < 7:
                        texto_codigo_ingresado += evento.unicode

            # 5. Interacción en el Puzzle de Fusibles
            elif estado_actual == PUZZLE_FUSIBLES:
                if evento.key == pygame.K_RETURN:
                    # Validar la respuesta introducida
                    if texto_codigo_fusibles == respuesta_correcta_fusibles:
                        estado_visual_fusibles = "CORRECTO"
                        tiempo_cambio_visual_fusibles = pygame.time.get_ticks()
                        luz_uv_activa = True
                        tiempo_inicio_uv = pygame.time.get_ticks()
                        puzzle_fusibles_resuelto = True
                        if sonido_ok: canal_efectos.play(sonido_ok)
                    else:
                        estado_visual_fusibles = "ERROR"
                        tiempo_cambio_visual_fusibles = pygame.time.get_ticks()
                        texto_codigo_fusibles = ""
                        if sonido_error: canal_efectos.play(sonido_error)
                        
                elif evento.key == pygame.K_BACKSPACE:
                    texto_codigo_fusibles = texto_codigo_fusibles[:-1]
                    estado_visual_fusibles = "NORMAL"
                    
                elif evento.unicode.isdigit() and len(texto_codigo_fusibles) < 3:
                    texto_codigo_fusibles += evento.unicode
                    estado_visual_fusibles = "NORMAL"

            # 6. Acciones e interacciones dentro del mapa del JUEGO
            elif estado_actual == JUEGO:
                if mostrar_ficha: 
                    mostrar_ficha = False
                else:
                    # --- INTERACCIONES EN EL PASILLO ---
                    if cuarto_actual == "PASILLO":
                        if evento.key == pygame.K_e:
                            if cerca_del_armario1 or cerca_del_armario2 or cerca_del_armario3:
                                investigador.esta_escondido = not investigador.esta_escondido
                                if sonido_armario: canal_efectos.play(sonido_armario)
                            elif cerca_del_escritorio:
                                mostrar_ficha = True
                                if mostrar_ficha1: canal_efectos.play(mostrar_ficha1)
                            elif cerca_de_puerta_1b:
                                pasillo_guardado_x = investigador.rect.x 
                                cuarto_actual = "SALA_REGISTROS"
                                investigador.rect.x = 180 
                                if sonido_puerta: canal_efectos.play(sonido_puerta)
                            elif cerca_de_la_reja and not reja_abierta:
                                texto_codigo_ingresado = ""
                                estado_actual = PAD_REJA

                        # Transición de nivel si cruza la reja abierta hacia la derecha
                        elif reja_abierta and investigador.rect.x > 1400:
                            estado_actual = "TRANSICION_ZOOM"
                            tiempo_inicio_zoom = pygame.time.get_ticks()
                            ecos_grupo = [EcoTecho(-100, 110), EcoTecho(-500, 130)]

                    # --- INTERACCIONES EN LA SALA DE REGISTROS ---
                    elif cuarto_actual == "SALA_REGISTROS":
                        if evento.key == pygame.K_e:
                            if cerca_de_la_salida_interior:
                                cuarto_actual = "PASILLO"
                                investigador.rect.x = pasillo_guardado_x 
                                if sonido_puerta: canal_efectos.play(sonido_puerta)
                            elif cerca_del_archivador_interior:
                                if sonido_abrir_archivador: canal_efectos.play(sonido_abrir_archivador)
                                estado_actual = INTERIOR_ARCHIVADOR 
                            elif cerca_de_la_caja_interior:
                                if not caja_fuerte_abierta:
                                    texto_codigo_ingresado = ""
                                    estado_actual = PAD_CAJA
                                else:
                                    estado_actual = INTERIOR_CAJA

                    # --- INTERACCIONES EN LOS DORMITORIOS (NIVEL 2) ---
                    elif cuarto_actual == "DORMITORIOS":
                        if evento.key == pygame.K_e:
                            # 1. Cerca de la Caja de Fusibles (ajustado al rectángulo modificado: x=300, ancho=500)
                            if 250 <= investigador.rect.x <= 800:
                                estado_actual = PUZZLE_FUSIBLES
                                texto_codigo_fusibles = ""
                            
                            # 2. Cerca de la Camilla (En el centro, ajustado a posición visual)
                            elif 350 <= investigador.rect.x <= 650:
                                item_inspeccionando = "Nota Camilla"
                                estado_actual = VISTA_EXAMEN

        # -------------------------------------------------------------
        # EVENTOS DE RATÓN (MOUSEBUTTONDOWN)
        # -------------------------------------------------------------
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_actual == INICIO:
                if btn_jugar_rect.collidepoint(pos_mouse): 
                    estado_actual = CINEMATICA
                    indice_escena_actual = 0
                    tiempo_inicio_escena = pygame.time.get_ticks()
                    if musica_inicio: canal_pasos_jugador.play(musica_inicio)
                elif btn_registros_rect.collidepoint(pos_mouse): 
                    estado_actual = REGISTROS
                elif btn_salir_rect.collidepoint(pos_mouse): 
                    jugando = False
                
            elif estado_actual == JUEGO:
                if "Código Caja Fuerte" in inventario and slot_codigo_rect.collidepoint(pos_mouse):
                    item_inspeccionando = "Código Caja Fuerte"
                    if mostrar_ficha1: canal_efectos.play(mostrar_ficha1)
                    estado_actual = VISTA_EXAMEN
                elif "Ficha Celestia" in inventario and slot_ficha_rect.collidepoint(pos_mouse):
                    item_inspeccionando = "Ficha Celestia"
                    if mostrar_ficha1: canal_efectos.play(mostrar_ficha1)
                    estado_actual = VISTA_EXAMEN
                elif "Nota Camilla" in inventario and slot_nota_rect.collidepoint(pos_mouse):
                    item_inspeccionando = "Nota Camilla"
                    if mostrar_ficha1: canal_efectos.play(mostrar_ficha1)
                    estado_actual = VISTA_EXAMEN

            elif estado_actual == INTERIOR_ARCHIVADOR:
                if rect_codigo_clickeable.collidepoint(pos_mouse) and not codigo_recogido:
                    inventario.append("Código Caja Fuerte")
                    codigo_recogido = True
                    if sonido_cerrar_archivador: canal_efectos.play(sonido_cerrar_archivador)
                    estado_actual = JUEGO

            elif estado_actual == INTERIOR_CAJA:
                if rect_ficha_clickeable.collidepoint(pos_mouse) and not ficha_recogida:
                    inventario.append("Ficha Celestia")
                    ficha_recogida = True
                    estado_actual = JUEGO

            elif estado_actual == VISTA_EXAMEN:
                if item_inspeccionando == "Nota Camilla" and not nota_camilla_recogida:
                    # Recoger la nota al hacer clic
                    inventario.append("Nota Camilla")
                    nota_camilla_recogida = True
                    if mostrar_ficha1: canal_efectos.play(mostrar_ficha1)
                    estado_actual = JUEGO
                else:
                    estado_actual = JUEGO


    # ==========================================
    # ACTUALIZACIONES LÓGICAS JUEGO
    # ==========================================
    tiempo_actual = pygame.time.get_ticks()

    if estado_actual == ANIM_REJA:
        if ancho_apertura_reja < reja_rect.width:
            ancho_apertura_reja += 3.5  
        if tiempo_actual - tiempo_espera_cambio > 2000:  
            # Cambiado para ir a TRANSICION_ZOOM en lugar de VICTORIA
            estado_actual = "TRANSICION_ZOOM"
            tiempo_inicio_zoom = pygame.time.get_ticks()
            ecos_grupo = [EcoTecho(-100, 110), EcoTecho(-500, 130)]

    elif estado_actual == ANIM_CAJA:
        if ancho_apertura_caja < caja_fuerte_interior_rect.width:
            ancho_apertura_caja += 0.85
        if tiempo_actual - tiempo_espera_cambio > 4500:  
            estado_actual = INTERIOR_CAJA

    # Lógica para volver al juego después de resolver el puzzle de fusibles
    if estado_actual == PUZZLE_FUSIBLES and estado_visual_fusibles == "CORRECTO":
        if pygame.time.get_ticks() - tiempo_cambio_visual_fusibles > 2000:  # 2 segundos de feedback
            estado_actual = JUEGO
            estado_visual_fusibles = "NORMAL"

    # TRANSICION_ZOOM se evalúa de manera independiente a JUEGO
    if estado_actual == "TRANSICION_ZOOM":
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_inicio_zoom > 1500:
            cuarto_actual = "DORMITORIOS"
            investigador.rect.x = 100
            estado_actual = JUEGO

    elif estado_actual == JUEGO:
        if not mostrar_ficha:
            ancho_limite_actual = ANCHO_NIVEL_REAL if cuarto_actual == "PASILLO" else ANCHO_SALA_INTERIOR
            investigador.controlar_movimiento(ancho_limite_actual)
        
        recepcionista.actualizar_patrulla(investigador.rect.x, cuarto_actual)
        
        if cuarto_actual == "PASILLO":
            camara_x = max(0, min(investigador.rect.x - ANCHO // 2, ANCHO_NIVEL_REAL - ANCHO))
            cerca_del_escritorio = escritorio_rect.x - 60 < investigador.rect.x < escritorio_rect.x + escritorio_rect.width
            cerca_del_armario1 = armario1_rect.x - 60 < investigador.rect.x < armario1_rect.x + armario1_rect.width
            cerca_del_armario2 = armario2_rect.x - 60 < investigador.rect.x < armario2_rect.x + armario2_rect.width
            cerca_del_armario3 = armario3_rect.x - 60 < investigador.rect.x < armario3_rect.x + armario3_rect.width
            cerca_de_la_reja = reja_rect.x - 100 < investigador.rect.x < reja_rect.x
            cerca_de_puerta_1b = puerta_1b_rect.x - 60 < investigador.rect.x < puerta_1b_rect.x + puerta_1b_rect.width

            if not investigador.esta_escondido and investigador.rect.colliderect(recepcionista.rect):
                estado_actual = GAMEOVER

        elif cuarto_actual == "SALA_REGISTROS":
            camara_x = 0
            cerca_de_la_salida_interior = investigador.rect.x < 200
            cerca_de_la_caja_interior = caja_fuerte_interior_rect.x - 60 < investigador.rect.x < caja_fuerte_interior_rect.x + caja_fuerte_interior_rect.width
            cerca_del_archivador_interior = archivador_interior_rect.x - 60 < investigador.rect.x < archivador_interior_rect.x + archivador_interior_rect.width

        # -------------------------------------------------------------
         # CONTROL DE LA TRANSICIÓN HACIA EL NIVEL 2
        # -------------------------------------------------------------
        elif estado_actual == "TRANSICION_ZOOM":
            tiempo_actual = pygame.time.get_ticks()
                        
            # Espera 1.5 segundos (1500 ms) haciendo el zoom/espera antes de cambiar
            if tiempo_actual - tiempo_inicio_zoom > 1500:
                cuarto_actual = "DORMITORIOS"  # Cambia la sala al Nivel 2
                investigador.rect.x = 100       # Reubica al jugador a la izquierda
                estado_actual = JUEGO           # Vuelve al estado normal de juego

# ==========================================
    # --- RENDERIZADO GENERAL ---
    # ==========================================
    if estado_actual == INICIO:
        if usar_inicio_real: 
            pantalla.blit(imagen_inicio, (0, 0))
        else: 
            pantalla.fill(NEGRO_FONDO)
        
        col_jugar = VIOLETA_CLARO if btn_jugar_rect.collidepoint(pos_mouse) else VIOLETA_UI
        col_reg = VIOLETA_CLARO if btn_registros_rect.collidepoint(pos_mouse) else VIOLETA_UI
        col_salir = ROJO_SANGRE if btn_salir_rect.collidepoint(pos_mouse) else VIOLETA_UI

        pygame.draw.rect(pantalla, col_jugar, btn_jugar_rect, border_radius=6)
        pygame.draw.rect(pantalla, col_reg, btn_registros_rect, border_radius=6)
        pygame.draw.rect(pantalla, col_salir, btn_salir_rect, border_radius=6)

        pantalla.blit(fuente_subtitulos.render("JUGAR", True, BLANCO_TEXTO), (btn_jugar_rect.x + 105, btn_jugar_rect.y + 15))
        pantalla.blit(fuente_subtitulos.render("REGISTROS", True, BLANCO_TEXTO), (btn_registros_rect.x + 80, btn_registros_rect.y + 15))
        pantalla.blit(fuente_subtitulos.render("SALIR", True, BLANCO_TEXTO), (btn_salir_rect.x + 110, btn_salir_rect.y + 15))

    elif estado_actual == REGISTROS:
        pantalla.fill(VIOLETA_UI)
        pantalla.blit(fuente_subtitulos.render("Presiona cualquier tecla para volver...", True, ORO_CAJA), (500, 550))

    elif estado_actual == CINEMATICA:
        tiempo_actual = pygame.time.get_ticks()
        
        if tiempo_inicio_escena == 0:
            tiempo_inicio_escena = tiempo_actual

        escena = escenas_cinematica[indice_escena_actual]
        tiempo_transcurrido = tiempo_actual - tiempo_inicio_escena
        duracion_escena = escena["duracion"]

        pantalla.fill((0, 0, 0))

        # 1. Dibujar la imagen de la escena actual
        if escena["imagen"]:
            img_dibujo = escena["imagen"][0] if isinstance(escena["imagen"], tuple) else escena["imagen"]
            pantalla.blit(img_dibujo, (0, 0))

        # 2. Lógica de la animación estilo "Máquina de Escribir"
        texto_completo = escena["texto"]
        velocidad_escritura = 40  
        caracteres_a_mostrar = min(len(texto_completo), tiempo_transcurrido // velocidad_escritura)
        texto_animado = texto_completo[:caracteres_a_mostrar]

        # 3. Dibujar texto sin recuadro (con sombra)
        if texto_animado:
            pos_x = ANCHO // 2
            pos_y = ALTO - 80

            # Sombra negra
            texto_sombra = fuente_subtitulos.render(texto_animado, True, (0, 0, 0))
            pantalla.blit(texto_sombra, (pos_x - texto_sombra.get_width() // 2 + 2, pos_y + 2))

            # Texto blanco
            texto_render = fuente_subtitulos.render(texto_animado, True, BLANCO_TEXTO)
            pantalla.blit(texto_render, (pos_x - texto_render.get_width() // 2, pos_y))

        # 4. Indicador flotante para saltar
        info_saltar = fuente_documento.render("Presiona [ESPACIO] para avanzar", True, (160, 180, 190))
        pantalla.blit(info_saltar, (ANCHO - 360, ALTO - 35))

        # 5. LÓGICA DE TRANSICIÓN (FADE IN Y FADE OUT)
        TIEMPO_FADE = 1000
        alpha = 0

        if tiempo_transcurrido < TIEMPO_FADE:
            alpha = int((1 - (tiempo_transcurrido / TIEMPO_FADE)) * 255)
        elif duracion_escena - tiempo_transcurrido < TIEMPO_FADE:
            tiempo_restante = duracion_escena - tiempo_transcurrido
            alpha = int((1 - (tiempo_restante / TIEMPO_FADE)) * 255)

        if alpha > 0:
            capa_fade = pygame.Surface((ANCHO, ALTO))
            capa_fade.fill((0, 0, 0))
            capa_fade.set_alpha(max(0, min(255, alpha)))
            pantalla.blit(capa_fade, (0, 0))

        # 6. Cambio al finalizar todas las escenas de la cinemática
        if tiempo_transcurrido > duracion_escena:
            indice_escena_actual += 1
            tiempo_inicio_escena = tiempo_actual
            
            if indice_escena_actual >= len(escenas_cinematica):
                estado_actual = "TRANSICION_PUERTA"
                paso_secuencia_puerta = 0
                
                if snd_forcejeo:
                    canal_efectos.play(snd_forcejeo)

    elif estado_actual == "TRANSICION_PUERTA":
        pantalla.fill((0, 0, 0))

        if paso_secuencia_puerta == 0:
            if not canal_efectos.get_busy():
                paso_secuencia_puerta = 1
                if snd_rechinar: canal_efectos.play(snd_rechinar)

        elif paso_secuencia_puerta == 1:
            if not canal_efectos.get_busy():
                paso_secuencia_puerta = 2
                if portazo: canal_efectos.play(portazo)

        elif paso_secuencia_puerta == 2:
            if not canal_efectos.get_busy():
                cuarto_actual = "PASILLO"
                investigador.rect.x = 100
                investigador.esta_escondido = False
                estado_actual = JUEGO

                canal_pasos_jugador.stop()
                pygame.mixer.music.stop()

                try:
                    pygame.mixer.music.load("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\musica_ambiental.MPEG")
                    pygame.mixer.music.set_volume(0.15)
                    pygame.mixer.music.play(-1)
                except Exception:
                    pass

    elif estado_actual in [JUEGO, PAD_REJA, PAD_CAJA, ANIM_REJA, ANIM_CAJA, INTERIOR_ARCHIVADOR, INTERIOR_CAJA, VISTA_EXAMEN, PUZZLE_FUSIBLES]:
        # 1. Dibujar el mapa según el cuarto actual
        if cuarto_actual == "PASILLO":
            if usar_fondo_real: 
                lienzo_juego.blit(imagen_fondo, (-camara_x, 0))
            else: 
                lienzo_juego.fill(NEGRO_FONDO)

            if reja_abierta or estado_actual == ANIM_REJA:
                pygame.draw.rect(lienzo_juego, PASILLO_OSCURO, (1925 - camara_x, reja_rect.y, ancho_apertura_reja, reja_rect.height))

            if investigador.esta_escondido:
                pygame.draw.rect(lienzo_juego, VIOLETA_UI, (550, 50, 500, 60), border_radius=8)
                lienzo_juego.blit(fuente_subtitulos.render("Presiona [E] para SALIR del armario", True, BLANCO_TEXTO), (570, 65))
            elif cerca_del_armario1 or cerca_del_armario2 or cerca_del_armario3:
                pygame.draw.rect(lienzo_juego, VIOLETA_UI, (550, 50, 500, 60), border_radius=8)
                lienzo_juego.blit(fuente_subtitulos.render("Presiona [E] para ESCONDERTE", True, BLANCO_TEXTO), (590, 65))

            if cerca_de_la_reja and not reja_abierta:
                pygame.draw.rect(lienzo_juego, VIOLETA_UI, (550, 50, 500, 60), border_radius=8)
                lienzo_juego.blit(fuente_subtitulos.render("Presiona [E] para usar teclado de la Reja", True, BLANCO_TEXTO), (560, 65))

            if cerca_de_puerta_1b:
                pygame.draw.rect(lienzo_juego, VIOLETA_UI, (550, 50, 500, 60), border_radius=8)
                lienzo_juego.blit(fuente_subtitulos.render("Presiona [E] para entrar a Sala 1B", True, BLANCO_TEXTO), (580, 65))

            if cerca_del_escritorio and not mostrar_ficha:
                pygame.draw.rect(lienzo_juego, VIOLETA_UI, (500, 50, 600, 60), border_radius=8)
                lienzo_juego.blit(fuente_subtitulos.render("Presiona [E] para leer ficha", True, BLANCO_TEXTO), (520, 65))

            if not investigador.esta_escondido: 
                lienzo_juego.blit(investigador.image, (investigador.rect.x - camara_x, investigador.rect.y))
            lienzo_juego.blit(recepcionista.image, (recepcionista.rect.x - camara_x, recepcionista.rect.y))

        elif cuarto_actual == "SALA_REGISTROS":
            if usar_sala_interior_real: 
                lienzo_juego.blit(imagen_sala_interior, (0, 0))
            else: 
                lienzo_juego.fill((20, 14, 16))

            if caja_fuerte_abierta or estado_actual == ANIM_CAJA:
                pygame.draw.rect(lienzo_juego, PASILLO_OSCURO, (900 - camara_x, caja_fuerte_interior_rect.y, ancho_apertura_caja, caja_fuerte_interior_rect.height))

            lienzo_juego.blit(investigador.image, (investigador.rect.x, investigador.rect.y))

            if cerca_de_la_salida_interior:
                pygame.draw.rect(lienzo_juego, VIOLETA_UI, (550, 50, 500, 60), border_radius=8)
                lienzo_juego.blit(fuente_subtitulos.render("Presiona [E] para salir", True, BLANCO_TEXTO), (590, 65))
            elif cerca_del_archivador_interior:
                pygame.draw.rect(lienzo_juego, VIOLETA_UI, (550, 50, 500, 60), border_radius=8)
                msg_arch = "¡Ya revisaste el Archivador!" if codigo_recogido else "Presiona [E] para revisar Archivador"
                lienzo_juego.blit(fuente_subtitulos.render(msg_arch, True, BLANCO_TEXTO), (570, 65))
            elif cerca_de_la_caja_interior:
                pygame.draw.rect(lienzo_juego, VIOLETA_UI, (500, 50, 600, 60), border_radius=8)
                msg_caja = "¡Ya tienes la Ficha de Celestia!" if ficha_recogida else "Presiona [E] para interactuar con la Caja"
                lienzo_juego.blit(fuente_subtitulos.render(msg_caja, True, BLANCO_TEXTO), (530, 65))

        elif cuarto_actual == "DORMITORIOS":
            if 'imagen_pabellon' in globals() and imagen_pabellon:
                lienzo_juego.blit(imagen_pabellon, (0, 0))

            if 'ecos_grupo' in globals():
                for eco in ecos_grupo:
                    eco.actualizar()
                    eco.dibujar(lienzo_juego)

            investigador.dibujar(lienzo_juego)

            # Indicadores de interacción en el nivel 2
            cerca_caja_fusibles = 30 <= investigador.rect.x <= 250
            cerca_camilla = 350 <= investigador.rect.x <= 650
            
            if cerca_caja_fusibles and not luz_uv_activa:
                pygame.draw.rect(lienzo_juego, VIOLETA_UI, (550, 50, 500, 60), border_radius=8)
                lienzo_juego.blit(fuente_subtitulos.render("Presiona [E] para usar Caja de Fusibles", True, BLANCO_TEXTO), (560, 65))
            
            if cerca_camilla and not nota_camilla_recogida:
                pygame.draw.rect(lienzo_juego, VIOLETA_UI, (550, 50, 500, 60), border_radius=8)
                lienzo_juego.blit(fuente_subtitulos.render("Presiona [E] para examinar Camilla", True, BLANCO_TEXTO), (570, 65))

            if not luz_uv_activa:
                centro = (investigador.rect.centerx, investigador.rect.centery)
                dibujar_circulo_vision(lienzo_juego, centro, radio=160)
            else:
                tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio_uv
                mostrar_luz = True
                
                if tiempo_transcurrido < 2000:
                    mostrar_luz = random.choice([True, True, False])
                
                if mostrar_luz:
                    capa_uv = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
                    capa_uv.fill((110, 25, 180, 75))
                    lienzo_juego.blit(capa_uv, (0, 0))

        # 2. Overlays y popups
        if mostrar_ficha and usar_ficha_real:
            lienzo_juego.blit(imagen_ficha, (400, 110))

        aplicar_parpadeo_luces(lienzo_juego)
        dibujar_inventario_roblox(lienzo_juego)

        if estado_actual == PAD_REJA:
            s_oscura = pygame.Surface((ANCHO, ALTO)); s_oscura.fill((0,0,0)); s_oscura.set_alpha(200); lienzo_juego.blit(s_oscura, (0,0))
            if usar_pad_reja: lienzo_juego.blit(imagen_pad_reja, (ANCHO//2 - 250, 50))
            pygame.draw.rect(lienzo_juego, GRIS_DISPLAY, (ANCHO//2 - 120, 140, 240, 60), border_radius=4)
            texto_p = fuente_pixel.render(texto_codigo_ingresado, True, VERDE_OK)
            lienzo_juego.blit(texto_p, (ANCHO//2 - 100, 150))

        elif estado_actual == PAD_CAJA:
            s_oscura = pygame.Surface((ANCHO, ALTO)); s_oscura.fill((0,0,0)); s_oscura.set_alpha(200); lienzo_juego.blit(s_oscura, (0,0))
            if usar_pad_caja: lienzo_juego.blit(imagen_pad_caja, (ANCHO//2 - 250, 50))
            pygame.draw.rect(lienzo_juego, GRIS_DISPLAY, (ANCHO//2 - 120, 140, 240, 60), border_radius=4)
            texto_c = fuente_pixel.render(texto_codigo_ingresado, True, ORO_CAJA)
            lienzo_juego.blit(texto_c, (ANCHO//2 - 100, 150))

        elif estado_actual in [ANIM_REJA, ANIM_CAJA]:
            s_transparente = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            s_transparente.fill((0, 0, 0, 40))
            lienzo_juego.blit(s_transparente, (0, 0))

        elif estado_actual == INTERIOR_ARCHIVADOR:
            if imagen_interior_archivador:
                lienzo_juego.blit(imagen_interior_archivador, (ANCHO // 2 - 400, ALTO // 2 - 250))
            if not codigo_recogido and sprite_codigo_caja:
                lienzo_juego.blit(sprite_codigo_caja, rect_codigo_clickeable)

        elif estado_actual == INTERIOR_CAJA:
            if imagen_interior_caja:
                lienzo_juego.blit(imagen_interior_caja, (ANCHO // 2 - 400, ALTO // 2 - 300))
            if not ficha_recogida and sprite_ficha_caja:
                lienzo_juego.blit(sprite_ficha_caja, rect_ficha_clickeable)

        elif estado_actual == VISTA_EXAMEN:
            s_fondo_papel = pygame.Surface((ANCHO, ALTO))
            s_fondo_papel.fill((0, 0, 0))
            s_fondo_papel.set_alpha(220)
            lienzo_juego.blit(s_fondo_papel, (0, 0))

            if item_inspeccionando == "Código Caja Fuerte" and grande_codigo_sprite:
                rect_img = grande_codigo_sprite.get_rect(center=(ANCHO // 2, ALTO // 2))
                lienzo_juego.blit(grande_codigo_sprite, rect_img)
            elif item_inspeccionando == "Ficha Celestia" and grande_ficha_celestia:
                rect_img = grande_ficha_celestia.get_rect(center=(ANCHO // 2, ALTO // 2))
                lienzo_juego.blit(grande_ficha_celestia, rect_img)
            elif item_inspeccionando == "Nota Camilla" and grande_nota_camilla:
                rect_img = grande_nota_camilla.get_rect(center=(ANCHO // 2, ALTO // 2))
                lienzo_juego.blit(grande_nota_camilla, rect_img)
                
                # Si la nota no ha sido recogida, mostrar instrucción para recogerla
                if not nota_camilla_recogida:
                    info_recoger = fuente_subtitulos.render("Haz clic para recoger la nota", True, VERDE_OK)
                    lienzo_juego.blit(info_recoger, (ANCHO // 2 - info_recoger.get_width() // 2, ALTO - 80))

            info_cerrar = fuente_subtitulos.render("Presiona ESC para cerrar", True, BLANCO_TEXTO)
            lienzo_juego.blit(info_cerrar, (ANCHO // 2 - info_cerrar.get_width() // 2, ALTO - 50))

        elif estado_actual == PUZZLE_FUSIBLES:
            s_fondo = pygame.Surface((ANCHO, ALTO))
            s_fondo.fill((0, 0, 0))
            s_fondo.set_alpha(215)
            lienzo_juego.blit(s_fondo, (0, 0))

            # Mostrar imagen progresiva según el estado
            if usar_fusibles_animados and len(imagenes_fusibles) >= 5:
                indice_imagen = 0
                if estado_visual_fusibles == "NORMAL":
                    # Variar entre imagen 1 y 2 mientras escribe
                    indice_imagen = 1 if len(texto_codigo_fusibles) > 0 else 0
                elif estado_visual_fusibles == "ERROR":
                    # Mostrar imagen 3 o 4 para error
                    indice_imagen = 3 if (pygame.time.get_ticks() // 200) % 2 == 0 else 4
                elif estado_visual_fusibles == "CORRECTO":
                    # Mostrar imagen 5 para correcto
                    indice_imagen = 4
                
                imagen_fusible = imagenes_fusibles[indice_imagen]
                rect_imagen = imagen_fusible.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
                lienzo_juego.blit(imagen_fusible, rect_imagen)
            
            # Panel de información
            rect_panel = pygame.Rect(ANCHO // 2 - 250, ALTO // 2 + 80, 500, 160)
            pygame.draw.rect(lienzo_juego, VIOLETA_UI, rect_panel, border_radius=12)
            pygame.draw.rect(lienzo_juego, VIOLETA_CLARO, rect_panel, 4, border_radius=12)

            t_titulo = fuente_subtitulos.render("REGULADOR DE VOLTAJE UV", True, BLANCO_TEXTO)
            t_formula = fuente_subtitulos.render("FÓRMULA: (A * B) + C = VOLTAJE", True, ORO_CAJA)
            t_valores = fuente_pixel.render("Pistas: A=4  |  B=5  |  C=6", True, BLANCO_TEXTO)
            
            lienzo_juego.blit(t_titulo, (ANCHO // 2 - t_titulo.get_width() // 2, ALTO // 2 + 100))
            lienzo_juego.blit(t_formula, (ANCHO // 2 - t_formula.get_width() // 2, ALTO // 2 + 130))
            lienzo_juego.blit(t_valores, (ANCHO // 2 - t_valores.get_width() // 2, ALTO // 2 + 160))

            # Solo mostrar el código si no está en estado correcto
            if estado_visual_fusibles != "CORRECTO":
                t_codigo = fuente_titulos.render(texto_codigo_fusibles + "_", True, VERDE_OK)
                lienzo_juego.blit(t_codigo, (ANCHO // 2 - t_codigo.get_width() // 2, ALTO // 2 + 195))
                
                t_ayuda = fuente_subtitulos.render("Ingresa el voltaje y presiona ENTER", True, BLANCO_TEXTO)
                lienzo_juego.blit(t_ayuda, (ANCHO // 2 - t_ayuda.get_width() // 2, ALTO // 2 + 225))
            else:
                t_exito = fuente_subtitulos.render("¡SISTEMA ACTIVADO!", True, VERDE_OK)
                lienzo_juego.blit(t_exito, (ANCHO // 2 - t_exito.get_width() // 2, ALTO // 2 + 195))

        # 3. Volcado final a pantalla con efecto de distorsión
        if intensidad_distorsion > 0:
            offset_x = random.randint(-intensidad_distorsion, intensidad_distorsion)
            offset_y = random.randint(-intensidad_distorsion, intensidad_distorsion)
            pantalla.blit(lienzo_juego, (offset_x, offset_y))
        else:
            pantalla.blit(lienzo_juego, (0, 0))

    elif estado_actual == VICTORIA:
        pantalla.fill(VERDE_OK)
        pantalla.blit(fuente_titulos.render("¡COMPLETADO!", True, NEGRO_FONDO), (600, 300))
    elif estado_actual == GAMEOVER:
        pantalla.fill(ROJO_SANGRE)
        pantalla.blit(fuente_titulos.render("GAME OVER", True, BLANCO_TEXTO), (600, 300))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()