""" Tests du module chemin avec pytest """
import re
import pytest
import pandas as pd
from plus_court_chemin.dijkstra import Dijkstra


df_ex_1 = {
    'Départ': ['Paris', 'Paris', 'Paris', 'Marseille', 'Bastia', 'Marseille',
               'Lyon', 'Lyon', 'Lyon', 'Rennes', 'Rennes', 'Ajaccio'],
    'Arrivé': ['Lyon', 'Rennes', 'Tarbes', 'Lyon', 'Ajaccio', 'Rennes',
               'Marseille', 'Paris', 'Rennes', 'Lyon', 'Paris', 'Bastia'],
    'Distance': [4, 3, 5, 2, None, 4, 2, 4, 3, 3, 3, 3.5]
}  # Valeur manquante

df_ex_2 = {
    'Départ': [101, 101, 101, 102, 107, 102, 103, 103, 103, 104, 104, 106],
    'Arrivé': [103, 104, 105, 103, 106, 104, 102, 101, 104, 103, 101, 107],
    'Distance': [4, 3, 5, 2, '0', 4, 2, 4, 3, 3, 3, 3.5]
}  # Poid non numérique

df_ex_3 = {
    'Départ': [101, 101, 101, 102, 107, 102, 103, 103, 103, 104, 104, 106],
    'Arrivé': [103, 104, 105, 103, 106, 104, 102, 101, 104, 103, 101, 107],
    'Distance': [4, 3, 5, 2, -3.5, 4, 2, 4, 3, 3, 3, 3.5]
}  # Poid non strictement positif

dataf_ex_1 = pd.DataFrame(df_ex_1)
dataf_ex_2 = pd.DataFrame(df_ex_2)
dataf_ex_3 = pd.DataFrame(df_ex_3)

MESSAGE_1 = "Distances non numeriques"
MESSAGE_2 = "Valeurs manquantes"
MESSAGE_3 = "Distances non strictement positives"


@pytest.mark.parametrize('''dataf, colonne_noeud_depart, colonne_noeud_arrivee,
 colonne_distance, message_erreur, type_erreur''', [
  (dataf_ex_1, 'Départ', 'Arrivé', 'Distance', MESSAGE_2, ValueError),
  (dataf_ex_2, 'Départ', 'Arrivé', 'Distance', MESSAGE_1, TypeError),
  (dataf_ex_3, 'Départ', 'Arrivé', 'Distance', MESSAGE_3, ValueError)])
def test_erreur_init_dijkstra(dataf, colonne_noeud_depart,
                              colonne_noeud_arrivee, colonne_distance,
                              message_erreur, type_erreur):
    """
    Test des erreurs provoquées par l'initialisation de la classe Dijkstra.
    """
    with pytest.raises(type_erreur, match=re.escape(message_erreur)):
        Dijkstra(dataf, colonne_noeud_depart, colonne_noeud_arrivee,
                 colonne_distance)


df_ex_1 = {
    'Départ': ['Paris', 'Paris', 'Paris', 'Marseille', 'Bastia', 'Marseille',
               'Lyon', 'Lyon', 'Lyon', 'Rennes', 'Rennes', 'Ajaccio'],
    'Arrivé': ['Lyon', 'Rennes', 'Tarbes', 'Lyon', 'Ajaccio', 'Rennes',
               'Marseille', 'Paris', 'Rennes', 'Lyon', 'Paris', 'Bastia'],
    'Distance': [4, 3, 5, 2, 9, 4, 2, 4, 3, 3, 3, 3.5]
}

df_ex_2 = {
    'Départ': [101, 101, 101, 102, 107, 102, 103, 103, 103, 104, 104, 106],
    'Arrivé': [103, 104, 105, 103, 106, 104, 102, 101, 104, 103, 101, 107],
    'Distance': [4, 3, 5, 2, 0, 4, 2, 4, 3, 3, 3, 3.5]
}
dataf_ex_1 = pd.DataFrame(df_ex_1)
dataf_ex_2 = pd.DataFrame(df_ex_2)


@pytest.mark.parametrize('''dataf, colonne_noeud_depart, colonne_noeud_arrivee,
 colonne_distance,source, destination, message_erreur''', [
  (dataf_ex_1, 'Départ', 'Arrivé', 'Distance', 'Paris', 'Paris',
   "Paris est la source et la destination"),
  (dataf_ex_2, 'Départ', 'Arrivé', 'Distance', 101, 101,
   "101 est la source et la destination"),
  (dataf_ex_2, 'Départ', 'Arrivé', 'Distance', 101, 'Paris',
   "Paris n'est pas atteignable")])
def test_erreur_destination_dijkstra(dataf, colonne_noeud_depart,
                                     colonne_noeud_arrivee, colonne_distance,
                                     source, destination, message_erreur):
    """
    Test des erreurs provoquées par chemin_destination de la classe
    Dijkstra.
    """
    with pytest.raises(ValueError, match=re.escape(message_erreur)):
        Dijkstra(dataf, colonne_noeud_depart, colonne_noeud_arrivee,
                 colonne_distance).chemin_destination(source, destination)


df_ex_4 = {
    'Distance': [4, 3, 5, 2, 4, 4, 2, 4, 3, 3, 3, 3.5],
    'Départ': ['Paris', 'Paris', 'Paris', 'Marseille', 'Bastia', 'Marseille',
               'Lyon', 'Lyon', 'Lyon', 'Rennes', 'Rennes', 'Ajaccio'],
    'Arrivé': ['Lyon', 'Rennes', 'Tarbes', 'Lyon', 'Ajaccio', 'Rennes',
               'Marseille', 'Paris', 'Rennes', 'Lyon', 'Paris', 'Bastia']
}

graphe_ex_4 = {
    'Paris': [('Lyon', 4), ('Rennes', 3), ('Tarbes', 5)],
    'Marseille': [('Lyon', 2), ('Rennes', 4)],
    'Bastia': [('Ajaccio', 4)],
    'Lyon': [('Marseille', 2), ('Paris', 4), ('Rennes', 3)],
    'Rennes': [('Lyon', 3), ('Paris', 3)],
    'Ajaccio': [('Bastia', 3.5)]
}

df_ex_5 = {
    'Départ': [101, 101, 101, 102, 107, 102, 103, 103, 103, 104, 104, 106],
    'Arrivé': [103, 104, 105, 103, 106, 104, 102, 101, 104, 103, 101, 107],
    'Distance': [4, 3, 5, 2, 4, 4, 2, 4, 3, 3, 3, 3.5]
}  # dataframe générant un graphe non symétrique

graphe_ex_5 = {
    101: [(103, 4), (104, 3), (105, 5)],
    102: [(103, 2), (104, 4)],
    107: [(106, 4)],
    103: [(102, 2), (101, 4), (104, 3)],
    104: [(103, 3), (101, 3)],
    106: [(107, 3.5)]}


dataf_ex_4 = pd.DataFrame(df_ex_4)
dataf_ex_5 = pd.DataFrame(df_ex_5)


@pytest.mark.parametrize('''dataf, colonne_noeud_depart, colonne_noeud_arrivee,
 colonne_distance, resultat''', [
  (dataf_ex_4, 'Départ', 'Arrivé', 'Distance', graphe_ex_4),
  (dataf_ex_5, 'Départ', 'Arrivé', 'Distance', graphe_ex_5)])
def test_resultat_graph_dijkstra(dataf, colonne_noeud_depart,
                                 colonne_noeud_arrivee, colonne_distance,
                                 resultat):
    """
    Test des résultats de graph de la classe Dijkstra.
    """
    assert Dijkstra(dataf, colonne_noeud_depart, colonne_noeud_arrivee,
                    colonne_distance).graph() == resultat


resultat_partout_ex_1 = {
    'Paris': 'Pas de trajet',
    'Marseille': 'Pas de trajet',
    'Bastia': 'Pas de trajet',
    'Lyon': 'Pas de trajet',
    'Rennes': 'Pas de trajet',
    'Ajaccio': 'Pas de trajet'}  # Cas du noeud sans issue / cul-de-sac

resultat_partout_ex_2 = {
    'Paris': 'Pas de trajet',
    'Marseille': 'Pas de trajet',
    'Lyon': 'Pas de trajet',
    'Rennes': 'Pas de trajet',
    'Ajaccio': [['Bastia', 'Ajaccio'], 4],
    'Tarbes': 'Pas de trajet'}  # Cas d'un graphe non connexe

resultat_partout_ex_3 = {
    'Marseille': [['Paris', 'Lyon', 'Marseille'], 6],
    'Bastia': 'Pas de trajet',
    'Lyon': [['Paris', 'Lyon'], 4],
    'Rennes': [['Paris', 'Rennes'], 3],
    'Ajaccio': 'Pas de trajet',
    'Tarbes': [['Paris', 'Tarbes'], 5]}

resultat_partout_ex_4 = {
    102: [[101, 103, 102], 6],
    107: 'Pas de trajet',
    103: [[101, 103], 4],
    104: [[101, 104], 3],
    106: 'Pas de trajet',
    105: [[101, 105], 5]}


@pytest.mark.parametrize('''dataf, colonne_noeud_depart, colonne_noeud_arrivee,
 colonne_distance, source, resultat''', [
  (dataf_ex_4, 'Départ', 'Arrivé', 'Distance', 'Tarbes',
   resultat_partout_ex_1),
  (dataf_ex_4, 'Départ', 'Arrivé', 'Distance', 'Bastia',
   resultat_partout_ex_2),
  (dataf_ex_4, 'Départ', 'Arrivé', 'Distance', 'Paris',
   resultat_partout_ex_3),
  (dataf_ex_5, 'Départ', 'Arrivé', 'Distance', 101,
   resultat_partout_ex_4)])
def test_resultat_partout_dijkstra(dataf, colonne_noeud_depart,
                                   colonne_noeud_arrivee, colonne_distance,
                                   source, resultat):
    """
    Test des résultats de chemin_partout de la classe Dijkstra.
    """
    assert Dijkstra(dataf, colonne_noeud_depart, colonne_noeud_arrivee,
                    colonne_distance).chemin_partout(source) == resultat


@pytest.mark.parametrize('''dataf, colonne_noeud_depart, colonne_noeud_arrivee,
 colonne_distance, source, destination, resultat''', [
  (dataf_ex_4, 'Départ', 'Arrivé', 'Distance', 'Tarbes', 'Paris',
   'Pas de trajet'),  # Non symétrie du graphe en terme de trajet respectée
  (dataf_ex_4, 'Départ', 'Arrivé', 'Distance', 'Bastia', 'Marseille',
   'Pas de trajet'),
  (dataf_ex_4, 'Départ', 'Arrivé', 'Distance', 'Paris', 'Marseille',
   [['Paris', 'Lyon', 'Marseille'], 6]),
  (dataf_ex_5, 'Départ', 'Arrivé', 'Distance', 106, 107,
   [[106, 107], 3.5]),
  (dataf_ex_5, 'Départ', 'Arrivé', 'Distance', 107, 106,
   [[107, 106], 4])])  # Non symétrie du graphe en terme de distances respectée
def test_resultat_destination_dijkstra(dataf, colonne_noeud_depart,
                                       colonne_noeud_arrivee, colonne_distance,
                                       source, destination, resultat):
    """
    Test des résultats de chemin_destination de la classe Dijkstra.
    """
    assert (Dijkstra(dataf, colonne_noeud_depart, colonne_noeud_arrivee,
                     colonne_distance).chemin_destination(source, destination)
            == resultat)
