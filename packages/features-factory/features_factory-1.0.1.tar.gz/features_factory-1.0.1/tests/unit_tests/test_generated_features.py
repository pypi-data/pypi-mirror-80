import warnings
from typing import Tuple
from unittest import TestCase

import pandas as pd

from features_factory.generated_features import GeneratedFeature
from features_factory.input_features import IntInputFeature


class TestGeneratedFeature(TestCase):

    class DuplicateValueGeneratedFeature(GeneratedFeature):

        def __init__(self, name: str, input_column_name: str):
            super().__init__(name)
            self.__input_feature = IntInputFeature(input_column_name)

        def get_dependencies(self, **kwargs) -> Tuple:
            return self.__input_feature,

        def generate(self, df: pd.DataFrame, **kwargs) -> pd.Series:
            return 2 * df[self.__input_feature.name()]

    def test_if_overwriting_column_name_there_is_no_thrown_exception_but_only_warning(self):
        name = 'x'
        duplicate_value_feature = self.DuplicateValueGeneratedFeature(name=name, input_column_name=name)
        df = pd.DataFrame({name: [1, 2, 3]})

        with warnings.catch_warnings(record=True) as w:
            df = duplicate_value_feature.insert_into(df)
            self.assertCountEqual([2, 4, 6], df[name])
            self.assertEqual(1, len(w))
            self.assertEqual(UserWarning, w[0].category)
            self.assertIn(duplicate_value_feature.name(), str(w[0].message))
