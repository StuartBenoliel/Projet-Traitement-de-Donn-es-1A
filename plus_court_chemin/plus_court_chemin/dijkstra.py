"""Algorithme de Dijkstra permettant de trouver le plus court chemin
dans un dataframe."""

import pandas as pd


class Dijkstra:
    """Algorithme du plus court chemin.

    Classe modélisant deux versions de l'algorithme de Dijkstra :
    la première calculant le plus court chemin entre le noeud de
    départ et tous les noeuds atteignables tandis que la deuxième
    se contente de trouver le plus court chemin avec un noeud
    d'arrivée et le noeud de départ. La classe modélise également
    le graphe utilisé dans ces deux différentes versions.

    Parametres
    ----------
    dataf : pandas.DataFrame
        Le dataframe contenant les données du graphe.
    colonne_noeud_depart : str
        Le nom de la colonne contenant les nœuds de départ.
    colonne_noeud_arrivee : str
        Le nom de la colonne contenant les nœuds d'arrivée.
    colonne_distance : str
        Le nom de la colonne contenant les distances entre les nœuds.
    """

    def __init__(self, dataf, colonne_noeud_depart, colonne_noeud_arrivee,
                 colonne_distance):

        if not isinstance(dataf, pd.DataFrame):
            raise TypeError("dataf doit être un dataframe pandas")
        if dataf[colonne_noeud_depart].isna().any():
            raise ValueError("Valeurs manquantes")
        if dataf[colonne_noeud_arrivee].isna().any():
            raise ValueError("Valeurs manquantes")
        if dataf[colonne_distance].isna().any():
            raise ValueError("Valeurs manquantes")
        for i in set(dataf[colonne_distance]):
            if not isinstance(i, (float, int)):
                raise TypeError("Distances non numeriques")
            if i < 0:
                raise ValueError("Distances non strictement positives")

        self.dataf = dataf
        self.colonne_noeud_depart = colonne_noeud_depart
        self.colonne_noeud_arrivee = colonne_noeud_arrivee
        self.colonne_distance = colonne_distance

    def graph(self):
        """Crée un graphe représentant les nœuds et les distances entre eux.

        Le graphe est représenté sous la forme d'un dictionnaire dont les
        clés sont les noeuds non culs-de-sac, c'est à dire qu'il existe un
        chemin amenant à une autre destination, et les valeurs une liste
        contenant les couples noeuds voisins et la distance associée également
        dans une liste.

        Renvoie
        --------
        dict[list] :
            Le graphe représenté sous forme de dictionnaire.
        """
        df_grouped = self.dataf.groupby([self.colonne_noeud_depart])
        graphe = {}
        for noeud, data in df_grouped:
            graphe[noeud] = list(zip(data[self.colonne_noeud_arrivee],
                                     data[self.colonne_distance]))
        return graphe

    def chemin_partout(self, source):
        """Trouve le plus court chemin pour une multitude de destinations
          atteignables.

        Renvoie pour chaque noeud atteignable à partir du noeud source
        - c'est à dire s'il existe un chemin reliant le reliant au noeud
        source - une liste contenant les noeuds dans l'ordre de
        passage du chemin ainsi que le coût minimal associé au trajet.
        Si le noeud n'est pas atteignable, la valeur associée au noeud
        est 'Pas de trajet'.

        Parametre
        ----------
        source : any
            noeud de départ nécessairement contenu dans la colonne des départs
            de la table.

        Renvoie
        -------
        dict[list or str] :
            renvoie un dictionnaire dont les clés sont représentés par des
            noeuds et les valeurs une liste comportant le plus court chemin
            et son coût si le noeud est atteignable sinon le
            string 'Pas de trajet'.
        """
        graphe = self.graph()
        marques = []  # Contiendra le nom des noeuds visités
        distances = {sommet: (None, 2**30) for sommet in
                     set(self.dataf[self.colonne_noeud_depart]).union(
                     set(self.dataf[self.colonne_noeud_arrivee]))}

        if source not in set(self.dataf[self.colonne_noeud_depart]):
            return {sommet: 'Pas de trajet' for sommet in distances
                    if sommet != source}
        selection = source
        coefficient = 0
        while len(marques) < len(graphe) and selection is not None:
            marques.append(selection)
            for voisin in graphe[selection]:  # On parcourt ses voisins
                # voisin est le couple (noeud, poids)
                noeud = voisin[0]  # Le noeud qu'on parcourt
                poids = voisin[1]  # Le poids de selection à noeud
                if (noeud not in marques and
                   coefficient + poids < distances[noeud][1]):
                    # On met à jour la distance du noeud à la source
                    distances[noeud] = (selection, coefficient + poids)

            # On recherche le minimum parmi les non marqués
            minimum = (None, 2**30)
            for sommet in graphe:
                if sommet not in marques and distances[sommet][1] < minimum[1]:
                    minimum = (sommet, distances[sommet][1])
            selection, coefficient = minimum

        dict_parcours = {}
        for sommet in distances:
            if sommet != source:
                if distances[sommet][1] == 2**30:
                    dict_parcours[sommet] = 'Pas de trajet'
                else:
                    # Parcourt le graphe à l'envers pour obtenir le chemin
                    parcours = [sommet]
                    intermediaire = sommet
                    while intermediaire != source:
                        intermediaire = distances[intermediaire][0]
                        parcours.append(intermediaire)
                    parcours.reverse()
                    dict_parcours[sommet] = [parcours,
                                             distances[sommet][1]]

        return dict_parcours

    def chemin_destination(self, source, destination):
        """Trouve le plus court chemin pour une destination
          atteignable donnée.

        Renvoie pour un noeud destination atteignable à partir du noeud source
        - c'est à dire s'il existe un chemin reliant le noeud source et le
        noeud destination - une liste contenant les noeuds dans l'odre de
        passage du chemin ainsi que le coût minimal associé au trajet.

        Parametres
        ----------
        source : any
            noeud de départ nécessairement contenu dans la colonne des départs
            de la table.
        destination : any
            noeud d'arrivée nécessairement contenu dans la colonne des arrivées
            de la table.

        Renvoie
        -------
        list or str :
            liste comportant le plus court chemin et son coût ou le string
            'Pas de trajet' si pas de chemin possible.
        """
        if destination == source:
            raise ValueError(f"{destination} est la source et la destination")
        if source not in set(self.dataf[self.colonne_noeud_depart]):
            return 'Pas de trajet'
        if destination not in set(self.dataf[self.colonne_noeud_arrivee]):
            raise ValueError(f"{destination} n'est pas atteignable")

        graphe = self.graph()
        marques = []  # Contiendra le nom des noeuds visités
        distances = {sommet: (None, 2**30) for sommet in
                     set(self.dataf[self.colonne_noeud_depart]).union(
                     set(self.dataf[self.colonne_noeud_arrivee]))}
        selection = source
        coefficient = 0
        while len(marques) < len(graphe) and selection is not None:
            marques.append(selection)
            for voisin in graphe[selection]:  # On parcours ses voisins
                # voisin est le couple (noeud, poids)
                noeud = voisin[0]  # Le noeud qu'on parcourt
                poids = voisin[1]  # Le poids de selection à noeud
                if (noeud not in marques and
                   coefficient + poids < distances[noeud][1]):
                    # On met à jour la distance du noeud à la source
                    distances[noeud] = (selection, coefficient + poids)

            # On recherche le minimum parmi les non marqués
            minimum = (None, 2**30)
            for sommet in graphe:
                if sommet not in marques and distances[sommet][1] < minimum[1]:
                    minimum = (sommet, distances[sommet][1])
            selection, coefficient = minimum

        if distances[destination][1] == 2**30:
            return 'Pas de trajet'
        # Parcourt le graphe à l'envers pour obtenir le chemin
        parcours = [destination]
        sommet = destination
        while sommet != source:
            sommet = distances[sommet][0]
            parcours.append(sommet)
        parcours.reverse()
        return [parcours, distances[destination][1]]
