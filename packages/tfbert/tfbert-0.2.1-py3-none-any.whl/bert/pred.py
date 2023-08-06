import tensorflow as tf

from .utils import get_activation
# from .similarity import Similarity


class Pred(tf.keras.Model):
    '''
def get_masked_lm_output(bert_config, input_tensor, output_weights, positions,
                         label_ids, label_weights):
  """Get loss and log probs for the masked LM."""
  input_tensor = gather_indexes(input_tensor, positions)

  with tf.variable_scope("cls/predictions"):
    # We apply one more non-linear transformation before the output layer.
    # This matrix is not used after pre-training.
    with tf.variable_scope("transform"):
      input_tensor = tf.layers.dense(
          input_tensor,
          units=bert_config.hidden_size,
          activation=modeling.get_activation(bert_config.hidden_act),
          kernel_initializer=modeling.create_initializer(
              bert_config.initializer_range))
      input_tensor = modeling.layer_norm(input_tensor)

    # The output weights are the same as the input embeddings, but there is
    # an output-only bias for each token.
    output_bias = tf.get_variable(
        "output_bias",
        shape=[bert_config.vocab_size],
        initializer=tf.zeros_initializer())
    logits = tf.matmul(input_tensor, output_weights, transpose_b=True)
    logits = tf.nn.bias_add(logits, output_bias)
    log_probs = tf.nn.log_softmax(logits, axis=-1)

    label_ids = tf.reshape(label_ids, [-1])
    label_weights = tf.reshape(label_weights, [-1])

    one_hot_labels = tf.one_hot(
        label_ids, depth=bert_config.vocab_size, dtype=tf.float32)

    # The `positions` tensor might be zero-padded (if the sequence is too
    # short to have the maximum number of predictions). The `label_weights`
    # tensor has a value of 1.0 for every real prediction and 0.0 for the
    # padding predictions.
    per_example_loss = -tf.reduce_sum(log_probs * one_hot_labels, axis=[-1])
    numerator = tf.reduce_sum(label_weights * per_example_loss)
    denominator = tf.reduce_sum(label_weights) + 1e-5
    loss = numerator / denominator

  return (loss, per_example_loss, log_probs)
    '''

    def __init__(self, hidden_size, vocab_size, hidden_act, **kwargs):
        self.hidden_size = hidden_size
        self.vocab_size = vocab_size
        self.hidden_act = hidden_act
        super(Pred, self).__init__(**kwargs)

    def build(self, input_shape):
        self.dense = tf.keras.layers.Dense(
            units=self.hidden_size,
            activation=get_activation(self.hidden_act),
            name='transform/dense')
        # epsilon is important be same with tf.contrib.layers.layer_norm
        # https://github.com/tensorflow/tensorflow/blob/r1.8/tensorflow/contrib/layers/python/layers/layers.py
        # L2174
        self.layer_norm = tf.keras.layers.LayerNormalization(
            epsilon=1e-12,
            name='transform/LayerNorm')
        self.output_bias = self.add_weight(
            name='output_bias',
            shape=(self.vocab_size, ),
            dtype=tf.keras.backend.floatx(),
            initializer='zeros')

    def similarity(self, input_tensor, embeddings):
        x = tf.matmul(input_tensor, embeddings, transpose_b=True)
        x = tf.nn.bias_add(x, self.output_bias)
        return x

    def call(self, inputs):
        x, embedding = inputs
        x = self.dense(x)
        x = self.layer_norm(x)
        x = self.similarity(x, embedding)
        x = tf.nn.log_softmax(x, axis=-1)
        return x
