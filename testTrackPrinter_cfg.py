import FWCore.ParameterSet.Config as cms

# process
process = cms.Process("TEST")

# number of events to be processed and source file
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(400)
)

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('/store/relval/CMSSW_12_2_0/RelValTTbar_14TeV/GEN-SIM-RECO/122X_mcRun3_2021_realistic_v5-v2/2580000/ac85ff65-dcea-4e7d-9995-d512f4bdafcf.root'
                            )
)

process.trackPrinter = cms.EDAnalyzer("TrackPrinter",
    tracks = cms.untracked.InputTag("generalTracks")
)

process.p = cms.Path(process.trackPrinter)
