import pytest
from flood_tool.algorithms.kdtree import KDTree
import math

def test_kdtree_build():
    points = [(1, 1), (2, 2), (3, 3)]
    tree = KDTree(points)
    assert tree.root is not None
    assert tree.root.point in points

def test_kdtree_radius_euclidean():
    # Points in a grid
    points = [
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1)
    ]
    tree = KDTree(points)
    
    # Query center (0,0) radius 1.1 -> should get (0,0), (1,0), (0,1)
    results = tree.query_radius((0, 0), 1.1)
    assert len(results) == 3
    assert (0, 0) in results
    assert (1, 0) in results
    assert (0, 1) in results

def test_kdtree_radius_empty():
    points = [(10, 10)]
    tree = KDTree(points)
    results = tree.query_radius((0, 0), 1)
    assert len(results) == 0

def test_kdtree_with_data():
    # Points with data
    points = [
        (1, 1, "A"),
        (5, 5, "B")
    ]
    tree = KDTree(points)
    
    # Query near (1,1)
    results = tree.query_radius((1, 1), 0.1)
    assert len(results) == 1
    assert results[0][2] == "A"

def test_points_within_radius_count():
    points = [(1, 1), (1.1, 1.1), (5, 5)]
    tree = KDTree(points)
    count = tree.points_within_radius_count((1, 1), 0.5)
    assert count == 2 # (1,1) and (1.1,1.1)
