# This file is part of meas.extensions.Petrosian.
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

import unittest
import lsst.utils.tests
import lsst.meas.base.tests
import lsst.meas.extensions.petrosian
import lsst.geom

class PetrosianTests(lsst.meas.base.tests.AlgorithmTestCase, lsst.utils.tests.TestCase):
    def setUp(self):
        box = lsst.geom.Box2I(lsst.geom.Point2I(-5,4),lsst.geom.Point2I(105,120))
        self.dataset = lsst.meas.base.tests.TestDataset(box) 
        self.dataset.addSource(1.0e5, lsst.geom.Point2D(50,50))

    def test_petrosian_flux(self):
        schema = self.dataset.makeMinimalSchema()
        task = self.makeSingleFrameMeasurementTask("ext_PetrosianFlux", ["base_CircularApertureFlux"],
                                                   schema=schema)
        exposure, catalog = self.dataset.realize(10., schema)
        task.run(catalog, exposure)
        print(catalog[0])
        self.assertEqual(catalog[0]["ext_PetrosianFlux_instFlux"], 10)

class TestMemory(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
