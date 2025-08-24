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
    id_uporabnika = service.id_uporabnika()

    return template_user('predstave_user.html', predstave=predstave, id_uporabnika=id_uporabnika)

@get('/uredi_predstavo/<id_predstave:int>')
@cookie_required
def uredi_predstavo(id_predstave):
    """
    Stran, ki je primarno za dodajanje pevcev vlogam in sekundarno za urejanje drugih podatkov
    v zvezi z že napovedano predstavo. Odvisna je od id_predstave, ki je zapisan v url.
    """
    predstava = service.dobi_predstavo(id_predstave)
    vloge = service.dobi_vloge(id_predstave)
    pevci = service.dobi_pevce()
    pevci = [pevec for pevec in pevci if service.je_pevec_prost(pevec.id, id_predstave)]

    return template_user('uredi_predstavo.html', predstava=predstava, vloge=vloge, pevci=pevci)

@post('/uredi_predstavo/<id_predstave:int>')
@cookie_required
def shrani_predstavo(id_predstave):
    """
    Shrani posodobljene podatke predstave in vlog.
    """

    datum_str = request.forms.get('datum')
    ura_str = request.forms.get('cas')
    cena_str = request.forms.get('cena')
    komentar = request.forms.get('komentar')

    service.posodobi_predstavo(id_predstave, datum_str, ura_str, cena_str, komentar)

    vloge = service.dobi_vloge(id_predstave)
    for vloga in vloge:
        id_pevca = int(request.forms.get(f'vloga_{vloga.id_vloge}'))
        service.posodobi_vlogo(id_predstave, vloga.id_vloge, id_pevca)

    redirect(url('/predstave_user'))

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
    password = request.forms.getunicode('password')
    password2 = request.forms.getunicode('password2')

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
    password = request.forms.getunicode('password')

    if not auth.obstaja_uporabnik(username):
        return template("index.html", napaka="Uporabnik s tem imenom ne obstaja")

    prijava = auth.prijavi_uporabnika(username, password)
    if prijava:
        response.set_cookie("uporabnik", username)

        redirect(url('/predstave_user'))

    else:
        return template("prijava.html", uporabnik=None, napaka="Neuspešna prijava. Napačno geslo ali uporabniško ime.")


@get('/dodaj_opero')
def dodaj_opero():
    """
    Stran za dodajanje opere.
    """
    
    return template_user('dodaj_opero.html')



@post('/dodaj_opero')
@cookie_required
def dodaj_opero():

     # Preberemo podatke iz forme

    naslov = request.forms.getunicode('naslov')
    skladatelj = request.forms.getunicode('skladatelj')
    trajanje = request.forms.get('trajanje')
    leto = request.forms.get('leto')   

    service.ustvari_opero(naslov, skladatelj, trajanje, leto)


    vloge = [vloga.decode('utf-8') for vloga in request.forms.getlist('vloga[]')]
    fachi = request.forms.getlist('fach[]')
    dvojice = list(zip(vloge, fachi))

    service.ustvari_vloge(dvojice, naslov)
    
    redirect(url('/predstave_user'))


@get('/dodaj_pevca')
def dodaj_opero():
    """
    Stran za dodajanje pevca. 
    """
    #response.content_type = 'text/html; charset=UTF-8'
    seznam = service.dobi_seznam_glasov()
    return template_user('dodaj_pevca.html', seznam_glasov = seznam)


@post('/dodaj_pevca')
@cookie_required
def dodaj_pevca():

    ime = request.forms.getunicode('ime')
    id_glas = int(request.forms.get('glas'))

    service.ustvari_pevca(ime, id_glas)
    #response.content_type = 'text/html; charset=UTF-8'

    redirect(url('/predstave_user'))


@get('/dodaj_predstavo')
@cookie_required
def dodaj_predstavo():
    """
    Stran za dodajanje predstav.  
    """
    seznam_oper = service.dobi_seznam_oper()

    return template_user('dodaj_predstavo.html', seznam_oper = seznam_oper)


@post('/dodaj_predstavo')
@cookie_required
def dodaj_predstavo():

    id_opere = int(request.forms.get('id_opere'))
    datum_str = request.forms.get('datum') 
    ura_str = request.forms.get('ura')
    cena_str = request.forms.get('cena')  
    komentar = request.forms.getunicode('komentar') 

    service.ustvari_predstavo(id_opere, datum_str, ura_str, cena_str, komentar)

    redirect(url('/predstave_user'))



@get('/odjava')
def odjava():
    """
    Odjavi uporabnika iz aplikacije. Pobriše piškotke o uporabniku in njegovi roli.
    """

    response.delete_cookie("uporabnik")

    return template('index.html', uporabnik=None, napaka=None)


if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)