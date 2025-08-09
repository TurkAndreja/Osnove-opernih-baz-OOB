from functools import wraps
from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.predstave_service import PredstaveService
from Services.auth_service import AuthService
import os

service = PredstaveService()
auth = AuthService()

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)



#POSKUS DEKORATORJA ZA UTF8
# def nastavi_utf8(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         response.content_type = 'text/html; charset=UTF-8'
#         return f(*args, **kwargs)
#     return wrapper


def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        cookie = request.get_cookie("uporabnik")
        if cookie:
            return f(*args, **kwargs)
        return template("index.html",uporabnik=None, napaka="Potrebna je prijava!")
    return decorated


@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')


@get('/')
def index():
    """
    Začetna stran s prijavo in dobrodošlico.
    """  
    return template('index.html')

@get('/predstave')
#@nastavi_utf8
def predstave():
    """
    Stran s predstavami.
    """   
    predstave = service.dobi_predstave()  
    return template('predstave.html', predstave = predstave)


@get('/predstave_user')
#@nastavi_utf8
@cookie_required
def predstave():
    """
    Stran s predstavami, ko je uporabnik prijavljen.
    """   
    predstave = service.dobi_predstave()  
    return template_user('predstave_user.html', predstave = predstave)

@get('/prijavna_stran')
#@nastavi_utf8
def prijavna_stran():
    """
    Stran s prijavo.
    """     
    return template('prijava.html')


@post('/prijava')
#@nastavi_utf8
def prijava():
    """
    Prijavi uporabnika v aplikacijo. Če je prijava uspešna, ustvari piškotke o uporabniku in operni hiši.
    Drugače sporoči, da je prijava neuspešna.
    """
    username = request.forms.get('username')
    password = request.forms.get('password')

    if not auth.obstaja_uporabnik(username):
        return template("index.html", napaka="Uporabnik s tem imenom ne obstaja")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)

        redirect(url('/predstave_user'))

    else:
        return template("prijava.html", uporabnik=None, napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")


@get('/dodaj_predstavo')
#@nastavi_utf8
@cookie_required
def dodaj_predstavo():
    """
    Vrne obrazec za izpolnjevanje nove predstave.
    """

    return template_user('dodaj_predstavo.html')


@get('/dodaj_opero')
#@nastavi_utf8
def dodaj_opero():
    """
    Stran za dodajanje opere.  """
    
    return template_user('dodaj_opero.html')



@post('/dodaj_opero')
#@nastavi_utf8
@cookie_required
def dodaj_opero():

     # Preberemo podatke iz forme. Lahko bi uporabili kakšno dodatno metodo iz service objekta

    naslov = request.forms.get('naslov')
    skladatelj = request.forms.get('skladatelj')
    trajanje = request.forms.get('trajanje')
    leto = request.forms.get('leto')   

    service.ustvari_opero(naslov, skladatelj, trajanje, leto)

    vloge = request.forms.getlist('vloga[]')
    fachi = request.forms.getlist('fach[]')
    dvojice = list(zip(vloge, fachi))

    service.ustvari_vloge(dvojice, naslov)

    #return "Opera in vloge so bile dodane!"
    
    redirect(url('/predstave_user'))


@get('/dodaj_pevca')
#@nastavi_utf8
def dodaj_opero():
    """
    Stran za dodajanje pevca.  """
    #response.content_type = 'text/html; charset=UTF-8'
    seznam = service.dobi_seznam_glasov()
    return template_user('dodaj_pevca.html', seznam_glasov = seznam)


@post('/dodaj_pevca')
#@nastavi_utf8
@cookie_required
def dodaj_pevca():

    ime = request.forms.get('ime')
    id_glas = int(request.forms.get('glas'))

    service.ustvari_pevca(ime, id_glas)
    #response.content_type = 'text/html; charset=UTF-8'

    redirect(url('/predstave_user'))


@get('/dodaj_predstavo')
#@nastavi_utf8
def dodaj_predstavo():
    """
    Stran za dodajanje predstav.  """
    seznam = service.dobi_seznam_oper()

    return template_user('dodaj_predstavo.html', seznam_oper = seznam)


@post('/dodaj_predstavo')
#@nastavi_utf8
@cookie_required
def dodaj_predstavo():

    id_opere = int(request.forms.get('id_opere'))
    datum_str = request.forms.get('datum') 
    ura_str = request.forms.get('ura')
    cena_str = request.forms.get('cena')  
    komentar = request.forms.get('komentar') 

    service.ustvari_predstavo(id_opere, datum_str, ura_str, cena_str, komentar)

    redirect(url('/predstave_user'))



@get('/odjava')
#@nastavi_utf8
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """

    response.delete_cookie("uporabnik")

    return template('index.html', uporabnik=None, napaka=None)


if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)