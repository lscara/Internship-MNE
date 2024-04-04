from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterVectorLayer, 
                       QgsProject,
                       QgsProcessingParameterMultipleLayers)

class LayerVisibilityControl(QgsProcessingAlgorithm):
    COUCHE_PERMANENTE_RASTER = 'COUCHE_PERMANENTE_RASTER'
    COUCHE_PERMANENTE_VECTEUR = 'COUCHE_PERMANENTE_VECTEUR'
    COUCHE_DYNAMIQUE = 'COUCHE_DYNAMIQUE'
    COUCHE_DYNAMIQUE2 = 'COUCHE_DYNAMIQUE2'
    COUCHE_DYNAMIQUE3 = 'COUCHE_DYNAMIQUE3'
    COUCHE_DYNAMIQUE4 = 'COUCHE_DYNAMIQUE4'
    COUCHE_DYNAMIQUE5 = 'COUCHE_DYNAMIQUE5'

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
        
        # Paramètre pour sélectionner la couche dynamique (vectorielle)
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.COUCHE_DYNAMIQUE2,
            'Sélectionnez la couche dynamique 2',
            optional=True))
        
        # Paramètre pour sélectionner la couche dynamique (vectorielle)
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.COUCHE_DYNAMIQUE3,
            'Sélectionnez la couche dynamique 3',
            optional=True))
        
        # Paramètre pour sélectionner la couche dynamique (vectorielle)
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.COUCHE_DYNAMIQUE4,
            'Sélectionnez la couche dynamique 4',
            optional=True))
        
        # Paramètre pour sélectionner la couche dynamique (vectorielle)
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.COUCHE_DYNAMIQUE5,
            'Sélectionnez la couche dynamique 5',
            optional=True))

    def processAlgorithm(self, parameters, context, feedback):
        couche_raster_permanente = self.parameterAsRasterLayer(parameters, self.COUCHE_PERMANENTE_RASTER, context)
        couche_vectorielle_permanente = self.parameterAsVectorLayer(parameters, self.COUCHE_PERMANENTE_VECTEUR, context)
        couche_dynamique = self.parameterAsVectorLayer(parameters, self.COUCHE_DYNAMIQUE, context)
        couche_dynamique2 = self.parameterAsVectorLayer(parameters, self.COUCHE_DYNAMIQUE2, context)
        couche_dynamique3 = self.parameterAsVectorLayer(parameters, self.COUCHE_DYNAMIQUE3, context)
        couche_dynamique4 = self.parameterAsVectorLayer(parameters, self.COUCHE_DYNAMIQUE4, context)
        couche_dynamique5 = self.parameterAsVectorLayer(parameters, self.COUCHE_DYNAMIQUE5, context)


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
        
        if couche_dynamique2:
            projet.layerTreeRoot().findLayer(couche_dynamique2.id()).setItemVisibilityChecked(True)

        if couche_dynamique3:
            projet.layerTreeRoot().findLayer(couche_dynamique3.id()).setItemVisibilityChecked(True)

        if couche_dynamique4:
            projet.layerTreeRoot().findLayer(couche_dynamique4.id()).setItemVisibilityChecked(True)
        
        if couche_dynamique5:
            projet.layerTreeRoot().findLayer(couche_dynamique5.id()).setItemVisibilityChecked(True)

        return {}
    
    def name(self):
        return 'activer_couche_v2'

    def displayName(self):
        return 'Activer la couche v2'

    def group(self):
        return 'Mes Scripts Personnalisés'
    
    def groupId(self):
        return 'mesScriptsPersonnalises'

    def createInstance(self):
        return LayerVisibilityControl()
