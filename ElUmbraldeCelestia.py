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
slot_codigo_rect = pygame.Rect(X_BARRA_INV + 40, Y_BARRA_INV + 10, 100, 100)
slot_ficha_rect = pygame.Rect(X_BARRA_INV + 320, Y_BARRA_INV + 10, 100, 100)

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
    pygame.mixer.music.load("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\musica_inicio.MPEG")
    pygame.mixer.music.set_volume(0.2) 
    pygame.mixer.music.play(-1)        
except Exception: pass

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
try: portazo = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\portazo.MPEG")
except Exception: portazo = None

# NUEVOS EFECTOS DE SONIDO SOLICITADOS
try: sonido_abrir_archivador = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\abrir_archivador.MPEG")
except Exception: sonido_abrir_archivador = None
try: sonido_cerrar_archivador = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\cerrar_archivador.MPEG")
except Exception: sonido_cerrar_archivador = None
try: sonido_abrir_caja = pygame.mixer.Sound("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\abrir_caja.MPEG")
except Exception: sonido_abrir_caja = None

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
            if distancia < 500:
                intensidad_distorsion = int((1.0 - (distancia / 500)) * 12) 
                
                volumen = max(0.1, 1.0 - (distancia / 500))
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

def cargar_img(ruta, dims, alpha=False):
    try:
        img = pygame.image.load(ruta)
        return pygame.transform.scale(img.convert_alpha() if alpha else img.convert(), dims), True
    except Exception: return None, False

imagen_inicio, usar_inicio_real = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\INICIO2.png", (ANCHO, ALTO))
imagen_ficha, usar_ficha_real = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\ingresos-egresos.png", (750, 500), True)
imagen_sala_interior, usar_sala_interior_real = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\sala_registros2.png", (1600, 720))

imagen_pad_reja, usar_pad_reja = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\pad_numeros.png", (500, 600), True)
imagen_pad_caja, usar_pad_caja = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\pad_numeros.png", (500, 600), True)
imagen_interior_caja, usar_interior_caja = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\interior_cajafuerte.png", (800, 600), True)
imagen_exterior_hospital, usar_exterior_hospital = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\exterior_hospital.png", (ANCHO, ALTO))
imagen_interior_archivador, usar_interior_archivador = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\interior_archivador.png", (800, 500), True)

# CARGA DE SPRITES REALES DE OBJETOS
imagen_codigo_sprite, usar_codigo_sprite = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\sprite_codigo.png", (200, 200), True)
imagen_ficha_celestia, usar_ficha_celestia = cargar_img("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\ficha_celestia.png", (200, 200), True)

# Crear versiones escaladas para miniaturas del inventario (80x80 para encajar centrado en slots de 100x100)
mini_codigo_sprite = pygame.transform.scale(imagen_codigo_sprite, (80, 80)) if usar_codigo_sprite else None
mini_ficha_celestia = pygame.transform.scale(imagen_ficha_celestia, (80, 80)) if usar_ficha_celestia else None

# Crear versiones en tamaño grande para la Vista Examen
grande_codigo_sprite = pygame.transform.scale(imagen_codigo_sprite, (180, 180)) if usar_codigo_sprite else None
grande_ficha_celestia = pygame.transform.scale(imagen_ficha_celestia, (180, 180)) if usar_ficha_celestia else None

# Rectángulos de interacción dentro de los contenedores emergentes
rect_codigo_clickeable = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 20, 200, 200)
# REAJUSTADO: Ubicación del sprite de la ficha en el centro inferior del contenedor interior de la caja fuerte
rect_ficha_clickeable = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 70, 200, 200)

try:
    imagen_fondo_original = pygame.image.load("C:\\Users\\sofia\\Downloads\\videojuego\\escenarios\\hospital_admision_fondo2.png").convert()
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

INICIO, REGISTROS, CINEMATICA, JUEGO, PAD_REJA, PAD_CAJA, ANIM_REJA, ANIM_CAJA, INTERIOR_ARCHIVADOR, INTERIOR_CAJA, VISTA_EXAMEN, VICTORIA, GAMEOVER = (
    "Bienvenida", "Registros", "Cinematica", "Juego", "PadReja", "PadCaja", "AnimReja", "AnimCaja", "InteriorArchivador", "InteriorCaja", "VistaExamen", "Ganaste", "Perdiste"
)
estado_actual = INICIO

lienzo_juego = pygame.Surface((ANCHO, ALTO))

def dibujar_inventario_roblox(superficie):
    """Renderiza el HUD del inventario flotante centrado con alineación calibrada de miniaturas."""
    barra_surf = pygame.Surface((ANCHO_BARRA_INV, ALTO_BARRA_INV), pygame.SRCALPHA)
    barra_surf.fill((20, 20, 20, 180))
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

# ==========================================
# 4. BUCLE PRINCIPAL DE JUEGO
# ==========================================
jugando = True
while jugando:
    pos_mouse = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if estado_actual in [PAD_REJA, PAD_CAJA, INTERIOR_ARCHIVADOR, INTERIOR_CAJA, VISTA_EXAMEN]: estado_actual = JUEGO
                else: jugando = False
            
            elif estado_actual == REGISTROS: estado_actual = INICIO
            
            elif estado_actual in [PAD_REJA, PAD_CAJA]:
                if evento.key == pygame.K_BACKSPACE: texto_codigo_ingresado = texto_codigo_ingresado[:-1]
                elif evento.key == pygame.K_RETURN:
                    if estado_actual == PAD_REJA:
                        # MODIFICADO: Código de la reja actualizado a 12
                        if texto_codigo_ingresado == "12":
                            reja_abierta = True
                            texto_codigo_ingresado = ""
                            if sonido_reja_abrir: canal_efectos.play(sonido_reja_abrir)
                            estado_actual = ANIM_REJA
                            tiempo_espera_cambio = pygame.time.get_ticks()
                        else: texto_codigo_ingresado = ""
                    
                    elif estado_actual == PAD_CAJA:
                        # Código de la caja fuerte actualizado a 170697
                        if texto_codigo_ingresado == "170697":
                            caja_fuerte_abierta = True
                            texto_codigo_ingresado = ""
                            # Reproduce el nuevo sonido de apertura de la caja fuerte
                            if sonido_abrir_caja: 
                                canal_efectos.play(sonido_abrir_caja)
                            estado_actual = ANIM_CAJA
                            tiempo_espera_cambio = pygame.time.get_ticks()
                        else: texto_codigo_ingresado = ""
                else:
                    # Permite hasta 7 caracteres en el buffer para acomodar la nueva clave larga
                    if evento.unicode.isdigit() and len(texto_codigo_ingresado) < 7:
                        texto_codigo_ingresado += evento.unicode

            elif estado_actual == JUEGO:
                if mostrar_ficha: mostrar_ficha = False
                else:
                    if cuarto_actual == "PASILLO":
                        if (cerca_del_armario1 or cerca_del_armario2 or cerca_del_armario3) and evento.key == pygame.K_e:
                            investigador.esta_escondido = not investigador.esta_escondido
                            if sonido_armario: canal_efectos.play(sonido_armario)
                        elif cerca_del_escritorio and evento.key == pygame.K_e:
                            mostrar_ficha = True
                            if mostrar_ficha1: canal_efectos.play(mostrar_ficha1)
                        elif cerca_de_puerta_1b and evento.key == pygame.K_e:
                            pasillo_guardado_x = investigador.rect.x 
                            cuarto_actual = "SALA_REGISTROS"; investigador.rect.x = 180 
                            if sonido_puerta: canal_efectos.play(sonido_puerta)
                        elif cerca_de_la_reja and not reja_abierta and evento.key == pygame.K_e:
                            texto_codigo_ingresado = ""; estado_actual = PAD_REJA

                    elif cuarto_actual == "SALA_REGISTROS":
                        if cerca_de_la_salida_interior and evento.key == pygame.K_e:
                            cuarto_actual = "PASILLO"; investigador.rect.x = pasillo_guardado_x 
                            if sonido_puerta: canal_efectos.play(sonido_puerta)
                        elif cerca_del_archivador_interior and evento.key == pygame.K_e:
                            # MODIFICADO: Al abrir el archivador suena su efecto correspondiente
                            if sonido_abrir_archivador:
                                canal_efectos.play(sonido_abrir_archivador)
                            estado_actual = INTERIOR_ARCHIVADOR 
                        elif cerca_de_la_caja_interior and evento.key == pygame.K_e:
                            if not caja_fuerte_abierta:
                                texto_codigo_ingresado = ""; estado_actual = PAD_CAJA
                            else:
                                estado_actual = INTERIOR_CAJA

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_actual == INICIO:
                if musica_inicio: 
                    canal_pasos_jugador.play(musica_inicio)
                    if btn_jugar_rect.collidepoint(pos_mouse): 
                        estado_actual = CINEMATICA
                        tiempo_inicio_cinematica = pygame.time.get_ticks()
                        fase_cinematica = 1
                        try:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\musica_cinematica.MP3")
                            pygame.mixer.music.set_volume(0.2)
                            pygame.mixer.music.play(-1)
                        except Exception: pass
                    elif btn_registros_rect.collidepoint(pos_mouse): estado_actual = REGISTROS
                    elif btn_salir_rect.collidepoint(pos_mouse): jugando = False
                
            elif estado_actual == JUEGO:
                # SELECCIÓN DESDE LOS NUEVOS SLOTS PARA ENTRAR DIRECTO A LA VISTA EXAMEN
                if "Código Caja Fuerte" in inventario and slot_codigo_rect.collidepoint(pos_mouse):
                    item_inspeccionando = "Código Caja Fuerte"
                    if mostrar_ficha1: canal_efectos.play(mostrar_ficha1)
                    estado_actual = VISTA_EXAMEN
                elif "Ficha Celestia" in inventario and slot_ficha_rect.collidepoint(pos_mouse):
                    item_inspeccionando = "Ficha Celestia"
                    if mostrar_ficha1: canal_efectos.play(mostrar_ficha1)
                    estado_actual = VISTA_EXAMEN

            elif estado_actual == INTERIOR_ARCHIVADOR:
                if rect_codigo_clickeable.collidepoint(pos_mouse) and not codigo_recogido:
                    inventario.append("Código Caja Fuerte")
                    codigo_recogido = True
                    # MODIFICADO: Al recoger la pista e interactuar, suena el cierre del archivador
                    if sonido_cerrar_archivador: canal_efectos.play(sonido_cerrar_archivador)
                    estado_actual = JUEGO

            elif estado_actual == INTERIOR_CAJA:
                if rect_ficha_clickeable.collidepoint(pos_mouse) and not ficha_recogida:
                    inventario.append("Ficha Celestia")
                    ficha_recogida = True
                    estado_actual = JUEGO
                    
            elif estado_actual == VISTA_EXAMEN:
                estado_actual = JUEGO

    # ==========================================
    # ACTUALIZACIONES LÓGICAS JUEGO
    # ==========================================
    tiempo_actual = pygame.time.get_ticks()

    if estado_actual == ANIM_REJA:
        if ancho_apertura_reja < reja_rect.width:
            ancho_apertura_reja += 3.5  
        if tiempo_actual - tiempo_espera_cambio > 2000:  
            estado_actual = VICTORIA

    elif estado_actual == ANIM_CAJA:
        # MODIFICADO: Ralentizado (de 2.5 a 0.85) para sincronizar con la duración del audio "sonido_abrir_caja"
        if ancho_apertura_caja < caja_fuerte_interior_rect.width:
            ancho_apertura_caja += 0.85
        if tiempo_actual - tiempo_espera_cambio > 4500:  # Espera ampliada proporcionalmente
            estado_actual = INTERIOR_CAJA

    if estado_actual == JUEGO:
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

    # ==========================================
    # --- RENDERIZADO GENERAL ---
    # ==========================================
    if estado_actual == INICIO:
        if usar_inicio_real: 
            pantalla.blit(imagen_inicio, (0, 0))
        else: pantalla.fill(NEGRO_FONDO)
        
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
        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicio_cinematica
        if tiempo_transcurrido < 10000:
            pantalla.fill((0, 0, 0))
            factor_zoom = 1.0 + (tiempo_transcurrido / 10000.0) * 1.2  
            nuevo_ancho = int(ANCHO * factor_zoom)
            nuevo_alto = int(ALTO * factor_zoom)
            if usar_exterior_hospital:
                img_escalada = pygame.transform.scale(imagen_exterior_hospital, (nuevo_ancho, nuevo_alto))
                pantalla.blit(img_escalada, (-(nuevo_ancho - ANCHO) // 2, -(nuevo_alto - ALTO) // 2))
            else:
                pygame.draw.rect(pantalla, (25, 20, 30), (ANCHO // 2 - nuevo_ancho // 4, ALTO // 2 - nuevo_alto // 4, nuevo_ancho // 2, nuevo_alto // 2))

            if pasos_exterior and (tiempo_actual - ULTIMO_PASO_JUGADOR > 500):
                if not canal_pasos_jugador.get_busy(): 
                    canal_pasos_jugador.set_volume(0.35)
                    canal_pasos_jugador.play(pasos_exterior)
                ULTIMO_PASO_JUGADOR = tiempo_actual

            pygame.draw.rect(pantalla, (5, 5, 10, 200), (0, 590, ANCHO, 130))
            texto_sub = fuente_subtitulos.render("Después de tanto tiempo... voy a descubrir lo que realmente le sucedió a mi madre.", True, BLANCO_TEXTO)
            pantalla.blit(texto_sub, (ANCHO // 2 - texto_sub.get_width() // 2, 640))

        elif 10000 <= tiempo_transcurrido < 14000:
            if fase_cinematica == 1:
                canal_pasos_jugador.stop()  
                if golpe_seco: canal_efectos.play(golpe_seco)
                fase_cinematica = 2
            if tiempo_transcurrido >= 12000 and fase_cinematica == 2:
                if portazo: canal_tension.play(portazo)
                fase_cinematica = 3 
            pantalla.fill((0, 0, 0)) 
            texto_sub = fuente_subtitulos.render("¿Qué pasó? ¿D-dónde estoy...?", True, ROJO_SANGRE)
            pantalla.blit(texto_sub, (ANCHO // 2 - texto_sub.get_width() // 2, ALTO // 2 - 20))
        else:
            cuarto_actual = "PASILLO"
            investigador.rect.x = 100
            investigador.esta_escondido = False
            estado_actual = JUEGO
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("C:\\Users\\sofia\\Downloads\\videojuego\\sonidos\\musica_ambiental.MPEG")
                pygame.mixer.music.set_volume(0.15)
                pygame.mixer.music.play(-1)
            except Exception: pass

    elif estado_actual in [JUEGO, PAD_REJA, PAD_CAJA, ANIM_REJA, ANIM_CAJA, INTERIOR_ARCHIVADOR, INTERIOR_CAJA, VISTA_EXAMEN]:
        if cuarto_actual == "PASILLO":
            if usar_fondo_real: lienzo_juego.blit(imagen_fondo, (-camara_x, 0))
            else: lienzo_juego.fill(NEGRO_FONDO)

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

            if not investigador.esta_escondido: lienzo_juego.blit(investigador.image, (investigador.rect.x - camara_x, investigador.rect.y))
            lienzo_juego.blit(recepcionista.image, (recepcionista.rect.x - camara_x, recepcionista.rect.y))

        elif cuarto_actual == "SALA_REGISTROS":
            if usar_sala_interior_real: lienzo_juego.blit(imagen_sala_interior, (0, 0))
            else: lienzo_juego.fill((20, 14, 16))

            # ANIMACIÓN DE LA CAJA FUERTE: Ahora usa las proporciones ampliadas de forma correcta
            if caja_fuerte_abierta or estado_actual == ANIM_CAJA:
                pygame.draw.rect(lienzo_juego, PASILLO_OSCURO, (900- camara_x, caja_fuerte_interior_rect.y, ancho_apertura_caja, caja_fuerte_interior_rect.height))

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
            s_oscura = pygame.Surface((ANCHO, ALTO)); s_oscura.fill((0,0,0)); s_oscura.set_alpha(220); lienzo_juego.blit(s_oscura, (0,0))
            if usar_interior_archivador: 
                lienzo_juego.blit(imagen_interior_archivador, (ANCHO//2 - 400, 110))
            
            if not codigo_recogido:
                if usar_codigo_sprite:
                    lienzo_juego.blit(imagen_codigo_sprite, (rect_codigo_clickeable.x, rect_codigo_clickeable.y))
                else:
                    pygame.draw.rect(lienzo_juego, ORO_CAJA, rect_codigo_clickeable, border_radius=5)
            lienzo_juego.blit(fuente_subtitulos.render("Haz clic en la pista del código para guardarlo [ESC para cerrar]", True, BLANCO_TEXTO), (ANCHO//2 - 350, 50))

        elif estado_actual == INTERIOR_CAJA:
            s_oscura = pygame.Surface((ANCHO, ALTO)); s_oscura.fill((0,0,0)); s_oscura.set_alpha(220); lienzo_juego.blit(s_oscura, (0,0))
            if usar_interior_caja: 
                lienzo_juego.blit(imagen_interior_caja, (ANCHO//2 - 400, 110))
            
            if not ficha_recogida:
                if usar_ficha_celestia:
                    lienzo_juego.blit(imagen_ficha_celestia, (rect_ficha_clickeable.x, rect_ficha_clickeable.y))
                else:
                    pygame.draw.rect(lienzo_juego, ROJO_SANGRE, rect_ficha_clickeable, border_radius=5)
            lienzo_juego.blit(fuente_subtitulos.render("Haz clic en la Ficha Médica de Celestia para recogerla [ESC para cerrar]", True, BLANCO_TEXTO), (ANCHO//2 - 380, 50))

        # INTERFAZ MODIFICADA DE EXAMEN: Muestra de manera exclusiva los sprites reales escalados a gran tamaño
        elif estado_actual == VISTA_EXAMEN:
            s_fondo_papel = pygame.Surface((ANCHO, ALTO)); s_fondo_papel.fill((0, 0, 0)); s_fondo_papel.set_alpha(235)
            lienzo_juego.blit(s_fondo_papel, (0, 0))
            
            rect_hoja = pygame.Rect(ANCHO // 2 - 350, 60, 700, 540)
            pygame.draw.rect(lienzo_juego, (245, 240, 225), rect_hoja, border_radius=8)
            pygame.draw.rect(lienzo_juego, ORO_CAJA, rect_hoja, 3, border_radius=8)

            if item_inspeccionando == "Código Caja Fuerte":
                lienzo_juego.blit(fuente_titulos.render("NOTA DEL ARCHIVADOR", True, (40, 40, 50)), (ANCHO // 2 - 270, 90))
                
                # Renderizado del sprite real del código en tamaño grande
                if grande_codigo_sprite:
                    lienzo_juego.blit(grande_codigo_sprite, (ANCHO // 2 - 90, 160))
                
                lienzo_juego.blit(fuente_documento.render("Anotación recuperada de admisión general:", True, (70, 70, 80)), (ANCHO // 2 - 260, 370))
                lienzo_juego.blit(fuente_pixel.render("CLAVE CAJA FUERTE: 170697", True, ROJO_SANGRE), (ANCHO // 2 - 250, 430))
                lienzo_juego.blit(fuente_documento.render("Nota: Destruir este papel inmediatamente.", True, (100, 100, 110)), (ANCHO // 2 - 240, 500))
            
            elif item_inspeccionando == "Ficha Celestia":
                lienzo_juego.blit(fuente_titulos.render("SANATORIO CELESTIA", True, ROJO_SANGRE), (ANCHO // 2 - 240, 90))
                
                # Renderizado del sprite real de la ficha médica en tamaño grande
                if grande_ficha_celestia:
                    lienzo_juego.blit(grande_ficha_celestia, (ANCHO // 2 - 90, 160))
                
                lienzo_juego.blit(fuente_documento.render("EXPEDIENTE CLÍNICO - REJA DE CONTENCIÓN", True, (40, 40, 50)), (ANCHO // 2 - 260, 360))
                # Mensaje claro con la información textual requerida
                lienzo_juego.blit(fuente_documento.render("Madre: Dra. Eleanor Vane. Nivel de aislamiento 12.", True, (50, 50, 60)), (ANCHO // 2 - 280, 410))
                lienzo_juego.blit(fuente_documento.render("Obsesión recurrente con el código primario de salida.", True, (50, 50, 60)), (ANCHO // 2 - 280, 450))
                lienzo_juego.blit(fuente_pixel.render("CÓDIGO DE LA REJA FINAL: 12", True, VERDE_OK), (ANCHO // 2 - 240, 510))

            lienzo_juego.blit(fuente_subtitulos.render("Haz clic o presiona ESC para cerrar e internalizar", True, BLANCO_TEXTO), (ANCHO // 2 - 280, 625))

        if intensidad_distorsion > 0 and cuarto_actual == "PASILLO":
            pantalla.blit(lienzo_juego, (random.randint(-intensidad_distorsion, intensidad_distorsion), random.randint(-intensidad_distorsion, intensidad_distorsion)))
        else: pantalla.blit(lienzo_juego, (0, 0))

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