from datamaestro.data import Base, Base
from datamaestro.data.ml import Supervised
from datamaestro.definitions import data, argument, datatasks, datatags, dataset
from datamaestro.data.tensor import IDX


@data()
class Image(Base):
    pass


@data()
class IDXImage(IDX, Image):
    pass


@datatasks("image classification")
@datatags("images")
@data()
class ImageClassification(Supervised):
    """Image classification dataset"""

    pass


@argument("images", Image)
@argument("labels", Base)
@datatasks("image classification")
@datatags("images")
@data()
class LabelledImages(Base):
    """Image classification dataset"""

    pass
