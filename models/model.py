from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
import tensorflow as tf
import numpy as np
from sklearn.model_selection import *
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import confusion_matrix
import seaborn as sns
from matplotlib import pyplot as plt
import json


def create_model_gru(input_shape, num_classes):
    model = Sequential()
    model.add(TimeDistributed(
        Conv2D(32, (3, 3), activation='relu', padding='same')))
    model.add(TimeDistributed(BatchNormalization()))
    model.add(TimeDistributed(Flatten()))
    model.add(Bidirectional(GRU(128, return_sequences=False)))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=[
                  'accuracy'])  # Use 'sparse_categorical_crossentropy' for integer labels
    return model


def data_generator(x_data, y_data, batch_size):
    num_samples = len(x_data)
    while True:
        for offset in range(0, num_samples, batch_size):
            batch_x = x_data[offset:offset+batch_size]
            batch_y = y_data[offset:offset+batch_size]
            yield batch_x, batch_y


def get_class_weights(y_train, num_classes):
    class_weights = compute_class_weight(class_weight='balanced',
                                         classes=np.arange(num_classes),
                                         y=y_train)  # No need for np.argmax since y_train is integer labels
    return dict(enumerate(class_weights))


data = np.load('reduced_normalized_data3.npz', allow_pickle=True)
xData_padded = data['xData']
y_mapped = data['yData']
# xData_padded = xData_padded.reshape(
#     (xData_padded.shape[0], xData_padded.shape[1], xData_padded.shape[2], 4, 1))
x_train, x_test, y_train, y_test = train_test_split(
    xData_padded, y_mapped, test_size=0.2, stratify=y_mapped, random_state=42)
num_classes = len(np.unique(y_train))
class_weights = get_class_weights(y_train, num_classes)
# print(f"Class weights: {class_weights}")


batch_size = 32

# Create training and validation generators
train_generator = data_generator(x_train, y_train, batch_size)
test_generator = data_generator(x_test, y_test, batch_size)

# Get the input shape based on your data
# Adjust height and width according to your reshaping
input_shape = (xData_padded.shape[1], xData_padded.shape[2], 4, 1)

# Create the GRU model
model = create_model_gru(input_shape, num_classes)

checkpoint = ModelCheckpoint(
    'best_model.keras', monitor='val_accuracy', save_best_only=True, mode='max')

# Early stopping to prevent overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=3)

# A dummy input for building the model
dummy_input = tf.random.normal((1, 145, 75, 4, 1))
model(dummy_input)  # This will build the model


print(model.summary())

# Add the callbacks to the training
history = model.fit(train_generator,
                    steps_per_epoch=len(x_train) // batch_size,
                    validation_data=test_generator,
                    validation_steps=len(x_test) // batch_size,
                    epochs=100,
                    class_weight=class_weights,
                    callbacks=[checkpoint, early_stopping])

# Step 1: Evaluate the model on the test data
loss, accuracy = model.evaluate(
    test_generator, steps=len(x_test) // batch_size)
print(f"Test Loss: {loss}")
print(f"Test Accuracy: {accuracy}")

# Step 2: Plot training & validation loss and accuracy
# Plot training & validation loss
plt.figure(figsize=(12, 6))

# Subplot 1: Loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], color='r')
plt.plot(history.history['val_loss'], color='b')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Validation'], loc='upper right')

# Subplot 2: Accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], color='r')
plt.plot(history.history['val_accuracy'], color='b')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Validation'], loc='upper left')

plt.show()

# Step 3: Predict the test data
# Use the test generator to get predictions
y_pred = model.predict(test_generator, steps=len(x_test) // batch_size)
y_pred_classes = np.argmax(y_pred, axis=1)  # Get the predicted class indices

# Step 4: Prepare true labels
# If y_test is already in integer form, use it directly.
# If y_test is one-hot encoded, convert it to class indices.
# Uncomment the appropriate line based on your data format:
# y_true = y_test  # If y_test is already in integer form
y_true = np.array(y_test)  # Ensure y_test is in a NumPy array if it was a list

# If y_test is one-hot encoded, uncomment the next line:
# y_true = np.argmax(y_test, axis=1)

# Compute the confusion matrix
cm = confusion_matrix(y_true, y_pred_classes)

# Load the label-to-class index mapping from the JSON file
with open('label_to_class_index.json', 'r') as f:
    label_to_class_index = json.load(f)

# Print the loaded mapping to verify (optional)
# print(label_to_class_index)

# Prepare words for plotting confusion matrix
words = [label for label, index in label_to_class_index.items()]

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=words, yticklabels=words)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()
