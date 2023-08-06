from sklearn.cluster import AgglomerativeClustering
from collections import Counter


def find_style_change_starts_by_ac(feature_vectors, hyperparams):
    # used hyper parameters
    n_clusters = 3 if not hyperparams else hyperparams[0]
    affinity = 'euclidean' if not hyperparams else hyperparams[1]
    linkage = 'ward' if not hyperparams else hyperparams[2]

    model = AgglomerativeClustering(n_clusters=n_clusters, affinity=affinity, linkage=linkage)
    clusters = model.fit_predict(feature_vectors)
    sorted_clusters = Counter(clusters).most_common()
    big_clusters_labels = [label for label, cap in sorted_clusters if cap == sorted_clusters[0][1]]
    results = []
    # Suppose, that if several clusters have "the biggest size"
    # author style can't be determined and all fragments are suspicious
    # in that case (Fragment,True)for all Fragment in page
    for index in range(len(feature_vectors)):
        if clusters[index] not in big_clusters_labels and len(big_clusters_labels) == 1:
            results.append(index)
    return results


def make_prediction(feature_vectors, hyperparams):
    # finds borders by Agglomerative Clustering
    style_changed_paragraphs= find_style_change_starts_by_ac(feature_vectors, hyperparams)
    result_dict = {"style_change": True if style_changed_paragraphs else False,
                   "style_breaches": style_changed_paragraphs}
    return result_dict