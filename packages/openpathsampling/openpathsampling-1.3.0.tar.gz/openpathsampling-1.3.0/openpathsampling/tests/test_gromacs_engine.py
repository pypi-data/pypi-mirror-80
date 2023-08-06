import pytest
import numpy.testing as npt
from nose.tools import (assert_equal, assert_not_equal, assert_almost_equal,
                        raises, assert_true)
from nose.plugins.skip import Skip, SkipTest
import numpy.testing as npt

from .test_helpers import data_filename, assert_items_equal

import openpathsampling as paths
try:
    import mdtraj as md
except ImportError:
    HAS_MDTRAJ = False
else:
    HAS_MDTRAJ = True


from openpathsampling.engines.gromacs import *

import logging
import numpy as np

import shutil

logging.getLogger('openpathsampling.initialization').setLevel(logging.CRITICAL)
logging.getLogger('openpathsampling.ensemble').setLevel(logging.CRITICAL)
logging.getLogger('openpathsampling.storage').setLevel(logging.CRITICAL)
logging.getLogger('openpathsampling.netcdfplus').setLevel(logging.CRITICAL)

# check whether we have Gromacs 5 available; otherwise some tests skipped
# lazily use subprocess here; in case we ever change use of psutil
import subprocess
import os
devnull = open(os.devnull, 'w')
try:
    has_gmx = not subprocess.call(["gmx", "-version"], stdout=devnull,
                                  stderr=devnull)
except OSError:
    has_gmx = False
finally:
    devnull.close()


class TestGromacsEngine(object):
    # Files used (in test_data/gromacs_engine/)
    # conf.gro, md.mdp, topol.top : standard Gromacs input files
    # project_trr/0000000.trr : working file, 4 frames
    # project_trr/0000099.trr : 49 working frames, final frame partial
    def setup(self):
        if not HAS_MDTRAJ:
            pytest.skip("MDTraj not installed.")
        self.test_dir = data_filename("gromacs_engine")
        self.engine = Engine(gro="conf.gro",
                             mdp="md.mdp",
                             top="topol.top",
                             options={},
                             base_dir=self.test_dir,
                             prefix="project")

    def teardown(self):
        files = ['topol.tpr', 'mdout.mdp', 'initial_frame.trr', 'state.cpt',
                 'state_prev.cpt', 'traj_comp.xtc',
                 self.engine.trajectory_filename(1)]
        for f in files:
            if os.path.isfile(f):
                os.remove(f)
            if os.path.isfile(os.path.join(self.engine.base_dir, f)):
                os.remove(os.path.join(self.engine.base_dir, f))
        shutil.rmtree(self.engine.prefix + "_log")
        shutil.rmtree(self.engine.prefix + "_edr")

    def test_read_frame_from_file_success(self):
        # when the frame is present, we should return it
        fname = os.path.join(self.test_dir, "project_trr", "0000000.trr")
        result = self.engine.read_frame_from_file(fname, 0)
        assert_true(isinstance(result, ExternalMDSnapshot))
        assert_equal(result.file_name, fname)
        assert_equal(result.file_position, 0)
        # TODO: add caching of xyz, vel, box; check that we have it now

        fname = os.path.join(self.test_dir, "project_trr", "0000000.trr")
        result = self.engine.read_frame_from_file(fname, 3)
        assert_true(isinstance(result, ExternalMDSnapshot))
        assert_equal(result.file_name, fname)
        assert_equal(result.file_position, 3)

    def test_read_frame_from_file_partial(self):
        # if a frame is partial, return 'partial'
        fname = os.path.join(self.test_dir, "project_trr", "0000099.trr")
        frame_2 = self.engine.read_frame_from_file(fname, 49)
        assert_true(isinstance(frame_2, ExternalMDSnapshot))
        frame_3 = self.engine.read_frame_from_file(fname, 50)
        assert_equal(frame_3, "partial")

    def test_read_frame_from_file_none(self):
        # if a frame is beyond the last frame, return None
        fname = os.path.join(self.test_dir, "project_trr", "0000000.trr")
        result = self.engine.read_frame_from_file(fname, 4)
        assert_equal(result, None)

    def test_write_frame_to_file_read_back(self):
        # write random frame; read back
        # sinfully, we start by reading in a frame to get the correct dims
        fname = os.path.join(self.test_dir, "project_trr", "0000000.trr")
        tmp = self.engine.read_frame_from_file(fname, 0)
        shape = tmp.xyz.shape
        xyz = np.random.randn(*shape)
        vel = np.random.randn(*shape)
        box = np.random.randn(3, 3)
        traj_50 = self.engine.trajectory_filename(50)
        # clear it out, in case it exists from a previous failed test
        if os.path.isfile(traj_50):
            os.remove(traj_50)
        file_49 = os.path.join(self.test_dir, "project_trr", "0000049.trr")
        snap = ExternalMDSnapshot(file_name=file_49, file_position=2,
                                  engine=self.engine)
        snap.set_details(xyz, vel, box)
        self.engine.write_frame_to_file(traj_50, snap)

        snap2 = self.engine.read_frame_from_file(traj_50, 0)
        assert_equal(snap2.file_name, traj_50)
        assert_equal(snap2.file_position, 0)
        npt.assert_array_almost_equal(snap.xyz, snap2.xyz)
        npt.assert_array_almost_equal(snap.velocities, snap2.velocities)
        npt.assert_array_almost_equal(snap.box_vectors, snap2.box_vectors)

        if os.path.isfile(traj_50):
            os.remove(traj_50)

    def test_set_filenames(self):
        test_engine = Engine(gro="conf.gro", mdp="md.mdp", top="topol.top",
                             base_dir=self.test_dir, options={},
                             prefix="proj")
        test_engine.set_filenames(0)
        assert test_engine.input_file == \
                os.path.join(self.test_dir, "initial_frame.trr")
        assert test_engine.output_file == \
                os.path.join(self.test_dir, "proj_trr", "0000001.trr")
        assert_equal(test_engine.edr_file,
                     os.path.join(self.test_dir, "proj_edr", "0000001.edr"))
        assert_equal(test_engine.log_file,
                     os.path.join(self.test_dir, "proj_log", "0000001.log"))

        test_engine.set_filenames(99)
        assert_equal(test_engine.input_file,
                     os.path.join(self.test_dir, "initial_frame.trr"))
        assert_equal(test_engine.output_file,
                     os.path.join(self.test_dir, "proj_trr", "0000100.trr"))
        assert_equal(test_engine.edr_file,
                     os.path.join(self.test_dir, "proj_edr", "0000100.edr"))
        assert_equal(test_engine.log_file,
                     os.path.join(self.test_dir, "proj_log", "0000100.log"))

    def test_engine_command(self):
        test_engine = Engine(gro="conf.gro", mdp="md.mdp", top="topol.top",
                             base_dir=self.test_dir, options={},
                             prefix="proj")
        test_engine.set_filenames(0)
        tpr = os.path.join("topol.tpr")
        trr = os.path.join(self.test_dir, "proj_trr", "0000001.trr")
        edr = os.path.join(self.test_dir, "proj_edr", "0000001.edr")
        log = os.path.join(self.test_dir, "proj_log", "0000001.log")
        beauty = test_engine.engine_command()
        truth = "gmx mdrun -s {tpr} -o {trr} -e {edr} -g {log} ".format(
                    tpr=tpr, trr=trr, edr=edr, log=log
        )  # space at the end before args (args is empty)
        assert len(beauty) == len(truth)
        assert beauty == truth

    def test_generate(self):
        if not has_gmx:
            raise SkipTest("Gromacs 5 (gmx) not found. Skipping test.")

        if not HAS_MDTRAJ:
            pytest.skip("MDTraj not found. Skipping test.")

        traj_0 = self.engine.trajectory_filename(0)
        snap = self.engine.read_frame_from_file(traj_0, 0)
        self.engine.set_filenames(0)

        ens = paths.LengthEnsemble(3)
        traj = self.engine.generate(snap, running=[ens.can_append])
        assert_equal(self.engine.proc.is_running(), False)
        assert_equal(len(traj), 3)
        ttraj = md.load(self.engine.trajectory_filename(1),
                        top=self.engine.gro)
        # the mdp suggests a max length of 100 frames
        assert_true(len(ttraj) < 100)

    def test_prepare(self):
        if not has_gmx:
            raise SkipTest("Gromacs 5 (gmx) not found. Skipping test.")
        self.engine.set_filenames(0)
        traj_0 = self.engine.trajectory_filename(0)
        snap = self.engine.read_frame_from_file(traj_0, 0)
        self.engine.write_frame_to_file(self.engine.input_file, snap)
        files = ['topol.tpr', 'mdout.mdp']
        for f in files:
            if os.path.isfile(f):
                raise AssertionError("File " + str(f) + " already exists!")

        assert_equal(self.engine.prepare(), 0)
        for f in files:
            if not os.path.isfile(f):
                raise AssertionError("File " + str(f) + " was not created!")

        for f in files:
            os.remove(f)

    def test_open_file_caching(self):
        # read several frames from one file, then switch to another file
        # first read from 0000000, then 0000099
        # TODO: what was I trying to test here? that I can switch between
        # files?
        pytest.skip()

    def test_serialization_cycle(self):
        serialized = self.engine.to_dict()
        deserialized = Engine.from_dict(serialized)
        reserialized = deserialized.to_dict()
        assert serialized == reserialized


class TestGromacsExternalMDSnapshot(object):
    def setup(self):
        if not HAS_MDTRAJ:
            pytest.skip("MDTraj not installed.")

        self.test_dir = data_filename("gromacs_engine")
        self.engine = Engine(gro="conf.gro",
                             mdp="md.mdp",
                             top="topol.top",
                             options={},
                             base_dir=self.test_dir,
                             prefix="proj")
        self.snapshot = ExternalMDSnapshot(
            file_name=os.path.join(self.test_dir, "project_trr",
                                   "0000000.trr"),
            file_position=2,
            engine=self.engine
        )
        self.snapshot_shape = (1651, 3)
        self.storage_filename = "gmx_snap.nc"

    def teardown(self):
        if os.path.isfile(self.storage_filename):
            os.remove(self.storage_filename)

    @pytest.mark.parametrize('snap_num', [0, 1])
    def test_storage(self, snap_num):
        if os.path.isfile(self.storage_filename):
            os.remove(self.storage_filename)

        storage = paths.Storage(self.storage_filename, mode='w')
        storage.save(self.snapshot)

        vel_mul = 1 - 2*snap_num  # 0->1; 1->-1

        assert len(storage.snapshots) == 2  # fwd and bkwc
        snap = storage.snapshots[snap_num]
        npt.assert_array_equal(snap.xyz, self.snapshot.xyz)
        npt.assert_array_equal(snap.velocities,
                               vel_mul * self.snapshot.velocities)
        npt.assert_array_equal(snap.box_vectors,
                               self.snapshot.box_vectors)

    def _check_all_empty(self):
        # before loading an attribute, all should be empty
        assert self.snapshot._velocities is None
        assert self.snapshot._xyz is None
        assert self.snapshot._box_vectors is None

    def _check_none_empty(self):
        # after loading an attribute, all should be present
        assert self.snapshot._velocities is not None
        assert self.snapshot._xyz is not None
        assert self.snapshot._box_vectors is not None

    def test_velocities(self):
        self._check_all_empty()
        velocities = self.snapshot.velocities
        assert velocities.shape == self.snapshot_shape
        self._check_none_empty()

    def test_coordinates_xyz(self):
        self._check_all_empty()
        coordinates = self.snapshot.coordinates
        assert coordinates.shape == self.snapshot_shape
        assert all(coordinates.flatten() == self.snapshot.xyz.flatten())
        self._check_none_empty()

    def test_box_vectors(self):
        self._check_all_empty()
        box_vectors = self.snapshot.box_vectors
        assert box_vectors.shape == (3, 3)
        self._check_none_empty()

    def test_clear_cache(self):
        self._check_all_empty()
        coordinates = self.snapshot.coordinates
        assert coordinates.shape == self.snapshot_shape
        self._check_none_empty()
        self.snapshot.clear_cache()
        self._check_all_empty()
