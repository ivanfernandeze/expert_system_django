from django import forms

class PreferenciasForm(forms.Form):
    CLIMA_CHOICES = [
        ('calido', 'Cálido'),
        ('humedo', 'Húmedo'),
        ('lluvioso', 'Lluvioso'),
        ('frio', 'Frío'),
        ('seco', 'Seco'),
        ('templado', 'Templado'),
        ('variable', 'Variable'),
        ('desértico', 'Desértico'),
        ('tropical', 'Tropical'),
    ]

    ACTIVIDAD_CHOICES = [
        ('senderismo', 'Senderismo'),
        ('turismo', 'Turismo'),
        ('aventura', 'Aventura'),
        ('observacion de la naturaleza', 'Observación de la Naturaleza'),
        ('caminata', 'Caminata'),
        ('escalar', 'Escalar'),
        ('gastronomia', 'Gastronomía'),
        ('compras', 'Compras'),
        ('relajacion', 'Relajación'),
        ('arte', 'Arte'),
        ('playa', 'Playa'),
        ('sandboarding', 'Sandboarding'),
        ('paseos en buggy', 'Paseos en Buggy'),
        ('observacion de cóndores', 'Observación de Cóndores'),
        ('escalada', 'Escalada'),
        ('exploracion de ruinas', 'Exploración de Ruinas'),
        ('visitas arqueológicas', 'Visitas Arqueológicas'),
        ('fotografía', 'Fotografía'),
        ('buceo', 'Buceo'),
        ('navegación', 'Navegación'),
    ]

    PRESUPUESTO_CHOICES = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
    ]

    DURACION_CHOICES = [
        ('corta', 'Corta'),
        ('larga', 'Larga'),
    ]

    PREFERENCIAS_CULTURALES_CHOICES = [
        ('vida nocturna', 'Vida Nocturna'),
        ('gastronomia', 'Gastronomía'),
        ('historia', 'Historia'),
        ('arquitectura', 'Arquitectura'),
        ('naturaleza', 'Naturaleza'),
        ('aventura', 'Aventura'),
        ('arte', 'Arte'),
        ('gastronomía marina', 'Gastronomía Marina'),
        ('ciencia', 'Ciencia'),
        ('relajación', 'Relajación'),
    ]

    EDAD_RECOMENDADA_CHOICES = [
        ('niños', 'Niños'),
        ('jovenes', 'Jóvenes'),
        ('adultos', 'Adultos'),
        ('mayores', 'Mayores'),
        ('todos', 'Todos'),
    ]

    IDIOMA_LOCAL_CHOICES = [
        ('español', 'Español'),
        ('ingles', 'Inglés'),
        ('frances', 'Francés'),
        ('quechua', 'Quechua'),
        ('rapa nui', 'Rapa Nui'),
        ('varios', 'Varios'),
    ]
    clima = forms.ChoiceField(
        choices=CLIMA_CHOICES,
        label='Clima Preferido',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    actividad = forms.ChoiceField(
        choices=ACTIVIDAD_CHOICES,
        label='Actividades Preferidas',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    presupuesto = forms.ChoiceField(
        choices=PRESUPUESTO_CHOICES,
        label='Presupuesto',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    duracion = forms.ChoiceField(
        choices=DURACION_CHOICES,
        label='Duración del Viaje',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    preferencias_culturales = forms.ChoiceField(
        choices=PREFERENCIAS_CULTURALES_CHOICES,
        label='Preferencias Culturales',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    edad_recomendada = forms.ChoiceField(
        choices=EDAD_RECOMENDADA_CHOICES,
        label='Grupo de Edad',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    idioma_local = forms.ChoiceField(
        choices=IDIOMA_LOCAL_CHOICES,
        label='Idioma Local Preferido',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
