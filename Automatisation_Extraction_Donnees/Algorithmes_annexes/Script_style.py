"""
Model exported as python.
Name : Modèle
Group : 
With QGIS : 32808
"""

from qgis.core import QgsProcessing, QgsProcessingAlgorithm, QgsProcessingParameterVectorLayer, QgsProcessingParameterFile

class ApplyStyleToLayerAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYER = 'INPUT_LAYER'
    STYLE_FILE = 'STYLE_FILE'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                'Layer to style',
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.STYLE_FILE,
                'Style file',
                extension='qml'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        vector_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        style_file = self.parameterAsFile(parameters, self.STYLE_FILE, context)
        
        if vector_layer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_LAYER))
        
        if not vector_layer.isValid():
            feedback.reportError('Layer is not valid!')
            return {}
        
        vector_layer.loadNamedStyle(style_file)
        vector_layer.triggerRepaint()
        
        return {}

    def name(self):
        return 'Style'

    def displayName(self):
        return 'Style'

    def group(self):
        return 'Mes Scripts Personnalisés'

    def groupId(self):
        return 'mesScriptsPersonnalises'

    def createInstance(self):
        return ApplyStyleToLayerAlgorithm()