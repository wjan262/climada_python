"""
Test ImpactFunc class.
"""

import unittest
import numpy as np

from climada.entity.impact_funcs.impact_func import ImpactFunc

class TestInterpolation(unittest.TestCase):
    """Impact function interpolation test"""

    def test_wrongAttribute_fail(self):
        """Interpolation of wrong variable fails."""
        imp_fun = ImpactFunc()
        intensity = 3
        with self.assertLogs('climada.entity.impact_funcs.impact_func', \
                             level='ERROR') as cm:
            with self.assertRaises(ValueError):
                imp_fun.interpolate(intensity, 'mdg')
        self.assertIn('Attribute of the impact function not found: mdg', \
                      cm.output[0])

    def test_mdd_pass(self):
        """Good interpolation of MDD."""
        imp_fun = ImpactFunc()
        imp_fun.intensity = np.array([0,1])
        imp_fun.mdd = np.array([1,2])
        imp_fun.paa = np.array([3,4])
        intensity = 0.5
        resul = imp_fun.interpolate(intensity, 'mdd')
        self.assertEqual(1.5, resul)

    def test_paa_pass(self):
        """Good interpolation of PAA."""
        imp_fun = ImpactFunc()
        imp_fun.intensity = np.array([0,1])
        imp_fun.mdd = np.array([1,2])
        imp_fun.paa = np.array([3,4])
        intensity = 0.5
        resul = imp_fun.interpolate(intensity, 'paa')
        self.assertEqual(3.5, resul)  
        
# Execute Tests
TESTS = unittest.TestLoader().loadTestsFromTestCase(TestInterpolation)
unittest.TextTestRunner(verbosity=2).run(TESTS)
