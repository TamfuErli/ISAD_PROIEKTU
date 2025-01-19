from controller import pagina_kontrola
import webbrowser

pagina_kontrola.app.run(debug=True)
webbrowser.open('http://127.0.0.1:5000')