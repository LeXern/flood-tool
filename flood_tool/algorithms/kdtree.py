import math

class Node:
    def __init__(self, point, left=None, right=None, axis=0, data=None):
        self.point = point
        self.left = left
        self.right = right
        self.axis = axis
        self.data = data # Store original object or metadata (e.g., building ID)

class KDTree:
    def __init__(self, points=None):
        """
        points: List of tuples (x, y, data) or (x, y). 
        If data is present, it's stored in the node.
        """
        self.root = None
        if points:
            # Defensive check: Ensure we have data to build on
            assert isinstance(points, list), "Points must be a list"
            self.root = self._build_tree(points)

    def _build_tree(self, points, depth=0):
        if not points:
            return None

        k = 2 # 2 dimensions (x, y)
        axis = depth % k

        # Sort point list and choose median as pivot element
        # We assume points are (x, y, ...) or (x, y)
        points.sort(key=lambda x: x[axis])
        median = len(points) // 2

        node = Node(
            point=points[median],
            axis=axis,
            data=points[median][2] if len(points[median]) > 2 else None
        )
        
        node.left = self._build_tree(points[:median], depth + 1)
        node.right = self._build_tree(points[median + 1:], depth + 1)

        return node

    def query_radius(self, center, radius, distance_func=None):
        """
        Find all points within a certain radius of the center.
        distance_func: function(p1, p2) -> float. Default is Euclidean.
        """
        if self.root is None:
            return []

        if distance_func is None:
            # Default Euclidean for 2D (x, y) coordinates
            distance_func = lambda p1, p2: math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
            
        return self._query_recursive(center, radius, self.root, distance_func)

    def _query_recursive(self, center, radius, node, distance_func):
        if node is None:
            return []

        results = []
        
        # Check distance to current node
        # node.point includes potential data, so take just first 2 coords for distance
        node_coords = node.point[:2]
        center_coords = center[:2]
        
        d = distance_func(center_coords, node_coords)
        if d <= radius:
            results.append(node.point)

        # Pruning
        axis = node.axis
        diff = center_coords[axis] - node_coords[axis]

        # If center is to the left of the splitting plane, search left
        if diff <= 0:
            results.extend(self._query_recursive(center, radius, node.left, distance_func))
            # If the sphere crosses the plane, search right too
            if abs(diff) <= radius:
                results.extend(self._query_recursive(center, radius, node.right, distance_func))
        else: # center is to the right
            results.extend(self._query_recursive(center, radius, node.right, distance_func))
            # If sphere crosses, search left
            if abs(diff) <= radius:
                results.extend(self._query_recursive(center, radius, node.left, distance_func))
                
        return results

    def points_within_radius_count(self, center, radius, distance_func=None):
        # Optimization if we only need the count for hotspot analysis
        return len(self.query_radius(center, radius, distance_func=distance_func))
