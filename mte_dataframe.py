import pandas as pd


class MTEDataFrame:
    FILES_TO_LOAD = ["data/pesajes-01-01-2019-31-12-2020_anonimizado.csv",
                     "data/pesajes-30-07-2021-06-08-2021_anonimizado.csv"]

    _instance = None

    
    def __init__(self):
        raise Exception("Cannot instanciate a singleton")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_instance()
        return cls._instance.copy()

    @classmethod
    def _create_instance(cls):
        dtypes = {'etapa': str,
                  'bolson': float,
                  'camion': str,
                  'peso': int,
                  'cartonero': str,
                  'legacyId': str,
                  'predio': str,
                  'material': str}

        dfs_per_date = [cls._read_mte_csv(filename, dtypes) for filename in cls.FILES_TO_LOAD]
        df = pd.concat(dfs_per_date, ignore_index=True)
        df['fecha'] = pd.to_datetime(df['fecha'])
        df = df.fillna('No especificado')
        return df

    @classmethod
    def _read_mte_csv(cls, csv_name, dtypes):
        return pd.read_csv(csv_name, dtype=dtypes, parse_dates=[0])

    @classmethod
    def create_features(cls):
        df=cls.get_instance()
        predios = df.predio.unique()
        rutas = df.etapa.unique()
        materiales = df.material.unique()
        cartoneres = ["LE", "RA", "No especificado"]
        return predios, rutas, materiales, cartoneres       