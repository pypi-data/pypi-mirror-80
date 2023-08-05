import logging

from horno.datos.Fechas import Fecha
from horno.utiles.IO import IOEscritor, IOArchivo, IOSistema, IOCarpeta


#================================================================================================
class Logger ():
    
    # ------------------------------------------------------------------------------------------
    def __init__(self, log_folder=None, data={}):

        self.sep_len = 60
        self.log_folder = log_folder
        self.printear = False
        self.config(data)

    # ------------------------------------------------------------------------------------------
    def config(self, data):

        self.printear = data.get('printear', False)
        self.timestamp = data.get('timestamp', False)

    # ------------------------------------------------------------------------------------------
    def get_log_file(self, log_file_rel):

        if self.log_folder:
            IOCarpeta(self.log_folder).Crear()
            log_file = '%s/%s' % (self.log_folder, log_file_rel)
        else:
            log_file = 'nul'

        return log_file

    # ------------------------------------------------------------------------------------------
    def reset(self, log_file_rel):

        log_file = self.get_log_file(log_file_rel)
        with IOEscritor.DeRuta(log_file).Abrir(False) as iow:
            iow.EscribirLinea('LOG FILE RESETEADO!')

    # ------------------------------------------------------------------------------------------
    def log(self, log_file_rel, texto):

        log_file = self.get_log_file(log_file_rel)
        with IOEscritor.DeRuta(log_file).Abrir(append=True, binario=False) as iow:
            if self.timestamp:
                fecha_ahora = Fecha.Ahora()
                sep = '-' * self.sep_len + '\n'
                iow.Escribir(sep + ('%s' % (fecha_ahora.to_human("%Y-%m-%d %H:%M:%S"))) + '\n')
            iow.Escribir(str(texto) + '\n')

        if self.printear:
            IOSistema().PrintLine(str(texto))

    # ------------------------------------------------------------------------------------------
    def attach(self, log_file_rel, clases):

        log_file = self.get_log_file(log_file_rel)
        for clase in clases:
            logger = logging.getLogger(clase)
            logger.handlers = [h for h in logger.handlers if not IOArchivo.PathFix(log_file) in IOArchivo.PathFix(h.baseFilename)]
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(log_file)
            handler.setLevel(logging.DEBUG)
            sep = '-' * self.sep_len + '\n'
            formatter = logging.Formatter(sep + '%(asctime)s, %(name)s [ %(levelname)s ]\n%(message)s' + '\n')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
