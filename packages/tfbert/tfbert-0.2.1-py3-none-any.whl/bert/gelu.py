import math
import tensorflow as tf


def gelu(x):
    """Gaussian Error Linear Unit.
  This is a smoother version of the RELU.
  Original paper: https://arxiv.org/abs/1606.08415
  Args:
    x: float Tensor to perform activation.
  Returns:
    `x` with the GELU activation applied.
  """
    cdf = 0.5 * (1.0 + tf.tanh(
        (math.sqrt(2 / math.pi) * (x + 0.044715 * tf.pow(x, 3)))))
    return x * cdf


def test():
    import tensorflow_addons as tfa
    x = tf.random.uniform((1, ))
    a = tfa.activations.gelu(x)
    b = gelu(x)
    print(x, a, b)


if __name__ == "__main__":
    test()
