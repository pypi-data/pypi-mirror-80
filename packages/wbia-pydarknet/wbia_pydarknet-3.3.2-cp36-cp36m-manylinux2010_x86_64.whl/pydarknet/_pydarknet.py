# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from collections import OrderedDict as odict
import ctypes as C
from six.moves import zip, range
from os.path import abspath, basename, join, exists
import utool as ut
import numpy as np
import time
import six
from pydarknet.pydarknet_helpers import (
    _load_c_shared_library,
    _cast_list_to_c,
    ensure_bytes_strings,
)


VERBOSE_DARK = ut.get_argflag('--verbdark') or ut.VERBOSE
QUIET_DARK = ut.get_argflag('--quietdark') or ut.QUIET

DEVICE = 'cpu' if ut.get_argflag('--cpudark') else 'gpu'
assert DEVICE in ['cpu', 'gpu']


CONFIG_URL_DICT = {
    'template': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.template.cfg',
    'original': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.5.cfg',
    'old': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.5.cfg',
    'v1': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.5.cfg',
    'v2': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.12.cfg',
    'v3': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.29.cfg',
    'lynx': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.lynx.cfg',
    'cheetah': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.cheetah.cfg',
    'seaturtle': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.sea_turtle.cfg',
    'sandtiger': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.shark_sandtiger.cfg',
    'hammerhead': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.shark_hammerhead.cfg',
    'whalefluke': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.whale_fluke.cfg',
    'whalefluke_v2': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.whale_fluke.v2.cfg',
    'sea': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.sea.cfg',
    'candidacy': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.candidacy.cfg',
    'default': 'https://wildbookiarepository.azureedge.net/models/detect.yolo.29.cfg',
    None: 'https://wildbookiarepository.azureedge.net/models/detect.yolo.29.cfg',
}


# ============================
# CTypes Interface Data Types
# ============================
"""
    Bindings for C Variable Types
"""
NP_FLAGS = 'aligned, c_contiguous, writeable'
# Primatives
C_OBJ = C.c_void_p
C_BYTE = C.c_char
C_CHAR = C.c_char_p
C_INT = C.c_int
C_BOOL = C.c_bool
C_FLOAT = C.c_float
NP_INT8 = np.uint8
NP_FLOAT32 = np.float32
# Arrays
C_ARRAY_CHAR = C.POINTER(C_CHAR)
C_ARRAY_FLOAT = C.POINTER(C_FLOAT)
NP_ARRAY_INT = np.ctypeslib.ndpointer(dtype=C_INT, ndim=1, flags=NP_FLAGS)
# NP_ARRAY_FLOAT = np.ctypeslib.ndpointer(dtype=NP_FLOAT32,     ndim=2, flags=NP_FLAGS)
NP_ARRAY_FLOAT = np.ctypeslib.ndpointer(dtype=NP_FLOAT32, ndim=1, flags=NP_FLAGS)
RESULTS_ARRAY = np.ctypeslib.ndpointer(dtype=NP_ARRAY_FLOAT, ndim=1, flags=NP_FLAGS)


# =================================
# Method Parameter Types
# =================================
"""
IMPORTANT:
    For functions that return void, use Python None as the return value.
    For functions that take no parameters, use the Python empty list [].
"""

METHODS = {}

METHODS['init'] = (
    [
        C_CHAR,  # config_filepath
        C_CHAR,  # weights_filepath
        C_INT,  # verbose
        C_INT,  # quiet
    ],
    C_OBJ,
)

METHODS['unload'] = ([C_OBJ], None)  # network

METHODS['train'] = (
    [
        C_OBJ,  # network
        C_CHAR,  # train_image_manifest
        C_CHAR,  # weights_path
        C_INT,  # num_input
        C_CHAR,  # final_weights_filepath
        C_INT,  # verbose
        C_INT,  # quiet
    ],
    None,
)

METHODS['detect'] = (
    [
        C_OBJ,  # network
        C_ARRAY_CHAR,  # input_gpath_array
        C_INT,  # num_input
        C_FLOAT,  # sensitivity
        C_INT,  # grid
        NP_ARRAY_FLOAT,  # results_array
        C_INT,  # verbose
        C_INT,  # quiet
    ],
    None,
)

DEFAULT_CLASS = 'UNKNOWN'
SIDES = 7
BOXES = 2
GRID = 1
PROB_RESULT_LENGTH = None
BBOX_RESULT_LENGTH = None
RESULT_LENGTH = None


def _update_globals(grid=GRID, class_list=None, verbose=True, num_classes_override=None):
    if num_classes_override is None:
        if class_list is None:
            config_url = CONFIG_URL_DICT['default']
            classes_url = _parse_classes_from_cfg(config_url)
            classes_filepath = ut.grab_file_url(
                classes_url, appname='pydarknet', check_hash=True, verbose=verbose
            )
            class_list = _parse_class_list(classes_filepath)
        if verbose:
            print('UPDATING GLOBALS: %r, %r' % (grid, class_list,))

        num_classes = len(class_list)
    else:
        num_classes = num_classes_override

    global PROB_RESULT_LENGTH, BBOX_RESULT_LENGTH, RESULT_LENGTH
    PROB_RESULT_LENGTH = grid * SIDES * SIDES * BOXES * num_classes
    BBOX_RESULT_LENGTH = grid * SIDES * SIDES * BOXES * 4
    RESULT_LENGTH = PROB_RESULT_LENGTH + BBOX_RESULT_LENGTH


def _parse_weights_from_cfg(url):
    return url.replace('.cfg', '.weights')


def _parse_classes_from_cfg(url):
    return url.replace('.cfg', '.classes')


def _parse_class_list(classes_filepath):
    # Load classes from file into the class list
    assert exists(classes_filepath)
    class_list = []
    with open(classes_filepath) as classes:
        for line in classes.readlines():
            line = line.strip()
            if len(line) > 0:
                class_list.append(line)
    return class_list


# =================================
# Load Dynamic Library
#=================================
try:
    _update_globals(verbose=False, num_classes_override=1)
except AssertionError:
    pass
DARKNET_CLIB, DARKNET_CFUNC = _load_c_shared_library(METHODS, device=DEVICE)


# =================================
# Darknet YOLO Detector
# =================================
class Darknet_YOLO_Detector(object):
    def __init__(
        dark,
        config_filepath=None,
        weights_filepath=None,
        classes_filepath=None,
        verbose=True,
        quiet=QUIET_DARK,
    ):
        """
            Create the C object for the PyDarknet YOLO detector.

            Args:
                verbose (bool, optional): verbose flag; defaults to --verbdark flag

            Returns:
                detector (object): the Darknet YOLO Detector object
        """
        if verbose:
            print('[pydarknet py init] config_filepath = %r' % (config_filepath,))
            print('[pydarknet py init] weights_filepath = %r' % (weights_filepath,))
            print('[pydarknet py init] classes_filepath = %r' % (classes_filepath,))

        # Get correct config if specified with shorthand
        config_url = None
        if config_filepath in CONFIG_URL_DICT:
            config_url = CONFIG_URL_DICT[config_filepath]
            config_filepath = ut.grab_file_url(
                config_url, appname='pydarknet', check_hash=True
            )

        # Get correct weights if specified with shorthand
        if weights_filepath in CONFIG_URL_DICT:
            if weights_filepath is None and config_url is not None:
                config_url_ = config_url
            else:
                config_url_ = CONFIG_URL_DICT[weights_filepath]
            weights_url = _parse_weights_from_cfg(config_url_)
            weights_filepath = ut.grab_file_url(
                weights_url, appname='pydarknet', check_hash=True
            )

        # Get correct classes if specified with shorthand
        if classes_filepath in CONFIG_URL_DICT:
            if classes_filepath is None and config_url is not None:
                config_url_ = config_url
            else:
                config_url_ = CONFIG_URL_DICT[classes_filepath]
            classes_url = _parse_classes_from_cfg(config_url_)
            classes_filepath = ut.grab_file_url(
                classes_url, appname='pydarknet', check_hash=True
            )

        assert exists(config_filepath)
        config_filepath = ut.truepath(config_filepath)
        assert exists(weights_filepath)
        weights_filepath = ut.truepath(weights_filepath)
        assert exists(classes_filepath)
        classes_filepath = ut.truepath(classes_filepath)

        dark.class_list = _parse_class_list(classes_filepath)

        # Save settings
        dark.verbose = verbose
        dark.quiet = quiet

        # Load the network
        dark._load(config_filepath, weights_filepath)

        if dark.verbose and not dark.quiet:
            print('[pydarknet py] New Darknet_YOLO Object Created')

    def __del__(dark):
        dark._unload()
        # super(Darknet_YOLO_Detector, dark).__del__()

    def _load(dark, config_filepath, weights_filepath):
        begin = time.time()

        if six.PY3:
            config_filepath = bytes(config_filepath, encoding='utf-8')
            weights_filepath = bytes(weights_filepath, encoding='utf-8')

        params_list = [
            config_filepath,
            weights_filepath,
            int(dark.verbose),
            int(dark.quiet),
        ]
        dark.net = DARKNET_CLIB.init(*params_list)
        conclude = time.time()
        if not dark.quiet:
            print('[pydarknet py] Took %r seconds to load' % (conclude - begin,))

    def _unload(dark):
        params_list = [
            dark.net,
        ]
        DARKNET_CLIB.unload(*params_list)
        dark.net = None

    def _train_setup(dark, voc_path, weights_path, dataset_list=['train', 'val']):

        class_list = []
        annotations_path = join(voc_path, 'Annotations')
        imagesets_path = join(voc_path, 'ImageSets')
        jpegimages_path = join(voc_path, 'JPEGImages')
        label_path = join(voc_path, 'labels')

        ut.delete(label_path)
        ut.ensuredir(label_path)

        def _convert_annotation(image_id):
            import xml.etree.ElementTree as ET

            def _convert(size, box):
                dw = 1.0 / size[0]
                dh = 1.0 / size[1]
                x = (box[0] + box[1]) / 2.0
                y = (box[2] + box[3]) / 2.0
                w = box[1] - box[0]
                h = box[3] - box[2]
                x = x * dw
                w = w * dw
                y = y * dh
                h = h * dh
                return (x, y, w, h)

            with open(join(label_path, '%s.txt' % (image_id,)), 'w') as out_file:
                with open(join(annotations_path, '%s.xml' % (image_id,)), 'r') as in_file:
                    tree = ET.parse(in_file)
                    root = tree.getroot()
                    size = root.find('size')
                    w = int(size.find('width').text)
                    h = int(size.find('height').text)

                    for obj in root.iter('object'):
                        if int(obj.find('difficult').text) == 1:
                            continue
                        class_ = obj.find('name').text
                        if class_ not in class_list:
                            class_list.append(class_)
                        class_id = class_list.index(class_)
                        xmlbox = obj.find('bndbox')
                        b = tuple(
                            map(
                                float,
                                [
                                    xmlbox.find('xmin').text,
                                    xmlbox.find('xmax').text,
                                    xmlbox.find('ymin').text,
                                    xmlbox.find('ymax').text,
                                ],
                            )
                        )
                        bb = _convert((w, h), b)
                        bb_str = ' '.join([str(_) for _ in bb])
                        out_file.write('%s %s\n' % (class_id, bb_str))

        num_images = 0
        print('[pydarknet py train] Processing manifest...')
        manifest_filename = join(voc_path, 'manifest.txt')
        with open(manifest_filename, 'w') as manifest:
            for dataset_name in dataset_list:
                dataset_filename = join(imagesets_path, 'Main', '%s.txt' % dataset_name)
                with open(dataset_filename, 'r') as dataset:
                    image_id_list = dataset.read().strip().split()

                for image_id in image_id_list:
                    print('[pydarknet py train]     processing: %r' % (image_id,))
                    image_filepath = abspath(join(jpegimages_path, '%s.jpg' % image_id))
                    if exists(image_filepath):
                        manifest.write('%s\n' % (image_filepath,))
                        _convert_annotation(image_id)
                        num_images += 1

        print('[pydarknet py train] Processing config and pretrained weights...')
        # Load default config and pretrained weights
        config_url = CONFIG_URL_DICT['template']
        config_filepath = ut.grab_file_url(
            config_url, appname='pydarknet', check_hash=True
        )
        with open(config_filepath, 'r') as config:
            config_template_str = config.read()

        config_filename = basename(config_filepath).replace(
            '.template.', '.%d.' % (len(class_list),)
        )
        config_filepath = join(weights_path, config_filename)
        with open(config_filepath, 'w') as config:
            replace_list = [
                ('_^_OUTPUT_^_', SIDES * SIDES * (BOXES * 5 + len(class_list))),
                ('_^_CLASSES_^_', len(class_list)),
                ('_^_SIDES_^_', SIDES),
                ('_^_BOXES_^_', BOXES),
            ]
            for needle, replacement in replace_list:
                config_template_str = config_template_str.replace(
                    needle, str(replacement)
                )
            config.write(config_template_str)

        classes_filepath = '%s.classes' % (config_filepath,)
        with open(classes_filepath, 'w') as class_file:
            for class_ in class_list:
                class_file.write('%s\n' % (class_,))

        config_url = CONFIG_URL_DICT['template']
        weights_url = _parse_weights_from_cfg(config_url)
        weights_filepath = ut.grab_file_url(
            weights_url, appname='pydarknet', check_hash=True
        )
        dark._load(config_filepath, weights_filepath)

        print('class_list = %r' % (class_list,))
        print('num_images = %r' % (num_images,))

        return manifest_filename, num_images, config_filepath, classes_filepath

    def train(dark, voc_path, weights_path, **kwargs):
        """
        Train a new forest with the given positive chips and negative chips.

        Args:
            train_pos_chip_path_list (list of str): list of positive training chips
            train_neg_chip_path_list (list of str): list of negative training chips
            trees_path (str): string path of where the newly trained trees are to be saved

        Kwargs:
            chips_norm_width (int, optional): Chip normalization width for resizing;
                the chip is resized to have a width of chips_norm_width and
                whatever resulting height in order to best match the original
                aspect ratio; defaults to 128

                If both chips_norm_width and chips_norm_height are specified,
                the original aspect ratio of the chip is not respected
            chips_norm_height (int, optional): Chip normalization height for resizing;
                the chip is resized to have a height of chips_norm_height and
                whatever resulting width in order to best match the original
                aspect ratio; defaults to None

                If both chips_norm_width and chips_norm_height are specified,
                the original aspect ratio of the chip is not respected
            verbose (bool, optional): verbose flag; defaults to object's verbose or
                selectively enabled for this function

        Returns:
            None
        """
        # Default values
        params = odict(
            [
                ('weights_filepath', None),  # This value always gets overwritten
                ('verbose', dark.verbose),
                ('quiet', dark.quiet),
            ]
        )
        # params.update(kwargs)
        ut.update_existing(params, kwargs)

        # Make the tree path absolute
        weights_path = abspath(weights_path)
        ut.ensuredir(weights_path)

        # Setup training files and folder structures
        results = dark._train_setup(voc_path, weights_path)
        manifest_filename, num_images, config_filepath, classes_filepath = results

        if six.PY3:
            manifest_filename = bytes(manifest_filename, encoding='utf-8')
            weights_path = bytes(weights_path, encoding='utf-8')

        # Run training algorithm
        params_list = [dark.net, manifest_filename, weights_path, num_images] + list(
            params.values()
        )
        DARKNET_CLIB.train(*params_list)
        weights_filepath = params['weights_filepath']

        if not params['quiet']:
            print('\n\n[pydarknet py] *************************************')
            print('[pydarknet py] Training Completed')
            print('[pydarknet py] Weight file saved to: %s' % (weights_filepath,))
        return weights_filepath, config_filepath, classes_filepath

    def detect(dark, input_gpath_list, **kwargs):
        """
        Run detection with a given loaded forest on a list of images

        Args:
            input_gpath_list (list of str): the list of image paths that you want
                to test
            config_filepath (str, optional): the network definition for YOLO to use
            weights_filepath (str, optional): the network weights for YOLO to use

        Kwargs:
            sensitivity (float, optional): the sensitivity of the detector, which
                accepts a value between 0.0 and 1.0; defaults to 0.0
            batch_size (int, optional): the number of images to test at a single
                time in paralell (if None, the number of CPUs is used); defaults to
                None
            verbose (bool, optional): verbose flag; defaults to object's verbose or
                selectively enabled for this function

        Yields:
            (str, (list of dict)): tuple of the input image path and a list
                of dictionaries specifying the detected bounding boxes

                The dictionaries returned by this function are of the form:
                    xtl (int): the top left x position of the bounding box
                    ytl (int): the top left y position of the bounding box
                    width (int): the width of the bounding box
                    height (int): the hiehgt of the bounding box
                    class (str): the most probably class detected by the network
                    confidence (float): the confidence that this bounding box is of
                        the class specified by the trees used during testing

        CommandLine:
            python -m pydarknet._pydarknet detect --show

        Example:
            >>> # DISABLE_DOCTEST
            >>> from pydarknet._pydarknet import *  # NOQA
            >>> dpath = '/media/raid/work/WS_ALL/localizer_backup/'
            >>> weights_filepath = join(dpath, 'detect.yolo.2.39000.weights')
            >>> config_filepath = join(dpath, 'detect.yolo.2.cfg')
            >>> dark = Darknet_YOLO_Detector(config_filepath=config_filepath,
            >>>                              weights_filepath=weights_filepath)
            >>> input_gpath_list = [u'/media/raid/work/WS_ALL/_ibsdb/images/0cb41f1e-d746-3052-ded4-555e11eb718b.jpg']
            >>> kwargs = {}
            >>> (input_gpath, result_list_) = dark.detect(input_gpath_list)
            >>> result = ('(input_gpath, result_list_) = %s' % (ut.repr2((input_gpath, result_list_)),))
            >>> print(result)
            >>> ut.quit_if_noshow()
            >>> import wbia.plottool as pt
            >>> ut.show_if_requested()
        """
        # Default values
        params = odict(
            [
                ('batch_size', None),
                ('class_list', dark.class_list),
                ('sensitivity', 0.2),
                ('grid', False),
                ('results_array', None),  # This value always gets overwritten
                ('verbose', dark.verbose),
                ('quiet', dark.quiet),
            ]
        )
        # params.update(kwargs)
        ut.update_existing(params, kwargs)
        class_list = params.pop('class_list')

        if params['grid']:
            _update_globals(grid=10, class_list=class_list)
        else:
            _update_globals(grid=1, class_list=class_list)

        # Try to determine the parallel processing batch size
        if params['batch_size'] is None:
            # try:
            #     cpu_count = multiprocessing.cpu_count()
            #     if not params['quiet']:
            #         print('[pydarknet py] Detecting with %d CPUs' % (cpu_count, ))
            #     params['batch_size'] = cpu_count
            # except Exception:
            #     params['batch_size'] = 128
            params['batch_size'] = 32

        params['verbose'] = int(params['verbose'])
        params['quiet'] = int(params['quiet'])

        # Data integrity
        assert (
            params['sensitivity'] >= 0 and params['sensitivity'] <= 1.0
        ), 'Threshold must be in the range [0, 1].'

        # Run training algorithm
        batch_size = params['batch_size']
        del params['batch_size']  # Remove this value from params
        batch_num = int(np.ceil(len(input_gpath_list) / float(batch_size)))
        # Detect for each batch
        for batch in ut.ProgIter(
            range(batch_num), lbl='[pydarknet py]', freq=1, invert_rate=True
        ):
            begin = time.time()
            start = batch * batch_size
            end = start + batch_size
            if end > len(input_gpath_list):
                end = len(input_gpath_list)
            input_gpath_list_ = input_gpath_list[start:end]
            num_images = len(input_gpath_list_)
            # Final sanity check
            params['results_array'] = np.empty(num_images * RESULT_LENGTH, dtype=C_FLOAT)
            # Make the params_list
            params_list = [
                dark.net,
                _cast_list_to_c(ensure_bytes_strings(input_gpath_list_), C_CHAR),
                num_images,
            ] + list(params.values())
            DARKNET_CLIB.detect(*params_list)
            results_list = params['results_array']
            conclude = time.time()
            results_list = results_list.reshape((num_images, -1))
            if not params['quiet']:
                print(
                    '[pydarknet py] Took %r seconds to compute %d images'
                    % (conclude - begin, num_images,)
                )
            for input_gpath, result_list in zip(input_gpath_list_, results_list):
                probs_list, bbox_list = np.split(result_list, [PROB_RESULT_LENGTH])
                assert (
                    probs_list.shape[0] == PROB_RESULT_LENGTH
                    and bbox_list.shape[0] == BBOX_RESULT_LENGTH
                )
                probs_list = probs_list.reshape((-1, len(class_list)))
                bbox_list = bbox_list.reshape((-1, 4))

                result_list_ = []
                for prob_list, bbox in zip(probs_list, bbox_list):
                    class_index = np.argmax(prob_list)
                    class_label = (
                        class_list[class_index]
                        if len(class_list) > class_index
                        else DEFAULT_CLASS
                    )
                    class_confidence = prob_list[class_index]
                    if class_confidence < params['sensitivity']:
                        continue
                    result_dict = {
                        'xtl': int(np.around(bbox[0])),
                        'ytl': int(np.around(bbox[1])),
                        'width': int(np.around(bbox[2])),
                        'height': int(np.around(bbox[3])),
                        'class': class_label,
                        'confidence': float(class_confidence),
                    }
                    result_list_.append(result_dict)

                yield (input_gpath, result_list_)
            params['results_array'] = None

    # Pickle functions
    # TODO: Just use __getstate__ and __setstate__ instead
    def dump(dark, file):
        """ UNIMPLEMENTED """
        pass

    def dumps(dark):
        """ UNIMPLEMENTED """
        pass

    def load(dark, file):
        """ UNIMPLEMENTED """
        pass

    def loads(dark, string):
        """ UNIMPLEMENTED """
        pass


def test_pydarknet():
    r"""

    CommandLine:
        python -m pydarknet._pydarknet --exec-test_pydarknet --show

    Example:
        >>> # ENABLE_DOCTEST
        >>> from pydarknet._pydarknet import *  # NOQA
        >>> test_pydarknet()
        >>> ut.quit_if_noshow()
        >>> ut.show_if_requested()
    """
    dark = Darknet_YOLO_Detector()
    # TODO: move test images out of the repo. Grab them via utool
    import pydarknet
    from os.path import dirname

    pydarknet_repo = dirname(ut.get_module_dir(pydarknet))
    input_gpath_list = ut.ls_images(join(pydarknet_repo, 'tests'), full=True)
    # input_gpath_list = [
    #    abspath(join('tests', 'test_%05d.jpg' % (i, )))
    #    for i in range(1, 76)
    # ]
    input_gpath_list = input_gpath_list[:5]

    results_list = dark.detect(input_gpath_list)

    for filename, result_list in list(results_list):
        print(filename)
        for result in result_list:
            print('    Found: %r' % (result,))

    del dark


def test_pydarknet2(
    input_gpath_list=None,
    config_filepath=None,
    weights_filepath=None,
    classes_filepath=None,
):
    r"""
    CommandLine:
        python -m pydarknet._pydarknet test_pydarknet2 --show

        python -m pydarknet test_pydarknet2 --show \
            --input_gpath_list=["~/work/WS_ALL/_ibsdb/images/0cb41f1e-d746-3052-ded4-555e11eb718b.jpg"] \
            --config_filepath="~/work/WS_ALL/localizer_backup/detect.yolo.2.cfg" \
            --weights_filepath="~/work/WS_ALL/localizer_backup/detect.yolo.2.39000.weights" \
            --classes_filepath="~/work/WS_ALL/localizer_backup/detect.yolo.2.cfg.classes"

    Ignore:
        >>> # Load in the second command line strings for faster testing
        >>> from pydarknet._pydarknet import *  # NOQA
        >>> cmdstr = ut.get_func_docblocks(test_pydarknet2)['CommandLine:'].split('\n\n')[1]
        >>> ut.aug_sysargv(cmdstr)

    Example:
        >>> # DISABLE_DOCTEST
        >>> from pydarknet._pydarknet import *  # NOQA
        >>> funckw = ut.argparse_funckw(test_pydarknet2)
        >>> exec(ut.execstr_dict(funckw), globals())
        >>> output_fpaths = test_pydarknet2(**funckw)
        >>> ut.quit_if_noshow()
        >>> import wbia.plottool as pt
        >>> inter = pt.MultiImageInteraction(output_fpaths)
        >>> inter.start()
        >>> ut.show_if_requested()
    """
    import pydarknet
    import cv2
    from pydarknet import Darknet_YOLO_Detector
    from os.path import join, basename, dirname

    if config_filepath is None:
        test_config_url = (
            'https://wildbookiarepository.azureedge.net/models/detect.yolo.12.cfg'
        )
        config_filepath = ut.grab_file_url(test_config_url, check_hash=True)
    if weights_filepath is None:
        test_weights_url = (
            'https://wildbookiarepository.azureedge.net/models/detect.yolo.12.weights'
        )
        weights_filepath = ut.grab_file_url(test_weights_url, check_hash=True)
    if classes_filepath is None:
        pass

    if input_gpath_list is None:
        pydarknet_repo = dirname(ut.get_module_dir(pydarknet))
        input_gpath_list = ut.ls_images(join(pydarknet_repo, 'tests'), full=True)

    input_gpath_list = [ut.truepath(gpath) for gpath in input_gpath_list]
    config_filepath = ut.truepath(config_filepath)
    weights_filepath = ut.truepath(weights_filepath)
    classes_filepath = ut.truepath(classes_filepath)

    dark = Darknet_YOLO_Detector(
        config_filepath=config_filepath,
        weights_filepath=weights_filepath,
        classes_filepath=classes_filepath,
    )

    temp_path = ut.ensure_app_resource_dir('pydarknet', 'temp')
    ut.delete(temp_path)
    ut.ensuredir(temp_path)

    results_list1 = list(dark.detect(input_gpath_list, grid=False))
    results_list2 = list(dark.detect(input_gpath_list, grid=True))

    zipped = zip(results_list1, results_list2)
    output_fpaths = []
    for (filename, result_list1), (filename2, result_list2) in zipped:
        print(filename)
        image = cv2.imread(filename)
        for result in result_list1:
            if result['confidence'] < 0.2:
                continue
            print('    Found 1: %r' % (result,))
            xtl = int(result['xtl'])
            ytl = int(result['ytl'])
            xbr = int(result['xtl'] + result['width'])
            ybr = int(result['ytl'] + result['height'])
            cv2.rectangle(image, (xtl, ytl), (xbr, ybr), (255, 140, 0), 5)
        for result in result_list2:
            if result['confidence'] < 0.2:
                continue
            print('    Found 2: %r' % (result,))
            xtl = int(result['xtl'])
            ytl = int(result['ytl'])
            xbr = int(result['xtl'] + result['width'])
            ybr = int(result['ytl'] + result['height'])
            cv2.rectangle(image, (xtl, ytl), (xbr, ybr), (0, 140, 255), 3)
        for result in result_list1:
            if result['confidence'] < 0.2:
                continue
            xtl = int(result['xtl'])
            ytl = int(result['ytl'])
            xbr = int(result['xtl'] + result['width'])
            ybr = int(result['ytl'] + result['height'])
            cv2.rectangle(image, (xtl, ytl), (xbr, ybr), (255, 140, 0), 1)
        temp_filepath = join(temp_path, basename(filename))
        cv2.imwrite(temp_filepath, image)
        output_fpaths.append(temp_filepath)
    return output_fpaths


if __name__ == '__main__':
    r"""
    CommandLine:
        python -m pydarknet._pydarknet
        python -m pydarknet._pydarknet --allexamples
    """
    import multiprocessing

    multiprocessing.freeze_support()  # for win32
    import utool as ut  # NOQA

    ut.doctest_funcs()
