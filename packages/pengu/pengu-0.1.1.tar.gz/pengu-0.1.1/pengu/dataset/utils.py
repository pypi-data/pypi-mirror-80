import tensorflow as tf


def _bytes_feature(value):
    """string / byte 型から byte_list を返す"""
    if isinstance(value, type(tf.constant(0))):
        # BytesList won't unpack a string from an EagerTensor.
        value = value.numpy()
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _float_feature(value):
    """float / double 型から float_list を返す"""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def _int64_feature(value):
    """bool / enum / int / uint 型から Int64_list を返す"""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
