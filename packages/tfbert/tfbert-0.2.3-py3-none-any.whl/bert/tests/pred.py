import tensorflow as tf
from bert.bert import Bert
from bert.pred import Pred
from .config import params


def build_model():

    bert = Bert(**params)
    pred = Pred()
    input_ids = tf.keras.layers.Input(shape=(None,), dtype=tf.int32)
    input_ids_type = tf.keras.layers.Input(shape=(None,), dtype=tf.int32)

    x = input_ids
    t = input_ids_type
    x = bert([x, t])
    emb = tf.identity(bert.embedding.word_embeddings_layer.weights[0])
    x = pred([x, emb])
    model = tf.keras.Model(inputs=[input_ids, input_ids_type], outputs=x)
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=tf.keras.optimizers.Adam()
    )
    return model


def test():

    n_samples = 320
    max_length = 20

    x = tf.random.uniform((n_samples, max_length),
                          minval=0,
                          maxval=params.get('vocab_size'),
                          dtype=tf.int32)
    t = tf.random.uniform((n_samples, max_length),
                          minval=0,
                          maxval=params.get('type_vocab_size'),
                          dtype=tf.int32)

    y = tf.random.uniform((n_samples, max_length),
                          minval=0,
                          maxval=params.get('vocab_size'),
                          dtype=tf.int32)

    x = tf.data.Dataset.from_tensor_slices(x)
    t = tf.data.Dataset.from_tensor_slices(t)
    y = tf.data.Dataset.from_tensor_slices(y)

    data = tf.data.Dataset.zip((x, t))
    data = tf.data.Dataset.zip((data, y))
    data = data.batch(32)

    model = build_model()
    model.fit(data)


if __name__ == "__main__":
    test()
