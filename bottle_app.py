# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route, template


# @route('/')
# def afficher_budget():
#     return 'Pour un budget de 0€ les salariés touchent 0€ chacun '


def get_salaire(budget):
    return budget / 3


@route('/budget/<budget:int>')
def afficher_budget(budget):
    salaire = get_salaire(budget)
    return f"Pour un budget de {budget}€ et un TJM égal pour tous, les 3 salariés touchent {salaire}€ chacun"


application = default_app()
