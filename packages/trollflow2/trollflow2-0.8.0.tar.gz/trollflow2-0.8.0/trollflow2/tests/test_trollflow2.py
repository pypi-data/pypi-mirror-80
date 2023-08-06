#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Pytroll developers
#
# Author(s):
#
#   Martin Raspaud <martin.raspaud@smhi.se>
#   Panu Lahtinen <pnuu+git@iki.fi>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
"""Test plugins."""

import datetime as dt
import os
import unittest
from unittest import mock

from trollflow2.tests.utils import TestCase


yaml_test1 = """
product_list:
  something: foo
  min_coverage: 5.0
  areas:
      euron1:
        areaname: euron1_in_fname
        min_coverage: 20.0
        products:
          cloud_top_height:
            productname: cloud_top_height_in_fname
            output_dir: /tmp/satdmz/pps/www/latest_2018/
            formats:
              - format: png
                writer: simple_image
              - format: jpg
                writer: simple_image
                fill_value: 0
            fname_pattern: "{platform_name:s}_{start_time:%Y%m%d_%H%M}_{areaname:s}_ctth_static.{format}"

      germ:
        areaname: germ_in_fname
        fname_pattern: "{start_time:%Y%m%d_%H%M}_{areaname:s}_{productname}.{format}"
        products:
          cloudtype:
            productname: cloudtype_in_fname
            output_dir: /tmp/satdmz/pps/www/latest_2018/
            formats:
              - format: png
                writer: simple_image

      omerc_bb:
        areaname: omerc_bb
        output_dir: /tmp
        products:
          ct:
            productname: ct
            formats:
              - format: nc
                writer: cf
          cloud_top_height:
            productname: cloud_top_height
            formats:
              - format: tif
                writer: geotiff
"""

yaml_test_publish = """
product_list:
  something: foo
  min_coverage: 5.0
  publish_topic: /raster/
  extra_metadata:
    processing_center: SMHI
  areas:
      euron1:
        areaname: euron1_in_fname
        min_coverage: 20.0
        products:
          cloud_top_height:
            productname: cloud_top_height_in_fname
            output_dir: /tmp/satdmz/pps/www/latest_2018/
            formats:
              - format: png
                writer: simple_image
                filename: /tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ctth_static.png
                dispatch:
                  - hostname: ftp.important_client.com
                    scheme: ftp
                    path: "/somewhere/{platform_name:s}_{start_time:%Y%m%d_%H%M}_{areaname:s}_ctth_static.{format}"
              - format: jpg
                writer: simple_image
                fill_value: 0
                filename: /tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ctth_static.jpg
            fname_pattern: "{platform_name:s}_{start_time:%Y%m%d_%H%M}_{areaname:s}_ctth_static.{format}"

      germ:
        areaname: germ_in_fname
        fname_pattern: "{start_time:%Y%m%d_%H%M}_{areaname:s}_{productname}.{format}"
        products:
          cloudtype:
            productname: cloudtype_in_fname
            output_dir: /tmp/satdmz/pps/www/latest_2018/
            formats:
              - format: png
                writer: simple_image
                filename: /tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_germ_in_fname_ct.png

      omerc_bb:
        areaname: omerc_bb
        output_dir: /tmp
        products:
          ct:
            productname: ct
            formats:
              - format: nc
                writer: cf
                filename: /tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_omerc_bb_in_fname_ct.png
          cloud_top_height:
            productname: cloud_top_height
            formats:
              - format: tif
                writer: geotiff
                filename: /tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_omerc_bb_in_fname_ctth.png
"""

yaml_test3 = """
product_list:
  something: foo
  min_coverage: 5.0
  areas:
      euron1:
        areaname: euron1_in_fname
        min_coverage: 20.0
        products:
          green_snow:
            productname: green_snow
            formats:
              - format: tif
                writer: geotiff
"""

yaml_test_save = """
product_list:
  output_dir: &output_dir
    /tmp/satnfs/polar_out/pps2018/direct_readout/
  publish_topic: /NWC-CF/L3
  use_extern_calib: false
  fname_pattern: &fname
    "{platform_name}_{start_time:%Y%m%d_%H%M}_{areaname}_{productname}.{format}"
  formats: &formats
    - format: tif
      writer: geotiff
    - format: nc
      writer: cf
  areas:
      euron1:
        areaname: euron1_in_fname
        min_coverage: 20.0
        products:
          cloud_top_height:
            productname: cloud_top_height_in_fname
            output_dir: /tmp/satdmz/pps/www/latest_2018/
            formats:
              - format: png
                writer: simple_image
                dispatch:
                  - hostname: ftp.important_client.com
                    scheme: ftp
                    path: "/somewhere/{platform_name:s}_{start_time:%Y%m%d_%H%M}_{areaname:s}_ctth_static.{format}"
              - format: jpg
                writer: simple_image
                fill_value: 0
            fname_pattern: "{platform_name:s}_{start_time:%Y%m%d_%H%M}_{areaname:s}_ctth_static.{format}"
          ("ct", "ctth"):
            productname: ct_and_ctth
            output_dir: /tmp/satdmz/pps/www/latest_2018/
            formats:
              - format: nc
                writer: cf

      germ:
        areaname: germ_in_fname
        use_tmp_file: True
        fname_pattern: "{start_time:%Y%m%d_%H%M}_{areaname:s}_{productname}.{format}"
        products:
          cloudtype:
            productname: cloudtype_in_fname
            output_dir: /tmp/satdmz/pps/www/latest_2018/{orig_platform_name}/
            formats:
              - format: png
                writer: simple_image

      omerc_bb:
        areaname: omerc_bb
        output_dir: /tmp
        products:
          ct:
            productname: ct
            formats:
              - format: nc
                writer: cf
          cloud_top_height:
            productname: cloud_top_height
            resolution: 500
            formats:
              - format: tif
                writer: geotiff
"""

yaml_test_null_area = """
product_list:
  areas:
      null:
        areaname: foo
        products:
          cloud_top_height:
            productname: ctth
            output_dir: /tmp/
            formats:
              - format: png
                writer: simple_image
            fname_pattern: "{platform_name:s}_{start_time:%Y%m%d_%H%M}_{areaname:s}_ctth_static.{format}"
"""

input_mda = {'orig_platform_name': 'noaa15', 'orbit_number': 7993,
             'start_time': dt.datetime(2019, 2, 17, 6, 0, 11, 100000), 'stfrac': 1,
             'end_time': dt.datetime(2019, 2, 17, 6, 15, 10, 400000), 'etfrac': 4, 'status': 'OK',
             'format': 'CF', 'data_processing_level': '2', 'orbit': 7993, 'module': 'ppsMakePhysiography',
             'platform_name': 'NOAA-15', 'pps_version': 'v2018', 'file_was_already_processed': False,
             'dataset': [{'uri': '/home/a001673/data/satellite/test_trollflow2/S_NWC_CMA_noaa15_07993_20190217T0600111Z_20190217T0615104Z.nc',  # noqa
                          'uid': 'S_NWC_CMA_noaa15_07993_20190217T0600111Z_20190217T0615104Z.nc'},
                         {'uri': '/home/a001673/data/satellite/test_trollflow2/S_NWC_CTTH_noaa15_07993_20190217T0600111Z_20190217T0615104Z.nc',  # noqa
                          'uid': 'S_NWC_CTTH_noaa15_07993_20190217T0600111Z_20190217T0615104Z.nc'},
                         {'uri': '/home/a001673/data/satellite/test_trollflow2/S_NWC_CT_noaa15_07993_20190217T0600111Z_20190217T0615104Z.nc',  # noqa
                          'uid': 'S_NWC_CT_noaa15_07993_20190217T0600111Z_20190217T0615104Z.nc'}],
             'sensor': ['avhrr']}

YAML_FILE_PUBLISHER = """
!!python/object:trollflow2.plugins.FilePublisher {port: 40002, nameservers: [localhost]}
"""


class TestSaveDatasets(TestCase):
    """Test case for saving datasets."""

    def test_prepared_filename(self):
        """Test the `prepared_filename` context."""
        from trollflow2.plugins import prepared_filename
        tst_file = 'hi.png'

        renames = {}
        fmat = {'fname_pattern': tst_file}
        with prepared_filename(fmat, renames) as filename:
            pass
        self.assertEqual(filename, tst_file)
        self.assertEqual(len(renames), 0)

        renames = {}
        fmat = {'use_tmp_file': False, 'fname_pattern': tst_file}
        with prepared_filename(fmat, renames) as filename:
            pass
        self.assertEqual(filename, tst_file)
        self.assertEqual(len(renames), 0)

        renames = {}
        fmat = {'use_tmp_file': True, 'fname_pattern': tst_file}
        with prepared_filename(fmat, renames) as filename:
            pass
        self.assertTrue(filename.startswith, 'tmp')
        self.assertEqual(len(renames), 1)
        self.assertEqual(list(renames.values())[0], tst_file)

        renames = {}
        fmat = {'use_tmp_file': True, 'fname_pattern': tst_file}
        try:
            with prepared_filename(fmat, renames) as filename:
                raise KeyError('Oh no!')
        except KeyError:
            pass
        self.assertTrue(filename.startswith, 'tmp')
        self.assertEqual(len(renames), 0)

        tst_dir = os.path.normpath('/tmp/bleh')
        renames = {}
        fmat = {'use_tmp_file': True, 'fname_pattern': tst_file, 'output_dir': tst_dir}
        with prepared_filename(fmat, renames) as filename:
            pass
        self.assertTrue(filename.startswith, 'tmp')
        self.assertEqual(len(renames), 1)
        self.assertEqual(list(renames.values())[0], os.path.join(tst_dir, tst_file))

        self.assertTrue(os.path.exists(tst_dir))
        os.rmdir(tst_dir)

    def test_prepare_filename_and_directory(self):
        """Test filename composition and directory creation."""
        from trollflow2.plugins import _prepare_filename_and_directory
        tst_file = 'goes_{name}.png'
        tst_dir = os.path.normpath('/tmp/bleh/{service}')
        fmat = {'use_tmp_file': True, 'fname_pattern': tst_file, 'output_dir': tst_dir,
                'name': 'mooh', 'service': 'cow'}
        directory, filename = _prepare_filename_and_directory(fmat)
        self.assertEqual(filename, os.path.normpath('/tmp/bleh/cow/goes_mooh.png'))
        self.assertTrue(os.path.exists(directory))
        os.rmdir(directory)

    def test_get_temp_filename(self):
        """Test temp filename generation."""
        from trollflow2.plugins import _get_temp_filename

        # Test uniqueness
        class FakeFO():
            def __init__(self, name):
                self.name = name

            def close(self):
                pass

        tst_dir = ''
        with mock.patch('trollflow2.plugins.NamedTemporaryFile') as ntf:
            ntf.side_effect = [FakeFO('cu'), FakeFO('cu'), FakeFO('mb'), FakeFO('er')]
            names = []
            for _i_ in range(3):
                names.append(_get_temp_filename(tst_dir, names))
            self.assertEqual(''.join(names), 'cumber')

    def test_save_datasets(self):
        """Test saving datasets."""
        self.maxDiff = None
        from trollflow2.launcher import yaml, UnsafeLoader
        from trollflow2.plugins import save_datasets, DEFAULT
        job = {}
        job['input_mda'] = input_mda
        job['product_list'] = {
            'product_list': yaml.load(yaml_test_save, Loader=UnsafeLoader)['product_list'],
        }
        job['resampled_scenes'] = {}
        the_queue = mock.MagicMock()
        job['produced_files'] = the_queue
        for area in job['product_list']['product_list']['areas']:
            job['resampled_scenes'][area] = mock.Mock()
        with mock.patch('trollflow2.plugins.compute_writer_results'),\
                mock.patch('trollflow2.plugins.DataQuery') as dsid,\
                mock.patch('os.rename') as rename:
            save_datasets(job)
            expected_sd = [mock.call(dsid.return_value, compute=False,
                                     filename='/tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ctth_static.png',  # noqa
                                     format='png', writer='simple_image'),
                           mock.call(dsid.return_value, compute=False,
                                     filename='/tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ctth_static.jpg',  # noqa
                                     fill_value=0, format='jpg', writer='simple_image'),
                           mock.call(dsid.return_value, compute=False,
                                     filename='/tmp/NOAA-15_20190217_0600_omerc_bb_ct.nc',
                                     format='nc', writer='cf'),
                           mock.call(dsid.return_value, compute=False,
                                     filename='/tmp/NOAA-15_20190217_0600_omerc_bb_cloud_top_height.tif',
                                     format='tif', writer='geotiff')
                           ]
            expected_sds = [mock.call(datasets=[dsid.return_value, dsid.return_value], compute=False,
                            filename='/tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ct_and_ctth.nc',  # noqa
                            writer='cf')]
            expected_dsid = [mock.call(name='cloud_top_height', resolution=DEFAULT, modifiers=DEFAULT),
                             mock.call(name='cloud_top_height', resolution=DEFAULT, modifiers=DEFAULT),
                             mock.call(name='ct', resolution=DEFAULT, modifiers=DEFAULT),
                             mock.call(name='ctth', resolution=DEFAULT, modifiers=DEFAULT),
                             mock.call(name='cloudtype', resolution=DEFAULT, modifiers=DEFAULT),
                             mock.call(name='ct', resolution=DEFAULT, modifiers=DEFAULT),
                             mock.call(name='cloud_top_height', resolution=500, modifiers=DEFAULT)
                             ]

            sd_calls = (job['resampled_scenes']['euron1'].save_dataset.mock_calls
                        + job['resampled_scenes']['omerc_bb'].save_dataset.mock_calls)
            for sd, esd in zip(sd_calls, expected_sd):
                self.assertEqual(sd, esd)
            sds_calls = job['resampled_scenes']['euron1'].save_datasets.mock_calls
            for sds, esds in zip(sds_calls, expected_sds):
                self.assertDictEqual(sds[2], esds[2])
            args, kwargs = job['resampled_scenes']['germ'].save_dataset.call_args_list[0]
            self.assertTrue(os.path.basename(kwargs['filename']).startswith('tmp'))
            for ds, eds in zip(dsid.mock_calls, expected_dsid):
                self.assertEqual(ds, eds)
            rename.assert_called_once()

        dexpected = {
            'output_dir': '/tmp/satnfs/polar_out/pps2018/direct_readout/',
            'publish_topic': '/NWC-CF/L3',
            'use_extern_calib': False,
            'fname_pattern': "{platform_name}_{start_time:%Y%m%d_%H%M}_{areaname}_{productname}.{format}",
            'formats': [{
                'format': 'tif',
                'writer': 'geotiff'
            },
            {
                'format': 'nc',
                'writer': 'cf'
            }],
            'areas': {
                'euron1': {
                    'areaname': 'euron1_in_fname',
                    'min_coverage': 20.0,
                    'products': {
                        'cloud_top_height': {
                            'fname_pattern': '{platform_name:s}_{start_time:%Y%m%d_%H%M}_{areaname:s}_ctth_static.{format}',  # noqa
                            'formats':
                            [{
                                'filename': '/tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ctth_static.png',  # noqa
                                'format': 'png',
                                'writer': 'simple_image',
                                'dispatch': [{
                                    'hostname': 'ftp.important_client.com',
                                    'scheme': 'ftp',
                                    'path': '/somewhere/{platform_name:s}_{start_time:%Y%m%d_%H%M}_{areaname:s}_ctth_static.{format}',  # noqa
                                 }],
                             },
                              {
                                 'filename':
                                 '/tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ctth_static.jpg',  # noqa
                                 'fill_value':
                                 0,
                                 'format':
                                 'jpg',
                                 'writer':
                                 'simple_image'
                             }],
                            'output_dir':
                            '/tmp/satdmz/pps/www/latest_2018/',
                            'productname':
                            'cloud_top_height_in_fname'
                        },
                        ('ct', 'ctth'): {
                            'formats':
                            [{
                                'filename': '/tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ct_and_ctth.nc',  # noqa
                                'format': 'nc',
                                'writer': 'cf'
                            }],
                            'output_dir': '/tmp/satdmz/pps/www/latest_2018/',
                            'productname': 'ct_and_ctth'
                        },
                    }
                },
                'germ': {
                    'areaname':
                    'germ_in_fname',
                    'use_tmp_file':
                    True,
                    'fname_pattern':
                    '{start_time:%Y%m%d_%H%M}_{areaname:s}_{productname}.{format}',
                    'products': {
                        'cloudtype': {
                            'formats': [{
                                'filename':
                                '/tmp/satdmz/pps/www/latest_2018/noaa15/20190217_0600_germ_in_fname_cloudtype_in_fname.png',  # noqa
                                'format':
                                'png',
                                'writer':
                                'simple_image'
                            }],
                            'output_dir':
                            '/tmp/satdmz/pps/www/latest_2018/{orig_platform_name}/',
                            'productname':
                            'cloudtype_in_fname'
                        }
                    }
                },
                'omerc_bb': {
                    'areaname': 'omerc_bb',
                    'output_dir': '/tmp',
                    'products': {
                        'cloud_top_height': {
                            'formats': [{
                                'filename':
                                '/tmp/NOAA-15_20190217_0600_omerc_bb_cloud_top_height.tif',
                                'format':
                                'tif',
                                'writer':
                                'geotiff'
                            }],
                            'productname':
                            'cloud_top_height',
                            'resolution':
                            500
                        },
                        'ct': {
                            'formats': [{
                                'filename':
                                '/tmp/NOAA-15_20190217_0600_omerc_bb_ct.nc',
                                'format':
                                'nc',
                                'writer':
                                'cf'
                            }],
                            'productname':
                            'ct'
                        }
                    }
                }
            }
        }
        self.assertDictEqual(dexpected, job['product_list']['product_list'])

        filenames = ['/tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ctth_static.png',
                     '/tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ctth_static.jpg',
                     '/tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ct_and_ctth.nc',
                     '/tmp/satdmz/pps/www/latest_2018/noaa15/20190217_0600_germ_in_fname_cloudtype_in_fname.png',
                     '/tmp/NOAA-15_20190217_0600_omerc_bb_ct.nc',
                     '/tmp/NOAA-15_20190217_0600_omerc_bb_cloud_top_height.tif']
        for fname, efname in zip(the_queue.put.mock_calls, filenames):
            self.assertEqual(fname, mock.call(efname))


class TestCreateScene(TestCase):
    """Test case for creating a scene."""

    def test_create_scene(self):
        """Test making a scene."""
        from trollflow2.plugins import create_scene
        with mock.patch("trollflow2.plugins.Scene") as scene:
            scene.return_value = "foo"
            job = {"input_filenames": "bar", "product_list": {}}
            create_scene(job)
            self.assertEqual(job["scene"], "foo")
            scene.assert_called_with(filenames='bar', reader=None,
                                     reader_kwargs=None, ppp_config_dir=None)
            job = {"input_filenames": "bar",
                   "product_list": {"product_list": {"reader": "baz"}}}
            create_scene(job)
            scene.assert_called_with(filenames='bar', reader='baz',
                                     reader_kwargs=None, ppp_config_dir=None)


class TestLoadComposites(TestCase):
    """Test case for loading composites."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        from trollflow2.launcher import yaml, UnsafeLoader
        self.product_list = yaml.load(yaml_test1, Loader=UnsafeLoader)

    def test_load_composites(self):
        """Test loading composites."""
        from trollflow2.plugins import load_composites
        scn = mock.MagicMock()
        job = {"product_list": self.product_list, "scene": scn}
        load_composites(job)
        scn.load.assert_called_with({'ct', 'cloudtype', 'cloud_top_height'}, resolution=None, generate=False)

    def test_load_composites_with_config(self):
        """Test loading composites with a config."""
        from trollflow2.plugins import load_composites
        scn = mock.MagicMock()
        self.product_list['product_list']['resolution'] = 1000
        self.product_list['product_list']['delay_composites'] = False
        job = {"product_list": self.product_list, "scene": scn}
        load_composites(job)
        scn.load.assert_called_with({'ct', 'cloudtype', 'cloud_top_height'}, resolution=1000, generate=True)

    def test_load_composites_with_different_resolutions(self):
        """Test loading composites with different resolutions."""
        from trollflow2.plugins import load_composites
        scn = mock.MagicMock()
        self.product_list['product_list']['resolution'] = 1000
        self.product_list['product_list']['areas']['euron1']['resolution'] = 500
        self.product_list['product_list']['delay_composites'] = False
        job = {"product_list": self.product_list, "scene": scn}
        load_composites(job)
        scn.load.assert_any_call({'cloudtype', 'ct', 'cloud_top_height'}, resolution=1000, generate=True)
        scn.load.assert_any_call({'cloud_top_height'}, resolution=500, generate=True)


class TestResample(TestCase):
    """Test case for resampling."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        from trollflow2.launcher import yaml, UnsafeLoader
        self.product_list = yaml.load(yaml_test1, Loader=UnsafeLoader)

    def test_resample(self):
        """Test resampling."""
        from trollflow2.plugins import resample
        scn = mock.MagicMock()
        scn.resample.return_value = "foo"
        job = {"scene": scn, "product_list": self.product_list}
        resample(job)
        self.assertTrue(mock.call('omerc_bb',
                                  radius_of_influence=None,
                                  resampler="nearest",
                                  reduce_data=True,
                                  cache_dir=None,
                                  mask_area=False,
                                  epsilon=0.0) in
                        scn.resample.mock_calls)
        self.assertTrue(mock.call('germ',
                                  radius_of_influence=None,
                                  resampler="nearest",
                                  reduce_data=True,
                                  cache_dir=None,
                                  mask_area=False,
                                  epsilon=0.0) in
                        scn.resample.mock_calls)
        self.assertTrue(mock.call('euron1',
                                  radius_of_influence=None,
                                  resampler="nearest",
                                  reduce_data=True,
                                  cache_dir=None,
                                  mask_area=False,
                                  epsilon=0.0) in
                        scn.resample.mock_calls)
        self.assertTrue("resampled_scenes" in job)
        for area in ["omerc_bb", "germ", "euron1"]:
            self.assertTrue(area in job["resampled_scenes"])
            self.assertTrue(job["resampled_scenes"][area] == "foo")

        prod_list = self.product_list.copy()
        prod_list["common"] = {"resampler": "bilinear"}
        prod_list["product_list"]['areas']["euron1"]["reduce_data"] = False
        job = {"product_list": prod_list, "scene": scn}
        resample(job)
        self.assertTrue(mock.call('euron1',
                                  radius_of_influence=None,
                                  resampler="bilinear",
                                  reduce_data=False,
                                  cache_dir=None,
                                  mask_area=False,
                                  epsilon=0.0) in
                        scn.resample.mock_calls)

    def test_resample_satproj(self):
        """Test keeping the satellite projection."""
        from trollflow2.plugins import resample
        scn = mock.MagicMock()
        scn.resample.return_value = "foo"
        job = {"scene": scn, "product_list": self.product_list.copy()}
        job['product_list']['product_list']['areas'][None] = job['product_list']['product_list']['areas']['germ']
        del job['product_list']['product_list']['areas']['germ']
        resample(job)
        self.assertTrue(mock.call('omerc_bb',
                                  radius_of_influence=None,
                                  resampler="nearest",
                                  reduce_data=True,
                                  cache_dir=None,
                                  mask_area=False,
                                  epsilon=0.0) in
                        scn.resample.mock_calls)
        self.assertTrue(mock.call('euron1',
                                  radius_of_influence=None,
                                  resampler="nearest",
                                  reduce_data=True,
                                  cache_dir=None,
                                  mask_area=False,
                                  epsilon=0.0) in
                        scn.resample.mock_calls)
        self.assertTrue(job['resampled_scenes'][None] is scn)
        self.assertTrue("resampled_scenes" in job)
        for area in ["omerc_bb", "euron1"]:
            self.assertTrue(area in job["resampled_scenes"])
            self.assertTrue(job["resampled_scenes"][area] == "foo")

    def test_minmax_area(self):
        """Test the min and max areas."""
        from trollflow2.plugins import resample
        scn = mock.MagicMock()
        scn.resample.return_value = "foo"
        product_list = self.product_list.copy()
        product_list['product_list']['areas'][None] = product_list['product_list']['areas']['germ']
        product_list['product_list']['areas'][None]['use_min_area'] = True
        del product_list['product_list']['areas']['germ']
        del product_list['product_list']['areas']['omerc_bb']
        del product_list['product_list']['areas']['euron1']
        job = {"scene": scn, "product_list": product_list.copy()}
        resample(job)
        self.assertTrue(mock.call(scn.min_area(),
                                  radius_of_influence=None,
                                  resampler="nearest",
                                  reduce_data=True,
                                  cache_dir=None,
                                  mask_area=False,
                                  epsilon=0.0) in
                        scn.resample.mock_calls)
        del product_list['product_list']['areas'][None]['use_min_area']
        product_list['product_list']['areas'][None]['use_max_area'] = True
        job = {"scene": scn, "product_list": product_list.copy()}
        resample(job)
        self.assertTrue(mock.call(scn.max_area(),
                                  radius_of_influence=None,
                                  resampler="nearest",
                                  reduce_data=True,
                                  cache_dir=None,
                                  mask_area=False,
                                  epsilon=0.0) in
                        scn.resample.mock_calls)


class TestResampleNullArea(TestCase):
    """Test case for resampling."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        from trollflow2.launcher import yaml, UnsafeLoader
        self.product_list = yaml.load(yaml_test_null_area, Loader=UnsafeLoader)

    def test_resample_null_area(self):
        """Test handling a `None` area in resampling."""
        from trollflow2.plugins import resample
        scn = mock.MagicMock()
        product_list = self.product_list.copy()
        job = {"scene": scn, "product_list": product_list.copy()}
        # The composites have been generated
        scn.keys.return_value = ['abc']
        scn.wishlist = {'abc'}
        resample(job)
        scn.load.assert_not_called()
        # The composites have not been generated
        scn.keys.return_value = ['a', 'b', 'c']
        scn.wishlist = {'abc'}
        resample(job)
        self.assertTrue(mock.call({'abc'}, generate=True) in
                        scn.load.mock_calls)

    def test_resample_native_null_area(self):
        """Test using `native` resampler with `None` area."""
        from trollflow2.plugins import resample
        scn = mock.MagicMock()
        product_list = self.product_list.copy()
        product_list["common"] = {"resampler": "native"}
        job = {"scene": scn, "product_list": product_list.copy()}
        # The composites have been generated
        scn.keys.return_value = ['abc']
        scn.wishlist = {'abc'}
        resample(job)
        self.assertTrue(mock.call(resampler='native') in
                        scn.resample.mock_calls)


class TestSunlightCovers(TestCase):
    """Test the sunlight coverage."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        from trollflow2.launcher import yaml, UnsafeLoader
        self.product_list = yaml.load(yaml_test1, Loader=UnsafeLoader)
        self.input_mda = {"platform_name": "NOAA-15",
                          "sensor": "avhrr-3",
                          "start_time": dt.datetime(2019, 4, 7, 20, 52),
                          "end_time": dt.datetime(2019, 4, 7, 20, 58),
                          }

    def test_coverage(self):
        """Test sunlight coverage."""
        from trollflow2.plugins import _get_sunlight_coverage
        import numpy as np
        with mock.patch('trollflow2.plugins.AreaDefBoundary') as area_def_boundary, \
                mock.patch('trollflow2.plugins.Boundary') as boundary, \
                mock.patch('trollflow2.plugins.get_twilight_poly'), \
                mock.patch('trollflow2.plugins.get_area_def'), \
                mock.patch('trollflow2.plugins.get_geostationary_bounding_box'):

            area_def_boundary.return_value.contour_poly.intersection.return_value.area.return_value = 0.02
            boundary.return_value.contour_poly.intersection.return_value.area.return_value = 0.02
            area_def_boundary.return_value.contour_poly.area.return_value = 0.2
            start_time = dt.datetime(2019, 4, 7, 20, 8)
            adef = mock.MagicMock(proj_dict={'proj': 'stere'})
            res = _get_sunlight_coverage(adef, start_time)
            np.testing.assert_allclose(res, 0.1)
            boundary.assert_not_called()
            adef = mock.MagicMock(proj_dict={'proj': 'geos'})
            res = _get_sunlight_coverage(adef, start_time)
            boundary.assert_called()


class TestGetProductAreaDef(TestCase):
    """Test case for finding area definition for a product."""

    def test_get_product_area_def(self):
        """Test _get_product_area_def()."""
        from trollflow2.plugins import _get_product_area_def
        # scn = mock.MagicMock()
        # scn.__getitem__.side_effect = KeyError

        # No area nor product
        scn = dict([])
        job = {'scene': scn}
        area = 'area'
        product = 'product'
        res = _get_product_area_def(job, area, product)
        self.assertIsNone(res)

        # Area not in the scene, take area def from the available first dataset
        adef = mock.MagicMock()
        prod = mock.MagicMock()
        prod.attrs.__getitem__.return_value = adef
        scn['1'] = prod
        job = {'scene': scn}
        res = _get_product_area_def(job, area, product)
        self.assertTrue(res is adef)
        prod.attrs.__getitem__.assert_called_once()

        # Area from the un-resampled scene
        adef = mock.MagicMock()
        prod = mock.MagicMock()
        prod.attrs.__getitem__.return_value = adef
        prod2 = mock.MagicMock()
        prod2.attrs.__getitem__.return_value = None
        scn = {area: prod, '1': prod2}
        job = {'scene': scn}
        res = _get_product_area_def(job, area, product)
        self.assertTrue(res is adef)
        prod.attrs.__getitem__.assert_called_once()
        prod2.attrs.__getitem__.assert_not_called()
        # Product is a tuple
        res = _get_product_area_def(job, area, (product, 'foo'))
        self.assertTrue(res is adef)

        # Area from a resampled scene
        adef = mock.MagicMock()
        prod = mock.MagicMock()
        prod.attrs.__getitem__.return_value = adef
        prod2 = mock.MagicMock()
        prod2.attrs.__getitem__.return_value = None
        scn = {area: prod, '1': prod2}
        job = {'resampled_scenes': {area: scn}}
        res = _get_product_area_def(job, area, product)
        self.assertTrue(res is adef)
        prod.attrs.__getitem__.assert_called_once()
        prod2.attrs.__getitem__.assert_not_called()
        # Product is a tuple
        res = _get_product_area_def(job, area, (product, 'foo'))
        self.assertTrue(res is adef)


class TestCheckSunlightCoverage(TestCase):
    """Test case for sunlight coverage."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        from trollflow2.launcher import yaml, UnsafeLoader
        self.product_list = yaml.load(yaml_test3, Loader=UnsafeLoader)
        self.input_mda = {"platform_name": "NOAA-15",
                          "sensor": "avhrr-3",
                          "start_time": dt.datetime(2019, 1, 19, 11),
                          "end_time": dt.datetime(2019, 1, 19, 12),
                          'not_changed': True,
                          }

    def test_product_not_loaded(self):
        """Test that product isn't loaded when sunlight coverage is to low."""
        from trollflow2.plugins import check_sunlight_coverage
        from trollflow2.plugins import metadata_alias
        with mock.patch('trollflow2.plugins.Pass') as ts_pass,\
                mock.patch('trollflow2.plugins.get_twilight_poly'),\
                mock.patch("trollflow2.plugins._get_sunlight_coverage") as _get_sunlight_coverage:
            job = {}
            scene = mock.MagicMock()
            scene.attrs = {'start_time': 42}
            job['scene'] = scene
            job['product_list'] = self.product_list.copy()
            job['input_mda'] = self.input_mda.copy()
            metadata_alias(job)

            job['resampled_scenes'] = {}
            for area in job['product_list']['product_list']['areas']:
                job['resampled_scenes'][area] = {}
            # Run without any settings
            check_sunlight_coverage(job)

            _get_sunlight_coverage.assert_not_called()
            ts_pass.assert_not_called()

    def test_sunlight_filter(self):
        """Test that product isn't loaded when sunlight coverage is to low."""
        from trollflow2.plugins import check_sunlight_coverage
        from trollflow2.plugins import metadata_alias
        with mock.patch('trollflow2.plugins.Pass'),\
                mock.patch('trollflow2.plugins.get_twilight_poly'),\
                mock.patch("trollflow2.plugins._get_sunlight_coverage") as _get_sunlight_coverage:
            job = {}
            scene = mock.MagicMock()
            scene.attrs = {'start_time': 42}
            job['scene'] = scene
            job['product_list'] = self.product_list.copy()
            job['input_mda'] = self.input_mda.copy()
            metadata_alias(job)

            job['resampled_scenes'] = {}
            for area in job['product_list']['product_list']['areas']:
                job['resampled_scenes'][area] = {}
            job['product_list']['product_list']['sunlight_coverage'] = {'min': 10, 'max': 40}
            green_snow = mock.MagicMock()
            green_snow.name = 'Green Snow Mock'
            job['resampled_scenes']['euron1']['green_snow'] = green_snow
            green_snow.attrs.__getitem__.return_value = 'euron1'
            # Run without any settings
            _get_sunlight_coverage.return_value = .3
            check_sunlight_coverage(job)

            pl_green = job['product_list']['product_list']['areas']['euron1']['products']['green_snow']

            _get_sunlight_coverage.assert_called_once()
            self.assertIn('green_snow', job['product_list']['product_list']['areas']['euron1']['products'])

            _get_sunlight_coverage.return_value = 0
            check_sunlight_coverage(job)
            self.assertNotIn('green_snow', job['product_list']['product_list']['areas']['euron1']['products'])

            job['product_list']['product_list']['areas']['euron1']['products']['green_snow'] = pl_green
            _get_sunlight_coverage.return_value = 1
            check_sunlight_coverage(job)
            self.assertNotIn('green_snow', job['product_list']['product_list']['areas']['euron1']['products'])


class TestCovers(TestCase):
    """Test case for coverage checks."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        from trollflow2.launcher import yaml, UnsafeLoader
        self.product_list = yaml.load(yaml_test1, Loader=UnsafeLoader)
        self.input_mda = {"platform_name": "NOAA-15",
                          "sensor": "avhrr-3",
                          "start_time": dt.datetime(2019, 1, 19, 11),
                          "end_time": dt.datetime(2019, 1, 19, 12),
                          }

    @mock.patch('trollflow2.plugins.Pass', new=None)
    def test_covers_no_trollsched(self):
        """Test coverage when pytroll schedule is missing."""
        from trollflow2.plugins import covers
        job_orig = {"foo": "bar"}
        job = job_orig.copy()
        covers(job)
        self.assertEqual(job, job_orig)

    def test_covers(self):
        """Test coverage."""
        from trollflow2.plugins import covers
        with mock.patch('trollflow2.plugins.get_scene_coverage') as get_scene_coverage,\
                mock.patch('trollflow2.plugins.Pass'):
            get_scene_coverage.return_value = 10.0
            scn = mock.MagicMock()
            scn.attrs = {}
            job = {"product_list": self.product_list,
                   "input_mda": self.input_mda,
                   "scene": scn}
            covers(job)
            # Area "euron1" should be removed
            self.assertFalse("euron1" in job['product_list']['product_list']['areas'])
            # Other areas should stay in the list
            self.assertTrue("germ" in job['product_list']['product_list']['areas'])
            self.assertTrue("omerc_bb" in job['product_list']['product_list']['areas'])

            # Test that only one sensor is used
            input_mda = self.input_mda.copy()
            input_mda['sensor'] = {'avhrr-4'}
            job = {"product_list": self.product_list,
                   "input_mda": input_mda,
                   "scene": scn}
            get_scene_coverage.reset_mock()
            covers(job)
            get_scene_coverage.assert_called_with(input_mda['platform_name'],
                                                  input_mda['start_time'],
                                                  input_mda['end_time'],
                                                  'avhrr-4', 'omerc_bb')

    def test_scene_coverage(self):
        """Test scene coverage."""
        from trollflow2.plugins import get_scene_coverage
        with mock.patch('trollflow2.plugins.get_area_def') as get_area_def,\
                mock.patch('trollflow2.plugins.Pass') as ts_pass:
            area_coverage = mock.MagicMock()
            area_coverage.return_value = 0.2
            overpass = mock.MagicMock()
            overpass.area_coverage = area_coverage
            ts_pass.return_value = overpass
            get_area_def.return_value = 6
            res = get_scene_coverage(1, 2, 3, 4, 5)
            self.assertEqual(res, 100 * 0.2)
            ts_pass.assert_called_with(1, 2, 3, instrument=4)
            get_area_def.assert_called_with(5)
            area_coverage.assert_called_with(6)

    def test_covers_collection_area_id(self):
        """Test the coverage of a collection area id."""
        from trollflow2.plugins import covers
        from trollflow2.plugins import AbortProcessing
        with mock.patch('trollflow2.plugins.get_scene_coverage') as get_scene_coverage,\
                mock.patch('trollflow2.plugins.Pass'):
            get_scene_coverage.return_value = 100.0
            scn = mock.MagicMock()
            scn.attrs = {}
            job = {"product_list": self.product_list,
                   "input_mda": self.input_mda,
                   "scene": scn}
            # Nothing should happen here
            covers(job)
            # Area that matches the product list, nothing should happen
            job['input_mda']['collection_area_id'] = 'euron1'
            covers(job)
            # By default collection_area_id isn't checked so nothing should happen
            job['input_mda']['collection_area_id'] = 'not_in_pl'
            covers(job)
            # Turn coverage check on, so area not in the product list
            # should raise AbortProcessing
            job['product_list']['product_list']['coverage_by_collection_area'] = True
            with self.assertRaises(AbortProcessing):
                covers(job)

            # And with existing area there shouldn't be an exception
            job['input_mda']['collection_area_id'] = 'euron1'
            covers(job)


class TestCheckMetadata(TestCase):
    """Test case for checking the input metadata."""

    def test_single_item(self):
        """Test checking a single metadata item."""
        from trollflow2.plugins import check_metadata
        from trollflow2.plugins import AbortProcessing
        with mock.patch('trollflow2.plugins.get_config_value') as get_config_value:
            get_config_value.return_value = None
            job = {'product_list': None, 'input_mda': {'sensor': 'foo'}}
            self.assertIsNone(check_metadata(job))
            get_config_value.return_value = {'sensor': ['foo', 'bar']}
            self.assertIsNone(check_metadata(job))
            get_config_value.return_value = {'sensor': ['bar']}
            with self.assertRaises(AbortProcessing):
                check_metadata(job)

    def test_multiple_items(self):
        """Test checking a single metadata item."""
        from trollflow2.plugins import check_metadata
        from trollflow2.plugins import AbortProcessing
        with mock.patch('trollflow2.plugins.get_config_value') as get_config_value:
            # Nothing configured
            get_config_value.return_value = None
            job = {'product_list': None,
                   'input_mda': {'sensor': 'foo',
                                 'platform_name': 'bar'}}
            self.assertIsNone(check_metadata(job))
            # Both sensor and platform name match
            get_config_value.return_value = {'sensor': ['foo', 'bar'],
                                             'platform_name': ['bar']}
            self.assertIsNone(check_metadata(job))
            # Sensor matches, 'variant' not in the message
            get_config_value.return_value = {'sensor': ['foo', 'bar'],
                                             'variant': ['e ascari']}
            self.assertIsNone(check_metadata(job))
            # Platform doesn't match -> abort
            get_config_value.return_value = {'sensor': ['foo'],
                                             'platform_name': ['not-bar']}
            with self.assertRaises(AbortProcessing):
                check_metadata(job)


class TestMetadataAlias(TestCase):
    """Test case for metadata alias."""

    def test_metadata_alias(self):
        """Test metadata aliasing."""
        from trollflow2.plugins import metadata_alias
        mda = {'platform_name': 'noaa15', 'not_changed': True}
        product_list = {'common': {'not_metadata_aliases': True}}
        job = {'input_mda': mda, 'product_list': product_list}
        metadata_alias(job)
        mda = job['input_mda']
        self.assertEqual(mda['platform_name'], 'noaa15')
        self.assertTrue(mda['not_changed'])
        product_list = {'common': {'metadata_aliases':
                                   {'platform_name': {'noaa15': 'NOAA-15'},
                                    'not_in_mda': {'something': 'other'}}}}
        job = {'input_mda': mda, 'product_list': product_list}
        metadata_alias(job)
        mda = job['input_mda']
        self.assertEqual(mda['platform_name'], 'NOAA-15')
        self.assertTrue(mda['not_changed'])
        self.assertTrue('not_in_mda' not in mda)

    def test_iterable_metadata(self):
        """Test that iterable metadata gets replaced."""
        from trollflow2.plugins import metadata_alias
        mda = {'sensor': ('a/b',), 'foo': set(['c/d'])}
        product_list = {'common': {'metadata_aliases':
                                   {'sensor': {'a/b': 'a-b'},
                                    'foo': {'c/d': 'c-d'}}}}
        job = {'input_mda': mda, 'product_list': product_list}
        metadata_alias(job)
        self.assertEqual(job['input_mda']['sensor'], ('a-b',))
        self.assertEqual(job['input_mda']['foo'], set(['c-d']))


class TestGetPluginConf(TestCase):
    """Test case for get_plugin_conf."""

    def test_get_plugin_conf(self):
        """Test the get_plugin_conf function."""
        from trollflow2.plugins import _get_plugin_conf
        conf = {"common": {"val1": "foo1"},
                "product_list": {"val2": "bar2"}}
        path = "/product_list"
        defaults = {"val1": "foo0", "val2": "bar0", "val3": "baz0"}
        res = _get_plugin_conf(conf, path, defaults)
        self.assertTrue("val1" in res)
        self.assertTrue("val2" in res)
        self.assertTrue("val3" in res)
        self.assertEqual(res["val1"], "foo1")
        self.assertEqual(res["val2"], "bar2")
        self.assertEqual(res["val3"], "baz0")


class TestSZACheck(TestCase):
    """Test case for SZA check."""

    def test_sza_check(self):
        """Test the SZA check."""
        from trollflow2.plugins import sza_check
        with mock.patch("trollflow2.plugins.sun_zenith_angle") as sun_zenith_angle:
            job = {}
            scene = mock.MagicMock()
            scene.attrs = {'start_time': 42}
            job['scene'] = scene
            from trollflow2.launcher import yaml, UnsafeLoader
            product_list = yaml.load(yaml_test1, Loader=UnsafeLoader)
            job['product_list'] = product_list.copy()
            # Run without any settings
            sza_check(job)
            sun_zenith_angle.assert_not_called()

            # Add SZA limits to couple of products
            # Day product
            product_list['product_list']['areas']['omerc_bb']['products']['ct']['sunzen_maximum_angle'] = 95.
            product_list['product_list']['areas']['omerc_bb']['products']['ct']['sunzen_check_lon'] = 25.
            product_list['product_list']['areas']['omerc_bb']['products']['ct']['sunzen_check_lat'] = 60.
            # Night product
            product_list['product_list']['areas']['germ']['products']['cloudtype']['sunzen_minimum_angle'] = 85.
            product_list['product_list']['areas']['germ']['products']['cloudtype']['sunzen_check_lon'] = 25.
            product_list['product_list']['areas']['germ']['products']['cloudtype']['sunzen_check_lat'] = 60.

            # Zenith angle that removes nothing
            sun_zenith_angle.return_value = 90.
            sza_check(job)
            sun_zenith_angle.assert_called_with(42, 25., 60.)
            self.assertDictEqual(job['product_list'], product_list)

            # Zenith angle that removes day products
            sun_zenith_angle.return_value = 100.
            sza_check(job)
            self.assertTrue('cloud_top_height' in product_list['product_list']['areas']['omerc_bb']['products'])
            self.assertFalse('ct' in product_list['product_list']['areas']['omerc_bb']['products'])

            # Zenith angle that removes night products
            sun_zenith_angle.return_value = 45.
            sza_check(job)
            # There was only one product, so the whole area is deleted
            self.assertFalse('germ' in job['product_list']['product_list']['areas'])


class TestOverviews(TestCase):
    """Test case for overviews."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        from trollflow2.launcher import yaml, BaseLoader
        self.product_list = yaml.load(yaml_test1, Loader=BaseLoader)

    def test_add_overviews(self):
        """Test adding overviews."""
        from trollflow2.plugins import add_overviews
        with mock.patch('trollflow2.plugins.Resampling') as resampling,\
                mock.patch('trollflow2.plugins.rasterio') as rasterio:
            # Mock the rasterio.open context manager
            dst = mock.MagicMock()
            rasterio.open.return_value.__enter__.return_value = dst

            product_list = self.product_list['product_list']['areas']
            product_list['germ']['products']['cloudtype']['formats'][0]['overviews'] = [4]
            # Add filename, otherwise added by `save_datasets()`
            product_list['germ']['products']['cloudtype']['formats'][0]['filename'] = 'foo'
            job = {"product_list": self.product_list}
            add_overviews(job)
            dst.build_overviews.assert_called_once_with([4], resampling.average)
            dst.update_tags.assert_called_once_with(ns='rio_overview',
                                                    resampling='average')


class TestFilePublisher(TestCase):
    """Test case for File publisher."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        from trollflow2.launcher import yaml, UnsafeLoader
        self.product_list = yaml.load(yaml_test_publish, Loader=UnsafeLoader)
        # Skip omerc_bb area, there's no fname_pattern
        del self.product_list['product_list']['areas']['omerc_bb']
        self.input_mda = input_mda.copy()
        self.input_mda['uri'] = 'foo.nc'

    def test_filepublisher_with_compose(self):
        """Test filepublisher with compose."""
        from trollflow2.plugins import FilePublisher
        from trollflow2.dict_tools import plist_iter
        from trollsift import compose
        import os.path
        with mock.patch('trollflow2.plugins.Message') as message, mock.patch('trollflow2.plugins.NoisyPublisher'):
            pub = FilePublisher()
            pub.pub.start.assert_called_once()
            product_list = self.product_list.copy()
            product_list['product_list']['publish_topic'] = '/{areaname}/{productname}'
            job = {'product_list': product_list,
                   'input_mda': self.input_mda}
            topic_pattern = job['product_list']['product_list']['publish_topic']
            topics = []
            # Create filenames and topics
            for fmat, fmat_config in plist_iter(job['product_list']['product_list'],
                                                job['input_mda'].copy()):
                fname_pattern = fmat['fname_pattern']
                filename = compose(os.path.join(fmat['output_dir'],
                                                fname_pattern), fmat)
                fmat.pop('format', None)
                fmat_config['filename'] = filename
                topics.append(compose(topic_pattern, fmat))

            pub(job)
            message.assert_called()
            pub.pub.send.assert_called()
            pub.__del__()
            pub.pub.stop.assert_called()
            i = 0
            for area in job['product_list']['product_list']['areas']:
                for _prod in job['product_list']['product_list']['areas'][area]:
                    # Skip calls to __str__
                    if 'call().__str__()' != str(message.mock_calls[i]):
                        self.assertTrue(topics[i] in str(message.mock_calls[i]))
                        i += 1
            self.assertEqual(message.call_args[0][2]['processing_center'], 'SMHI')

    def test_filepublisher_without_compose(self):
        """Test filepublisher without compose."""
        from trollflow2.plugins import FilePublisher
        from trollflow2.dict_tools import plist_iter
        from trollsift import compose
        import os.path
        with mock.patch('trollflow2.plugins.Message') as message, mock.patch('trollflow2.plugins.NoisyPublisher'):
            pub = FilePublisher()
            pub.pub.start.assert_called_once()
            product_list = self.product_list.copy()
            product_list['product_list']['publish_topic'] = '/static_topic'
            job = {'product_list': product_list,
                   'input_mda': self.input_mda}
            topic_pattern = job['product_list']['product_list']['publish_topic']
            topics = []
            # Create filenames and topics
            for fmat, fmat_config in plist_iter(job['product_list']['product_list'],
                                                job['input_mda'].copy()):
                fname_pattern = fmat['fname_pattern']
                filename = compose(os.path.join(fmat['output_dir'],
                                                fname_pattern), fmat)
                fmat.pop('format', None)
                fmat_config['filename'] = filename
                topics.append(compose(topic_pattern, fmat))

            pub(job)
            message.assert_called()
            pub.pub.send.assert_called()
            pub.__del__()
            pub.pub.stop.assert_called()
            i = 0
            for area in job['product_list']['product_list']['areas']:
                for _prod in job['product_list']['product_list']['areas'][area]:
                    # Skip calls to __str__
                    if 'call().__str__()' != str(message.mock_calls[i]):
                        self.assertTrue(topics[i] in str(message.mock_calls[i]))
                        i += 1

    def test_filepublisher_kwargs(self):
        """Test filepublisher keyword argument usage."""
        import yaml
        from trollflow2.plugins import FilePublisher

        # Direct instantiation
        with mock.patch('trollflow2.plugins.Message'), mock.patch('trollflow2.plugins.NoisyPublisher') as nb_:
            pub = FilePublisher()
            pub.pub.start.assert_called_once()
            assert mock.call('l2processor', port=0, nameservers=None) in nb_.mock_calls
            assert pub.port == 0
            assert pub.nameservers is None
            pub = FilePublisher(port=40000, nameservers=['localhost'])
            assert mock.call('l2processor', port=40000,
                             nameservers=['localhost']) in nb_.mock_calls
            assert pub.port == 40000
            assert pub.nameservers == ['localhost']
            assert len(pub.pub.start.mock_calls) == 2

        # Instantiate via loading YAML
        with mock.patch('trollflow2.plugins.Message'), mock.patch('trollflow2.plugins.NoisyPublisher') as nb_:

            fpub = yaml.load(YAML_FILE_PUBLISHER, Loader=yaml.UnsafeLoader)
            assert mock.call('l2processor', port=40002,
                             nameservers=['localhost']) in nb_.mock_calls
            fpub.pub.start.assert_called_once()
            assert fpub.port == 40002
            assert fpub.nameservers == ['localhost']

    def test_dispatch(self):
        """Test dispatch order messages."""
        from trollflow2.plugins import FilePublisher
        with mock.patch('trollflow2.plugins.Message') as message, mock.patch('trollflow2.plugins.NoisyPublisher'):
            pub = FilePublisher()
            job = {'product_list': self.product_list,
                   'input_mda': self.input_mda}
            pub(job)
            dispatches = 0
            for args, _kwargs in message.call_args_list:
                mda = args[2]
                if args[1] == 'file':
                    self.assertIn('uri', mda)
                    self.assertIn('uid', mda)
                elif args[1] == 'dispatch':
                    self.assertIn('source', mda)
                    self.assertIn('target', mda)
                    self.assertIn('file_mda', mda)
                    self.assertEqual(mda['source'],
                                     '/tmp/satdmz/pps/www/latest_2018/NOAA-15_20190217_0600_euron1_in_fname_ctth_static.png')  # noqa
                    self.assertEqual(mda['target'],
                                     'ftp://ftp.important_client.com/somewhere/NOAA-15_20190217_0600_euron1_in_fname_ctth_static.png')  # noqa
                    dispatches += 1
            self.assertEqual(dispatches, 1)

    def test_deleting(self):
        """Test deleting the publisher."""
        from trollflow2.plugins import FilePublisher
        nb_ = mock.MagicMock()
        with mock.patch('trollflow2.plugins.Message'), mock.patch('trollflow2.plugins.NoisyPublisher') as nb:
            nb.return_value = nb_
            pub = FilePublisher()
            job = {'product_list': self.product_list,
                   'input_mda': self.input_mda}
            pub(job)

        nb_.stop.assert_not_called()
        del pub
        nb_.stop.assert_called_once()

    def test_stopping(self):
        """Test stopping the publisher."""
        from trollflow2.plugins import FilePublisher
        nb_ = mock.MagicMock()
        with mock.patch('trollflow2.plugins.Message'), mock.patch('trollflow2.plugins.NoisyPublisher') as nb:
            nb.return_value = nb_
            pub = FilePublisher()
            job = {'product_list': self.product_list,
                   'input_mda': self.input_mda}
            pub(job)

        nb_.stop.assert_not_called()
        pub.stop()
        nb_.stop.assert_called_once()


if __name__ == '__main__':
    unittest.main()
