"""
Model exported as python.
Name : Extraction des couches (communes) 3.28
Group : 
With QGIS : 32808
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsExpression
import processing


class ExtractionDesCouchesCommunes328(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('donnes_lpo', 'Données LPO ', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('dossier_styles', 'Dossier styles', behavior=QgsProcessingParameterFile.Folder, fileFilter='Tous les fichiers (*.*)', defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('fichier_gtes', 'Fichier gîtes', optional=True, behavior=QgsProcessingParameterFile.File, fileFilter='Tous les fichiers (*.*)', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('zone_dtude', "Zone d'étude", types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterFile('dossier_couches', 'Dossier couches', behavior=QgsProcessingParameterFile.Folder, fileFilter='Tous les fichiers (*.*)', defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(95, model_feedback)
        results = {}
        outputs = {}

        # Créer un index spatial
        alg_params = {
            'INPUT': parameters['zone_dtude']
        }
        outputs['CrerUnIndexSpatial'] = processing.run('native:createspatialindex', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Sauvegarder les entités vectorielles dans un fichier
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': parameters['donnes_lpo'],
            'LAYER_NAME': 'Données observation sauvegardées',
            'LAYER_OPTIONS': '',
            'OUTPUT': QgsExpression("concat(@dossier_couches, '/', 'Données observation sauvegardées.shp')\n").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SauvegarderLesEntitsVectoriellesDansUnFichier'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche communes
        alg_params = {
            'INPUT': parameters['zone_dtude'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'MASK_Communes.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheCommunes'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

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
            'OUTPUT': QgsExpression("concat(@dossier_couches, '/', 'Jointure.shp')\n").evaluate(),
            'PREDICATE': [0],  # intersecte
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoindreLesAttributsParLocalisation'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Séparer une couche vecteur
        alg_params = {
            'FIELD': QgsExpression(" 'groupe_tax' ").evaluate(),
            'FILE_TYPE': 1,  # shp
            'INPUT': outputs['JoindreLesAttributsParLocalisation']['OUTPUT'],
            'OUTPUT': QgsExpression(' @dossier_couches').evaluate(),
            'PREFIX_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SparerUneCoucheVecteur'] = processing.run('native:splitvectorlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle odonates
        alg_params = {
        }
        outputs['BrancheConditionnelleOdonates'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle rhopalocères
        alg_params = {
        }
        outputs['BrancheConditionnelleRhopalocres'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle odonates 2 
        alg_params = {
        }
        outputs['BrancheConditionnelleOdonates2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle hétérocères
        alg_params = {
        }
        outputs['BrancheConditionnelleHtrocres'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle hétérocères 2
        alg_params = {
        }
        outputs['BrancheConditionnelleHtrocres2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle orthoptères
        alg_params = {
        }
        outputs['BrancheConditionnelleOrthoptres'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet odonates
        alg_params = {
            'INPUT': QgsExpression("concat(@dossier_couches, '/', 'groupe_tax_Odonates.shp')").evaluate(),
            'NAME': 'Odonates'
        }
        outputs['ChargerLaCoucheDansLeProjetOdonates'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

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

        # Branche conditionnelle orthoptères 2 
        alg_params = {
        }
        outputs['BrancheConditionnelleOrthoptres2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle amphi 2
        alg_params = {
        }
        outputs['BrancheConditionnelleAmphi2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle amphi
        alg_params = {
        }
        outputs['BrancheConditionnelleAmphi'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet rhopalocères
        alg_params = {
            'INPUT': QgsExpression("concat(@dossier_couches, '/', 'groupe_tax_Papillons de jour.shp')").evaluate(),
            'NAME': 'Rhopalocères'
        }
        outputs['ChargerLaCoucheDansLeProjetRhopalocres'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet hétérocères
        alg_params = {
            'INPUT': QgsExpression("concat(@dossier_couches, '/', 'groupe_tax_Papillons de nuit.shp')").evaluate(),
            'NAME': 'Hétérocères'
        }
        outputs['ChargerLaCoucheDansLeProjetHtrocres'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle oiseaux
        alg_params = {
        }
        outputs['BrancheConditionnelleOiseaux'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche hétérocères
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetHtrocres']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'HETEROCERES.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheHtrocres'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet oiseaux
        alg_params = {
            'INPUT': QgsExpression("concat(@dossier_couches, '/', 'groupe_tax_Oiseaux.shp')").evaluate(),
            'NAME': 'Oiseaux'
        }
        outputs['ChargerLaCoucheDansLeProjetOiseaux'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle reptiles
        alg_params = {
        }
        outputs['BrancheConditionnelleReptiles'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle chiroptères 2
        alg_params = {
        }
        outputs['BrancheConditionnelleChiroptres2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet mammif
        alg_params = {
            'INPUT': QgsExpression("concat(@dossier_couches, '/', 'groupe_tax_Mammifères.shp')").evaluate(),
            'NAME': 'Mammifères'
        }
        outputs['ChargerLaCoucheDansLeProjetMammif'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle chiroptères
        alg_params = {
        }
        outputs['BrancheConditionnelleChiroptres'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet chiroptères
        alg_params = {
            'INPUT': QgsExpression("concat(@dossier_couches, '/', 'groupe_tax_Chauves-souris.shp')").evaluate(),
            'NAME': 'Chiroptères'
        }
        outputs['ChargerLaCoucheDansLeProjetChiroptres'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet gîtes
        alg_params = {
            'INPUT': QgsExpression('@fichier_gtes').evaluate(),
            'NAME': 'Type de gîte'
        }
        outputs['ChargerLaCoucheDansLeProjetGtes'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle rhopalocères 2 
        alg_params = {
        }
        outputs['BrancheConditionnelleRhopalocres2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet orthoptères
        alg_params = {
            'INPUT': QgsExpression("concat(@dossier_couches, '/', 'groupe_tax_Orthoptères.shp')").evaluate(),
            'NAME': 'Orthoptères'
        }
        outputs['ChargerLaCoucheDansLeProjetOrthoptres'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle coléoptères 2 
        alg_params = {
        }
        outputs['BrancheConditionnelleColoptres2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle coléoptères
        alg_params = {
        }
        outputs['BrancheConditionnelleColoptres'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche odonates
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOdonates']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'ODONATES.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheOdonates'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet amphi
        alg_params = {
            'INPUT': QgsExpression("concat(@dossier_couches, '/', 'groupe_tax_Amphibiens.shp')").evaluate(),
            'NAME': 'Amphibiens'
        }
        outputs['ChargerLaCoucheDansLeProjetAmphi'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche oiseaux
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOiseaux']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'AVIFAUNE.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheOiseaux'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons oiseaux du bâti
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOiseaux']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Oiseaux du bâti.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsOiseauxDuBti'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle mammif 2
        alg_params = {
        }
        outputs['BrancheConditionnelleMammif2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche mammif
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetMammif']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'AUTRE_FAUNE.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheMammif'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons hétérocères
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheHtrocres']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Hétérocères patrimoniaux.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsHtrocres'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons oiseaux forestiers
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOiseaux']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Oiseaux forestiers.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsOiseauxForestiers'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle oiseaux 2
        alg_params = {
        }
        outputs['BrancheConditionnelleOiseaux2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # Branche conditionnelle reptiles 2 
        alg_params = {
        }
        outputs['BrancheConditionnelleReptiles2'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche amphi
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetAmphi']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'AUTRE_FAUNE.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheAmphi'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet oiseaux forestiers
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsOiseauxForestiers']['OUTPUT_LAYER'],
            'NAME': 'Oiseaux forestiers'
        }
        outputs['ChargerLaCoucheDansLeProjetOiseauxForestiers'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(43)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche rhopalocères
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetRhopalocres']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'RHOPALO.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheRhopalocres'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}

        # Reprojeter une couche
        alg_params = {
            'INPUT': parameters['zone_dtude'],
            'OPERATION': '',
            'OUTPUT': QgsExpression("concat(@dossier_couches, '/', 'Communes_sans_nom.shp')").evaluate(),
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:2154'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojeterUneCouche'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(45)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche chiroptères
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetChiroptres']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'CHIRO.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheChiroptres'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(46)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet reptiles
        alg_params = {
            'INPUT': QgsExpression("concat(@dossier_couches, '/', 'groupe_tax_Reptiles.shp')").evaluate(),
            'NAME': 'Reptiles'
        }
        outputs['ChargerLaCoucheDansLeProjetReptiles'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(47)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet oiseaux du bâti
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsOiseauxDuBti']['OUTPUT_LAYER'],
            'NAME': 'Oiseaux du bâti'
        }
        outputs['ChargerLaCoucheDansLeProjetOiseauxDuBti'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(48)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons odonates
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOdonates']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Odonates patrimoniaux.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsOdonates'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(49)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet odonates patri
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsOdonates']['OUTPUT_LAYER'],
            'NAME': 'Odonates patrimoniaux'
        }
        outputs['ChargerLaCoucheDansLeProjetOdonatesPatri'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(50)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche odonates 2 
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOdonatesPatri']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'ODONATES_PATRI.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheOdonates2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(51)
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
            'OUTPUT': QgsExpression("concat(@dossier_couches, '/', 'Tampon_gîtes.shp')").evaluate(),
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Tampon'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(52)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons rapaces
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOiseaux']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Rapaces.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsRapaces'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(53)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons rhopalocères
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheRhopalocres']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Rhopalocères patrimoniaux.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsRhopalocres'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(54)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet coléoptères
        alg_params = {
            'INPUT': QgsExpression("concat(@dossier_couches, '/', 'groupe_tax_Coléoptères.shp')").evaluate(),
            'NAME': 'Coléoptères'
        }
        outputs['ChargerLaCoucheDansLeProjetColoptres'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(55)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche reptiles
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetReptiles']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'AUTRE_FAUNE.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheReptiles'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(56)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche gîtes
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetGtes']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'GITE.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheGtes'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(57)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons oiseaux marins
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOiseaux']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Oiseaux marins.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsOiseauxMarins'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(58)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet tampon 
        alg_params = {
            'INPUT': outputs['Tampon']['OUTPUT'],
            'NAME': 'Tampon'
        }
        outputs['ChargerLaCoucheDansLeProjetTampon'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(59)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet hétérocères patri
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsHtrocres']['OUTPUT_LAYER'],
            'NAME': 'Hétérocères patrimoniaux'
        }
        outputs['ChargerLaCoucheDansLeProjetHtrocresPatri'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(60)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche pour oiseaux du bâti
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOiseauxDuBti']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'AVIFAUNE_BATI.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCouchePourOiseauxDuBti'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(61)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons amphi
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheAmphi']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Amphibiens patrimoniaux.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsAmphi'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(62)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons reptiles
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheReptiles']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Reptiles patrimoniaux.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsReptiles'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(63)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche orthoptères
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOrthoptres']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'ORTHOPTERES.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheOrthoptres'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(64)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons oiseaux agricoles
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOiseaux']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Oiseaux des milieux agricoles.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsOiseauxAgricoles'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(65)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons oiseaux humides
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOiseaux']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Oiseaux des zones humides.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsOiseauxHumides'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(66)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons mammif
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheMammif']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Mammifères patrimoniaux.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsMammif'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(67)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet rapaces
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsRapaces']['OUTPUT_LAYER'],
            'NAME': 'Rapaces'
        }
        outputs['ChargerLaCoucheDansLeProjetRapaces'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(68)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche coléoptères
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetColoptres']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'COLEO.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheColoptres'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(69)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche oiseaux milieux forestiers
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOiseauxForestiers']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'AVIFAUNE_FORESTIER.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheOiseauxMilieuxForestiers'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(70)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet oiseaux marins
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsOiseauxMarins']['OUTPUT_LAYER'],
            'NAME': 'Oiseaux marins'
        }
        outputs['ChargerLaCoucheDansLeProjetOiseauxMarins'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(71)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet amphi patri
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsAmphi']['OUTPUT_LAYER'],
            'NAME': 'Amphibiens patrimoniaux'
        }
        outputs['ChargerLaCoucheDansLeProjetAmphiPatri'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(72)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet communes sans nom
        alg_params = {
            'INPUT': outputs['ReprojeterUneCouche']['OUTPUT'],
            'NAME': 'Zone'
        }
        outputs['ChargerLaCoucheDansLeProjetCommunesSansNom'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(73)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet rhopalocères patri
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsRhopalocres']['OUTPUT_LAYER'],
            'NAME': 'Rhopalocères patrimoniaux'
        }
        outputs['ChargerLaCoucheDansLeProjetRhopalocresPatri'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(74)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche rapaces
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetRapaces']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'RAPACES.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheRapaces'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(75)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche hétérocères 2
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetHtrocresPatri']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'HETEROCERES_PATRI.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheHtrocres2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(76)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons orthoptères
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheOrthoptres']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Orthoptères patrimoniaux.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsOrthoptres'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(77)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche amphi 2
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetAmphiPatri']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'AMPHI.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheAmphi2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(78)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet orthoptères patri
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsOrthoptres']['OUTPUT_LAYER'],
            'NAME': 'Orthoptères patrimoniaux'
        }
        outputs['ChargerLaCoucheDansLeProjetOrthoptresPatri'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(79)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche gîtes tampon
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetTampon']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'MASK.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheGtesTampon'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(80)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet reptiles patri
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsReptiles']['OUTPUT_LAYER'],
            'NAME': 'Reptiles patrimoniaux'
        }
        outputs['ChargerLaCoucheDansLeProjetReptilesPatri'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(81)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet oiseaux humides
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsOiseauxHumides']['OUTPUT_LAYER'],
            'NAME': 'Oiseaux des zones humides'
        }
        outputs['ChargerLaCoucheDansLeProjetOiseauxHumides'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(82)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet oiseaux agricoles
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsOiseauxAgricoles']['OUTPUT_LAYER'],
            'NAME': 'Oiseaux des milieux agricoles'
        }
        outputs['ChargerLaCoucheDansLeProjetOiseauxAgricoles'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(83)
        if feedback.isCanceled():
            return {}

        # Suppression des doublons coléoptères
        alg_params = {
            'INPUT_LAYER': outputs['DfinirLeStyleDeLaCoucheColoptres']['OUTPUT'],
            'OUTPUT_LAYER': QgsExpression("concat(@dossier_couches, '/', 'Coléoptères patrimoniaux.shp')").evaluate(),
            'OUTPUT_LAYER': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SuppressionDesDoublonsColoptres'] = processing.run('script:Suppression_doublons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(84)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet mammif patri
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsMammif']['OUTPUT_LAYER'],
            'NAME': 'Mammifères patrimoniaux'
        }
        outputs['ChargerLaCoucheDansLeProjetMammifPatri'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(85)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche oiseaux humides
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOiseauxHumides']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'AVIFAUNE_HUMIDE.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheOiseauxHumides'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(86)
        if feedback.isCanceled():
            return {}

        # Charger la couche dans le projet coléoptères patri
        alg_params = {
            'INPUT': outputs['SuppressionDesDoublonsColoptres']['OUTPUT_LAYER'],
            'NAME': 'Coléoptères patrimoniaux '
        }
        outputs['ChargerLaCoucheDansLeProjetColoptresPatri'] = processing.run('native:loadlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(87)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche oiseaux marins
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOiseauxMarins']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'AVIFAUNE_MARINE.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheOiseauxMarins'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(88)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche rhopalocères 2 
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetRhopalocresPatri']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'RHOPALO_PATRI.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheRhopalocres2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(89)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche pour gîtes
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetCommunesSansNom']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'COMMUNE_ORTHO_SANS_NOM.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCouchePourGtes'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(90)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche orthoptères 2
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOrthoptresPatri']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'ORTHOPTERES_PATRI.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheOrthoptres2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(91)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche reptiles 2 
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetReptilesPatri']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'REPTILES.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheReptiles2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(92)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche oiseaux agricoles
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetOiseauxAgricoles']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'AVIFAUNE_AGRICOLE.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheOiseauxAgricoles'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(93)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche mammif 2
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetMammifPatri']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'MAMMIF.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheMammif2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(94)
        if feedback.isCanceled():
            return {}

        # Définir le style de la couche coléoptères 2 
        alg_params = {
            'INPUT': outputs['ChargerLaCoucheDansLeProjetColoptresPatri']['OUTPUT'],
            'STYLE': QgsExpression("concat(@dossier_styles , '/', 'COLEO_PATRI.qml')").evaluate()
        }
        outputs['DfinirLeStyleDeLaCoucheColoptres2'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'Extraction des couches (communes) 3.28'

    def displayName(self):
        return 'Extraction des couches (communes) 3.28'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return ExtractionDesCouchesCommunes328()
