===============
Taperable Helix
===============

..
  TODO: eventually we'll enable the badges
  .. image:: https://img.shields.io/pypi/v/taperable_helix.svg
        :target: https://pypi.python.org/pypi/taperable_helix

  .. image:: https://img.shields.io/travis/winksaville/taperable_helix.svg
          :target: https://travis-ci.com/winksaville/taperable_helix

.. image:: https://readthedocs.org/projects/taperable-helix/badge/?version=latest
         :target: https://taperable-helix.readthedocs.io/en/latest/?badge=latest
         :alt: Documentation Status

Generate helixes that can optionally taper to a point at each end.

* GitHub repo: https://github.com/winksaville/py-taperable-helix/
* Documentation: https://taperable-helix.readthedocs.io/
* PyPi package: https://pypi.org/project/taperable-helix/
* Free software: MIT license


Package Docs
------------

* docs: https://taperable-helix.readthedocs.io/en/latest/taperable_helix.html
* source: `helix.py`_

..
    I wish the code-block's below could be a `.. literalinclude::`,
    but I couldn't get that to work.

.. code-block:: python

    def helix(
        radius: float,
        pitch: float,
        height: float,
        taper_rpos: float = 0,
        inset_offset: float = 0,
        horz_offset: float = 0,
        vert_offset: float = 0,
        first_t: float = 0,
        last_t: float = 1,
    ) -> Callable[[float], Tuple[float, float, float]]:
        ...

Examples
--------

* `helical_line.py`_

.. code-block:: python

    def helical_line(
        radius: float = 5, pitch: float = 2, height: float = 6, num_points: int = 100
    ) -> List[Tuple[float, float, float]]:
        f = helix(radius, pitch, height)
        points = list(map(f, linspace(start=0, stop=1, num=num_points, dtype=float)))
        # print(f"helical_line: points={points}")
        return points

    
.. image:: /data/helical_line.webp


* `helical_tri.py`_

.. code-block:: python

    def helical_triangle(
        radius: float = 1,
        pitch: float = 2,
        height: float = 4,
        num_points: int = 100,
        tri_height: float = 0.2,
        tri_width: float = 0.2,
    ) -> Tuple[
        List[Tuple[float, float, float]],
        List[Tuple[float, float, float]],
        List[Tuple[float, float, float]],
    ]:
        taper_out_rpos = 0.1
        taper_in_rpos = 0.9
        first_t = 0
        last_t = 1

        # Create three helixes that taper to a point
        fU = helix(radius, pitch, height, taper_out_rpos=taper_out_rpos, taper_in_rpos=taper_in_rpos, vert_offset=tri_height / 2)
        points_fU = list(map(fU, linspace(first_t, last_t, num=100, dtype=float)))

        fM = helix(radius, pitch, height, taper_out_rpos=taper_out_rpos, taper_in_rpos=taper_in_rpos, horz_offset=tri_width)
        points_fM = list(map(fM, linspace(first_t, last_t, num=100, dtype=float)))

        fL = helix(
            radius, pitch, height, taper_out_rpos=taper_out_rpos, taper_in_rpos=taper_in_rpos, vert_offset=-tri_height / 2
        )
        points_fL = list(map(fL, linspace(first_t, last_t, num=100, dtype=float)))
        return (points_fU, points_fM, points_fL)


.. image:: /data/helical_tri.webp


Prerequisites
-------------

Using
#####

* python >= 3.7


Development and Examples
########################

* sphinx
* plotly

  * numpy
  * panda
  * python-kaleido

Credits
-------

This code originated from a post_ by Adam Urbanczyk to the CadQuery_ forum_ and this
package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _post: https://groups.google.com/g/cadquery/c/5kVRpECcxAU/m/7no7_ja6AAAJ
.. _CadQuery: https://github.com/cadquery/cadquery
.. _forum: https://groups.google.com/g/cadquery
.. _`helix.py`: https://github.com/winksaville/py-taperable-helix/blob/master/taperable_helix/helix.py
.. _`helical_line.py`: https://github.com/winksaville/py-taperable-helix/blob/master/examples/helical_line.py
.. _`helical_tri.py`: https://github.com/winksaville/py-taperable-helix/blob/master/examples/helical_tri.py
