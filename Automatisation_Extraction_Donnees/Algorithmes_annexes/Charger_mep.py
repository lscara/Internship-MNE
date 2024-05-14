from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, QgsProcessingParameterFile, QgsProject, QgsPrintLayout, QgsReadWriteContext)
from qgis.PyQt.QtXml import QDomDocument
import os

class LoadLayoutsAlgorithm(QgsProcessingAlgorithm):

    FOLDER = 'FOLDER'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDER,
                "Dossier des modèles de mise en page",
                behavior=QgsProcessingParameterFile.Folder
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        folder_path = self.parameterAsString(parameters, self.FOLDER, context)
        for filename in os.listdir(folder_path):
            if filename.endswith('.qpt'):
                file_path = os.path.join(folder_path, filename)
                doc = QDomDocument()
                with open(file_path, 'r') as file:
                    doc.setContent(file.read())
                layout = QgsPrintLayout(QgsProject.instance())
                layout.loadFromTemplate(doc, QgsReadWriteContext())
                layout.setName(os.path.splitext(filename)[0])
                QgsProject.instance().layoutManager().addLayout(layout)
        return {}

    def name(self):
        return 'Charger_les_mises_en_page_depuis_un_dossier'

    def displayName(self):
        return 'Charger les mises en page depuis un dossier'

    def group(self):
        return 'Mes Scripts Personnalisés'

    def groupId(self):
        return 'mesScriptsPersonnalises'
    
    def shortHelpString(self):
        return "Cet algorithme charge tous les modèles de mise en page (.qpt) d'un dossier spécifié dans le projet QGIS actuel."

    def createInstance(self):
        return LoadLayoutsAlgorithm()





