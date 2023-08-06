from typing import List, Tuple
from IntrinsicAnalysis.clustering.main import make_prediction
from IntrinsicAnalysis.feature_extractors.computation import compute_feature_vectors


class ACModel(object):

    def __init__(self, hyperparams: List = None, features: List[str] = None):
        self.features = features
        self.hyperparams = hyperparams

    def train(self, train_set: List[Tuple[str, dict]], dev_set: List[Tuple[str, dict]]):
        pass

    def test(self, test_set: List[Tuple[str, dict]]):
        docs = [x for x, y in test_set]
        pred_results = self.analyse_documents(docs)
        return pred_results

    def analyse_paragraphs(self, paragraphs: List[str]):
        text = '\n'.join(paragraphs)
        feature_vectors = compute_feature_vectors(text, paragraphs, self.features)
        return self._analyse(feature_vectors)


    def _analyse(self, feature_vectors: List[List[float]]):
        predicted = make_prediction(feature_vectors, self.hyperparams)
        return{
            "style_change": predicted["style_change"],
            "suspicious_parts": predicted["style_breaches"]
        }