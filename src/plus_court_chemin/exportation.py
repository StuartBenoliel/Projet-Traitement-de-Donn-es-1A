"""Exportation des données"""

import pandas as pd


class Exportation:
    """Exportation des données.

    Cette classe permet d'exporter le fichier de données
    traité au format voulu par l'utilisateur.

    Parameters
    ----------
    dataframe : pandas.core.frame.DataFrame
        DataFrame correspondant au fichier de données déjà traité

    chemin : Chemin du fichier
        Chemin du fichier après exportation

    format : Fichier csv, xlsx, xls ou json
        Format souhaité pour le fichier exporté
    """

    def __init__(self, dataframe, chemin, format):
        self.dataframe = dataframe
        self.chemin = chemin
        self.format = format

    def export(self, sep):
        """Permet d'exporter un fichier.

        La fonction export permet d'exporter un fichier csv, excel (xls ou
        xlsx) ou json initialement sous forme de DataFrame pandas. Elle
        vérifiera que le format voulu existe et puisse être créé à
        partir d'un DataFrame pandas.

        Returns
        -------
        Fichier csv, json ou excel
            Fichier traité exporté au format voulu.

        Examples
        --------
        >>> dataframe = Exportation(pd.DataFrame({'C1': [1, 2, 3], 'C2': [2, 4, 5], 'C3': [1, 5, 7], 'C4': [9, 3, 8]}, index = ['L1', 'L2', 'L3']), "././data/exportation_test.csv", "csv")
        >>> print(dataframe.export(";"))
        None
        """
        match self.format:
            case "csv":
                return self.dataframe.to_csv(self.chemin, sep)

            case "xlsx":
                return self.dataframe.to_excel(self.chemin)

            case "xls":
                return self.dataframe.to_excel(self.chemin)

            case "json":
                return self.dataframe.to_json(self.chemin)

            case _:
                raise TypeError("Format d'exportation indisponible")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
