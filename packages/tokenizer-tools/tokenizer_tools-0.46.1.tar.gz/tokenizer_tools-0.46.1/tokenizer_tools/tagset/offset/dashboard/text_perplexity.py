from typing import List
import math

import numpy as np
import requests
from micro_toolkit.data_process.batch_iterator import BatchingIterator

from tokenizer_tools.tagset.offset.corpus import Corpus

def batch_get_text_perplexity(server_url: str, text: List[str]) -> List[float]:
    result = []

    batch_iterator = BatchingIterator(1000)
    for batch_text in batch_iterator(text):
        r = requests.post(server_url, json=batch_text)
        part_result = r.json()
        result.extend(part_result)

    return result


def compute_histogram(data, bin_num=200):
    hist, bin_edges = np.histogram(data, bin_num)
    hist = hist.tolist()
    bin_edges = bin_edges.tolist()

    text_edges = ["{:.2f}".format(x) for x in bin_edges]
    text_range = [",".join(x) for x in zip(text_edges[:-1], text_edges[1:])]

    assert len(hist) == len(text_range)

    return hist, bin_edges, text_range


if __name__ == "__main__":
    # data = list(range(20))
    # hist, bin_edges, text_range = compute_histogram(data, 10)
    # print(hist, bin_edges, text_range)

    corpus = Corpus.read_from_file("../corpus.pb")
    text = ["".join(doc.text) for doc in corpus[:1000]]

    data = batch_get_text_perplexity("http://127.0.0.1:5000/parse", text)

    print(len(data))
