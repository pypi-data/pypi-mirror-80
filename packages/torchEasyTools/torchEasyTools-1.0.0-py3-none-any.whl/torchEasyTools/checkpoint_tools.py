#!/usr/bin/python3
# *_* coding: utf-8 *_*
# @Author: samon
# @Email: samonsix@163.com
# @IDE: PyCharm
# @File: checkpoint_tools.py
# @Modify Time        @Author    @Version    @Desciption
# ----------------    -------    --------    -----------
# 2019.10.09 10:09    samon      v0.1        creation

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os.path as osp
import pickle
import warnings
from collections import OrderedDict
from functools import partial

import torch
import torch.nn as nn


def load_checkpoint(fpath, map_location=None):
    r"""Loads checkpoint.

    ``UnicodeDecodeError`` can be well handled, which means
    python2-saved files can be read from python3.

    Args:
        fpath (str): path to checkpoint.
        map_location:
            If :attr:`map_location` is a callable, it will be called once for each serialized
        storage with two arguments: storage and location. The storage argument
        will be the initial deserialization of the storage, residing on the CPU.
        Each serialized storage has a location tag associated with it which
        identifies the device it was saved from, and this tag is the second
        argument passed to :attr:`map_location`. The builtin location tags are ``'cpu'``
        for CPU tensors and ``'cuda:device_id'`` (e.g. ``'cuda:2'``) for CUDA tensors.
        :attr:`map_location` should return either ``None`` or a storage. If
        :attr:`map_location` returns a storage, it will be used as the final deserialized
        object, already moved to the right device. Otherwise, :func:`torch.load` will
        fall back to the default behavior, as if :attr:`map_location` wasn't specified.


    Returns:
        dict

    Examples::
        >>> fpath = 'log/my_model/model.pth.tar-10'
        >>> checkpoint = load_checkpoint(fpath)
    """
    if fpath is None:
        raise ValueError('File path is None')
    if not osp.exists(fpath):
        raise FileNotFoundError('File is not found at "{}"'.format(fpath))

    if map_location is None:
        map_location = 'cpu'

    try:
        checkpoint = torch.load(fpath, map_location=map_location)
    except UnicodeDecodeError:
        pickle.load = partial(pickle.load, encoding="latin1")
        pickle.Unpickler = partial(pickle.Unpickler, encoding="latin1")
        checkpoint = torch.load(fpath, pickle_module=pickle, map_location=map_location)
    except Exception:
        print('Unable to load checkpoint from "{}"'.format(fpath))
        raise
    return checkpoint


def resume_from_checkpoint(fpath, model, optimizer=None):
    r"""Resumes training from a checkpoint.

    This will load (1) model weights and (2) ``state_dict``
    of optimizer if ``optimizer`` is not None.

    Args:
        fpath (str): path to checkpoint.
        model (nn.Module): model.
        optimizer (Optimizer, optional): an Optimizer.

    Returns:
        int: start_epoch.

    Examples::
        >>> fpath = 'log/my_model/model.pth.tar-10'
        >>> start_epoch = resume_from_checkpoint(fpath, model, optimizer)
    """
    print('Loading checkpoint from "{}"'.format(fpath))
    checkpoint = load_checkpoint(fpath)
    model.load_state_dict(checkpoint['state_dict'])
    print('Loaded model weights')
    if optimizer is not None and 'optimizer' in checkpoint.keys():
        optimizer.load_state_dict(checkpoint['optimizer'])
        print('Loaded optimizer')
    start_epoch = checkpoint['epoch']
    print('Last epoch = {}'.format(start_epoch))
    if 'rank1' in checkpoint.keys():
        print('Last rank1 = {:.1%}'.format(checkpoint['rank1']))
    return start_epoch


def adjust_learning_rate(optimizer, base_lr, epoch, stepsize=20, gamma=0.1,
                         linear_decay=False, final_lr=0, max_epoch=100):
    r"""Adjusts learning rate.

    Deprecated.
    """
    if linear_decay:
        # linearly decay learning rate from base_lr to final_lr
        frac_done = epoch / max_epoch
        lr = frac_done * final_lr + (1. - frac_done) * base_lr
    else:
        # decay learning rate by gamma for every stepsize
        lr = base_lr * (gamma ** (epoch // stepsize))

    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


def set_bn_to_eval(m):
    r"""Sets BatchNorm layers to eval mode."""
    # 1. no update for running mean and var
    # 2. scale and shift parameters are still trainable
    classname = m.__class__.__name__
    if classname.find('BatchNorm') != -1:
        m.eval()


def open_all_layers(model):
    r"""Opens all layers in model for training.

    Examples::
        >>> open_all_layers(model)
    """
    model.train()
    for p in model.parameters():
        p.requires_grad = True


def close_all_layers(model):
    r"""frozen all layers in model for training.

    Args:
        model (nn.Module): neural net model.

    Examples::
        >>> close_all_layers(model)
    """
    if isinstance(model, nn.DataParallel):
        model = model.module

    for _, module in model.named_children():
        module.eval()
        for p in module.parameters():
            p.requires_grad = False


def open_specified_layers(model, open_layers):
    r"""Opens specified layers in model for training while keeping
    other layers frozen.

    Args:
        model (nn.Module): neural net model.
        open_layers (str or list): layers open for training.

    Examples::
        >>> # Only model.classifier will be updated.
        >>> open_layers = 'classifier'
        >>> open_specified_layers(model, open_layers)
        >>> # Only model.fc and model.classifier will be updated.
        >>> open_layers = ['fc', 'classifier']
        >>> open_specified_layers(model, open_layers)
    """
    if isinstance(model, nn.DataParallel):
        model = model.module

    if isinstance(open_layers, str):
        open_layers = [open_layers]

    for layer in open_layers:
        assert hasattr(model, layer), '"{}" is not an attribute of the model'.format(layer)

    for name, module in model.named_children():
        if name in open_layers:
            print("open", name)
            module.train()
            for p in module.parameters():
                p.requires_grad = True
        else:
            print("close", name)
            module.eval()
            for p in module.parameters():
                p.requires_grad = False


def load_pretrained_weights(model, weight_path, map_location=None, verbose=True):
    r"""Loads pretrianed weights to model.

    Features::
        - Incompatible layers (unmatched in name or size) will be ignored.
        - Can automatically deal with keys containing "module.".

    Args:
        model (nn.Module): network model.
        weight_path (str): path to pretrained weights.

    Examples::
        >>> weight_path = 'log/my_model/model-best.pth.tar'
        >>> load_pretrained_weights(model, weight_path)
    """

    checkpoint = load_checkpoint(weight_path, map_location=map_location)
    if 'state_dict' in checkpoint:
        state_dict = checkpoint['state_dict']
    else:
        state_dict = checkpoint

    model_dict = model.state_dict()
    new_state_dict = OrderedDict()
    matched_layers, discarded_layers = [], []
    for k, v in state_dict.items():
        if k.startswith('module.'):
            k = k[7:]  # discard module.

        if k in model_dict and model_dict[k].size() == v.size():
            new_state_dict[k] = v
            matched_layers.append(k)
        else:  # the layers in pretrained but not in model
            discarded_layers.append(k)

    # the layers in model but not in pretrained
    for k, v in model_dict.items():
        if k not in state_dict or state_dict[k].size() != v.size():
            discarded_layers.append(k)

    model_dict.update(new_state_dict)
    model.load_state_dict(model_dict)

    if verbose:
        if len(matched_layers) == 0:
            warnings.warn(
                'The pretrained weights "{}" cannot be loaded, '
                'please check the key names manually '
                '(** ignored and continue **)'.format(weight_path))
        else:
            print('Successfully loaded pretrained weights from "{}"'.format(weight_path))
            if len(discarded_layers) > 0:
                print("*" * 80)
                print('The following layers are discarded due to unmatched keys or layer size')
                print(discarded_layers)
                print("*" * 80)
                print('The following layers are success')
                print(matched_layers)

