from controller import pagina_kontrola
import webbrowser

webbrowser.open('http://127.0.0.1:5000')
pagina_kontrola.app.run(debug=True)