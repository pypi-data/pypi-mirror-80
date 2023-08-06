# Copyright 2020-present Tae Hwan Jung
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import unittest
import numpy as np
from tqdm import tqdm
import tensorflow as tf

from tests.test_data import DataTest

from matorage.data.config import DataConfig
from matorage.data.saver import DataSaver
from matorage.data.attribute import DataAttribute
from matorage.testing_utils import require_tf


@require_tf
class TFDataTest(DataTest, unittest.TestCase):
    def test_tf_saver(self, data_config=None, save_to_json_file=False):
        if data_config is None:
            self.data_config = DataConfig(
                **self.storage_config,
                dataset_name="test_tf_saver",
                additional={"framework": "tensorflow"},
                attributes=[
                    DataAttribute("image", "uint8", (2, 2), itemsize=32),
                    DataAttribute("target", "uint8", (1), itemsize=32),
                ]
            )
        else:
            self.data_config = data_config

        if save_to_json_file:
            self.data_config_file = "data_config_file.json"
            self.data_config.to_json_file(self.data_config_file)

        self.data_saver = DataSaver(config=self.data_config)

        self.data_saver(
            {
                "image": np.asarray([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
                "target": np.asarray([0, 1]),
            }
        )
        self.data_saver.disconnect()

    def test_tf_loader(self):
        from matorage.tensorflow import Dataset

        self.test_tf_saver()

        self.dataset = Dataset(config=self.data_config, cache_folder_path=self.cache_folder_path)

        for batch_idx, (image, target) in enumerate(
            tqdm(self.dataset.dataloader, total=2)
        ):
            pass

    def test_tf_loader_with_compressor(self):
        from matorage.tensorflow import Dataset

        data_config = DataConfig(
            **self.storage_config,
            dataset_name="test_tf_loader_with_compressor",
            additional={"framework": "tensorflow"},
            compressor={"complevel": 4, "complib": "zlib"},
            attributes=[
                DataAttribute("image", "uint8", (2, 2), itemsize=32),
                DataAttribute("target", "uint8", (1), itemsize=32),
            ]
        )

        self.test_tf_saver(data_config=data_config)

        self.dataset = Dataset(config=data_config, cache_folder_path=self.cache_folder_path)

        for batch_idx, (image, target) in enumerate(
            tqdm(self.dataset.dataloader, total=2)
        ):
            pass

    def test_tf_index(self):
        from matorage.tensorflow import Dataset

        self.test_tf_loader()

        dataset = Dataset(config=self.data_config, index=True, cache_folder_path=self.cache_folder_path)

        assert tf.reduce_all(
            tf.equal(dataset[0][0], tf.constant([[1, 2], [3, 4]], dtype=tf.uint8))
        )
        assert tf.reduce_all(tf.equal(dataset[0][1], tf.constant([0], dtype=tf.uint8)))

    def test_tf_index_with_compressor(self):
        from matorage.tensorflow import Dataset

        data_config = DataConfig(
            **self.storage_config,
            dataset_name="test_tf_index_with_compressor",
            additional={"framework": "tensorflow"},
            compressor={"complevel": 4, "complib": "zlib"},
            attributes=[
                DataAttribute("image", "uint8", (2, 2), itemsize=32),
                DataAttribute("target", "uint8", (1), itemsize=32),
            ]
        )

        self.test_tf_saver(data_config=data_config)

        dataset = Dataset(config=self.data_config, index=True, cache_folder_path=self.cache_folder_path)

        assert tf.reduce_all(
            tf.equal(dataset[0][0], tf.constant([[1, 2], [3, 4]], dtype=tf.uint8))
        )
        assert tf.reduce_all(tf.equal(dataset[0][1], tf.constant([0], dtype=tf.uint8)))

    def test_saver_from_json_file(self):

        self.test_tf_saver(save_to_json_file=True)

        self.data_config = None
        self.data_saver = None

        self.data_config = DataConfig.from_json_file(self.data_config_file)

        self.data_saver = DataSaver(config=self.data_config)

        self.data_saver(
            {
                "image": np.asarray([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
                "target": np.asarray([0, 1]),
            }
        )
        self.data_saver.disconnect()

    def test_loader_from_json_file(self):
        from matorage.tensorflow import Dataset

        self.test_tf_saver(save_to_json_file=True)

        self.data_config = None

        self.data_config = DataConfig.from_json_file(self.data_config_file)

        self.dataset = Dataset(config=self.data_config, cache_folder_path=self.cache_folder_path)

        for batch_idx, (image, target) in enumerate(
            tqdm(self.dataset.dataloader, total=2)
        ):
            pass

    def test_tf_not_clear(self):
        from matorage.tensorflow import Dataset

        self.test_tf_loader()

        if os.path.exists(self.dataset.cache_path):
            with open(self.dataset.cache_path) as f:
                _pre_file_mapper = json.load(f)

        self.dataset = Dataset(config=self.data_config, clear=False, cache_folder_path=self.cache_folder_path)

        if os.path.exists(self.dataset.cache_path):
            with open(self.dataset.cache_path) as f:
                _next_file_mapper = json.load(f)

        self.assertEqual(_pre_file_mapper, _next_file_mapper)

    def test_datasaver_filetype(self):
        from matorage.tensorflow import Dataset

        self.data_config = DataConfig(
            **self.storage_config,
            dataset_name="test_datasaver_filetype",
            attributes=[DataAttribute("x", "float64", (2), itemsize=32)],
        )
        self.data_saver = DataSaver(config=self.data_config)
        x = np.asarray([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        self.assertEqual(x.shape, (3, 2))
        self.data_saver({"x": x})

        _file = open("test.txt", "w")
        _file.write('this is test')
        self.data_saver({"file": "test.txt"}, filetype=True)
        _file.close()

        self.data_saver.disconnect()

        self.dataset = Dataset(config=self.data_config, cache_folder_path=self.cache_folder_path)
        self.assertEqual(
            self.dataset.get_filetype_list, ["file"]
        )
        _local_filepath = self.dataset.get_filetype_from_key("file")
        with open(_local_filepath, 'r') as f:
            self.assertEqual(f.read(), 'this is test')

    def test_tf_saver_nas(self):
        self.data_config = DataConfig(
            **self.nas_config,
            dataset_name="test_tf_saver_nas",
            additional={"framework": "tensorflow"},
            attributes=[
                DataAttribute("image", "uint8", (2, 2), itemsize=32),
                DataAttribute("target", "uint8", (1), itemsize=32),
            ]
        )

        self.data_saver = DataSaver(config=self.data_config)

        self.data_saver(
            {
                "image": np.asarray([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
                "target": np.asarray([0, 1]),
            }
        )
        self.data_saver.disconnect()

    def test_tf_loader_nas(self):
        from matorage.tensorflow import Dataset

        self.test_tf_saver_nas()

        self.dataset = Dataset(config=self.data_config, cache_folder_path=self.cache_folder_path)

        for batch_idx, (image, target) in enumerate(
            tqdm(self.dataset.dataloader, total=2)
        ):
            pass

def suite():
    return unittest.TestSuite(unittest.makeSuite(TFDataTest))


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
