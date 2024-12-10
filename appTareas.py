
# Este código crea una aplicación gráfica de tareas usando la biblioteca Flet
import flet as ft # Se importa la biblioteca Flet, que permite construir aplicaciones multiplataforma con interfaces gráficas modernas


# Esta es la función principal de la aplicación. Configura la ventana y contiene todas las funciones necesarias para gestionar la interfaz y las funcionalidades
def principal(pagina: ft.Page):

    # Configura las propiedades básicas de la ventana:
    pagina.window.width = 410 # Tamaño: 410 px de ancho
    pagina.window.height = 820 # Tamaño: 820 px de alto
    pagina.window.center() # Posición: Centra la ventana en la pantalla
    pagina.bgcolor = ft.colors.WHITE # Color de fondo: Blanco

    # Crea la estructura de la imagen de perfil: Genera un elemento visual que representa el perfil del usuario con un diseño circular y gradiente
    def crear_imagen_perfil():
        return ft.Stack( # Permite apilar elementos (contenedores) uno encima del otro; Aquí se usa para superponer varias capas circulares con gradientes
            controls=[ 
                ft.Container(
                    gradient=ft.SweepGradient( # Gradiente circular: Para decorar el borde del avatar, aplica un gradiente circular al borde exterior del avatar con dos colores: #EEEEEE y #eb06ff
                        center=ft.alignment.center,
                        start_angle=0.0,
                        end_angle=3,
                        stops=[0.5, 0.5],
                        colors=['#EEEEEE', '#eb06ff'], # Colores para el circulo del perfil
                    ),
                    width=100,
                    height=100,
                    border_radius=50,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[ 
                            ft.Container( # Se crean varios círculos, cada uno más pequeño que el anterior
                                padding=ft.padding.all(5),
                                bgcolor="#2D033B",
                                width=90,
                                height=90,
                                border_radius=50,
                                content=ft.Container(
                                    bgcolor="#3450A1", # Color opaco de la foto
                                    height=80,
                                    width=80,
                                    border_radius=40,
                                    content=ft.CircleAvatar( # Avatar circular: Usa ft.CircleAvatar para cargar una imagen desde una URL
                                        opacity=0.8, # Ajusta la transparencia de la imagen (0.8 es ligeramente translúcida)
                                        foreground_image_url="https://instagram.fagt4-1.fna.fbcdn.net/v/t51.2885-19/464309753_1615611152709754_7173169988519059617_n.jpg?stp=dst-jpg_tt6&_nc_ht=instagram.fagt4-1.fna.fbcdn.net&_nc_cat=110&_nc_ohc=ar7NkAp4gmcQ7kNvgE2Kk5Z&_nc_gid=4da5008406f24a9aada45b1df5dbc354&edm=ALGbJPMBAAAA&ccb=7-5&oh=00_AYBYRhr3w2AoZy7btSv5aHL-wKVkOARe6ASHGvIMrqHAfg&oe=675AFBF4&_nc_sid=7d3ac5",
                                    ),
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )

    # Categorías disponibles
    categorias = { # Define un diccionario para almacenar las tareas agrupadas en tres categorías:
        "Estudio": [],
        "Trabajo": [],
        "Hogar": [],
    }

    # Función para agregar tareas a una categoría
    def agregar_tarea(categoria, tarea): # Permite añadir tareas a una categoría específica:
        if tarea != "": # Comprueba si la tarea no está vacía
            if categoria in categorias: # Agrega la tarea como un diccionario con dos claves (tarea: El texto de la tarea / completa: Estado de la tarea (incompleta al principio))
                categorias[categoria].append({"tarea": tarea, "completa": False})

                # Llama a funciones para actualizar las barras de progreso y la lista de tareas
                actualizar_barras()
                actualizar_tareas()

    # Función para editar una tarea
    def editar_tarea(indice, categoria): 
        tarea_actual = categorias[categoria][indice]["tarea"]
        
        def guardar_cambio(e):
            nueva_tarea = campo_edicion.value.strip() 
            if nueva_tarea:
                categorias[categoria][indice]["tarea"] = nueva_tarea 
                actualizar_tareas() # Cuando el usuario guarda los cambios, actualiza la tarea en la lista correspondiente
                cerrar_dialogo()

        campo_edicion = ft.TextField(value=tarea_actual) # Permite modificar el texto de una tarea específica
        dialogo_editar = ft.AlertDialog(
            title=ft.Text("Editar Tarea"), 
            content=campo_edicion, # Muestra un cuadro de diálogo con un campo de texto editable
            actions=[ 
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo()),
                ft.TextButton("Guardar", on_click=guardar_cambio),
            ],
        )
        pagina.overlay.append(dialogo_editar)
        dialogo_editar.open = True
        pagina.update() 

    # Función para eliminar una tarea: Elimina una tarea de la lista
    def eliminar_tarea(indice, categoria):
        categorias[categoria].pop(indice) # Usa el índice para localizar la tarea en la categoría y eliminarla

        #Actualiza las barras de progreso y las tareas visibles
        actualizar_barras()
        actualizar_tareas()

    # Función para cerrar el cuadro de diálogo
    def cerrar_dialogo():
        for control in pagina.overlay:
            if isinstance(control, ft.AlertDialog):
                control.open = False
        pagina.update()

    # Función para marcar tarea como completa/incompleta: Cambia el estado de una tarea
    def marcar_tarea(indice, categoria):
        tarea_completa = categorias[categoria][indice]["completa"]
        categorias[categoria][indice]["completa"] = not tarea_completa # Si la tarea está incompleta, la marca como completada, y viceversa
        
        # Llama a las funciones de actualización
        actualizar_barras()
        actualizar_tareas()

    # Actualiza las barras de progreso de acuerdo con las tareas: Calcula y actualiza el progreso de cada categoría
    def actualizar_barras():
        for i, categoria in enumerate(["Estudio", "Trabajo", "Hogar"]):
            progreso = (

                # Divide las tareas completadas por el total de tareas
                sum(1 for tarea in categorias[categoria] if tarea["completa"]) # sum: Cuenta cuántas tareas están completas ("completa": True)
                / len(categorias[categoria]) # División: Divide las tareas completas entre el total de tareas para calcular el progreso
                if categorias[categoria]
                else 0 # Si una categoría no tiene tareas, el progreso se establece en 0 para evitar divisiones por cero
            )
            contenedor_barras.controls[i].content.controls[1].value = progreso # Actualiza los valores de las barras de progreso visibles
        pagina.update()

    # Función para actualizar la lista de tareas: Muestra todas las tareas de la categoría seleccionada
    def actualizar_tareas():
        contenedor_tareas.content = ft.ListView(
            controls=[
                # Título con la categoría seleccionada
                ft.Container(
                    padding=ft.padding.all(8),
                    content=ft.Text(f"Tareas de {categoria_seleccionada}", 
                        size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER
                    ),
                ),
                # Listado de tareas dentro del contenedor
                *[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.Checkbox( # Checkbox: Para marcarla como completa
                                value=tarea["completa"],
                                on_change=lambda e, idx=indice: marcar_tarea(idx, categoria_seleccionada),
                            ),
                            ft.Text(
                                tarea["tarea"],
                                style=ft.TextStyle(
                                    decoration=ft.TextDecoration.LINE_THROUGH if tarea["completa"] else None
                                ),
                            ),

                            # Botones de editar y eliminar
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color="#eb06ff",  # Color del icono de editar
                                on_click=lambda e, idx=indice: editar_tarea(idx, categoria_seleccionada),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color="#eb06ff",  # Color del icono de eliminar
                                on_click=lambda e, idx=indice: eliminar_tarea(idx, categoria_seleccionada),
                            ),
                        ],
                    )
                    for indice, tarea in enumerate(categorias[categoria_seleccionada])
                ],
            ],
            auto_scroll=True,
        )
        pagina.update()

    # Función para validar el formulario de agregar tarea: Verifica si los datos ingresados por el usuario son válidos
    def validar_formulario(e):
        if categoria_seleccionada not in categorias.keys(): # Comprueba que se haya seleccionado una categoría válida
            mostrar_alerta("Por favor selecciona una categoría válida: Estudio, Trabajo o Hogar.")
        elif not campo_tarea.value.strip(): # Verifica que el campo de texto de la tarea no esté vacío
            mostrar_alerta("Por favor ingresa una tarea válida.")
        else: # Si los datos son correctos, llama a la función para agregar la tarea
            agregar_tarea(categoria_seleccionada, campo_tarea.value.strip())
            campo_tarea.value = ""
            pagina.update()

    # Función para mostrar alertas
    def mostrar_alerta(mensaje):
        alerta = ft.AlertDialog( # Muestra un mensaje emergente si ocurre un error (por ejemplo, datos inválidos)
            title=ft.Text("Error"),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("OK", on_click=lambda e: cerrar_alerta(alerta))],
        )
        pagina.overlay.append(alerta)
        alerta.open = True
        pagina.update()

    # Función para cerrar alertas
    def cerrar_alerta(alerta):
        alerta.open = False
        pagina.update()

    # Contenedor de las barras de progreso
    contenedor_barras = ft.Row( # Define una fila de barras de progreso, una para cada categoría
        alignment=ft.MainAxisAlignment.CENTER,  # Centra los contenedores de barras de progreso
        controls=[ # Cada barra tiene un diseño y color específico
            ft.Container(
                width=100,
                height=110,
                bgcolor="#24032E",
                border_radius=15,
                padding=ft.padding.all(10),
                content=ft.Column(
                    controls=[
                        ft.Text("Estudio", color=ft.colors.WHITE, size=12),
                        ft.ProgressBar(value=0.0, color="#FFEC9E"),
                    ]
                ),
            ),
            ft.Container(
                width=100,
                height=110,
                bgcolor="#3A014C",
                border_radius=10,
                padding=ft.padding.all(10),
                content=ft.Column(
                    controls=[
                        ft.Text("Trabajo", color=ft.colors.WHITE, size=12),
                        ft.ProgressBar(value=0.0, color="#FFBB70"),
                    ]
                ),
            ),
            ft.Container(
                width=100,
                height=110,
                bgcolor="#55036F",
                border_radius=10,
                padding=ft.padding.all(10),
                content=ft.Column(
                    controls=[
                        ft.Text("Hogar", color=ft.colors.WHITE, size=12),
                        ft.ProgressBar(value=0.0, color="#ED9455"),
                    ]
                ),
            ),
        ],
        spacing=10,
    )

    # Variables para almacenar elementos dinámicos
    global campo_tarea, contenedor_tareas, categoria_seleccionada
    campo_tarea = None
    contenedor_tareas = None
    categoria_seleccionada = "Estudio"

    # Función para actualizar la categoría seleccionada: Actualiza la categoría seleccionada y reordena la lista de tareas
    def actualizar_categoria(categoria):
        global categoria_seleccionada
        categoria_seleccionada = categoria
        actualizar_tareas()

    # Crea la interfaz inicial de la aplicación
    def mostrar_pagina_inicio():
        pagina.clean() # Limpia todos los elementos actuales de la ventana antes de agregar los nuevos

        # Crea el encabezado con imagen y texto
        encabezado = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Container(
                    padding=ft.padding.only(left=10),  # Padding para separar la imagen del borde
                    content=ft.Image(src="https://lh3.googleusercontent.com/a/ACg8ocKxfjvXAqQ1oe01pd4RLmqxvJJKpFqUPNzXhL1fFjPlisdhHa0=s96-c", width=30, height=30),  # Aquí va la URL de la imagen
                ),
                ft.Text(
                    "App de tareas",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.WHITE,
                    text_align=ft.TextAlign.START,
                ),
            ],
            spacing=10,  # Espaciado entre la imagen y el texto
        )

        # Iconos de las categorías en la página de inicio con sus respectivos contadores
        textos_categorias = [
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=0),
                        content=ft.Icon(
                            name=ft.icons.BOOK if categoria == "Estudio" else
                                ft.icons.BUSINESS_CENTER if categoria == "Trabajo" else
                                ft.icons.HOUSE,
                            color=ft.colors.WHITE,
                            size=20,
                        ),
                    ),
                    ft.Text(
                        f"{categoria}: {len(tareas)} tareas",
                        size=16,
                        color=ft.colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                spacing=10,
            )
            for categoria, tareas in categorias.items()
        ]

        pagina.add(
            ft.Container(
                width=400,
                height=765,
                bgcolor="#2D033B",
                border_radius=35,
                padding=ft.padding.all(20),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        encabezado,  
                        ft.Container(height=100),  # Espacio entre el encabezado y el resto del contenido
                        crear_imagen_perfil(),
                        ft.Text(
                            "Erika Benítez",
                            size=27,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(
                            padding=ft.padding.only(top=20, bottom=10),
                            content=ft.Column(
                                controls=textos_categorias, # Estadísticas de tareas por categoría
                                spacing=10,
                            ),
                        ),
                        ft.Container(height=240),
                        ft.Row( # Botón para navegar a la pantalla de tareas
                            alignment=ft.MainAxisAlignment.END,
                            controls=[ft.TextButton("Revisar tareas", on_click=lambda _: mostrar_pagina_categorias(), style=ft.ButtonStyle(color="#daa0f2"))],
                        ),
                    ],
                ),
            )
        )







    # Crea la pantalla para gestionar tareas
    def mostrar_pagina_categorias():
        global campo_tarea, contenedor_tareas
        pagina.clean()

        # Campo de texto para agregar nuevas tareas
        campo_tarea = ft.TextField(label="Nueva tarea", on_submit=validar_formulario, focused_border_color="#C27FDC", label_style=ft.TextStyle(color="#d2b5de"), border_color="#260234")
        contenedor_tareas = ft.Container(
            bgcolor="#15011C", # Color del contenedor donde se listan las tareas
            border_radius=15,
            width=400,
            height=200,
            padding=ft.padding.all(10),
            content=ft.Column(
                controls=[ 
                    ft.Text(f"Tareas de {categoria_seleccionada}", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.ListView(auto_scroll=True)
                ]
            ),
        )
        pagina.add(
            ft.Container(
                width=400,
                height=765,
                bgcolor="#810CA8",
                border_radius=35,
                padding=ft.padding.all(20),
                content=ft.Column(
                    controls=[
                        ft.TextButton("Regresar a Inicio", on_click=lambda _: mostrar_pagina_inicio(), style=ft.ButtonStyle(color="#f5ddff")),
                        ft.Container(height=30),
                        ft.Text("Tareas", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ft.Dropdown( # Desplegable para seleccionar una categoría
                            label="Categoría",
                            focused_border_color="#C27FDC",
                            label_style=ft.TextStyle(color="#d2b5de"),
                            border_color="#260234",
                            options=[ft.dropdown.Option(c) for c in categorias.keys()],
                            value=categoria_seleccionada,
                            on_change=lambda e: actualizar_categoria(e.control.value),
                        ),
                        campo_tarea,
                        ft.ElevatedButton("AGREGAR", 
                                          on_click=validar_formulario, 
                                          width=400, height=50, 
                                          bgcolor='#bf77da', 
                                          color='white',  
                                          style=ft.ButtonStyle(  # Estilos del borde para el botón
                                            side=ft.BorderSide(color="#66048C", width=1)
                                            )
                                        ),
                        ft.Container(height=30),
                        ft.Text("Categorías", color=ft.colors.WHITE, size=18),
                        contenedor_barras,
                        contenedor_tareas, # Lista de tareas con opciones de editar, eliminar y marcar como completa
                    ],
                ),
            )
        )
        actualizar_tareas()

    mostrar_pagina_inicio()

ft.app(target=principal) # Inicia la aplicación ejecutando la función principal
