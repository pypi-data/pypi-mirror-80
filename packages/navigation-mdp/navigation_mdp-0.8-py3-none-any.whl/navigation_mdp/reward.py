import numpy as np
"""
Objective, Utility
"""

class AbstractStateRewardSpec:

    def __init__(self, key=None, feature_key=None, preprocess_fn=lambda x: x, postprocess_fn=lambda x: x):
        self.key = key
        self.feature_key = key if feature_key is None else feature_key
        self.preprocess_fn = preprocess_fn
        self.postprocess_fn = postprocess_fn

    def __call__(self, state):
        return self.compute_reward(state)

    def get_key(self):
        return self.key

    def get_feature_key(self):
        return self.feature_key

    def compute_reward(self, state):
        raise NotImplementedError

    def reward(self, state):
        return self.compute_reward(state)

    def preprocess(self, features):
        return self.preprocess_fn(features)

    def postprocess(self, reward):
        return self.postprocess_fn(reward)

    def features(self, state):
        return self.preprocess(state.get_features(key=self.get_feature_key()))


class RewardStateScalar(AbstractStateRewardSpec):

    def __init__(self, loc_to_reward_dict, class_id_to_reward_dict, default=0,
                 key=None, feature_key=None, preprocess_fn=lambda x: x, postprocess_fn=lambda x: x):
        super().__init__(key, feature_key, preprocess_fn, postprocess_fn)
        self.loc_to_reward_dict = loc_to_reward_dict
        self.class_id_to_reward_dict = class_id_to_reward_dict
        self.default = default

    def compute_reward(self, state):
        # loc_to_reward_dict overrides class_id_to_reward_dict
        if (self.loc_to_reward_dict is not None) and state.location in self.loc_to_reward_dict:
            return self.postprocess_fn(
                self.loc_to_reward_dict[self.preprocess_fn(state.location)]
            )
        elif (self.class_id_to_reward_dict is not None) and state.class_id in self.class_id_to_reward_dict:
            return self.postprocess_fn(
                self.class_id_to_reward_dict[self.preprocess_fn(state.class_id)]
            )
        else:
            return self.postprocess_fn(
                self.preprocess_fn(self.default)
            )

class RewardStateFeatureModel(AbstractStateRewardSpec):

    def __init__(self, r_model, key=None, feature_key=None,
                 preprocess_fn=lambda x: x, postprocess_fn=lambda x: x):
        super().__init__(key, feature_key, preprocess_fn, postprocess_fn)
        self.r_model = r_model

    def compute_reward(self, state):
        return self.postprocess_fn(
            self.r_model(self.preprocess_fn(state.get_features(key=self.get_feature_key())))
        )
