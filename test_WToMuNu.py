import FWCore.ParameterSet.Config as cms

process = cms.Process("TEST")

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(100))

process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

process.RandomNumberGeneratorService = cms.Service(
    "RandomNumberGeneratorService",
    generator=cms.PSet(
        engineName=cms.untracked.string("HepJamesRandom"),
        initialSeed=cms.untracked.uint32(123456789),
    ),
)

process.generator = cms.EDFilter(
    "Pythia8GeneratorFilter",
    PythiaParameters=cms.PSet(
        parameterSets=cms.vstring(
            "pythia8CommonSettings", "pythia8CUEP8M1Settings", "processParameters"
        ),
        processParameters=cms.vstring(
            "WeakSingleBoson:ffbar2W = on", "24:onMode = off", "24:onIfAny = 13,14"
        ),
        pythia8CUEP8M1Settings=cms.vstring(
            "Tune:pp 14",
            "Tune:ee 7",
            "MultipartonInteractions:pT0Ref=2.4024",
            "MultipartonInteractions:ecmPow=0.25208",
            "MultipartonInteractions:expPow=1.6",
        ),
        pythia8CommonSettings=cms.vstring(
            "Tune:preferLHAPDF = 2",
            "Main:timesAllowErrors = 10000",
            "Check:epTolErr = 0.01",
            "Beams:setProductionScalesFromLHEF = off",
            "ParticleDecays:limitTau0 = on",
            "ParticleDecays:tau0Max = 10",
            "ParticleDecays:allowPhotonRadiation = on",
        ),
    ),
    comEnergy=cms.double(13000.0),
    crossSection=cms.untracked.double(1),
    filterEfficiency=cms.untracked.double(1),
    maxEventsToPrint=cms.untracked.int32(1),
    pythiaHepMCVerbosity=cms.untracked.bool(False),
    pythiaPylistVerbosity=cms.untracked.int32(1),
)

process.p = cms.Path(process.generator)
