from django import template

register = template.Library()

@register.filter
def is_numeric(dado):

    try:
        int(dado)
        return True
    except:
        return False
    

@register.filter
def retorna_valor(l, i):

    return l[i]
