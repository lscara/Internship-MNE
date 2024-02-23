from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, QgsProcessingParameterVectorLayer, QgsProcessingFeedback, edit)

class RemoveDuplicateFeaturesAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYER = 'INPUT_LAYER'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.INPUT_LAYER,
            'Input layer',
            [QgsProcessing.TypeVectorAnyGeometry]
        ))

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        unique_combinations = {}
        ids_to_delete = []

        for feature in layer.getFeatures():
            key = (feature['nom_vern'], feature['NOM'])
            if key in unique_combinations:
                ids_to_delete.append(feature.id())
            else:
                unique_combinations[key] = feature.id()
            
        if ids_to_delete:
            with edit(layer):
                layer.deleteFeatures(ids_to_delete)

        return {}

    
    def name(self):
        return 'Suppression_doublons1.1'

    def displayName(self):
        return 'Suppression des doublons 1.29'

    def group(self):
        return 'Mes Scripts Personnalisés'

    def groupId(self):
        return 'mesScriptsPersonnalises'

    def createInstance(self):
        return RemoveDuplicateFeaturesAlgorithm()
