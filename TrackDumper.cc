// -*- C++ -*-
//
// Package:    TestAnalyzer/TrackDumper
// Class:      TrackDumper
//
/**\class TrackDumper TrackDumper.cc TestAnalyzer/TrackDumper/plugins/TrackDumper.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Thiago Tomei Fernandez
//         Created:  Thu, 14 Apr 2022 20:00:00 GMT
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TTree.h"
//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.

using reco::TrackCollection;

class TrackDumper : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit TrackDumper(const edm::ParameterSet&);
  ~TrackDumper();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;

  // ----------member data ---------------------------
  edm::EDGetTokenT<TrackCollection> tracksToken_;  //used to select what tracks to read from configuration file
  edm::Service<TFileService> fs;
  TTree * tree_tracks;
  Int_t numTracks;
  Float_t track1Pt;
  Float_t track2Pt;
  Float_t track3Pt;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
TrackDumper::TrackDumper(const edm::ParameterSet& iConfig)
    : tracksToken_(consumes<TrackCollection>(iConfig.getUntrackedParameter<edm::InputTag>("tracks"))) {
    tree_tracks = fs->make<TTree>("tree_tracks", "Tree of tracks");
    tree_tracks->Branch("numTracks",&numTracks,"numTracks/I");
    tree_tracks->Branch("track1Pt",&track1Pt,"track1Pt/F");
    tree_tracks->Branch("track2Pt",&track2Pt,"track2Pt/F");
    tree_tracks->Branch("track3Pt",&track3Pt,"track3Pt/F");
  //now do what ever initialization is needed
}

TrackDumper::~TrackDumper() {
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
  //
  // please remove this method altogether if it would be left empty
}

//
// member functions
//

// ------------ method called for each event  ------------
void TrackDumper::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;

  std::vector<float> trackPts;

  for (const auto& track : iEvent.get(tracksToken_)) {
      if(track.pt() > 3.0) {
          trackPts.push_back(float(track.pt()));
      }
  }

  std::sort(trackPts.begin(), trackPts.end());
  std::reverse(trackPts.begin(), trackPts.end());
  numTracks = Int_t(trackPts.size());
  track1Pt = Float_t(trackPts.at(0));
  track2Pt = Float_t(trackPts.at(1));
  track3Pt = Float_t(trackPts.at(2));
  tree_tracks->Fill();
}

// ------------ method called once each job just before starting event loop  ------------
void TrackDumper::beginJob() {
  // please remove this method if not needed
}

// ------------ method called once each job just after ending the event loop  ------------
void TrackDumper::endJob() {
  // please remove this method if not needed
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void TrackDumper::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

  //Specify that only 'tracks' is allowed
  //To use, remove the default given above and uncomment below
  //ParameterSetDescription desc;
  //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
  //descriptions.addWithDefaultLabel(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TrackDumper);
