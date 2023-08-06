cdef class SentenceSplitter:

    SEPARATORS = "()[]{}\"'\u05F4\uFF02\u055B"
    SENTENCE_ENDERS = ".?!…"
    PUNCTUATION_CHARACTERS = ",:;"

    cpdef list split(self, str line):
        pass
