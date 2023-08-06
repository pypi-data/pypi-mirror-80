import warnings
from abc import ABC

import pandas as pd
from features_factory.feature_archetype import FeatureArchetype
from features_factory.input_data_error import InputDataError


class GeneratedFeature(FeatureArchetype, ABC):

    def verify_input(self, df: pd.DataFrame, **kwargs) -> InputDataError:
        if self.name() in df.columns:
            warnings.warn(
                'The GeneratedFeature {feature_name} will overwrite a pre-existing column'.format(
                    feature_name=self.name()),
                UserWarning)
        return InputDataError()
