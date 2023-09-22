"""Importation des données"""

import pandas as pd


class Importation:
    """Importation des données.

    Cette classe permet d'importer des données
    et de vérifier que le fichier associé soit lisible.

    Parameters
    ----------
    chemin_fichier : str
        Chemin du fichier à importer

    sep : str
        Séparateur des colonnes dans le fichier
        initial (par défaut : ";")
    """

    def __init__(self, chemin_fichier, sep=";"):
        self.chemin_fichier = chemin_fichier
        self.sep = sep

    def lecture(self):
        """Permet d'importer un fichier.

        La fonction lecture permet d'importer un fichier csv, excel
        (xls ou xlsx) ou json sous forme de DataFrame pandas. Elle
        vérifiera que le fichier à importer a une extension valable
        et le format correspondant.


        Returns
        -------
        pandas.core.frame.DataFrame
        DataFrame pandas contenant toutes les données du fichier importé.

        Examples
        --------
        >>> trajets_sncf = Importation("././data/referentiel-gares-voyageurs.csv")
        >>> print(trajets_sncf.lecture().iat[0,2])
        87784793
        """

        match self.chemin_fichier[-4:]:
            case ".csv":
                try:
                    data = pd.read_csv(self.chemin_fichier, sep=self.sep)
                except Exception as exception:
                    print(
                        """Le nom de l'extension du fichier ne correspond pas
                        à son format. Cause erreur:"""
                        + exception
                    )

            case "xlsx":
                try:
                    data = pd.read_excel(self.chemin_fichier)
                except Exception as exception:
                    print(
                        """Le nom de l'extension du fichier ne correspond pas
                        à son format. Cause erreur:"""
                        + exception
                    )

            case ".xls":
                try:
                    data = pd.read_excel(self.chemin_fichier)
                except Exception as exception:
                    print(
                        """Le nom de l'extension du fichier ne correspond pas
                        à son format. Cause erreur:"""
                        + exception
                    )

            case "json":
                try:
                    data = pd.read_json(self.chemin_fichier)
                except Exception as exception:
                    print(
                        """Le nom de l'extension du fichier ne correspond pas
                        à son format. Cause erreur:"""
                        + exception
                    )

            case _:
                raise TypeError("Mauvaise extension")

        return data

    def fusion(self, clef1, clef2, type_fusion, fichier2):
        """Permet de fusionner 2 fichiers.

        La fonction fusion permet de fusionner deux fichiers de types csv,
        excel (xls ou xlsx) ou json (les formats des fichiers étant
        éventuellement distincts) sous forme d'un unique DataFrame pandas.
        Elle vérifiera que les clefs permettant de fusionner
        les 2 fichiers existent.

        Parameters
        ----------
        clef1 : str
            Nom de la colonne en commun des fichiers à fusionner
            (pour le fichier 1)

        clef2 : str
            Nom de la colonne en commun des fichiers à fusionner
            (pour le fichier 2)

        type_fusion : str
            Type de fusion entre les deux fichiers ("inner", "outer",
            "left", "right" ou "cross")

        fichier2 : Importation
            Fichier à fusionner avec le premier

        Returns
        -------
        pandas.core.frame.DataFrame
        DataFrame pandas contenant les données fusionnées des 2 fichiers.

        Examples
        --------
        >>> trajets_sncf = Importation("././data/referentiel-gares-voyageurs.csv")
        >>> tgv_sncf = Importation("././data/tarifs-tgv-inoui-ouigo.csv")
        >>> fusion_test = trajets_sncf.fusion("Code UIC", "Gare origine - code UIC", "inner", tgv_sncf)
        >>> print(fusion_test.iat[0,31])
        87784009
        """
        if clef2 is None:
            clef2 = clef1
        dataframe1 = self.lecture()
        dataframe2 = fichier2.lecture()
        if not isinstance(clef1, str):
            raise TypeError("""La clef doit correspondre au nom d'une colonne
            du fichier 1.""")
        if not isinstance(clef2, str):
            raise TypeError("""La clef doit correspondre au nom d'une colonne
            du fichier 2.""")
        if clef1 not in dataframe1.columns or clef2 not in dataframe2.columns:
            raise ValueError("""Les clefs de fusion doivent être des colonnes
            des fichiers.""")
        return pd.merge(dataframe1, dataframe2, left_on=clef1,
                        right_on=clef2, how=type_fusion)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
