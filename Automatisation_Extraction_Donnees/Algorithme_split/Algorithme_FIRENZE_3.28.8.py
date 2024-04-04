"""
Model exported as python.
Name : Modèle FIRENZE v16 (communes)
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
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsExpression
import processing


class ModleFirenzeV16Communes(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('donnes_lpo', 'Données LPO ', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('zone_dtude', "Zone d'étude", optional=True, types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TamponPourGtesChiro', 'Tampon pour gîtes chiro', type=QgsProcessing.TypeVectorPolygon, createByDefault=True, supportsAppend=True, defaultValue='C:/Users/lored/Documents/MNE/Tampon.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('DuplicationCoucheSwarm', 'Duplication couche swarm', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/Annuaire_Gîte_Chiro_53_3.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('Jointure', 'Jointure', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/Jointure.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('DuplicationCoucheHiver', 'Duplication couche hiver', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='C:/Users/lored/Documents/MNE/Annuaire_Gîte_Chiro_53_2.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('CouchePourGtes', 'Couche pour gîtes', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='C:/Users/lored/Documents/MNE/Couche_pour_gîtes.shp'))
        self.addParameter(QgsProcessingParameterFileDestination('DonnesDobservationSauvegardes', "Données d'observation sauvegardées", fileFilter='GeoPackage (*.gpkg *.GPKG);;ESRI Shapefile (*.shp *.SHP);;(Geo)Arrow (*.arrow *.feather *.arrows *.ipc *.ARROW *.FEATHER *.ARROWS *.IPC);;(Geo)Parquet (*.parquet *.PARQUET);;AutoCAD DXF (*.dxf *.DXF);;Fichier de Geodatabase ESRI (*.gdb *.GDB);;FlatGeobuf (*.fgb *.FGB);;Geoconcept (*.gxt *.txt *.GXT *.TXT);;Geography Markup Language [GML] (*.gml *.GML);;GeoJSON - Newline Delimited (*.geojsonl *.geojsons *.json *.GEOJSONL *.GEOJSONS *.JSON);;GeoJSON (*.geojson *.GEOJSON);;GeoRSS (*.xml *.XML);;GPS eXchange Format [GPX] (*.gpx *.GPX);;INTERLIS 1 (*.itf *.xml *.ili *.ITF *.XML *.ILI);;INTERLIS 2 (*.xtf *.xml *.ili *.XTF *.XML *.ILI);;Keyhole Markup Language [KML] (*.kml *.KML);;Mapinfo TAB (*.tab *.TAB);;Microstation DGN (*.dgn *.DGN);;PostgreSQL SQL dump (*.sql *.SQL);;S-57 Base file (*.000 *.000);;SQLite (*.sqlite *.SQLITE);;Tableur MS Office Open XML [XLSX] (*.xlsx *.XLSX);;Tableur Open Document  [ODS] (*.ods *.ODS);;Valeurs séparées par une virgule [CSV] (*.csv *.CSV)', createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/Données observation sauvegardées.shp'))
        self.addParameter(QgsProcessingParameterFolderDestination('DossierMne', 'Dossier MNE', createByDefault=True, defaultValue='C:\\Users\\lored\\Documents\\MNE'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsOiseaux', 'Suppression des doublons oiseaux', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/oiseaux_patrimoniaux.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsAmphi', 'Suppression des doublons amphi', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/amphi_patrimoniaux.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsMammif', 'Suppression des doublons mammif', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/mammif_patrimoniaux.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsReptiles', 'Suppression des doublons reptiles', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/reptiles_patrimoniaux.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsOdonates', 'Suppression des doublons odonates', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/odonates_patrimoniaux.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsOrthoptres', 'Suppression des doublons orthoptères', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/orthopteres_patrimoniaux.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsColoptres', 'Suppression des doublons coléoptères', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/coleopteres_patrimoniaux.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsRhopalocres', 'Suppression des doublons rhopalocères', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/rhopaloceres_patrimoniaux.shp'))
        self.addParameter(QgsProcessingParameterFeatureSink('SuppressionDesDoublonsHtrocres', 'Suppression des doublons hétérocères', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/heteroceres_patrimoniaux.shp'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(74, model_feedback)
        results = {}
        outputs = {}

        # Définir le style de la couche communes
        alg_params = {
            'INPUT': parameters['zone_dtude'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_MASK_Communes.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheCommunes'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Créer un index spatial
        alg_params = {
            'INPUT': parameters['zone_dtude']
        }
        outputs['CrerUnIndexSpatial'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Sauvegarder les entités vectorielles dans un fichier
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': parameters['donnes_lpo'],
            'LAYER_NAME': 'Données observation sauvegardées',
            'LAYER_OPTIONS': '',
            'OUTPUT': parameters['DonnesDobservationSauvegardes']
        }
        outputs['SauvegarderLesEntitsVectoriellesDansUnFichier'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DonnesDobservationSauvegardes'] = outputs['SauvegarderLesEntitsVectoriellesDansUnFichier']['OUTPUT']

        feedback.setCurrentStep(3)
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

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Définir l'encodage de la couche
        alg_params = {
            'ENCODING': 'UTF-8',
            'INPUT': outputs['JoindreLesAttributsParLocalisation']['OUTPUT']
        }
        outputs['DfinirLencodageDeLaCouche'] = processing.run('native:setlayerencoding', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
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

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle orthoptères
        alg_params = {
        }
        outputs['BrancheConditionnelleOrthoptres'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle odonates
        alg_params = {
        }
        outputs['BrancheConditionnelleOdonates'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

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

        # Branche conditionnelle odonates 2 
        alg_params = {
        }
        outputs['BrancheConditionnelleOdonates2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle oiseaux 2
        alg_params = {
        }
        outputs['BrancheConditionnelleOiseaux2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle rhopalocères 2 
        alg_params = {
        }
        outputs['BrancheConditionnelleRhopalocres2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle amphi 2
        alg_params = {
        }
        outputs['BrancheConditionnelleAmphi2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle amphi
        alg_params = {
        }
        outputs['BrancheConditionnelleAmphi'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

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

        # Branche conditionnelle coléoptères 2 
        alg_params = {
        }
        outputs['BrancheConditionnelleColoptres2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle coléoptères
        alg_params = {
        }
        outputs['BrancheConditionnelleColoptres'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle chiroptères
        alg_params = {
        }
        outputs['BrancheConditionnelleChiroptres'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle mammif
        alg_params = {
        }
        outputs['BrancheConditionnelleMammif'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet orthoptères
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Orthoptères.shp',
            'NAME': 'Orthoptères'
        }
        outputs['ChargerLaCoucheDansLeProjetOrthoptres'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle orthoptères 2 
        alg_params = {
        }
        outputs['BrancheConditionnelleOrthoptres2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle hétérocères 2
        alg_params = {
        }
        outputs['BrancheConditionnelleHtrocres2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle mammif 2
        alg_params = {
        }
        outputs['BrancheConditionnelleMammif2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle hétérocères
        alg_params = {
        }
        outputs['BrancheConditionnelleHtrocres'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle oiseaux
        alg_params = {
        }
        outputs['BrancheConditionnelleOiseaux'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle rhopalocères
        alg_params = {
        }
        outputs['BrancheConditionnelleRhopalocres'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle chiroptères 2
        alg_params = {
        }
        outputs['BrancheConditionnelleChiroptres2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet oiseaux
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Oiseaux.shp',
            'NAME': 'Oiseaux'
        }
        outputs['ChargerLaCoucheDansLeProjetOiseaux'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet odonates
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Odonates.shp',
            'NAME': 'Odonates'
        }
        outputs['ChargerLaCoucheDansLeProjetOdonates'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet mammif
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Mammifères.shp',
            'NAME': 'Mammifères'
        }
        outputs['ChargerLaCoucheDansLeProjetMammif'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet reptiles
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Reptiles.shp',
            'NAME': 'Reptiles'
        }
        outputs['ChargerLaCoucheDansLeProjetReptiles'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche odonates
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOdonates']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_ODONATES_MAJ2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheOdonates'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet rhopalocères
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Papillons de jour.shp',
            'NAME': 'Rhopalocères'
        }
        outputs['ChargerLaCoucheDansLeProjetRhopalocres'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet chiroptères
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Chauves-souris.shp',
            'NAME': 'Chiroptères'
        }
        outputs['ChargerLaCoucheDansLeProjetChiroptres'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet amphi
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Amphibiens.shp',
            'NAME': 'Amphibiens'
        }
        outputs['ChargerLaCoucheDansLeProjetAmphi'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche reptiles
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetReptiles']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AUTRE FAUNE TOTALE.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheReptiles'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche orthoptères
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOrthoptres']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_ORTHOPTERES_MAJ2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheOrthoptres'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche mammif
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetMammif']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AUTRE FAUNE TOTALE.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheMammif'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons odonates
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOdonates']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsOdonates']
        }
        outputs['SuppressionDesDoublonsOdonates'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsOdonates'] = outputs['SuppressionDesDoublonsOdonates']['OUTPUT_LAYER']

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche chiroptères
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetChiroptres']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_CHIROPTERES_MAJ2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheChiroptres'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet coléoptères
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Coléoptères.shp',
            'NAME': 'Coléoptères'
        }
        outputs['ChargerLaCoucheDansLeProjetColoptres'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche coléoptères
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetColoptres']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_COLEOPTERES_MAJ2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheColoptres'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}

        # Reprojeter une couche
        alg_params = {
            'INPUT': parameters['zone_dtude'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
            'OUTPUT': parameters['CouchePourGtes']
        }
        outputs['ReprojeterUneCouche'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['CouchePourGtes'] = outputs['ReprojeterUneCouche']['OUTPUT']

        feedback.setCurrentStep(43)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche odonates 2 
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsOdonates']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_ODONATES_PATRIMONIAUX_2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheOdonates2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons reptiles
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheReptiles']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsReptiles']
        }
        outputs['SuppressionDesDoublonsReptiles'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsReptiles'] = outputs['SuppressionDesDoublonsReptiles']['OUTPUT_LAYER']

        feedback.setCurrentStep(45)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche amphi
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetAmphi']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AUTRE FAUNE TOTALE.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheAmphi'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(46)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche rhopalocères
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetRhopalocres']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_RHOPALOCERES_MAJ2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheRhopalocres'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(47)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet hétérocères
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Papillons de nuit.shp',
            'NAME': 'Hétérocères'
        }
        outputs['ChargerLaCoucheDansLeProjetHtrocres'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(48)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons orthoptères
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOrthoptres']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsOrthoptres']
        }
        outputs['SuppressionDesDoublonsOrthoptres'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsOrthoptres'] = outputs['SuppressionDesDoublonsOrthoptres']['OUTPUT_LAYER']

        feedback.setCurrentStep(49)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche oiseaux
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOiseaux']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AVIFAUNE TOTALE.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheOiseaux'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(50)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche pour gîtes
        alg_params = {
            'INPUT': outputs['ReprojeterUneCouche']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_COMMUNE_ORTHO_SANS_NOM.qml'
        }
        outputs['DfinirLeStyleDeLaCouchePourGtes'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(51)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet gîtes été
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/10-PROCEDURES EXTRACTION DONNEES/10-PROCEDURES EXTRACTION DONNEES/Synthèses générales/COUCHES_RESSOURCES/Annuaire_Gîte_Chiro_53_v050121.shp',
            'NAME': 'Annuaire_Gîte_Chiro_53_1'
        }
        outputs['ChargerLaCoucheDansLeProjetGtesT'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(52)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons amphi
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheAmphi']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsAmphi']
        }
        outputs['SuppressionDesDoublonsAmphi'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsAmphi'] = outputs['SuppressionDesDoublonsAmphi']['OUTPUT_LAYER']

        feedback.setCurrentStep(53)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons mammif
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheMammif']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsMammif']
        }
        outputs['SuppressionDesDoublonsMammif'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsMammif'] = outputs['SuppressionDesDoublonsMammif']['OUTPUT_LAYER']

        feedback.setCurrentStep(54)
        if feedback.isCanceled():
            return {}

        # Extraire par expression swarm
        alg_params = {
            'EXPRESSION': '1 = 1',
            'INPUT': outputs['ChargerLaCoucheDansLeProjetGtesT']['OUTPUT'],
            'OUTPUT': parameters['DuplicationCoucheSwarm']
        }
        outputs['ExtraireParExpressionSwarm'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DuplicationCoucheSwarm'] = outputs['ExtraireParExpressionSwarm']['OUTPUT']

        feedback.setCurrentStep(55)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche gîtes 
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetGtesT']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_GITE_CHIRO_ETE.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheGtes'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(56)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons coléoptères
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheColoptres']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsColoptres']
        }
        outputs['SuppressionDesDoublonsColoptres'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsColoptres'] = outputs['SuppressionDesDoublonsColoptres']['OUTPUT_LAYER']

        feedback.setCurrentStep(57)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche reptiles 2 
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsReptiles']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_REPTILES_PATRIMONIAUX_MAJ.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheReptiles2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(58)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons rhopalocères
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheRhopalocres']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsRhopalocres']
        }
        outputs['SuppressionDesDoublonsRhopalocres'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsRhopalocres'] = outputs['SuppressionDesDoublonsRhopalocres']['OUTPUT_LAYER']

        feedback.setCurrentStep(59)
        if feedback.isCanceled():
            return {}

        # Reprojeter une couche gîtes hiver
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetGtesT']['OUTPUT'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
            'OUTPUT': parameters['DuplicationCoucheHiver']
        }
        outputs['ReprojeterUneCoucheGtesHiver'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DuplicationCoucheHiver'] = outputs['ReprojeterUneCoucheGtesHiver']['OUTPUT']

        feedback.setCurrentStep(60)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche mammif 2
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsMammif']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_MAMMIFERES_PATRIMONIAUX_MAJ.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheMammif2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(61)
        if feedback.isCanceled():
            return {}

        # Tampon
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': 10000,
            'END_CAP_STYLE': 0,  # Rond
            'INPUT': outputs['ReprojeterUneCouche']['OUTPUT'],
            'JOIN_STYLE': 0,  # Rond
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': parameters['TamponPourGtesChiro']
        }
        outputs['Tampon'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TamponPourGtesChiro'] = outputs['Tampon']['OUTPUT']

        feedback.setCurrentStep(62)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche gîtes 3 
        alg_params = {
            'INPUT': outputs['ExtraireParExpressionSwarm']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_GITE_CHIRO_SWARMING.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheGtes3'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(63)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons oiseaux
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOiseaux']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsOiseaux']
        }
        outputs['SuppressionDesDoublonsOiseaux'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsOiseaux'] = outputs['SuppressionDesDoublonsOiseaux']['OUTPUT_LAYER']

        feedback.setCurrentStep(64)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche orthoptères 2
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsOrthoptres']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_ORTHOPTERES_PATRIMONIAUX_2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheOrthoptres2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(65)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche hétérocères
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetHtrocres']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_HETEROCERES_MAJ2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheHtrocres'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(66)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche amphi 2
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsAmphi']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AMPHIBIENS_PATRIMONIAUX_maj2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheAmphi2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(67)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche coléoptères 2 
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsColoptres']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_COLEOPTERES_PATRIMONIAUX_2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheColoptres2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(68)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche gîtes tampon
        alg_params = {
            'INPUT': outputs['Tampon']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_MASK.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheGtesTampon'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(69)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche rhopalocères 2 
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsRhopalocres']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_RHOPALOCERES_PATRIMONIAUX_2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheRhopalocres2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(70)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche gîtes 2 
        alg_params = {
            'INPUT': outputs['ReprojeterUneCoucheGtesHiver']['OUTPUT'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_GITE_CHIRO_HIVER.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheGtes2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(71)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche oiseaux 2
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsOiseaux']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_AVIFAUNE_PATRIMONIALE_NICHEUSE_MAJ2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheOiseaux2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(72)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons hétérocères
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheHtrocres']['OUTPUT'],
            'OUTPUT_LAYER': parameters['SuppressionDesDoublonsHtrocres']
        }
        outputs['SuppressionDesDoublonsHtrocres'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuppressionDesDoublonsHtrocres'] = outputs['SuppressionDesDoublonsHtrocres']['OUTPUT_LAYER']

        feedback.setCurrentStep(73)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche hétérocères 2
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsHtrocres']['OUTPUT_LAYER'],
            'STYLE': 'C:\\Users\\lored\\Documents\\MNE\\10-PROCEDURES EXTRACTION DONNEES\\10-PROCEDURES EXTRACTION DONNEES\\Synthèses générales\\STYLES\\Style_HETEROCERES_PATRIMONIAUX_2024.qml'
        }
        outputs['DfinirLeStyleDeLaCoucheHtrocres2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'Modèle FIRENZE v16 (communes)'

    def displayName(self):
        return 'Modèle FIRENZE v16 (communes)'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return ModleFirenzeV16Communes()
