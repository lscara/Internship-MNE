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
    OUTPUT_FILE = 'OUTPUT_FILE'

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
        self.addParameter(
            QgsProcessingParameterFile(
                self.OUTPUT_FILE,
                'Output file',
                extension='shp'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        style_file = self.parameterAsFile(parameters, self.STYLE_FILE, context)
        output_file = self.parameterAsString(parameters, self.OUTPUT_FILE, context)
        
        if input_layer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_LAYER))
        
        if not input_layer.isValid():
            feedback.reportError('Layer is not valid!')
            return {}
        
        # Créez une nouvelle couche vectorielle vide
        output_layer = QgsVectorLayer(input_layer.source(), input_layer.name(), input_layer.providerType())
        if not output_layer.isValid():
            feedback.reportError('Failed to create output layer!')
            return {}
        
        # Appliquer le style à la nouvelle couche
        output_layer.loadNamedStyle(style_file)
        output_layer.triggerRepaint()

        # Sauvegarder la couche dans un fichier
        error = QgsVectorFileWriter.writeAsVectorFormat(output_layer, output_file, 'utf-8', output_layer.crs(), 'ESRI Shapefile')
        if error[0] != QgsVectorFileWriter.NoError:
            feedback.reportError('Failed to save output file: {}'.format(error))
            return {}

        return {self.OUTPUT_FILE: output_file}

    def name(self):
        return 'StyleV2'

    def displayName(self):
        return 'Style V2'

    def group(self):
        return 'Mes Scripts Personnalisés'

    def groupId(self):
        return 'mesScriptsPersonnalises'

    def createInstance(self):
        return ApplyStyleToLayerAlgorithm()
