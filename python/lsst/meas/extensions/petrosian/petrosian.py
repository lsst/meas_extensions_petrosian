# This file is part of meas_extensions_petrosian.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__all__ = ["PetrosianPlugin", "PetrosianConfig"]

import logging
import lsst.meas.base

class PetrosianConfig(lsst.meas.base.SingleFramePluginConfig):
    pass

@lsst.meas.base.register("ext_PetrosianFlux")
class PetrosianPlugin(lsst.meas.base.SingleFramePlugin):
    ConfigClass = PetrosianConfig

    def __init__(self, config, name, schema, metadata, logName=None, **kwargs):
        
        if logName is None:
            logName = __name__
        
        self.fluxkey = lsst.meas.base.FluxResultKey.addFields(schema, 
                                                              name, 
                                                              "Petrosian Flux")
        super().__init__(config, name, schema, metadata)
    
        # Define flags for possible issues that might arise during measurement.
        flagDefs = lsst.meas.base.FlagDefinitionList()
        self.DIVZERO = flagDefs.add("flag_divzero", "Encountered division by zero")
        # Embed the flag definitions in the schema using a flag handler.
        self.flagHandler = lsst.meas.base.FlagHandler.addFields(schema, name, flagDefs)

        self.log = logging.getLogger(self.logName)

    
    @classmethod 
    def getExecutionOrder(cls):
        #return cls.APCORR_ORDER + 1
        return cls.FLUX_ORDER

    def calculatePetrosianFlux(self, aperture, apertureFlux, eta):
        # place-holder...
        petrosianFlux = apertureFlux/eta
        return petrosianFlux
    
    def measure(self, record, exposure):
        # placeholder values to test error handling...
        aperture = 2.
        apertureFlux = 10.
        # Set eta to 0. to test ZeroDivisionError exception...
        #eta = 0.
        eta = 1.
        try:
            petrosianFlux = self.calculatePetrosianFlux(aperture, apertureFlux, eta)
        except ZeroDivisionError:
            raise lsst.meas.base.MeasurementError(self.DIVZERO.doc, self.DIVZERO.number)
        
        record[self.fluxkey.getInstFlux()] = petrosianFlux

    #def fail(self, record):
    #    
    #    self.log.error("Failure measuring Petrosian Flux on source %s", record["id"])

    def fail(self, record, error=None):
        # Docstring inherited.
        self.flagHandler.handleFailure(record)
        if error:
            #centroid = self.centroidExtractor(record, self.flagHandler)
            self.log.debug(
                "Failure measuring Petrosian Flux on source %s: %s",
                record.getId(),
                error,
            )


