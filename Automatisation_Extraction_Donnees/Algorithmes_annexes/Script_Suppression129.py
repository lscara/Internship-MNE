from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, QgsProcessingParameterVectorLayer, QgsProcessingFeedback, QgsFeatureSink, QgsProcessingParameterFeatureSink, QgsVectorLayer, QgsField, QgsFields, QgsFeature)

class RemoveDuplicateFeaturesAlgorithm(QgsProcessingAlgorithm):
    INPUT_LAYER = 'INPUT_LAYER'
    OUTPUT_LAYER = 'OUTPUT_LAYER'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.INPUT_LAYER,
            'Input layer',
            [QgsProcessing.TypeVectorAnyGeometry]
        ))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT_LAYER,
            'Output layer'
        ))

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
        total = 100.0 / input_layer.featureCount() if input_layer.featureCount() else 0
        unique_combinations = {}
        fields = input_layer.fields()

        # Créer une nouvelle couche en mémoire avec la même structure que la couche d'entrée
        crs = input_layer.crs().toWkt()
        uri = f"Point?crs={crs}" if input_layer.wkbType() == 1 else f"Linestring?crs={crs}" if input_layer.wkbType() == 2 else f"Polygon?crs={crs}"
        output_layer = QgsVectorLayer(uri, "unique_features", "memory")
        output_layer_data = output_layer.dataProvider()
        output_layer_data.addAttributes(fields)
        output_layer.updateFields()

        # Copier les entités uniques dans la nouvelle couche
        for current, feature in enumerate(input_layer.getFeatures()):
            if feedback.isCanceled():
                break
            key = (feature['nom_vern'], feature['NOM'])
            if key not in unique_combinations:
                unique_combinations[key] = feature
                output_layer_data.addFeature(feature)
            feedback.setProgress(int(current * total))

        # Ajouter la nouvelle couche au projet (facultatif)
        # QgsProject.instance().addMapLayer(output_layer)

        # Renvoyer la nouvelle couche comme résultat de l'algorithme
        (sink, output_layer_id) = self.parameterAsSink(parameters, self.OUTPUT_LAYER, context, fields, input_layer.wkbType(), input_layer.sourceCrs())
        for feature in unique_combinations.values():
            sink.addFeature(feature, QgsFeatureSink.FastInsert)

        return {self.OUTPUT_LAYER: output_layer_id}
    

    def name(self):
        return 'Suppression_doublons1.1.1'

    def displayName(self):
        return 'Suppression des doublons 1.29.1'

    def group(self):
        return 'Mes Scripts Personnalisés'

    def groupId(self):
        return 'mesScriptsPersonnalises'

    def createInstance(self):
        return RemoveDuplicateFeaturesAlgorithm()
