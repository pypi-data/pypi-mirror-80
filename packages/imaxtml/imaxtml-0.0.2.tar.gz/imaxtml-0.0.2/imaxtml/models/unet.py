from keras.layers import Conv2D as _Conv2D
from keras.layers import (
    Dropout,
    Input,
    MaxPooling2D,
    UpSampling2D,
    concatenate,
)
from keras.models import Model
from keras.optimizers import Adam


def Conv2D(filters, size, activation="relu", kernel_initializer="he_normal"):
    """Shortcut for the convolutional layer
    """
    return _Conv2D(
        filters,
        size,
        activation=activation,
        padding="same",
        kernel_initializer=kernel_initializer,
    )


def UNet(
    input_size=(256, 256, 1),
    n_classes=1,
    learning_rate=1e-4,
    loss="binary_crossentropy",
    metrics=None,
    activation="sigmoid",
):
    inputs = Input(input_size)
    conv1 = Conv2D(64, 3)(inputs)
    conv1 = Conv2D(64, 3)(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(128, 3)(pool1)
    conv2 = Conv2D(128, 3)(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(256, 3)(pool2)
    conv3 = Conv2D(256, 3)(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

    conv4 = Conv2D(512, 3)(pool3)
    conv4 = Conv2D(512, 3)(conv4)
    drop4 = Dropout(0.5)(conv4)
    pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)

    conv5 = Conv2D(1024, 3)(pool4)
    conv5 = Conv2D(1024, 3)(conv5)
    drop5 = Dropout(0.5)(conv5)

    up6 = Conv2D(512, 2)(UpSampling2D(size=(2, 2))(drop5))
    merge6 = concatenate([drop4, up6], axis=3)
    conv6 = Conv2D(512, 3)(merge6)
    conv6 = Conv2D(512, 3)(conv6)

    up7 = Conv2D(256, 2)(UpSampling2D(size=(2, 2))(conv6))
    merge7 = concatenate([conv3, up7], axis=3)
    conv7 = Conv2D(256, 3)(merge7)
    conv7 = Conv2D(256, 3)(conv7)

    up8 = Conv2D(128, 2)(UpSampling2D(size=(2, 2))(conv7))
    merge8 = concatenate([conv2, up8], axis=3)
    conv8 = Conv2D(128, 3)(merge8)
    conv8 = Conv2D(128, 3)(conv8)

    up9 = Conv2D(64, 2)(UpSampling2D(size=(2, 2))(conv8))
    merge9 = concatenate([conv1, up9], axis=3)
    conv9 = Conv2D(64, 3)(merge9)
    conv9 = Conv2D(64, 3)(conv9)
    conv9 = Conv2D(2, 3)(conv9)
    conv10 = _Conv2D(n_classes, 1, activation=activation)(conv9)

    model = Model(inputs=inputs, outputs=conv10)

    if metrics is None:
        metrics = ["accuracy"]

    model.compile(optimizer=Adam(lr=learning_rate), loss=loss, metrics=metrics)

    model.name = "UNet"
    return model


def SmallUNet(
    input_size=(256, 256, 1),
    n_classes=1,
    learning_rate=1e-4,
    loss="binary_crossentropy",
    metrics=None,
    activation="sigmoid",
):
    inputs = Input(input_size)
    conv1 = Conv2D(32, 3)(inputs)
    conv1 = Conv2D(32, 3)(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(64, 3)(pool1)
    conv2 = Conv2D(64, 3)(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(128, 3)(pool2)
    conv3 = Conv2D(128, 3)(conv3)
    drop3 = Dropout(0.5)(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2))(drop3)

    conv4 = Conv2D(256, 3)(pool3)
    conv4 = Conv2D(256, 3)(conv4)
    drop4 = Dropout(0.5)(conv4)

    up5 = Conv2D(128, 2)(UpSampling2D(size=(2, 2))(drop4))
    merge5 = concatenate([drop3, up5], axis=3)
    conv5 = Conv2D(128, 3)(merge5)
    conv5 = Conv2D(128, 3)(conv5)

    up6 = Conv2D(64, 2)(UpSampling2D(size=(2, 2))(conv5))
    merge6 = concatenate([conv2, up6], axis=3)
    conv6 = Conv2D(64, 3)(merge6)
    conv6 = Conv2D(64, 3)(conv6)

    up7 = Conv2D(32, 2)(UpSampling2D(size=(2, 2))(conv6))
    merge7 = concatenate([conv1, up7], axis=3)
    conv7 = Conv2D(32, 3)(merge7)
    conv7 = Conv2D(32, 3)(conv7)
    conv7 = Conv2D(2, 3)(conv7)
    conv8 = _Conv2D(n_classes, 1, activation=activation)(conv7)

    model = Model(inputs=inputs, outputs=conv8)

    if metrics is None:
        metrics = ["accuracy"]

    model.compile(optimizer=Adam(lr=learning_rate), loss=loss, metrics=metrics)

    model.name = "SmallUNet"
    return model
