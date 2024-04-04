from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterVectorLayer, QgsProject)

class LayerVisibilityControl(QgsProcessingAlgorithm):
    COUCHE_PERMANENTE_RASTER = 'COUCHE_PERMANENTE_RASTER'
    COUCHE_PERMANENTE_VECTEUR = 'COUCHE_PERMANENTE_VECTEUR'
    COUCHE_DYNAMIQUE = 'COUCHE_DYNAMIQUE'

    def initAlgorithm(self, config=None):
        # Paramètre pour sélectionner une couche raster permanente
        self.addParameter(QgsProcessingParameterRasterLayer(
            self.COUCHE_PERMANENTE_RASTER,
            'Sélectionnez la couche raster permanente',
            optional=True))  # Rendre ce paramètre optionnel au cas où l'utilisateur n'a pas de couche raster à sélectionner

        # Paramètre pour sélectionner une ou plusieurs couches vectorielles permanentes
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.COUCHE_PERMANENTE_VECTEUR,
            'Sélectionnez la couche vectorielle permanente',
            optional=True))  # Ce paramètre est également optionnel

        # Paramètre pour sélectionner la couche dynamique (vectorielle)
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.COUCHE_DYNAMIQUE,
            'Sélectionnez la couche dynamique',
            optional=True))

    def processAlgorithm(self, parameters, context, feedback):
        couche_raster_permanente = self.parameterAsRasterLayer(parameters, self.COUCHE_PERMANENTE_RASTER, context)
        couche_vectorielle_permanente = self.parameterAsVectorLayer(parameters, self.COUCHE_PERMANENTE_VECTEUR, context)
        couche_dynamique = self.parameterAsVectorLayer(parameters, self.COUCHE_DYNAMIQUE, context)

        projet = QgsProject.instance()

        # Désactive toutes les couches d'abord
        for layer in projet.mapLayers().values():
            projet.layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(False)

        # Active la couche raster permanente, si spécifiée
        if couche_raster_permanente:
            projet.layerTreeRoot().findLayer(couche_raster_permanente.id()).setItemVisibilityChecked(True)

        # Active la couche vectorielle permanente, si spécifiée
        if couche_vectorielle_permanente:
            projet.layerTreeRoot().findLayer(couche_vectorielle_permanente.id()).setItemVisibilityChecked(True)

        # Active la couche dynamique, si spécifiée
        if couche_dynamique:
            projet.layerTreeRoot().findLayer(couche_dynamique.id()).setItemVisibilityChecked(True)

        return {}
    
    def name(self):
        return 'activer_couche'

    def displayName(self):
        return 'Activer la couche'

    def group(self):
        return 'Mes Scripts Personnalisés'
    
    def groupId(self):
        return 'mesScriptsPersonnalises'

    def createInstance(self):
        return LayerVisibilityControl()
