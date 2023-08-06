# -*- coding: utf-8 -*-

import pandas as pd
import pytest
from fiona.crs import from_epsg
from datetime import timedelta, datetime
from .test_trajectory import make_traj, Node
from movingpandas.trajectory_collection import TrajectoryCollection
from movingpandas.trajectory_stop_detector import TrajectoryStopDetector


CRS_METRIC = from_epsg(31256)
CRS_LATLON = from_epsg(4326)


class TestTrajectorySplitter:

    def test_stop_detector_middle_stop(self):
        traj = make_traj([Node(0, 0), Node(0, 10, second=1), Node(0, 20, second=2), Node(0, 21, second=4),
                          Node(0, 22, second=6), Node(0, 30, second=8), Node(0, 40, second=10), Node(1, 50, second=15)])
        detector = TrajectoryStopDetector(traj)
        stop_times = detector.get_stop_time_ranges(max_diameter=3, min_duration=timedelta(seconds=2))
        assert len(stop_times) == 1
        assert stop_times[0].t_0 == datetime(1970,1,1,0,0,2)
        assert stop_times[0].t_n == datetime(1970,1,1,0,0,6)
        stop_segments = detector.get_stop_segments(max_diameter=3, min_duration=timedelta(seconds=2))
        assert len(stop_segments) == 1
        assert stop_segments.trajectories[0].to_linestringm_wkt() == "LINESTRING M (0.0 20.0 2.0, 0.0 21.0 4.0, 0.0 22.0 6.0)"

    def test_stop_detector_start_stop(self):
        traj = make_traj([Node(0, 0), Node(0, 1, second=1), Node(0, 2, second=2), Node(0, 1, second=3),
                          Node(0, 22, second=4), Node(0, 30, second=8), Node(0, 40, second=10), Node(1, 50, second=15)])
        detector = TrajectoryStopDetector(traj)
        stop_times = detector.get_stop_time_ranges(max_diameter=3, min_duration=timedelta(seconds=2))
        assert len(stop_times) == 1
        assert stop_times[0].t_0 == datetime(1970,1,1,0,0,0)
        assert stop_times[0].t_n == datetime(1970,1,1,0,0,3)

    def test_stop_detector_end_stop(self):
        traj = make_traj([Node(0, -100), Node(0, -10, second=1), Node(0, 2, second=2), Node(0, 1, second=3),
                          Node(0, 22, second=4), Node(0, 30, second=8), Node(0, 31, second=10), Node(1, 32, second=15)])
        detector = TrajectoryStopDetector(traj)
        stop_times = detector.get_stop_time_ranges(max_diameter=3, min_duration=timedelta(seconds=2))
        assert len(stop_times) == 1
        assert stop_times[0].t_0 == datetime(1970,1,1,0,0,8)
        assert stop_times[0].t_n == datetime(1970,1,1,0,0,15)

    def test_stop_detector_multiple_stops(self):
        traj = make_traj([Node(0, 0), Node(0, 1, second=1), Node(0, 2, second=2), Node(0, 1, second=3),
                          Node(0, 22, second=4), Node(0, 30, second=8), Node(0, 31, second=10), Node(1, 32, second=15)])
        detector = TrajectoryStopDetector(traj)
        stop_times = detector.get_stop_time_ranges(max_diameter=3, min_duration=timedelta(seconds=2))
        assert len(stop_times) == 2
        assert stop_times[0].t_0 == datetime(1970,1,1,0,0,0)
        assert stop_times[0].t_n == datetime(1970,1,1,0,0,3)
        assert stop_times[1].t_0 == datetime(1970,1,1,0,0,8)
        assert stop_times[1].t_n == datetime(1970,1,1,0,0,15)

    def test_stop_detector_collection(self):
        traj1 = make_traj([Node(0, 0), Node(0, 1, second=1), Node(0, 2, second=2), Node(0, 1, second=3),
                          Node(0, 22, second=4), Node(0, 30, second=8), Node(0, 40, second=10), Node(1, 50, second=15)], id=1)
        traj2 = make_traj([Node(0, -100), Node(0, -10, second=1), Node(0, 2, second=2), Node(0, 1, second=3),
                          Node(0, 22, second=4), Node(0, 30, second=8), Node(0, 31, second=10), Node(1, 32, second=15)], id=2)
        collection = TrajectoryCollection([traj1, traj2])
        detector = TrajectoryStopDetector(collection)
        stop_times = detector.get_stop_time_ranges(max_diameter=3, min_duration=timedelta(seconds=2))
        stop_segments = detector.get_stop_segments(max_diameter=3, min_duration=timedelta(seconds=2))
        assert len(stop_times) == 2
        assert len(stop_segments) == 2
