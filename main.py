from flask import Flask, render_template, request, jsonify
import src.plus_court_chemin as pcc
import pandas as pd
import time


app = Flask(__name__)

def nom_to_code(nom, ref):
    if nom == "":
        raise ValueError("Une gare n'a pas été renseignée")

    result = ref[ref["Intitulé plateforme"] == nom]["Code UIC"]

    if result.empty:
        raise ValueError(f"La gare '{nom}' est inconnu")
    else:
        return int(result.iloc[0])

def code_to_nom(code, ref):
    conv = ref[ref["Code UIC"] == code]
    return(list(conv["Intitulé plateforme"])[0])

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search_route', methods=['POST'])
def search_route():
    #on importe les variables de selection depuis le code javascript
    from_gare = request.form['from_gare']
    to_gare = request.form['to_gare']
    tgv = request.form['tgv']
    ouigo = request.form['ouigo']
    ter = request.form['ter']
    classe1 = request.form['classe1']
    classe2 = request.form['classe2']
    prix = request.form['prix']
    
    #on importe et traite les données
    ref_gare = pcc.Importation("data/referentiel-gares-voyageurs.csv").lecture()
    ref_gare = ref_gare[["Code UIC", "Intitulé plateforme"]]

    df1 = pcc.Importation("data/tarifs-tgv-inoui-ouigo.csv").lecture()
    if prix == "max":
        colonne_to_drop = "Prix minimum"
    else :
        colonne_to_drop = "Prix maximum"

    df1 = df1.drop(["Gare origine", "Destination", "Profil tarifaire", colonne_to_drop], axis= 1)
    df1 = df1.set_axis(["Transporteur", "Origine", "Destination", "Classe", "Prix"], axis= 1)

    df2 = pcc.Importation("data/tarifs-ter-par-od.csv").lecture()
    df2 = df2.drop(["Région", "Origine", "Destination", "Libellé tarif"], axis= 1)
    df2 = df2[df2.iloc[:,2] == "Tarif normal"]
    df2 = df2.drop(["Type tarif"], axis= 1)
    
    df2 = df2.set_axis(["Origine", "Destination", "Prix"], axis= 1)

    df = pd.concat([df1, df2],ignore_index=True, sort=False)
    df = df.fillna('ter')

    #on ajoute les correspondances de transport en commun dans quelques villes
    def correspondance():
        df = {
        'Origine': [87751404,87319012,87765024,87765024,87765008,87765008,87318964,87318964,87747006,87335521,87109306,87109306,87223263,87223263,87286005,87286005,
                8751008,87751081,87590299,87590299,87756353,87756353,87756254,87756254,87721175,87723197,87721175,87282624,87721175,87721001,87721175,87722025,
                87721159,87282624,87721159,87721001,87723197,87282624,87697128,87723197,87547000,87547000,87547000,87547000,87547000,87547000,87686667,87686667,
                87686667,87686667,87686667,87686667,87391003,87391003,87391003,87391003,87391003,87391003,87113001,87113001,87113001,87113001,87113001,87113001,
                87686006,87686006,87686006,87686006,87686006,87686006,87271007,87271007,87271007,87271007,87271007,87271007,87271494,87271494,87271494,87271494,
                87271494,87271494],
        'Destination': [87319012,87751404,87765008,87318964,87318964,87765024,87765024,87765008,87335521,87747006,87223263,87286005,87109306,87286005,87109306,87223263,
                87751081,8751008,87756353,87756254,87590299,87756254,87590299,87756353,87723197,87721175,87282624,87721175,87721001,87721175,87722025,87721175,
                87282624,87721159,87721001,87721159,87282624,87723197,87723197,87697128,87686667,87391003,87113001,87686006,87271007,87271494,87391003,87113001,
                87686006,87271007,87271494,87547000,87113001,87686006,87271007,87271494,87547000,87686667,87686006,87271007,87271494,87547000,87686667,87391003,
                87271007,87271494,87547000,87686667,87391003,87113001,87271494,87547000,87686667,87391003,87113001,87686006,87271007,87547000,87686667,87391003,
                87113001,87686006],
        'Prix': [2]*82
        }
        data=pd.DataFrame(df)
        return data

    df = pd.concat([df, correspondance()],ignore_index=True, sort=False)
    df = df.fillna('corres')
    
    
    if tgv == 'false':
        df = df.query('Transporteur != "TGV INOUI"')
        
    if ouigo == 'false':
        df  = df.query('Transporteur != "OUIGO"')
        
    if ter == 'false':
        df = df.query('Transporteur != "ter"')
        
    if classe1 == 'false':
        df  = df.query('Classe != 1.0')
        
    if classe2 == 'false':
        df = df.query('Classe != 2.0')
    
    try:
        from_code = nom_to_code(from_gare, ref_gare)
        to_code = nom_to_code(to_gare, ref_gare)
        t = time.time()
        route =  pcc.Dijkstra(df, "Origine", "Destination", "Prix").chemin_destination(from_code, to_code)
    except ValueError as route:
        result = {
        'route':  str(route),
        }
        return jsonify(result)
    
    route_str = str([code_to_nom(gare, ref_gare) for gare in route[0]])
    route_str = route_str.replace('[', '')
    route_str = route_str.replace(']', '')
    route_str = route_str.replace("'", ' ')
    route_str = route_str.replace('"', ' ')
    route_str = route_str.replace(',', '\n\u2003↓\n\u2003↓\n\u2003↓\n')


    
    result = {
        'route':   f"Itinéraire de {from_gare} à {to_gare}: \n\n{route_str} \n\nPrix {prix} : {route[1]}€  \n\nExecution de Dijkstra : {time.time()-t}s\n\n",
    }
    
    return jsonify(result)

@app.route('/route')
def route():
    return render_template('route.html')

if __name__ == '__main__':
    app.run(debug=True)
