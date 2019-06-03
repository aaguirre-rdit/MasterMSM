import unittest
import mdtraj as md
import numpy as np
from mastermsm.trajectory import traj
from mastermsm.msm import msm
import matplotlib.pyplot as plt

class TestMDtraj(unittest.TestCase):
    def setUp(self):
        self.traj = md.load('trajectory/tests/data/protein_only.xtc', \
                top='trajectory/tests/data/alaTB.gro')

    def test_traj(self):
        self.assertEqual(self.traj.n_atoms, 19, 'incorrect number of atoms')
        self.assertEqual(self.traj.timestep, 1.0, 'incorrect timestep')
        self.assertEqual(self.traj.n_residues, 3, 'incorrent number of residues')


class UseMDtraj(unittest.TestCase):

    def setUp(self):
        print('self', self)
        top='trajectory/tests/data/alaTB.gro'
        trj=['trajectory/tests/data/protein_only.xtc']
        tr = traj.TimeSeries(top=top, traj=trj)
        self.tr = tr
        pass

    def test_atributes(self):
        #print('mdt',self.tr.mdt, type(self.tr.mdt))
        #print(dir(self.tr.mdt),self.tr.file_name)
        self.assertEqual(self.tr.dt, 1.0, 'incorrect timestamp')
        self.assertIn('discretize',dir(self.tr),'discretize not in attributes')
        self.assertIsInstance(self.tr.file_name,list,'file_name attribute is not a list')
        self.assertIn('trajectory/tests/data/protein_only.xtc', self.tr.file_name, \
                      'sample trajectory is not TimeSeries file name')
        self.assertIsInstance(self.tr.discretize, object, 'discretize attribute is not an object')
        self.assertIn('mdt', dir(self.tr), 'MDTraj is not in attributes')
        print('******************')
    def test_discretize(self):
        self.tr.discretize(method='rama', states=['A','E','L'])
        self.assertIsNotNone(self.tr.distraj,'no discrete trajectory was created')

        y = [1]*10003
        for ind,i in enumerate(self.tr.distraj):
            if i == 'A':
                y[ind]=0
            if i == 'E':
                y[ind]=2
            if i == 'O':
                y[ind]=3

        #plt.plot(range(len(self.tr.distraj[1:])), y[1:])
        #plt.show()
        self.tr.find_keys()
        self.assertEqual(len(self.tr.keys), 3, 'incorrect number of states')


class UseMSM(unittest.TestCase):
    def setUp(self):
        top = 'trajectory/tests/data/alaTB.gro'
        trj = ['trajectory/tests/data/protein_only.xtc']
        tr = traj.TimeSeries(top=top, traj=trj)
        self.tr = tr
        self.tr.discretize(method='rama', states=['A','E','L'])
        self.tr.find_keys()
        self.msm = msm.SuperMSM([self.tr])
    def test_msm(self):
        self.assertEqual(1,1)
        lagt=10
        self.msm.do_msm(lagt)
        self.msm.msms[lagt].do_trans(evecs=True)
        self.msm.msms[lagt].boots()
        print(dir(self.msm.msms[10]))
        fig, ax = plt.subplots()
        ax.errorbar(range(1, len(self.msm.msms[lagt].tauT) + 1), self.msm.msms[lagt].tauT, fmt='o-', \
                     ms=10)
        ax.set_xlabel('Eigenvalue')
        ax.set_ylabel(r'$\tau_i$')
        #ax.set_ylim(0, 2100)
        #ax.set_xlim(0, 32)
        plt.tight_layout()
        plt.show()
    def test_convergence(self):
        #self.msm.convergence_test(time=[1, 10, 100], error=True)
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)
