"""This test script contains tests for analyze.py
"""
# -*- coding: utf-8 -*-

import os
import shutil
import sys

package_path = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))))
if not(package_path in sys.path):
    sys.path.append(package_path)
import ABXpy.task
import ABXpy.distances.distances as distances
import ABXpy.distances.metrics.cosine as cosine
import ABXpy.distances.metrics.dtw as dtw
import ABXpy.score as score
import ABXpy.misc.items as items
import ABXpy.analyze as analyze
import numpy as np


frozen_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'frozen_files')


def frozen_file(ext):
    return os.path.join(frozen_folder, 'data') + '.' + ext


def dtw_cosine_distance(x, y, normalized):
    return dtw.dtw(x, y, cosine.cosine_distance, normalized)


def test_analyze():
    try:
        if not os.path.exists('test_items'):
            os.makedirs('test_items')
        item_file = 'test_items/data.item'
        feature_file = 'test_items/data.features'
        distance_file = 'test_items/data.distance'
        scorefilename = 'test_items/data.score'
        taskfilename = 'test_items/data.abx'
        analyzefilename = 'test_items/data.csv'

        items.generate_db_and_feat(3, 3, 1, item_file, 2, 3, feature_file)
        task = ABXpy.task.Task(item_file, 'c0', 'c1', 'c2')
        task.generate_triplets(taskfilename)
        distances.compute_distances(feature_file, '/features/', taskfilename,
                                    distance_file, dtw_cosine_distance,
                                    normalized = True, n_cpu=1)
        score.score(taskfilename, distance_file, scorefilename)
        analyze.analyze(taskfilename, scorefilename, analyzefilename)
    finally:
        try:
            shutil.rmtree('test_items')
            # os.remove(item_file)
            # os.remove(feature_file)
            # os.remove(taskfilename)
            # os.remove(distance_file)
            # os.remove(scorefilename)
            # os.remove(analyzefilename)
        except:
            pass


def test_threshold_analyze():
    try:
        if not os.path.exists('test_items'):
            os.makedirs('test_items')
        item_file = 'test_items/data.item'
        feature_file = 'test_items/data.features'
        distance_file = 'test_items/data.distance'
        scorefilename = 'test_items/data.score'
        taskfilename = 'test_items/data.abx'
        analyzefilename = 'test_items/data.csv'
        threshold = 2

        items.generate_db_and_feat(3, 3, 1, item_file, 2, 3, feature_file)
        task = ABXpy.task.Task(item_file, 'c0', 'c1', 'c2')
        task.generate_triplets(taskfilename, threshold=threshold)
        distances.compute_distances(
            feature_file, '/features/', taskfilename,
            distance_file, dtw_cosine_distance,
            normalized = True, n_cpu=1)
        score.score(taskfilename, distance_file, scorefilename)
        analyze.analyze(taskfilename, scorefilename, analyzefilename)
        number_triplets = np.loadtxt(analyzefilename, dtype=int,
                                     delimiter='\t', skiprows=1, usecols=[-1])
        assert np.all(number_triplets == threshold)
    finally:
        try:
            shutil.rmtree('test_items')
            # os.remove(item_file)
            # os.remove(feature_file)
            # os.remove(taskfilename)
            # os.remove(distance_file)
            # os.remove(scorefilename)
            # os.remove(analyzefilename)
        except:
            pass


def test_frozen_analyze():
    """Frozen analyze compare the results of a previously "frozen" run with
    a new one, asserting that the code did not change in behaviour.
    """
    try:
        if not os.path.exists('test_items'):
            os.makedirs('test_items')
        item_file = frozen_file('item')
        feature_file = frozen_file('features')
        distance_file = 'test_items/data.distance'
        scorefilename = 'test_items/data.score'
        taskfilename = 'test_items/data.abx'
        analyzefilename = 'test_items/data.csv'

        task = ABXpy.task.Task(item_file, 'c0', 'c1', 'c2')
        task.generate_triplets(taskfilename)
        distances.compute_distances(feature_file, '/features/', taskfilename,
                                    distance_file, dtw_cosine_distance,
                                    normalized = True, n_cpu=1)
        score.score(taskfilename, distance_file, scorefilename)
        analyze.analyze(taskfilename, scorefilename, analyzefilename)

        # assert items.h5cmp(taskfilename, frozen_file('abx'))
        # assert items.h5cmp(distance_file, frozen_file('distance'))
        # assert items.h5cmp(scorefilename, frozen_file('score'))
        assert items.csv_cmp(analyzefilename, frozen_file('csv'))

    finally:
        try:
            shutil.rmtree('test_items')
            # os.remove(taskfilename)
            # os.remove(distance_file)
            # os.remove(scorefilename)
            # os.remove(analyzefilename)
        except:
            pass
