from controller import pagina_kontrola
import webbrowser
import threading
def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

browser_thread = threading.Thread(target=open_browser)
browser_thread.start()

pagina_kontrola.app.run(debug=True)