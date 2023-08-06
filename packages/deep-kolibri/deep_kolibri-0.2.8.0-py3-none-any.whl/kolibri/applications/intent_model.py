import tensorflow as tf

from kolibri.dnn.tasks.text.base_model import TextBaseModel
from kolibri.dnn.tasks.text.classification.multi_input_output_model import MultiInputBaseModel
from kolibri.dnn.tensorflow.embeddings import DefaultEmbedding
from kolibri.dnn.tensorflow.layers import L
from kolibri.dnn.tensorflow.layers.crf import ConditionalRandomField as CRF


class MultiTaskIntent_Model(MultiInputBaseModel):

    def __init__(self, embeddings=None, sequence_length=None, hyper_parameters=None,
                 content_indexers=None, label_indexers=None):

        self.hyper_parameters = self.get_default_hyper_parameters()
        if embeddings is None:
            embeddings = []
            self.embedding_layer = DefaultEmbedding(embedding_size=self.hyper_parameters['word_embedding_size'],
                                                    name='word_input')
            self.char_embedding_layer = DefaultEmbedding(embedding_size=self.hyper_parameters['char_embedding_size'],
                                                         input_length=self.hyper_parameters['word_length'],
                                                         name='char_input')
            embeddings.append(self.embedding_layer)
            embeddings.append(self.char_embedding_layer)
        super().__init__(embeddings, sequence_length, hyper_parameters, content_indexers, label_indexers)

    @classmethod
    def get_default_hyper_parameters(cls):
        return {
            'word_length': 12,
            'word_embedding_size': 100,
            'char_embedding_size': 30,
            'char_lstm_dim': 30,
            'tagger_lstm_dims': 150,
            'layer_bi_lstm': {
                'units': 150,
                'return_sequences': True,
                'return_state': True
            },
            'dropout': {
                'rate': 0.5
            },
        }

    def build_model_arc(self):

        output_dims = [label_indexer.vocab_size for label_indexer in self.label_indexer.label_indexers]
        config = self.hyper_parameters
        embeddings = [embedding for embedding in self.embeddings]

        word_embeddings = embeddings[0].embedded_tensor

        word_embeddings = L.Dropout(**config['dropout'], name='drop_out_1')(word_embeddings)

        # first BiLSTM layer (used for intent classification)
        first_bilstm_layer = L.Bidirectional(L.LSTM(**config['layer_bi_lstm']), name='bilstm_2')(word_embeddings)

        lstm_y_sequence = first_bilstm_layer[:1][0]  # save y states of the LSTM layer
        states = first_bilstm_layer[1:]
        hf, _, hb, _ = states  # extract last hidden states
        h_state = L.concatenate([hf, hb], axis=-1)
        intents = L.Dense(output_dims[0], activation="softmax", name="intent_classifier_output")(h_state)

        char_embeddings = embeddings[1].embedded_tensor
        # feed dense char vectors into BiLSTM
        char_embeddings = tf.keras.layers.TimeDistributed(
            tf.keras.layers.Bidirectional(L.LSTM(self.hyper_parameters['char_lstm_dim']), name='bilistm_1'),
            name='time_distrinuted')(char_embeddings)
        char_embeddings = tf.keras.layers.Dropout(**config['dropout'], name='drop_out2')(char_embeddings)

        # create the 2nd feature vectors
        combined_features = tf.keras.layers.concatenate([lstm_y_sequence, char_embeddings], axis=-1)

        # 2nd BiLSTM layer for label classification
        second_bilstm_layer = tf.keras.layers.Bidirectional(
            L.LSTM(self.hyper_parameters['tagger_lstm_dims'], return_sequences=True), name='bidirectional')(
            combined_features)
        second_bilstm_layer = tf.keras.layers.Dropout(**config['dropout'], name="dropout3")(second_bilstm_layer)
        bilstm_out = tf.keras.layers.Dense(output_dims[1], name='dense3')(second_bilstm_layer)

        # feed BiLSTM vectors into CRF
        with tf.device("/cpu:0"):
            self.crf = CRF(output_dims[1], name="intent_slot_crf")
            labels = self.crf(bilstm_out)

        # compile the model

        self.tf_model = tf.keras.Model(inputs=[embeddings[0].input_tensor, embeddings[1].input_tensor],
                                       outputs=[intents, labels])

    def compile_model(self, loss=None, optimizer=None, metrics=None, **kwargs):
        """
        Configures the model for training.
        """
        if loss is None:
            if self.multi_label:
                loss = {
                    "intent_classifier_output": "categorical_crossentropy",
                    "intent_slot_crf": self.crf.loss,
                }

            else:
                loss = {
                    "intent_classifier_output": "sparse_categorical_crossentropy",
                    "intent_slot_crf": self.crf.sparse_loss,
                }
        if optimizer is None:
            optimizer = tf.compat.v1.train.AdamOptimizer()
        if metrics is None:
            metrics = {
                "intent_classifier_output": "sparse_categorical_accuracy",
                "intent_slot_crf": self.crf.sparse_viterbi_accuracy,
            }

        self.tf_model.compile(loss=loss, optimizer=optimizer, metrics=metrics, **kwargs)


#
# class MultiTaskIntentModel(TextBaseModel):
#     """
#     Multi-Task Intent and Slot tagging model (using tf.keras)
#
#     Args:
#         use_cudnn (bool, optional): use GPU based model (CUDNNA cells)
#     """
#
#     def __init__(self, use_cudnn=False):
#         super().__init__()
#         self.model = None
#         self.word_length = None
#         self.num_labels = None
#         self.num_intent_labels = None
#         self.word_vocab_size = None
#         self.char_vocab_size = None
#         self.word_emb_dims = None
#         self.char_emb_dims = None
#         self.char_lstm_dims = None
#         self.tagger_lstm_dims = None
#         self.dropout = None
#         self.use_cudnn = use_cudnn
#
#     def build(self,
#         word_length,
#         num_labels,
#         num_intent_labels,
#         word_vocab_size,
#         char_vocab_size,
#         word_emb_dims=100,
#         char_emb_dims=30,
#         char_lstm_dims=30,
#         tagger_lstm_dims=100,
#         dropout=0.2,
#     ):
#         """
#         Build a model
#
#         Args:
#             word_length (int): max word length (in characters)
#             num_labels (int): number of slot labels
#             num_intent_labels (int): number of intent classes
#             word_vocab_size (int): word vocabulary size
#             char_vocab_size (int): character vocabulary size
#             word_emb_dims (int, optional): word embedding dimensions
#             char_emb_dims (int, optional): character embedding dimensions
#             char_lstm_dims (int, optional): character feature LSTM hidden size
#             tagger_lstm_dims (int, optional): tagger LSTM hidden size
#             dropout (float, optional): dropout rate
#         """
#         self.word_length = word_length
#         self.num_labels = num_labels
#         self.num_intent_labels = num_intent_labels
#         self.word_vocab_size = word_vocab_size
#         self.char_vocab_size = char_vocab_size
#         self.word_emb_dims = word_emb_dims
#         self.char_emb_dims = char_emb_dims
#         self.char_lstm_dims = char_lstm_dims
#         self.tagger_lstm_dims = tagger_lstm_dims
#         self.dropout = dropout
#
#         words_input = tf.keras.layers.Input(shape=(None,), name="words_input")
#         embedding_layer = tf.keras.layers.Embedding( self.word_vocab_size, self.word_emb_dims, name="word_embedding" )
#         word_embeddings = embedding_layer(words_input)
#
#         word_embeddings = tf.keras.layers.Dropout(self.dropout, name='drop_out_1')(word_embeddings)
#
#         # create word character input and embeddings layer
#         word_chars_input = tf.keras.layers.Input(shape=(None, self.word_length), name="word_chars_input")
#         char_embedding_layer = tf.keras.layers.Embedding(self.char_vocab_size, self.char_emb_dims, input_length=self.word_length,name="char_embedding")
#         # apply embedding to each word
#         char_embeddings = char_embedding_layer(word_chars_input)
#         # feed dense char vectors into BiLSTM
#         char_embeddings = tf.keras.layers.TimeDistributed(tf.keras.layers.Bidirectional(self._rnn_cell(self.char_lstm_dims),name='bilistm_1'), name='time_distrinuted')(char_embeddings)
#         char_embeddings = tf.keras.layers.Dropout(self.dropout, name='drop_out2')(char_embeddings)
#
#         # first BiLSTM layer (used for intent classification)
#         first_bilstm_layer = tf.keras.layers.Bidirectional(self._rnn_cell(self.tagger_lstm_dims, return_sequences=True, return_state=True), name='bilstm_2')
#         first_lstm_out = first_bilstm_layer(word_embeddings)
#
#         lstm_y_sequence = first_lstm_out[:1][0]  # save y states of the LSTM layer
#         states = first_lstm_out[1:]
#         hf, _, hb, _ = states  # extract last hidden states
#         h_state = tf.keras.layers.concatenate([hf, hb], axis=-1)
#         intents = tf.keras.layers.Dense(self.num_intent_labels, activation="softmax", name="intent_classifier_output")(h_state)
#
#         # create the 2nd feature vectors
#         combined_features = tf.keras.layers.concatenate([lstm_y_sequence, char_embeddings], axis=-1)
#
#         # 2nd BiLSTM layer for label classification
#         second_bilstm_layer = tf.keras.layers.Bidirectional(self._rnn_cell(self.tagger_lstm_dims, return_sequences=True), name='bidirectional')(combined_features)
#         second_bilstm_layer = tf.keras.layers.Dropout(self.dropout, name="dropout3")(second_bilstm_layer)
#         bilstm_out = tf.keras.layers.Dense(self.num_labels, name='dense3')(second_bilstm_layer)
#
#         # feed BiLSTM vectors into CRF
#         with tf.device("/cpu:0"):
#             crf = CRF(self.num_labels, name="intent_slot_crf")
#             labels = crf(bilstm_out)
#
#         # compile the model
#         model = tf.keras.Model(inputs=[words_input, word_chars_input], outputs=[intents, labels])
#
#         # define losses and metrics
#         loss_f = {
#             "intent_classifier_output": "sparse_categorical_crossentropy",
#             "intent_slot_crf": crf.sparse_loss,
#         }
#         metrics = {
#             "intent_classifier_output": "sparse_categorical_accuracy",
#             "intent_slot_crf": crf.sparse_viterbi_accuracy,
#         }
#
#         model.compile(loss=loss_f, optimizer=tf.compat.v1.train.AdamOptimizer(), metrics=metrics)
#         self.model = model
#
#         keras.utils.plot_model(model, "model.png", show_shapes=True)
#
#     def fit(self, x, y, epochs=1, batch_size=1, callbacks=None, validation=None):
#         """
#         Train a model given input samples and target labels.
#
#         Args:
#             x: input samples
#             y: input sample labels
#             epochs (:obj:`int`, optional): number of epochs to train
#             batch_size (:obj:`int`, optional): batch size
#             callbacks(:obj:`Callback`, optional): Keras compatible callbacks
#             validation(:obj:`list` of :obj:`numpy.ndarray`, optional): optional validation data
#                 to be evaluated when training
#         """
#         assert self.model, "Model was not initialized"
#         self.model.fit(
#             x,
#             y,
#             epochs=epochs,
#             batch_size=batch_size,
#             shuffle=True,
#             validation_data=validation,
#             callbacks=callbacks,
#         )
#
#
#     def _rnn_cell(self, units, **kwargs):
#         if self.use_cudnn:
#             rnn_cell = tf.keras.layers.CuDNNLSTM(units, **kwargs)
#         else:
#             rnn_cell = tf.keras.layers.LSTM(units, **kwargs)
#         return rnn_cell
#
#     # pylint: disable=arguments-differ
#     def save(self, path):
#         """
#         Save model to path
#
#         Args:
#             path (str): path to save model
#         """
#         super().save(path, ["use_cudnn"])
#
#     @classmethod
#     def get_default_hyper_parameters(self):
#         return {
#             'layer_bi_lstm': {
#                 'units': 128,
#                 'return_sequences': False
#             },
#             'layer_output': {
#             }
#         }
#


class Seq2SeqIntentModel(TextBaseModel):
    """
    Encoder Decoder Deep LSTM Tagger Model (using tf.keras)
    """

    def __init__(self):
        super().__init__()
        self.model = None
        self.vocab_size = None
        self.tag_labels = None
        self.token_emb_size = None
        self.encoder_depth = None
        self.decoder_depth = None
        self.lstm_hidden_size = None
        self.encoder_dropout = None
        self.decoder_dropout = None

    def build(
            self,
            vocab_size,
            tag_labels,
            token_emb_size=100,
            encoder_depth=1,
            decoder_depth=1,
            lstm_hidden_size=100,
            encoder_dropout=0.5,
            decoder_dropout=0.5,
    ):
        """
        Build the model

        Args:
            vocab_size (int): vocabulary size
            tag_labels (int): number of tag labels
            token_emb_size (int, optional): token embedding vector size
            encoder_depth (int, optional): number of encoder LSTM layers
            decoder_depth (int, optional): number of decoder LSTM layers
            lstm_hidden_size (int, optional): LSTM layers hidden size
            encoder_dropout (float, optional): encoder dropout
            decoder_dropout (float, optional): decoder dropout
        """
        self.vocab_size = vocab_size
        self.tag_labels = tag_labels
        self.token_emb_size = token_emb_size
        self.encoder_depth = encoder_depth
        self.decoder_depth = decoder_depth
        self.lstm_hidden_size = lstm_hidden_size
        self.encoder_dropout = encoder_dropout
        self.decoder_dropout = decoder_dropout

        words_input = tf.keras.layers.Input(shape=(None,), name="words_input")
        emb_layer = tf.keras.layers.Embedding(
            self.vocab_size, self.token_emb_size, name="word_embedding"
        )
        benc_in = emb_layer(words_input)

        assert self.encoder_depth > 0, "Encoder depth must be > 0"
        for i in range(self.encoder_depth):
            bencoder = tf.keras.layers.LSTM(
                self.lstm_hidden_size,
                return_sequences=True,
                return_state=True,
                go_backwards=True,
                dropout=self.encoder_dropout,
                name="encoder_blstm_{}".format(i),
            )(benc_in)
            benc_in = bencoder[0]
        b_states = bencoder[1:]
        benc_h, bene_c = b_states

        decoder_inputs = benc_in
        assert self.decoder_depth > 0, "Decoder depth must be > 0"
        for i in range(self.decoder_depth):
            decoder = tf.keras.layers.LSTM(
                self.lstm_hidden_size, return_sequences=True, name="decoder_lstm_{}".format(i)
            )(decoder_inputs, initial_state=[benc_h, bene_c])
            decoder_inputs = decoder
        decoder_outputs = tf.keras.layers.Dropout(self.decoder_dropout)(decoder)
        decoder_predictions = tf.keras.layers.TimeDistributed(
            tf.keras.layers.Dense(self.tag_labels, activation="softmax"), name="decoder_classifier"
        )(decoder_outputs)

        self.model = tf.keras.Model(words_input, decoder_predictions)
        self.model.compile(
            optimizer=tf.train.AdamOptimizer(),
            loss="categorical_crossentropy",
            metrics=["categorical_accuracy"],
        )
