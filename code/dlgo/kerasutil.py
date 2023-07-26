import os
import tempfile

import h5py
from keras.models import save_model, load_model


def save_model_to_hdf5_group(model, f):
    tempfd, tempfname = tempfile.mkstemp(prefix='tmp-kerasmodel', suffix='.h5')
    try:
        os.close(tempfd)
        save_model(model, tempfname, save_format='h5')
        serialized_model = h5py.File(tempfname, 'r')
        root_item = serialized_model.get('/')
        serialized_model.copy(root_item, f, 'kerasmodel')
        serialized_model.close()
    finally:
        os.unlink(tempfname)


def load_model_from_hdf5_group(f, custom_objects=None):
    tempfd, tempfname = tempfile.mkstemp(prefix='tmp-kerasmodel', suffix='.h5')
    try:
        os.close(tempfd)
        serialized_model = h5py.File(tempfname, 'w')
        root_item = f.get('kerasmodel')
        for attr_name, attr_value in root_item.attrs.items():
            serialized_model.attrs[attr_name] = attr_value
        for k in root_item.keys():
            f.copy(root_item.get(k), serialized_model, k)
        serialized_model.close()
        return load_model(tempfname, custom_objects=custom_objects)
    finally:
        os.unlink(tempfname)
