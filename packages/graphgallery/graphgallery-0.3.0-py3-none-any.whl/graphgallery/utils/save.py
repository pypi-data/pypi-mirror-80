import torch
import six
import os.path as osp
import tensorflow as tf

_TORCH_POSTFIX = '.pt'
_TF_POSTFIX = '.h5'


def save_tf_model(model, filepath, overwrite=True, save_format=None, **kwargs):

    postfix = _TF_POSTFIX
    filepath_with_postfix = filepath
    if not filepath_with_postfix.endswith(postfix):
        filepath_with_postfix = filepath_with_postfix + postfix

    model.save(filepath_with_postfix, overwrite=overwrite, save_format=save_format, **kwargs)


def save_torch_model(model, filepath, overwrite=True, save_format=None, **kwargs):
    postfix = _TORCH_POSTFIX

    filepath_with_postfix = filepath
    if not filepath_with_postfix.endswith(postfix):
        filepath_with_postfix = filepath_with_postfix + postfix

    if not overwrite and osp.isfile(filepath_with_postfix):
        proceed = ask_to_proceed_with_overwrite(filepath_with_postfix)
        if not proceed:
            return

    torch.save(model, filepath_with_postfix)


def save_tf_weights(model, filepath, overwrite=True, save_format=None):
    postfix = _TF_POSTFIX

    filepath_with_postfix = filepath
    if not filepath_with_postfix.endswith(postfix):
        filepath_with_postfix = filepath_with_postfix + postfix
    try:
        model.save_weights(filepath_with_postfix, overwrite=overwrite, save_format=save_format)
    except ValueError as e:
        model.save_weights(filepath_with_postfix[:-3], overwrite=overwrite, save_format=save_format)


def save_torch_weights(model, filepath, overwrite=True, save_format=None):
    postfix = _TORCH_POSTFIX

    filepath_with_postfix = filepath
    if not filepath_with_postfix.endswith(postfix):
        filepath_with_postfix = filepath_with_postfix + postfix

    if not overwrite and osp.isfile(filepath_with_postfix):
        proceed = ask_to_proceed_with_overwrite(filepath_with_postfix)
        if not proceed:
            return

    torch.save(model.state_dict(), filepath_with_postfix)


def load_tf_weights(model, filepath):
    postfix = _TF_POSTFIX

    filepath_with_postfix = filepath
    if not filepath_with_postfix.endswith(postfix):
        filepath_with_postfix = filepath_with_postfix + postfix
    try:
        model.load_weights(filepath_with_postfix)
    except KeyError as e:
        model.load_weights(filepath_with_postfix[:-3])


def load_torch_weights(model, filepath):
    postfix = _TORCH_POSTFIX

    filepath_with_postfix = filepath
    if not filepath_with_postfix.endswith(postfix):
        filepath_with_postfix = filepath_with_postfix + postfix

    checkpoint = torch.load(filepath_with_postfix)
    model.load_state_dict(checkpoint)


def load_tf_model(filepath, custom_objects=None, **kwargs):
    postfix = _TF_POSTFIX

    filepath_with_postfix = filepath
    if not filepath_with_postfix.endswith(postfix):
        filepath_with_postfix = filepath_with_postfix + postfix

    return tf.keras.models.load_model(filepath_with_postfix,
                                      custom_objects=custom_objects, **kwargs)


def load_torch_model(filepath):
    postfix = _TORCH_POSTFIX

    filepath_with_postfix = filepath
    if not filepath_with_postfix.endswith(postfix):
        filepath_with_postfix = filepath_with_postfix + postfix

    return torch.load(filepath_with_postfix)


def ask_to_proceed_with_overwrite(filepath):
    """Produces a prompt asking about overwriting a file.

    Parameters:
      filepath: the path to the file to be overwritten.

    Returns:
      True if we can proceed with overwrite, False otherwise.
    """
    overwrite = six.moves.input('[WARNING] %s already exists - overwrite? '
                                '[y/n]' % (filepath)).strip().lower()
    while overwrite not in ('y', 'n'):
        overwrite = six.moves.input('Enter "y" (overwrite) or "n" '
                                    '(cancel).').strip().lower()
    if overwrite == 'n':
        return False
    print('[TIP] Next time specify overwrite=True!')
    return True
