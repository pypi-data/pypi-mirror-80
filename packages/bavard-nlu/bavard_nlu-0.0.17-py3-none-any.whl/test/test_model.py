import json
from unittest import TestCase

import tensorflow as tf

from bavard_nlu.model import NLUModel
from bavard_nlu.data_preprocessing.prediction_input import PredictionInput


class TestModel(TestCase):
    def setUp(self):
        super().setUp()
        self.max_seq_len = 200
        self.tokenizer = NLUModel.get_tokenizer()
        self.prediction_input = "how much is a flight from washington to boston"
        with open("test_data/test-agent.json") as f:
            self.agent_data = json.load(f)
    
    def test_train_and_predict(self):
        model = NLUModel(self.agent_data, self.max_seq_len)
        model.build_and_compile_model()
        model.train(batch_size=1, epochs=1)

        # Make the predictions.
        raw_intent_pred, raw_tags_pred = model.predict(
            self.prediction_input,
            self.tokenizer
        )

        # Decode the predictions.
        intent = model.decode_intent(raw_intent_pred)
        self.assertIn(intent, self.agent_data["nluData"]["intents"])

        pred_input = PredictionInput(self.prediction_input, self.max_seq_len, self.tokenizer)
        tags = model.decode_tags(raw_tags_pred, self.prediction_input, pred_input.word_start_mask)
        for tag in tags:
            self.assertIn(tag["tag_type"], self.agent_data["nluData"]["tagTypes"])
    
    def test_determine_batch_size(self):
        b = NLUModel._determine_batch_size(NLUModel.min_num_examples)
        self.assertEqual(b, NLUModel.min_batch_size)

        b = NLUModel._determine_batch_size(300)
        self.assertEqual(b, 8)

        b = NLUModel._determine_batch_size(1e7)
        self.assertEqual(b, 64)
    
    def test_get_training_setup(self):
        
        # Test the `auto==False` case.
        hparams = {"batch_size": 5, "epochs": 12}
        expected_n = 11
        dataset = tf.data.Dataset.from_tensor_slices(list(range(expected_n)))
        train_data, val_data, hparams, callbacks = NLUModel.get_training_setup(False, dataset, hparams)
        n = sum(1 for _ in train_data)

        self.assertEqual(n, expected_n, "dataset length not what expected")
        # New hparams should be set correctly.
        self.assertEqual(hparams["steps_per_epoch"], 3, "incorrect steps_per_epoch")
        # Original hparams should be unchanged.
        self.assertEqual(hparams["batch_size"], 5, "batch size should not have changed")
        self.assertEqual(hparams["epochs"], 12, "epochs should not have changed")

        # Test the `auto==True` case without early stopping.

        hparams = {"batch_size": 5, "epochs": 1}
        expected_n = NLUModel.min_train_size_for_validation - 1
        dataset = tf.data.Dataset.from_tensor_slices(list(range(expected_n)))
        train_data, val_data, hparams, callbacks = NLUModel.get_training_setup(True, dataset, hparams)
        n = sum(1 for _ in train_data)

        self.assertEqual(n, expected_n, "dataset length not what expected")
        self.assertIsNone(val_data)
        self.assertEqual(hparams["batch_size"], NLUModel._determine_batch_size(expected_n))
        self.assertEqual(
            hparams["steps_per_epoch"],
            NLUModel._get_steps_per_epoch(expected_n, hparams["batch_size"])
        )

        # Test the `auto==True` case *with* early stopping.

        hparams = {"batch_size": 5, "epochs": 1}
        expected_n = NLUModel.min_train_size_for_validation
        dataset = tf.data.Dataset.from_tensor_slices(list(range(expected_n)))
        train_data, val_data, hparams, callbacks = NLUModel.get_training_setup(True, dataset, hparams)
        train_n = sum(1 for _ in train_data)

        self.assertIsNotNone(val_data)
        val_n = sum(1 for _ in val_data)

        # Train and validation sets should be the expected size.
        self.assertEqual(train_n, expected_n - NLUModel._get_val_size(expected_n))
        self.assertEqual(val_n, NLUModel._get_val_size(expected_n))

        self.assertEqual(hparams["batch_size"], NLUModel._determine_batch_size(train_n))
        self.assertEqual(
            hparams["steps_per_epoch"],
            NLUModel._get_steps_per_epoch(train_n, hparams["batch_size"])
        )
