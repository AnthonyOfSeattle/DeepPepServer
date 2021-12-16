from deeppep import preprocessing


class TestSequenceEncoder:
    def test_encoder_fit(self):
        # Simple strings
        true_vocab = {"A" : 1,
                      "B" : 2,
                      "C" : 3,
                      "D" : 4}
        encoder = preprocessing.SequenceEncoder()
        encoder.fit("BDAC")
        assert encoder.vocab == true_vocab

        true_vocab.update({"E" : 5,
                           "F" : 6})
        encoder.fit(["BDAC",
                     "BFEA"])
        assert encoder.vocab == true_vocab

        # Strings with mods
        true_vocab = {"A"     : 1,
                      "B"     : 2,
                      "C"     : 3,
                      "C[10]" : 4,
                      "D"     : 5}
        encoder = preprocessing.SequenceEncoder(pattern="[A-Z][^A-Z]*")
        encoder.fit("BDAC[10]BCAD")
        assert encoder.vocab == true_vocab

        true_vocab.update({"E"     : 6,
                           "E[20]" : 7})
        encoder.fit(["BDAC[10]",
                     "BEE[20]A"])
        assert encoder.vocab == true_vocab

    def test_encoder_transformation(self):
        # Test integer encoding
        vocab = {"A"     : 1,
                 "B"     : 2,
                 "C"     : 3,
                 "C[10]" : 4,
                 "D"     : 5}
        encoder = preprocessing.SequenceEncoder(vocab=vocab,
                                                seq_len=10,
                                                pattern="[A-Z][^A-Z]*",
                                                oov_warn=False)
        output = encoder.transform("BDAC[10]BCADX")
        assert output.tolist() == [[2, 5, 1, 4, 2, 3, 1, 5, 0, 0]]

        # Test one-hot encoding
        encoder = preprocessing.SequenceEncoder(vocab=vocab,
                                                seq_len=10,
                                                pattern="[A-Z][^A-Z]*",
                                                one_hot=True,
                                                oov_warn=False)
        output = encoder.transform("BDAC[10]BCADX")
        assert output.astype(int).tolist() == [[[0, 1, 0, 0, 0],
                                                [0, 0, 0, 0, 1],
                                                [1, 0, 0, 0, 0],
                                                [0, 0, 0, 1, 0],
                                                [0, 1, 0, 0, 0],
                                                [0, 0, 1, 0, 0],
                                                [1, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 1],
                                                [0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0]]]

    def test_pipeline(self):
        # Test ability to both fit and transform
        encoder = preprocessing.SequenceEncoder(pattern="[A-Z][^A-Z]*")
        encoder.fit("BDAC[10]BCAD")
        output = encoder.transform(["C[10]BBCAD",
                                    "BEE[20]AC[10]CAAD"])
        assert output.tolist() == [[4, 2, 2, 3, 1, 5, 0, 0, 0],
                                   [2, 0, 0, 1, 4, 3, 1, 1, 5]]
