### Run this over a RECO file that contains generalTracks and BeamSpot
### Run this with CMSSW_11_2_0_pre7 or later 

import FWCore.ParameterSet.Config as cms

process = cms.Process("RECO2")
NUM_EVENTS = 10
NUM_THREADS = 1

# import of standard configurations
process.load("Configuration.StandardSequences.Services_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.StandardSequences.Reconstruction_Data_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(NUM_EVENTS))

# Input source
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(
        "/store/relval/CMSSW_11_2_0_pre6/RelValH125GGgluonfusion_14/GEN-SIM-RECO/PU_112X_mcRun3_2021_realistic_v7-v1/20000/A457D85C-5A6C-1548-9823-5C7E9CBC79B8.root",
    ),
    secondaryFileNames=cms.untracked.vstring(),
)

process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag

process.GlobalTag = GlobalTag(process.GlobalTag, "112X_mcRun3_2021_realistic_v7", "")

process.develPrimaryVertices = cms.EDProducer(
    "PrimaryVertexProducer",
    TkClusParameters=cms.PSet(
        TkDAClusParameters=cms.PSet(
            Tmin=cms.double(2.0),
            Tpurge=cms.double(2.0),
            Tstop=cms.double(0.5),
            coolingFactor=cms.double(0.6),
            d0CutOff=cms.double(3.0),
            dzCutOff=cms.double(3.0),
            uniquetrkweight=cms.double(0.8),
            vertexSize=cms.double(0.006),
            zmerge=cms.double(0.01),
        ),
        algorithm=cms.string("DA_vect"),
    ),
    TkFilterParameters=cms.PSet(
        algorithm=cms.string("filter"),
        maxD0Significance=cms.double(4.0),
        maxEta=cms.double(2.4),
        maxNormalizedChi2=cms.double(10.0),
        minPixelLayersWithHits=cms.int32(2),
        minPt=cms.double(0.0),
        minSiliconLayersWithHits=cms.int32(5),
        trackQuality=cms.string("any"),
    ),
    TrackLabel=cms.InputTag("generalTracks"),
    beamSpotLabel=cms.InputTag("offlineBeamSpot"),
    verbose=cms.untracked.bool(False),
    vertexCollections=cms.VPSet(
        cms.PSet(
            algorithm=cms.string("AdaptiveVertexFitter"),
            chi2cutoff=cms.double(2.5),
            label=cms.string(""),
            maxDistanceToBeam=cms.double(1.0),
            minNdof=cms.double(0.0),
            useBeamConstraint=cms.bool(False),
        ),
        cms.PSet(
            algorithm=cms.string("AdaptiveVertexFitter"),
            chi2cutoff=cms.double(2.5),
            label=cms.string("WithBS"),
            maxDistanceToBeam=cms.double(1.0),
            minNdof=cms.double(2.0),
            useBeamConstraint=cms.bool(True),
        ),
    ),
)

process.makeVerticesPath = cms.Path(process.develPrimaryVertices)

# Schedule definition
process.schedule = cms.Schedule(process.makeVerticesPath)

# Setup FWK for multithreaded
process.options.numberOfThreads = cms.untracked.uint32(1)
process.options.numberOfStreams = cms.untracked.uint32(0)
process.options.numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(1)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring

# call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions
# do not add changes to your config after this point (unless you know what you are doing)
# from FWCore.ParameterSet.Utilities import convertToUnscheduled
# process=convertToUnscheduled(process)


# Customisation from command line

# Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import (
    customiseLogErrorHarvesterUsingOutputCommands,
)

process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete

process = customiseEarlyDelete(process)
# End adding early deletion
