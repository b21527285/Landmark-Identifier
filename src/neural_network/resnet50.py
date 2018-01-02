from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
import keras
from keras.optimizers import SGD
import os
import glob

train_dir = 'C:/Users/Mavi/PycharmProjects/wc/images2/images_train/'
test_dir = 'C:/Users/Mavi/PycharmProjects/wc/images2/images_test/'

def get_nb_files(directory):
    """Get number of files by searching directory recursively"""
    if not os.path.exists(directory):
        return 0
    cnt = 0
    for r, dirs, files in os.walk(directory):
        for dr in dirs:
            cnt += len(glob.glob(os.path.join(r, dr + "/*")))
    return cnt

nb_train_samples = get_nb_files(train_dir)
nb_test_samples = get_nb_files(test_dir)
nb_classes = len(glob.glob(train_dir + "/*"))
nb_epoch = 200
batch_size = 64

train_datagen = ImageDataGenerator(
    rescale=1./255,
    preprocessing_function=preprocess_input,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(
    rescale=1./255,
    preprocessing_function=preprocess_input,
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224,224),
    batch_size=batch_size
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224,224),
    batch_size=batch_size
)

# create the base pre-trained model
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224,224,3))

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# and a logistic layer -- let's say we have 176 classes
predictions = Dense(176, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
'''for i, layer in enumerate(base_model.layers):
   print(i, layer.name)'''

for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
#sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
#model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

# train the model on the new data for a few epochs
model.load_weights("weights_res50.E018-L1.13-A0.708.hdf5")

'''check_point_file = "weights.E{epoch:03d}-L{loss:.2f}-A{acc:.3f}.hdf5" //already done
check_point = keras.callbacks.ModelCheckpoint(filepath=check_point_file,
                                                  monitor='val_acc',
                                                  verbose=1
                                                  )
model.fit_generator(
        generator=train_generator,
        steps_per_epoch=nb_train_samples/64,
        epochs=5,
        class_weight='auto',
        callbacks=[check_point],
        validation_data=test_generator,
        shuffle=True,
        verbose=1
    )'''
#model.save("modelres50.h5")
# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.

# let's visualize layer names and layer indices to see how many layers
# we should freeze:

# we chose to train the top 2 inception blocks, i.e. we will freeze
# the first 249 layers and unfreeze the rest:

for layer in model.layers[:153]:
   layer.trainable = False
for layer in model.layers[153:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate

sgd = SGD(lr=0.001, momentum=0.9)
model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
try:

    check_point_file = "weights_res50.E{epoch:03d}-L{loss:.2f}-A{acc:.3f}.hdf5"
    check_point = keras.callbacks.ModelCheckpoint(filepath=check_point_file,
                                                  monitor='val_acc',
                                                  verbose=1
                                                  )
    # Start Fine-tuning
    model.fit_generator(
            generator=train_generator,
            steps_per_epoch=nb_train_samples/64,
            epochs=nb_epoch,
            class_weight='auto',
            callbacks=[check_point],
            validation_data=test_generator,
            shuffle=True,
            verbose=1
    )

    model.save("model.h5")
except Exception as e:
    print(e)
    model.save("model.h5")
