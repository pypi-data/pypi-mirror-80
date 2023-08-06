from .gam_g4 import *

import wget
import os
import tarfile

#Download Geant4 data if not present:
dataPackages = [
    "https://cern.ch/geant4-data/datasets/G4NDL.4.6.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4EMLOW.7.9.1.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4PhotonEvaporation.5.5.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4RadioactiveDecay.5.4.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4SAIDDATA.2.0.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4PARTICLEXS.2.1.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4ABLA.3.1.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4INCL.1.0.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4PII.1.3.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4ENSDFSTATE.2.2.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4RealSurface.2.1.1.tar.gz",
    "https://cern.ch/geant4-data/datasets/G4TENDL.1.3.2.tar.gz"]

packageLocation = os.path.dirname(os.path.realpath(__file__))
dataLocation = os.path.join(packageLocation, "geant4_data")
if not os.path.exists(dataLocation):
    print("No Geant4 data available in: " + dataLocation)
    print("I download it for you.")
    os.mkdir(dataLocation)
    for package in dataPackages:
      packageArchive = wget.download(package, out=dataLocation)
      with tarfile.open(packageArchive) as tar:
        tar.extractall(path=dataLocation)
      os.remove(packageArchive)
    print("")
    print("Done")

