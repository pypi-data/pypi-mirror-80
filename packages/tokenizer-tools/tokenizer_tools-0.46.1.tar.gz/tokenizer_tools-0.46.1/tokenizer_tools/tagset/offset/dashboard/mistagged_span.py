from collections import defaultdict
from typing import List, Dict

import ahocorasick

from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.document import Document


class MistaggedSpan:
    def __init__(self):
        self.automaton = ahocorasick.Automaton()

    def add_spans(self, spans: List[str]):
        for idx, key in enumerate(spans):
            self.automaton.add_word(key, (idx, key))
        self.automaton.make_automaton()

    def process_doc(self, doc: Document) -> List[str]:
        result = []

        text_str = "".join(doc.text)
        for end_index, (insert_order, original_value) in self.automaton.iter(text_str):
            start_index = end_index - len(original_value) + 1
            # print((start_index, end_index, (insert_order, original_value)))

            if not doc.get_entity_cover_range(start_index, end_index):
                result.append(original_value)

        return result

    def process_corpus(self, corpus: Corpus) -> Dict[str, List[Document]]:
        result = defaultdict(list)
        for doc in corpus:
            doc_results = self.process_doc(doc)
            for doc_result in doc_results:
                result[doc_result].append(doc)

        return result


if __name__ == "__main__":
    corpus = Corpus.read_from_file("../corpus.pb")
    spans = defaultdict(list)
    for doc in corpus:
        for span in doc.span_set:
            spans["".join(span.value)].append(doc)

    ms = MistaggedSpan()
    ms.add_spans(list(spans.keys()))
    result = ms.process_corpus(corpus)

    print(result)
