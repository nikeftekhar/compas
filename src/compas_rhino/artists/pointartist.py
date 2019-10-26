from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from itertools import zip_longest

import compas_rhino
# from compas.utilities import like_list
from compas_rhino.artists import _PrimitiveArtist


__all__ = ['PointArtist']


def list_like(target, value, fillvalue=None):
    if not isinstance(value, list):
        value = [value]
    return [u for _ , u in zip_longest(target, value, fillvalue=fillvalue)]


class PointArtist(_PrimitiveArtist):
    """Artist for drawing ``Point`` objects.

    Parameters
    ----------
    point : :class:`compas.geometry.Point`
        A COMPAS point.
    layer : str (optional)
        The name of the layer that will contain the point.
        Default value is ``None``, in which case the current layer will be used.

    Examples
    --------
    >>>

    """"

    __module__ = "compas_rhino.artists"

    def __init__(self, point, layer=None):
        super(PointArtist, self).__init__(point, layer=layer)
        self.settings.update({
            'color.point': (0, 0, 0)})

    def draw(self):
        """Draw the point.
        
        Returns
        -------
        guid: str
            The GUID of the created Rhino object.

        """
        points = [{'pos': list(self.primitive), 'color': self.settings['color.point']}]
        guids = compas_rhino.draw_points(points, layer=self.settings['layer'], clear=False)
        return guids

    @staticmethod
    def draw_collection(collection, color=None, layer=None, clear=False, group_collection=False, group_name=None):
        """Draw a collection of points.
        
        Parameters
        ----------
        collection: list of compas.geometry.Point
            A collection of ``Point`` objects.
        color: tuple or list of tuple (optional)
            Color specification of the points.
            If one RGB color is provided, it will be applied to all points.
            If a list of RGB colors is provided, these colors are applied to the corresponding points.
            A list of colors should have the same length as the collection, with one color per item.
            Default value is ``None`` in which case the default point color of the artist is used.
        layer: str (optional)
            The layer in which the objects of the collection should be created.
            Default is ``None``, in which case the default layer setting of the artist is used.
        clear: bool (optional)
            Clear the layer before drawing.
            Default is ``False``.
        group_collection: bool (optional)
            Flag for grouping the objects of the collection.
            Default is ``False``.
        group_name: str (optional).
            The name of the group.
            Default is ``None``.

        Returns
        -------
        guids: list
            A list of GUIDs if the collection is not grouped.
        groupname: str
            The name of the group if the collection objects are grouped. 

        """
        layer = layer or self.settings['layer']
        colors = list_like(collection, color, fill_value=self.settings['color.point'])
        points = []
        for point, color in zip(collection, colors):
            points.append({
                'pos': list(point),
                'color': color})
        if clear:
            if layer:
                compas_rhino.clear_layer(layer)
            else:
                compas_rhino.clear_current_layer()
        guids = compas_rhino.draw_points(points, layer=layer)
        if not group_collection:
            return guids
        group = compas_rhino.rs.AddGroup(group_name)
        if group:
            compas_rhino.rs.AddObjectsToGroup(guids, group)
        return group


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
