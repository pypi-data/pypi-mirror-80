from IntrinsicAnalysis.clustering.AC_model import ACModel


def analyse_paragraphs(paragraphs):
    ac = ACModel(None, None)
    results = ac.analyse_paragraphs(paragraphs)
    indicis = results['suspicious_parts']
    suspicious_paragraphs = [paragraphs[index]for index in indicis]if indicis else []
    return suspicious_paragraphs


