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
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterFolderDestination
from qgis.core import QgsExpression
import processing


class Modle(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('couche', 'Couche', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('DonnesDobservationSauvegardes', "Données d'observation sauvegardées", fileFilter='GeoPackage (*.gpkg *.GPKG);;ESRI Shapefile (*.shp *.SHP);;(Geo)Arrow (*.arrow *.feather *.arrows *.ipc *.ARROW *.FEATHER *.ARROWS *.IPC);;(Geo)Parquet (*.parquet *.PARQUET);;AutoCAD DXF (*.dxf *.DXF);;Fichier de Geodatabase ESRI (*.gdb *.GDB);;FlatGeobuf (*.fgb *.FGB);;Geoconcept (*.gxt *.txt *.GXT *.TXT);;Geography Markup Language [GML] (*.gml *.GML);;GeoJSON - Newline Delimited (*.geojsonl *.geojsons *.json *.GEOJSONL *.GEOJSONS *.JSON);;GeoJSON (*.geojson *.GEOJSON);;GeoRSS (*.xml *.XML);;GPS eXchange Format [GPX] (*.gpx *.GPX);;INTERLIS 1 (*.itf *.xml *.ili *.ITF *.XML *.ILI);;INTERLIS 2 (*.xtf *.xml *.ili *.XTF *.XML *.ILI);;Keyhole Markup Language [KML] (*.kml *.KML);;Mapinfo TAB (*.tab *.TAB);;Microstation DGN (*.dgn *.DGN);;PostgreSQL SQL dump (*.sql *.SQL);;S-57 Base file (*.000 *.000);;SQLite (*.sqlite *.SQLITE);;Tableur MS Office Open XML [XLSX] (*.xlsx *.XLSX);;Tableur Open Document  [ODS] (*.ods *.ODS);;Valeurs séparées par une virgule [CSV] (*.csv *.CSV)', createByDefault=True, defaultValue='C:/Users/lored/Documents/MNE/Données observation sauvegardées.shp'))
        self.addParameter(QgsProcessingParameterFolderDestination('DossierMne', 'Dossier MNE', createByDefault=True, defaultValue='C:\\Users\\lored\\Documents\\MNE'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

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

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Séparer une couche vecteur
        alg_params = {
            'FIELD': QgsExpression(" 'groupe_tax' ").evaluate(),
            'FILE_TYPE': 1,  # shp
            'INPUT': outputs['SauvegarderLesEntitsVectoriellesDansUnFichier']['OUTPUT'],
            'PREFIX_FIELD': True,
            'OUTPUT': parameters['DossierMne']
        }
        outputs['SparerUneCoucheVecteur'] = processing.run('native:splitvectorlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DossierMne'] = outputs['SparerUneCoucheVecteur']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet mammif
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_MammifÃ¨res.shp',
            'NAME': 'Mammifères'
        }
        outputs['ChargerLaCoucheDansLeProjetMammif'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet amphi
        alg_params = {
            'INPUT': 'C:/Users/lored/Documents/MNE/groupe_tax_Amphibiens.shp',
            'NAME': 'Amphibiens'
        }
        outputs['ChargerLaCoucheDansLeProjetAmphi'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle amphi
        alg_params = {
        }
        outputs['BrancheConditionnelleAmphi'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
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
