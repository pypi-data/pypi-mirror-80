# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['routingpy', 'routingpy.routers']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.0.0,<3.0.0']

extras_require = \
{'notebooks': ['pandas>=1.1.0,<2.0.0',
               'folium>=0.11.0,<0.12.0',
               'shapely>=1.7.0,<2.0.0',
               'ipykernel>=5.3.4,<6.0.0']}

setup_kwargs = {
    'name': 'routingpy',
    'version': '0.3.2',
    'description': 'One lib to route them all.',
    'long_description': 'routing-py\n==========\n\n.. image:: https://travis-ci.org/gis-ops/routing-py.svg?branch=master\n    :target: https://travis-ci.org/gis-ops/routing-py\n    :alt: Build status\n\n.. image:: https://coveralls.io/repos/github/gis-ops/routing-py/badge.svg?branch=master\n    :target: https://coveralls.io/github/gis-ops/routing-py?branch=master\n    :alt: Coveralls coverage\n\n.. image:: https://readthedocs.org/projects/routingpy/badge/?version=latest\n    :target: https://routingpy.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://mybinder.org/badge_logo.svg\n    :target: https://mybinder.org/v2/gh/gis-ops/routing-py/master?filepath=examples\n    :alt: MyBinder.org\n\n\n*One lib to route them all* - **routingpy** is a Python 3 client for several\npopular routing webservices.\n\nInspired by `geopy <https://github.com/geopy/geopy>`_ and its great community of contributors, **routingpy** enables\neasy and consistent access to third-party spatial webservices to request **route directions**, **isochrones**\nor **time-distance matrices**.\n\n**routingpy** currently includes support for the following services:\n\n-  `Mapbox, either Valhalla or OSRM`_\n-  `Openrouteservice`_\n-  `Here Maps`_\n-  `Google Maps`_\n-  `Graphhopper`_\n-  `Local Valhalla`_\n-  `Local Mapbox`_\n\nThis list is hopefully growing with time and contributions by other developers. An up-to-date list is always availaable\nin our documentation_.\n\n**routing-py** is tested against CPython versions 3.6, 3.7, 3.8-dev and against PyPy 3.6.x. As other major libraries like ``numpy``\nand ``pandas`` decided to drop Python 2 support, we did not see any reason to burden the project with the compatibility\nweight.\n\n© routing-py contributors 2020 under the `Apache 2.0 License`_.\n\n.. image:: https://user-images.githubusercontent.com/10322094/57357720-e180c080-7173-11e9-97a4-cecb4670065d.jpg\n    :alt: routing-py-image\n\n\nWhy routing-py?\n---------------\n\nYou want to\n\n- get from A to B by transit, foot, bike, car or hgv\n- compute a region of reachability\n- calculate a time distance matrix for a N x M table\n\nand don\'t know which provider to use? Great. Then **routingpy** is exactly what you\'re looking for.\n\nFor the better or worse, every provider works on different spatial global datasets and uses a plethora of algorithms on top.\nWhile Google or HERE build on top of proprietary datasets, providers such as Mapbox or Graphhopper consume OpenStreetMap data\nfor their base network. Also, all providers offer a different amount of options one can use to restrict the wayfinding.\nUltimately this means that **results may differ** - and our experience tells us: they do, and not\ntoo little. This calls for a careful evaluation which service provider to use for which specific use case.\n\nWith **routingpy** we have made an attempt to simplify this process for you.\n\nInstallation\n------------\n\n.. image:: https://badge.fury.io/py/routingpy.svg\n    :target: https://badge.fury.io/py/routingpy\n    :alt: PyPI version\n\n.. image:: https://anaconda.org/nilsnolde/routingpy/badges/version.svg\n    :target: https://anaconda.org/nilsnolde/routingpy\n    :alt: Conda install\n\n**Recommended**: Install via poetry_:\n\n.. code:: bash\n\n    poetry install [--no-dev]\n\nInstall using ``pip`` with\n\n.. code:: bash\n\n   pip install routingpy\n\nOr with conda (**deprecated**)\n\n.. code:: bash\n\n   conda install -c nilsnolde routingpy\n\nOr the lastest from source\n\n.. code:: bash\n\n   pip install git+git://github.com/gis-ops/routing-py\n\n\n\nAPI\n-----------\n\nEvery provider has its own specifications and features. However the basic blueprints are the same across all. We tried hard\nto make the transition from one provider to the other as seamless as possible. We follow two dogmas for all implementations:\n\n- All basic parameters have to be the same for all routers for each endpoint\n\n- All routers still retain their special parameters for their endpoints, which make them unique in the end\n\nThis naturally means that usually those **basic parameters are not named the same way** as the endpoints they query. However,\nall **provider specific parameters are named the exact same** as their remote counterparts.\n\nThe following table gives you an overview which basic arguments are abstracted:\n\n+-----------------------+-------------------+--------------------------------------------------------------+\n|       Endpoint        |     Argument      | Function                                                     |\n+=======================+===================+==============================================================+\n|   ``directions``      | locations         | | Specify the locations to be visited in order. Usually this |\n|                       |                   | | is done with ``[Lon, Lat]`` tuples, but some routers offer |\n|                       |                   | | additional options to create a location element.           |\n|                       +-------------------+--------------------------------------------------------------+\n|                       | profile           | | The mode of transport, i.e. car, bicycle, pedestrian. Each |\n|                       |                   | | router specifies their own profiles.                       |\n+-----------------------+-------------------+--------------------------------------------------------------+\n|   ``isochrones``      | locations         | | Specify the locations to calculate isochrones for. Usually |\n|                       |                   | | this is done with ``[Lon, Lat]`` tuples, but some routers  |\n|                       |                   | | offer additional options to create a location element.     |\n|                       +-------------------+--------------------------------------------------------------+\n|                       | profile           | | The mode of transport, i.e. car, bicycle, pedestrian. Each |\n|                       |                   | | router specifies their own profiles.                       |\n|                       +-------------------+--------------------------------------------------------------+\n|                       | intervals         | | The ranges to calculate isochrones for. Either in seconds  |\n|                       |                   | | or in meters, depending on ``interval_type``.              |\n|                       +-------------------+--------------------------------------------------------------+\n|                       | intervals _type   | | The dimension of ``intervals``, which takes router         |\n|                       |                   | | dependent values, but generally describes time or distance |\n+-----------------------+-------------------+--------------------------------------------------------------+\n|      ``matrix``       | locations         | | Specify all locations you want to calculate a matrix       |\n|                       |                   | | for. If ``sources`` or ``destinations`` is not set, this   |\n|                       |                   | | will return a symmetrical matrix. Usually this is done     |\n|                       |                   | | with ``[Lon, Lat]`` tuples, but some routers offer         |\n|                       |                   | | additional options to create a location element.           |\n|                       +-------------------+--------------------------------------------------------------+\n|                       | profile           | | The mode of transport, i.e. car, bicycle, pedestrian. Each |\n|                       |                   | | router specifies their own profiles.                       |\n|                       +-------------------+--------------------------------------------------------------+\n|                       | sources           | | The indices of the ``locations`` parameter iterable to     |\n|                       |                   | | take as sources for the matrix calculation. If not         |\n|                       |                   | | specified all ``locations`` are considered to be sources.  |\n|                       +-------------------+--------------------------------------------------------------+\n|                       | sources           | | The indices of the ``locations`` parameter iterable to     |\n|                       |                   | | take as destinations for the matrix calculation. If not    |\n|                       |                   | | specified all ``locations`` are considered to be           |\n|                       |                   | | destinations.                                              |\n+-----------------------+-------------------+--------------------------------------------------------------+\n\nContributing\n------------\n\nWe :heart: contributions and realistically think that\'s the only way to support and maintain most\nrouting engines in the long run. To get you started, we created a `Contribution guideline <./CONTRIBUTING.md>`_.\n\nExamples\n--------\n\nFollow our examples to understand how simple **routingpy** is to use.\n\nOn top of the examples listed below, find interactive notebook(s) on mybinder.org_.\n\nBasic Usage\n~~~~~~~~~~~\n\nGet all attributes\n++++++++++++++++++\n\n**routingpy** is designed to take the burden off your shoulder to parse the JSON response of each provider, exposing\nthe most important information of the response as attributes of the response object. The actual JSON is always accessible via\nthe ``raw`` attribute:\n\n.. code:: python\n\n    from routingpy import MapboxValhalla\n    from pprint import pprint\n\n    # Some locations in Berlin\n    coords = [[13.413706, 52.490202], [13.421838, 52.514105],\n              [13.453649, 52.507987], [13.401947, 52.543373]]\n    client = MapboxValhalla(api_key=\'mapbox_key\')\n\n    route = client.directions(locations=coords, profile=\'pedestrian\')\n    isochrones = client.isochrones(locations=coords[0], profile=\'pedestrian\', intervals=[600, 1200])\n    matrix = client.matrix(locations=coords, profile=\'pedestrian\')\n\n    pprint((route.geometry, route.duration, route.distance, route.raw))\n    pprint((isochrones.raw, isochrones[0].geometry, isochrones[0].center, isochrones[0].interval))\n    pprint((matrix.durations, matrix.distances, matrix.raw))\n\n\nMulti Provider\n++++++++++++++\n\nEasily calculate routes, isochrones and matrices for multiple providers:\n\n.. code:: python\n\n    from routingpy import Graphhopper, ORS, MapboxOSRM\n    from shapely.geometry import Polygon\n\n    # Define the clients and their profile parameter\n    apis = (\n       (ORS(api_key=\'ors_key\'), \'cycling-regular\'),\n       (Graphhopper(api_key=\'gh_key\'), \'bike\'),\n       (MapboxOSRM(api_key=\'mapbox_key\'), \'cycling\')\n    )\n    # Some locations in Berlin\n    coords = [[13.413706, 52.490202], [13.421838, 52.514105],\n              [13.453649, 52.507987], [13.401947, 52.543373]]\n\n    for api in apis:\n        client, profile = api\n        route = client.directions(locations=coords, profile=profile)\n        print("Direction - {}:\\n\\tDuration: {}\\n\\tDistance: {}".format(client.__class__.__name__,\n                                                                       route.duration,\n                                                                       route.distance))\n        isochrones = client.isochrones(locations=coords[0], profile=profile, intervals=[600, 1200])\n        for iso in isochrones:\n            print("Isochrone {} secs - {}:\\n\\tArea: {} sqm".format(client.__class__.__name__,\n                                                                   iso.interval,\n                                                                   Polygon(iso.geometry).area))\n        matrix = client.matrix(locations=coords, profile=profile)\n        print("Matrix - {}:\\n\\tDurations: {}\\n\\tDistances: {}".format(client.__class__.__name__,\n                                                                      matrix.durations,\n                                                                      matrix.distances))\n\n\nDry run - Debug\n+++++++++++++++\n\nOften it is crucial to examine the request before it is sent. Mostly useful for debugging:\n\n.. code:: python\n\n    from routingpy import ORS\n\n    client = ORS(api_key=\'ors_key\')\n    route = client.directions(\n        locations = [[13.413706, 52.490202], [13.421838, 52.514105]],\n        profile=\'driving-hgv\',\n        dry_run=True\n    )\n\n\nAdvanced Usage\n~~~~~~~~~~~~~~\n\nLocal instance of FOSS router\n+++++++++++++++++++++++++++++\n\nAll FOSS routing engines can be run locally, such as openrouteservice, Valhalla, OSRM and GraphHopper. To be able\nto use **routingpy** with a local installation, just change the ``base_url`` of the client. This assumes that you did\nnot change the URL(s) of the exposed endpoint(s):\n\n.. code:: python\n\n    from routingpy import Valhalla\n\n    # no trailing slash, api_key is not necessary\n    client = Valhalla(base_url=\'http://localhost:8088/v1\')\n\nProxies, Rate limiters and API errors\n+++++++++++++++++++++++++++++++++++++\n\nProxies are easily set up using following ``requests`` scheme for proxying. Also, when batch requesting, **routingpy**\ncan be set up to resume its requests when the remote API rate limits (i.e. responds\nwith HTTP 429). Also, it can be set up to ignore API errors and instead print them as warnings to ``stdout``. Be careful,\nwhen ignoring ``RouterApiErrors``, those often count towards your rate limit.\n\nAll these parameters, and more, can optionally be **globally set** for all router modules or individually per instance:\n\n.. code:: python\n\n    from routingpy import Graphhopper, ORS\n    from routingpy.routers import options\n\n    request_kwargs = dict(proxies=dict(https=\'129.125.12.0\'))\n\n    client = Graphhopper(\n        api_key=\'gh_key\',\n        retry_over_query_limit=False,\n        skip_api_error=True,\n        requests_kwargs=request_kwargs\n    )\n\n    # Or alternvatively, set these options globally:\n    options.default_proxies = {\'https\': \'129.125.12.0\'}\n    options.default_retry_over_query_limit = False\n    options.default_skip_api_error = True\n\n\n.. _Mapbox, either Valhalla or OSRM: https://docs.mapbox.com/api/navigation\n.. _Openrouteservice: https://openrouteservice.org/dev/#/api-docs\n.. _Here Maps: https://developer.here.com/documentation\n.. _Google Maps: https://developers.google.com/maps/documentation\n.. _Graphhopper: https://graphhopper.com/api/1/docs\n.. _Local Valhalla: https://github.com/valhalla/valhalla-docs\n.. _Local Mapbox: https://github.com/Project-OSRM/osrm-backend/wiki\n.. _documentation: https://routingpy.readthedocs.io/en/latest\n.. _routing-py.routers: https://routingpy.readthedocs.io/en/latest/#module-routingpy.routers\n.. _Apache 2.0 License: https://github.com/gis-ops/routing-py/blob/master/LICENSE\n.. _mybinder.org: https://mybinder.org/v2/gh/gis-ops/routing-py/master?filepath=examples\n.. _poetry: https://github.com/sdispater/poetry\n',
    'author': 'Nils Nolde',
    'author_email': 'nils@gis-ops.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
