import os
import json
from requests.sessions import Session
from . import querySerializer
from . import mainExecutable
from ..blocks import *

class handler():
    def init(self):
        # Cambiar de un dominio externo a una ruta local
        self.ROOT = "local_data"  # Cambia este valor a la ruta local deseada
        self.RP = mainExecutable.Generator.selector(querySerializer.cursor().getConfig("libs")[2])
        self.SYS = mainExecutable.Generator.selector(querySerializer.cursor().getConfig("libs")[4])
        self.RQ = mainExecutable.Generator.selector(querySerializer.cursor().getConfig("libs")[3])

    def pull(self):
        DIRREPO = self.SYS.path.join(querySerializer.cursor().hereFile, "..", "..", "..")
        repo = self.RP.Repo(DIRREPO)
        configUser = self.SYS.path.join(DIRREPO, "src", "config", "config.json")

        try:
            # Stash changes to config.json if there are any
            if repo.is_dirty(path=configUser):
                repo.git.stash('save', 'Auto stash config.json before pull', configUser)

            # Perform the pull
            repo.remotes.origin.pull()
            
            # Restore the stashed config.json if it was stashed
            stashes = repo.git.stash('list')
            if 'Auto stash config.json before pull' in stashes:
                repo.git.stash('pop')

        except self.RP.exc.GitCommandError as e:
            animERROR(f"Git pull failed: {e}")
            raise

    def deprecated(self) -> dict:
        echo = str(self.RP.Repo(self.SYS.path.join(querySerializer.cursor().hereFile, "..", "..", "..")).head.commit.hexsha)
        # Comparar commits de manera local usando un hash fijo o archivo local
        local_hash = "a1b2c3d4e5f6"  # Cambia a tu hash local o a otro método de comparación
        return {'STTS': echo != local_hash}

def getNews(self) -> list:
    try:
        # Verifica si el archivo existe antes de intentar cargarlo
        local_path = self.joinerDirs(["DisponibleValor", "agregarName.json"])
        if not os.path.exists(local_path):
            animERROR(f"El archivo {local_path} no existe.")
            return []  # Devuelve una lista vacía si no existe el archivo

        with open(local_path, "r") as file:
            rsp = json.load(file)
    except Exception as Error:
        animERROR(f"Error al cargar el archivo: {Error}")
        return []  # En caso de error, devolver una lista vacía
    else:
        return rsp.get("news", [])  # Si no hay error, devolver los datos de "news"




    def api(self) -> Session:
        # Si necesitas la funcionalidad de 'requests', mantenla
        return self.RQ.session()
    
    def joinerDirs(self, listData: list) -> str:
        DIR = os.path.join(self.ROOT, *listData)  # Unir la ruta relativa
        return os.path.abspath(DIR)  # Asegura que devuelva la ruta absoluta

    def listDataRequirements(self) -> list:
        return ([self.joinerDirs(["DisponibleValor", "agregarName.json"]),
            self.joinerDirs(["DisponibleValor", "Comprobantes", "descargar.json"])],
            self.joinerDirs(["DisponibleValor", "upload.json"]),
            ["NumeroNequi", "Nombre", "Valor"])