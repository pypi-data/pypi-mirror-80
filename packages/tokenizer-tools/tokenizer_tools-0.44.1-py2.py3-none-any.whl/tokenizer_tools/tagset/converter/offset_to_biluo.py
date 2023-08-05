from typing import List, Tuple

from tokenizer_tools.tagset.NER.BILUO import BILUOEncoderDecoder
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.span import Span


def offset_to_biluo(sequence: Document) -> Tuple[List[str], List[str], List[str]]:
    """
    Convert Sequence object to BILUO string

    :param sequence: Sequence example
    :return: string of BILUO encoding
    """
    encoding = ['O'] * len(sequence.text)
    for span in sequence.span_set:
        encoder = BILUOEncoderDecoder(span.entity)
        entity_text = sequence.text[span.start: span.end]
        entity_encoding = encoder.encode(entity_text)
        encoding[span.start: span.end] = entity_encoding

    role = ['O'] * len(sequence.text)
    for span in sequence.span_set:
        if span.role is not None:
            encoder = BILUOEncoderDecoder(span.role)
            entity_text = sequence.text[span.start: span.end]
            entity_encoding = encoder.encode(entity_text)
            role[span.start: span.end] = entity_encoding

    group = ['O'] * len(sequence.text)
    for span in sequence.span_set:
        if span.group is not None:
            encoder = BILUOEncoderDecoder(span.group)
            entity_text = sequence.text[span.start: span.end]
            entity_encoding = encoder.encode(entity_text)
            group[span.start: span.end] = entity_encoding

    return encoding, role, group


if __name__ == "__main__":
    seq = Document("王小明在北京的清华大学读书。")
    seq.span_set.append(Span(0, 3, 'PERSON', '王小明'))
    seq.span_set.append(Span(4, 6, 'GPE', '北京'))
    seq.span_set.append(Span(7, 11, 'ORG', '清华大学'))

    check_result = seq.check_span_set()
    print(check_result)

    encoding = offset_to_biluo(seq)
    print(encoding)
