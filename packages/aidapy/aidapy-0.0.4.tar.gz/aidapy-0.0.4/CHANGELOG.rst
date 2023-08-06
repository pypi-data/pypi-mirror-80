.. _changes:


AIDApy 0.0.4 (2020-09-23)
===========================

Second release of *aidapy*.

Features
----------
- New reference frame for VDF: another B-field aligned reference frame, with the bulk of the ion flow equal to zero, and with the electron bulk velocity into the (v_x, v_z)-plane. Called by the keyword 'B_electron'
- New plots for VDF: xy_plane(): cut in (v_perp_1, v_perp_2) plane, original VDF, scaled and normalised.
- New plot method spher_gyro(): a more comprehensive plot to look at the average (v_para, v_perp)-plane, as well as a cut through the (v_perp, v_perp)-plane, and four sectors of (v_para, v_perp) to diagnose gyrotropy.


Enhancements
--------------
- Add the correction version in aidapy/__init__.py
- Add electron heat flux (e_heatq) to MMS mission
- Change defaults probes for MMS and cluster to '1'
- Change 'data_settings' key in get_mision_info into 'product_catalog'
- Increase the test covering for xevents and statistics
- Vectorize threshold in aidapy.aidaxr.xevents
- Add tests for event_search
- Add tests for l3 MMS products: e_beta, i_beta, and j_curl
- Add tests for vdf_utils
- Change name in get_mission_info from 'data_settings' to 'product_catalog'

Documentation
----------------------
- New docstrings in aidaxr.vdf
- Improve docstrings in aidafunc.load_data

Bug fixes
----------
- Fix spacecraft position problem with duplicated index (see issue #49)
- Correct argument bug in aidaxr.vdf


AIDApy 0.0.3 (2020-09-22)
===========================

No version 0.0.3


AIDApy 0.0.2 (2020-06-24)
===========================

This is the first release of *aidapy*.


Features
----------

- ``aidapy.data.mission``: wrap *heliopy* to provide data from
  3 different missions (OMNI, cluster, and MMS) in *xarray* format
  with high-level products.
- ``aidapy.aidaxr``: provides extensions to `xarray.DataSet` and
  `xarrayDataArray`.
  Statistical methods are computed on the xarray data. Visualization and
  computations are provided for velocity distribution functions.
  Specific methods for observations are also added,
  such as curlometer or plasma beta. Extreme events methods are also provided.
- ``aidapy.ml``: basic classes providing multi layer perceptrons
  and GMM for particle
  distribution analysis.
- ``aidapy.tools``: various scripts to support velocity distribution plots
  and MMS analysis.
- ``aidapy.aidafunc``: high-levels methods helping the users to retrieve
  observational data, to perform search of specific events, and
  to set specific configuration for heliopy and ESA cookie.

Enhancements
--------------

- Creation of the CHANGELOG, LICENSE, MANIFEST, README, STYLEGUIDE,
  requirements.txt.
- Add setup.py with full information and a installation guide
- *heliopy_multid* is now a dependency


Documentation
----------------------

- Creation of the documentation generated with sphinx.
- Upload on readthedocs.
- Link with the jupyter notebooks.

Bug fixes
----------
