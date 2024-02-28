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
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterFolderDestination
from qgis.core import QgsExpression
import processing


class Modle(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('communes_mayenne', 'Communes_Mayenne', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('couche', 'Couche', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Jointure', 'Jointure', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/Jointure.shp'))
        self.addParameter(QgsProcessingParameterFileDestination('DonnesDobservationSauvegardes', "Données d'observation sauvegardées", fileFilter='GeoPackage (*.gpkg *.GPKG);;ESRI Shapefile (*.shp *.SHP);;(Geo)Arrow (*.arrow *.feather *.arrows *.ipc *.ARROW *.FEATHER *.ARROWS *.IPC);;(Geo)Parquet (*.parquet *.PARQUET);;AutoCAD DXF (*.dxf *.DXF);;Fichier de Geodatabase ESRI (*.gdb *.GDB);;FlatGeobuf (*.fgb *.FGB);;Geoconcept (*.gxt *.txt *.GXT *.TXT);;Geography Markup Language [GML] (*.gml *.GML);;GeoJSON - Newline Delimited (*.geojsonl *.geojsons *.json *.GEOJSONL *.GEOJSONS *.JSON);;GeoJSON (*.geojson *.GEOJSON);;GeoRSS (*.xml *.XML);;GPS eXchange Format [GPX] (*.gpx *.GPX);;INTERLIS 1 (*.itf *.xml *.ili *.ITF *.XML *.ILI);;INTERLIS 2 (*.xtf *.xml *.ili *.XTF *.XML *.ILI);;Keyhole Markup Language [KML] (*.kml *.KML);;Mapinfo TAB (*.tab *.TAB);;Microstation DGN (*.dgn *.DGN);;PostgreSQL SQL dump (*.sql *.SQL);;S-57 Base file (*.000 *.000);;SQLite (*.sqlite *.SQLITE);;Tableur MS Office Open XML [XLSX] (*.xlsx *.XLSX);;Tableur Open Document  [ODS] (*.ods *.ODS);;Valeurs séparées par une virgule [CSV] (*.csv *.CSV)', createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/Données observation sauvegardées.shp'))
        self.addParameter(QgsProcessingParameterFolderDestination('DossierMne', 'Dossier MNE', createByDefault=True, defaultValue='C:\\Users\\lored\\Documents\\MNE'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsOiseaux', 'Suppression des doublons oiseaux', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/oiseaux_sans_doublon.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsAmphi', 'Suppression des doublons amphi', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/amphi_sans_doublon.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsMammif', 'Suppression des doublons mammif', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/mammif_sans_doublon.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsReptiles', 'Suppression des doublons reptiles', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(39, model_feedback)
        results = {}
        outputs = {}

        # Créer un index spatial
        alg_params = {
            'INPUT': parameters['communes_mayenne']
        }
        outputs['CrerUnIndexSpatial'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Sauvegarder les entités vectorielles dans un fichier
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': parameters['couche'],
            'LAYER_NAME': 'Données observation sauvegardées',
            'LAYER_OPTIONS': '',
            'OUTPUT': parameters['DonnesDobservationSauvegardes']
        }
        outputs['SauvegarderLesEntitsVectoriellesDansUnFichier'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DonnesDobservationSauvegardes'] = outputs['SauvegarderLesEntitsVectoriellesDansUnFichier']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche communes
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['CrerUnIndexSpatial']['OUTPUT']
        }
        outputs['DfinirLencodageDeLaCoucheCommunes'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['SauvegarderLesEntitsVectoriellesDansUnFichier']['OUTPUT']
        }
        outputs['DfinirLencodageDeLaCouche'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Joindre les attributs par localisation
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': outputs['SauvegarderLesEntitsVectoriellesDansUnFichier']['OUTPUT'],
            'JOIN': outputs['CrerUnIndexSpatial']['OUTPUT'],
            'JOIN_FIELDS': [''],
            'METHOD': 0,  # Créer une entité distincte pour chaque entité correspondante (un à plusieurs)
            'PREDICATE': [0],  # intersecte
            'PREFIX': '',
            'OUTPUT': parameters['Jointure']
        }
        outputs['JoindreLesAttributsParLocalisation'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Jointure'] = outputs['JoindreLesAttributsParLocalisation']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['JoindreLesAttributsParLocalisation']['OUTPUT']
        }
        outputs['DfinirLencodageDeLaCouche'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Séparer une couche vecteur
        alg_params = {
            'FIELD': QgsExpression(" 'groupe_tax' ").evaluate(),
            'FILE_TYPE': 1,  # shp
            'INPUT': outputs['JoindreLesAttributsParLocalisation']['OUTPUT'],
            'PREFIX_FIELD': True,
            'OUTPUT': parameters['DossierMne']
        }
        outputs['SparerUneCoucheVecteur'] = processing.run('native:splitvectorlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DossierMne'] = outputs['SparerUneCoucheVecteur']['OUTPUT']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle oiseaux 2
        alg_params = {
        }
        outputs['BrancheConditionnelleOiseaux2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle reptiles 2 
        alg_params = {
        }
        outputs['BrancheConditionnelleReptiles2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle mammif 2
        alg_params = {
        }
        outputs['BrancheConditionnelleMammif2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle amphi
        alg_params = {
        }
        outputs['BrancheConditionnelleAmphi'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle oiseaux
        alg_params = {
        }
        outputs['BrancheConditionnelleOiseaux'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle mammif
        alg_params = {
        }
        outputs['BrancheConditionnelleMammif'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet mammif
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Mammifères.shp',
            'NAME': 'Mammifères'
        }
        outputs['ChargerLaCoucheDansLeProjetMammif'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle reptiles
        alg_params = {
        }
        outputs['BrancheConditionnelleReptiles'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle amphi 2
        alg_params = {
        }
        outputs['BrancheConditionnelleAmphi2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet oiseaux
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Oiseaux.shp',
            'NAME': 'Oiseaux'
        }
        outputs['ChargerLaCoucheDansLeProjetOiseaux'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet amphi
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Amphibiens.shp',
            'NAME': 'Amphibiens'
        }
        outputs['ChargerLaCoucheDansLeProjetAmphi'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche mammif
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetMammif']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AUTRE FAUNE TOTALE.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheMammif'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOiseaux']['OUTPUT']
        }
        outputs['DfinirLencodageDeLaCouche'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet reptiles
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Reptiles.shp',
            'NAME': 'Reptiles'
        }
        outputs['ChargerLaCoucheDansLeProjetReptiles'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['ChargerLaCoucheDansLeProjetReptiles']['OUTPUT']
        }
        outputs['DfinirLencodageDeLaCouche'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche oiseaux
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOiseaux']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AVIFAUNE TOTALE.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheOiseaux'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['ChargerLaCoucheDansLeProjetMammif']['OUTPUT']
        }
        outputs['DfinirLencodageDeLaCouche'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche amphi
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetAmphi']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AUTRE FAUNE TOTALE.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheAmphi'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche reptiles
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetReptiles']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AUTRE FAUNE TOTALE.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheReptiles'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons 1.29.1 mammif
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheMammif']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsMammif']
        }
        outputs['SuppressionDesDoublons1291Mammif'] = processing.run('script:Suppression_doublons1.1.1', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsMammif'] = outputs['SuppressionDesDoublons1291Mammif']['OUTPUT_LAYER']

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['ChargerLaCoucheDansLeProjetAmphi']['OUTPUT']
        }
        outputs['DfinirLencodageDeLaCouche'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['SuppressionDesDoublons1291Mammif']['OUTPUT_LAYER']
        }
        outputs['DfinirLencodageDeLaCouche'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche mammif 2
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublons1291Mammif']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_MAMMIFERES_PATRIMONIAUX_MAJ.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheMammif2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons 1.29.1 reptiles
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheReptiles']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsReptiles']
        }
        outputs['SuppressionDesDoublons1291Reptiles'] = processing.run('script:Suppression_doublons1.1.1', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsReptiles'] = outputs['SuppressionDesDoublons1291Reptiles']['OUTPUT_LAYER']

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons 1.29.1 oiseaux
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOiseaux']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsOiseaux']
        }
        outputs['SuppressionDesDoublons1291Oiseaux'] = processing.run('script:Suppression_doublons1.1.1', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsOiseaux'] = outputs['SuppressionDesDoublons1291Oiseaux']['OUTPUT_LAYER']

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['SuppressionDesDoublons1291Oiseaux']['OUTPUT_LAYER']
        }
        outputs['DfinirLencodageDeLaCouche'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche reptiles 2 
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublons1291Reptiles']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_REPTILES_PATRIMONIAUX_MAJ.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheReptiles2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons 1.29.1 amphi
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheAmphi']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsAmphi']
        }
        outputs['SuppressionDesDoublons1291Amphi'] = processing.run('script:Suppression_doublons1.1.1', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsAmphi'] = outputs['SuppressionDesDoublons1291Amphi']['OUTPUT_LAYER']

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['SuppressionDesDoublons1291Reptiles']['OUTPUT_LAYER']
        }
        outputs['DfinirLencodageDeLaCouche'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche oiseaux 2
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublons1291Oiseaux']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AVIFAUNE_PATRIMONIALE_NICHEUSE_MAJ2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheOiseaux2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['SuppressionDesDoublons1291Amphi']['OUTPUT_LAYER']
        }
        outputs['DfinirLencodageDeLaCouche'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche amphi 2
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublons1291Amphi']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AMPHIBIENS_PATRIMONIAUX_maj2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheAmphi2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
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
