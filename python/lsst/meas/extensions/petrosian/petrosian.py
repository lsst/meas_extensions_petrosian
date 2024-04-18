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

import lsst.meas.base

class PetrosianConfig(lsst.meas.base.SingleFramePluginConfig):
    pass

@lsst.meas.base.register("ext_PetrosianFlux")
class PetrosianPlugin(lsst.meas.base.SingleFramePlugin):
    ConfigClass = PetrosianConfig

    def __init__(self, config, name, schema, metadata, **kwargs):
        self.fluxkey = lsst.meas.base.FluxResultKey.addFields(schema, 
                                                              name, 
                                                              "Petrosian Flux")
        super().__init__(config, name, schema, metadata)

    @classmethod 
    def getExecutionOrder(cls):
        return cls.APCORR_ORDER + 1

    def measure(self, record, exposure):
        record[self.fluxkey.getInstFlux()] = 10
        return

    def fail(self, record):
        self.log.error("Failure measuring Petrosian Flux on source %s", record["id"])

