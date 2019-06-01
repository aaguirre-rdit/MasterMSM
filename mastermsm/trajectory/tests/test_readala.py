import unittest
import mdtraj as md
from mastermsm.trajectory import traj

class TestMDtraj(unittest.TestCase):
    def setUp(self):
        self.traj = md.load('trajectory/tests/data/protein_only.xtc', \
                top='trajectory/tests/data/alaTB.gro')

    def test_traj(self):
        self.assertEqual(self.traj.n_atoms, 19, 'incorrect number of atoms')
        self.assertEqual(self.traj.timestep, 1.0, 'incorrect timestep')

class UseMDtraj(unittest.TestCase):

    def setUp(self):
        print('self', self)
        top='trajectory/tests/data/alaTB.gro'
        trj=['trajectory/tests/data/protein_only.xtc']
        tr = traj.TimeSeries(top=top, traj=trj)
        self.tr = tr
        pass

    def test_atributes(self):
        print('mdt',self.tr.mdt)
        print(dir(self.tr),self.tr.file_name)
        self.assertEqual(self.tr.dt, 1.0, 'incorrect timestamp')
        self.assertIn('discretize',dir(self.tr),'discretize not in attributes')
        self.assertIsInstance(self.tr.file_name,list,'file_name attribute is not a list')
        self.assertIn('trajectory/tests/data/protein_only.xtc', self.tr.file_name, \
                      'sample trajectory is not TimeSeries file name')
        self.assertIsInstance(self.tr.discretize, object, 'discretize attribute is not an object')

#    def test_discretize(self):
#        assert self.tr.n_traj == 1

if __name__ == "__main__":
    unittest.main(verbosity=2)
