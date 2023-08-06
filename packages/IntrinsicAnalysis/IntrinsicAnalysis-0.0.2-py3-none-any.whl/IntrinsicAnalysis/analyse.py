from IntrinsicAnalysis.clustering.AC_model import ACModel


def analyse_paragraphs(paragraphs):
    answer_pairs=[]
    ac = ACModel(None, None)
    results = ac.analyse_paragraphs(paragraphs)
    indicis = results['suspicious_parts']
    for index in range(len(paragraphs)):
        answer_pairs.append((paragraphs[index], index in indicis))
    return answer_pairs


