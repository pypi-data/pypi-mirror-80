from datamaestro_image.data import ImageClassification, LabelledImages, Base, IDXImage
from datamaestro.download.single import filedownloader
from datamaestro.definitions import dataset
from datamaestro.data.tensor import IDX


@filedownloader(
    "train_images.idx", "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz"
)
@filedownloader(
    "train_labels.idx", "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz"
)
@filedownloader(
    "test_images.idx", "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz"
)
@filedownloader(
    "test_labels.idx", "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"
)
@dataset(
    ImageClassification,
    url="http://yann.lecun.com/exdb/mnist/",
)
def MNIST(train_images, train_labels, test_images, test_labels):
    """The MNIST database

    The MNIST database of handwritten digits, available from this page, has a
    training set of 60,000 examples, and a test set of 10,000 examples. It is a
    subset of a larger set available from NIST. The digits have been
    size-normalized and centered in a fixed-size image.
    """
    return {
        "train": LabelledImages(
            images=IDXImage(path=train_images), labels=IDX(path=train_labels)
        ),
        "test": LabelledImages(
            images=IDXImage(path=test_images), labels=IDX(path=test_labels)
        ),
    }
