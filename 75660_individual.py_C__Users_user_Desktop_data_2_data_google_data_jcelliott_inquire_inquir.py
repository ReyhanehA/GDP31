# answer extractor for human: individual type

from ..extractors import NETagExtractor

TAG = "PERSON"

class Extractor(NETagExtractor):
    def __init__(self, question, docs):
        super(Extractor, self).__init__(question, docs, tag=TAG)

