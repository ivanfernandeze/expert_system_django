from django import forms

class PreferenciasForm(forms.Form):
    CATEGORIAS = [
        ('aventura', 'Aventura'),
        ('cultural', 'Cultural'),
        ('relajación', 'Relajación'),
    ]

    CLIMAS = [
        ('templado', 'Templado'),
        ('frío', 'Frío'),
        ('caliente', 'Caliente'),
    ]

    PRESUPUESTOS = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
    ]

    categoria = forms.ChoiceField(choices=CATEGORIAS, label="Categoría de interés")
    clima = forms.ChoiceField(choices=CLIMAS, label="Preferencia de clima")
    presupuesto = forms.ChoiceField(choices=PRESUPUESTOS, label="Presupuesto")
