from Presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user

from Services.predstave_service import PredstaveService
import os
service = PredstaveService()

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='Presentation/static')


@get('/')
def index():
    """
    Domača stran s predstavami.
    """   

    predstave = service.dobi_predstave()  

    return template('predstave.html', predstave = predstave)

#@get('/transakcije_dto')
#def index():
#    """
#    Stran z dto transakcijami.
#    """   
#
#    transakcije_dto = service.dobi_transakcije_dto()  
#
#    return template('transakcije_dto.html', transakcije = transakcije_dto)

if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)