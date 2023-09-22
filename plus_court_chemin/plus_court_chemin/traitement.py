"""
Module pour traiter les dataframes en tant que graphes.
"""
import pandas as pd


class Traitement:
    """
    Une classe pour traiter les dataframes pandas en tant que graphes.
    Attributs
    ----------
    df : pandas.DataFrame
        Le dataframe contenant les données du graphe.
    colonne_noeud_depart : str
        Le nom de la colonne contenant les nœuds de départ.
    colonne_noeud_arrivee : str
        Le nom de la colonne contenant les nœuds d'arrivée.
    colonne_distance : str
        Le nom de la colonne contenant les distances entre les nœuds.
    """
    def __init__(self, df, colonne_noeud_depart,
                 colonne_noeud_arrivee, colonne_distance):

        if not isinstance(df, pd.DataFrame):
            raise TypeError("df doit être un dataframe pandas")
        self.df = df
        self.colonne_noeud_depart = colonne_noeud_depart
        self.colonne_noeud_arrivee = colonne_noeud_arrivee
        self.colonne_distance = colonne_distance

    def ajouter_aretes(self, lignes):
        """
        Ajoute une arête à notre graphe.

        Paramètre
        ----------
        ligne : list
            L'arête à ajouter.

        Retour
        -------
        None
        """
        return pd.concat([self.df, lignes], ignore_index=True, sort=False)

    def supprimer_arete(self, ligne):
        """
        Supprime une arête de notre graphe.

        Paramètres
        ----------
        ligne : int
            L'indice de l'arête à supprimer.

        Retour
        -------
        None
        """
        return self.df.drop(ligne)

    def graph(self):
        """
        Crée un graphe représentant les nœuds et les distances entre eux.

        Retour :
        --------
        dict :
            Le graphe représenté sous forme de dictionnaire.
        """
        df_grouped = self.df.groupby([self.colonne_noeud_depart])
        graphe = {}
        for noeud, data in df_grouped:
            graphe[noeud] = list(zip(data[self.colonne_noeud_arrivee],
                                     data[self.colonne_distance]))
        return graphe

    def filtrer_dataframe(self, colonne, condition, valeur):
        """
        Filtre un DataFrame en fonction d'une condition et d'une valeur dans
        une colonne spécifique. Pour du filtrage plus complexe : utiliser la
        méthode query pour les dataframes.

        Paramètres
        ----------
        df : pandas.DataFrame
            Le DataFrame à filtrer.
        colonne : str
            Le nom de la colonne sur laquelle appliquer le filtre.
        condition : str
            La condition à appliquer ('>', '<', '==', '>=', '<=', '!=').
        valeur : any
            La valeur à comparer.

        Retour
        -------
        pandas.DataFrame :
            Le DataFrame filtré.
        """
        if condition == '>':
            return self.df[self.df[colonne] > valeur]
        if condition == '<':
            return self.df[self.df[colonne] < valeur]
        if condition == '==':
            return self.df[self.df[colonne] == valeur]
        if condition == '>=':
            return self.df[self.df[colonne] >= valeur]
        if condition == '<=':
            return self.df[self.df[colonne] <= valeur]
        if condition == '!=':
            return self.df[self.df[colonne] != valeur]
        raise ValueError(f"""Condition invalide {condition}. Doit etre '>',
                         '<', '==', '>=', '<=', '!='.""")

    def retirer_manquant(self):
        """
        Cette fonction supprime les lignes avec des valeurs manquantes dans un
        DataFrame pandas.

        Parametre
        ----------
            df : DataFrame pandas

        Renvoie
        --------
            DataFrame pandas après suppression des lignes contenant des
            valeurs manquantes.
        """
        return self.df.dropna()
