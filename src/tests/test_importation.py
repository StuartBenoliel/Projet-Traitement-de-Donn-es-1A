"""Tests sur l'importation des données avec pytest"""

import pytest
import openpyxl
import plus_court_chemin as pcc

#  Tests de lecture de fichiers


@pytest.mark.parametrize(
        'fichier, resultat_attendu',
        [(pcc.Importation("././data/referentiel-gares-voyageurs.csv"),
          87784793),
         (pcc.Importation("././data/tarifs-ter-par-od.csv"),
          87751321),
         (pcc.Importation("././data/tarifs-tgv-inoui-ouigo.csv"),
          71116000),
         (pcc.Importation("././data/air_routes_edges.csv", ","),
          3),
         (pcc.Importation("././data/referentiel-gares-voyageurs.xlsx"),
          87784793)]
)
def test_importation_lecture(fichier, resultat_attendu):
    """Test de la méthode lecture de Importation"""
    assert fichier.lecture().iat[0, 2] == resultat_attendu


#  Tests de fusion de fichiers

@pytest.mark.parametrize(
    'fichier1, fichier2, clef1, clef2, type_fusion, resultat_attendu',
    [(pcc.Importation("././data/lettres_type.xlsx", ";"),
      pcc.Importation("././data/lettres_position.csv", ";"),
      "Lettre", "lettre", "inner", 2)]
)
def test_importation_fusion(fichier1, fichier2, clef1, clef2,
                            type_fusion, resultat_attendu):
    """Test de la méthode fusion de Importation"""
    assert (fichier1.fusion(clef1, clef2, type_fusion, fichier2).iat[0, 2]
            == resultat_attendu)
