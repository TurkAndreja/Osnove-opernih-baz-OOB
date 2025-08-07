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
def predstave():
    """
    Stran s predstavami.
    """   
    predstave = service.dobi_predstave()  
    return template('predstave.html', predstave = predstave)


@get('/predstave_user')
@cookie_required
def predstave():
    """
    Stran s predstavami, ko je uporabnik prijavljen.
    """   
    predstave = service.dobi_predstave()  
    return template_user('predstave_user.html', predstave = predstave)

@get('/prijavna_stran')
def prijavna_stran():
    """
    Stran s prijavo.
    """     
    return template('prijava.html')

@get('/registracija')
def registracija():
    """
    Stran z registracijo.
    """
    operne_hise = service.dobi_vse_operne_hise()
    return template('registracija.html', operne_hise=operne_hise, napaka=None)

@post('/registracija_post')
def registracija_post():

    username = request.forms.get('username')
    hisa = request.forms.get('hisa')
    password = request.forms.get('password')
    password2 = request.forms.get('password2')

    # Preveri, če se gesli ujemata
    if password != password2:
        operne_hise = service.dobi_vse_operne_hise()
        return template('registracija.html', operne_hise=operne_hise, napaka="Gesli se ne ujemata!")

    auth.dodaj_uporabnika(username, hisa, password)
    return redirect('/prijavna_stran')

@post('/prijava')
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
@cookie_required
def dodaj_predstavo():
    """
    Vrne obrazec za izpolnjevanje nove predstave.
    """

    return template_user('dodaj_predstavo.html')

@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """

    response.delete_cookie("uporabnik")

    return template('index.html', uporabnik=None, napaka=None)


if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)