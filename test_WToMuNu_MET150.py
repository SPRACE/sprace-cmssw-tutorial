import FWCore.ParameterSet.Config as cms

process = cms.Process("TEST")

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(100))

process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

process.load("Configuration.StandardSequences.SimulationRandomNumberGeneratorSeeds_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

process.generator = cms.EDFilter(
    "Pythia8GeneratorFilter",
    comEnergy=cms.double(13000.0),
    crossSection=cms.untracked.double(1.6315e02),
    filterEfficiency=cms.untracked.double(1),
    maxEventsToPrint=cms.untracked.int32(1),
    pythiaHepMCVerbosity=cms.untracked.bool(False),
    pythiaPylistVerbosity=cms.untracked.int32(1),
    PythiaParameters=cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters=cms.vstring(
            "WeakSingleBoson:ffbar2ffbar(s:W) = on",
            "24:onMode = off",
            "24:onIfAny = 13,14",
            "PhaseSpace:pTHatMin = 120",
        ),
        parameterSets=cms.vstring(
            "pythia8CommonSettings", "pythia8CUEP8M1Settings", "processParameters"
        ),
    ),
)

nuetamax = 1000.0
nuetamin = -1000.0
nustatus = 1
nuptmin = 150.0

process.genENeutrinos = cms.EDFilter(
#    "PythiaFilter",
#    Status=cms.untracked.int32(1),
#    MaxEta=cms.untracked.double(1000.0),
#    MinEta=cms.untracked.double(-1000.0),
#    MinPt=cms.untracked.double(150),
#    ParticleID=cms.untracked.int32(12, 14, 16),

    "MCSingleParticleFilter",
    MaxEta = cms.untracked.vdouble(nuetamax, nuetamax, nuetamax),
    Status = cms.untracked.vint32(nustatus, nustatus, nustatus),
    MinEta = cms.untracked.vdouble(nuetamin, nuetamin, nuetamin),
    MinPt = cms.untracked.vdouble(nuptmin, nuptmin, nuptmin),
    ParticleID = cms.untracked.vint32(12, 14, 16)

)

process.p = cms.Path(process.generator * process.genENeutrinos)

process.out = cms.OutputModule(
    "PoolOutputModule", fileName=cms.untracked.string("output.root")
)

process.outMET150 = process.out.clone(
    fileName=cms.untracked.string("outputMET150.root"),
    SelectEvents=cms.untracked.PSet(SelectEvents=cms.vstring("p")),
)

process.ep = cms.EndPath(process.out)
process.ep150 = cms.EndPath(process.outMET150)
