import pandas as pd

from utils.utils import determinar_tipo_cartonero


class MTEDataFrame:
    FILES_TO_LOAD = None
    _instance = None

    def __init__(self):
        raise Exception("Cannot instanciate a singleton")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_instance()
        print("~~~~~~~~~~~~~~~")
        print(cls._instance)
        print("~~~~~~~~~~~~~~~")
        return cls._instance.copy()

    @classmethod
    def _create_instance(cls):
        print("files to load ")
        print(cls.FILES_TO_LOAD)
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
        df['tipoCartonero'] = df.apply(determinar_tipo_cartonero, axis=1)
        return df

    @classmethod
    def _read_mte_csv(cls, csv_name, dtypes):
        return pd.read_csv(csv_name, dtype=dtypes, parse_dates=[0])

    @classmethod
    def reset_with_files(cls, files):
        print("reseteando files")
        print(f"{files}")
        cls._instance = None
        cls.FILES_TO_LOAD = files

    @classmethod
    def create_features(cls):
        df = cls.get_instance()
        predios = df.predio.unique()
        rutas = df.etapa.unique()
        materiales = df.material.unique()
        cartoneres = df.tipoCartonero.unique()
        return predios, rutas, materiales, cartoneres
