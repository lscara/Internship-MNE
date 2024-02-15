"""
Model exported as python.
Name : Modèle
Group : 
With QGIS : 32808
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsExpression
import processing


class Modle(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('couche', 'Couche', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Extraction de données d'observation
        alg_params = {
            'CLASSE': [],
            'DATABASE': 'geonature_lpo',
            'END_DATE': '2024-02-14T00:00:00',
            'EXTRA_WHERE': '',
            'FAMILLE': [],
            'GROUP1_INPN': [],
            'GROUP2_INPN': [],
            'GROUPE_TAXO': [17],  # Oiseaux
            'ORDRE': [],
            'OUTPUT_NAME': "Données d'observation oiseaux",
            'PERIOD': 2,  # 10 dernières années
            'PHYLUM': [],
            'REGNE': [],
            'SOURCE_DATA': [0],  # [LPO]
            'START_DATE': '2024-02-14T00:00:00',
            'STUDY_AREA': parameters['couche'],
            'TYPE_GEOM': 0,  # Point
        }
        outputs['ExtractionDeDonnesDobservation'] = processing.run('scriptsLPO:ExtractData', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Style
        alg_params = {
            'INPUT_LAYER': QgsExpression(' @Extraction_de_données_d_observation_OUTPUT ').evaluate(),
            'STYLE_FILE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AVIFAUNE TOTALE.qml'
        }
        outputs['Style'] = processing.run('script:Style', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'Modèle'

    def displayName(self):
        return 'Modèle'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modle()
