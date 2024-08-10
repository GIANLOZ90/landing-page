import os
from flask import Flask

app = Flask(__name__)

# Definisci le tue rotte qui
@app.route("/")
def home():
    return "Hello, Render!"

if __name__ == "__main__":
    # Ottieni la porta dall'ambiente, o usa 5000 come default
    port = int(os.environ.get('PORT', 5000))
    # Avvia l'app su 0.0.0.0 con la porta specificata
    app.run(host='0.0.0.0', port=port, debug=True)

