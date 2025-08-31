import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Path ke dataset
dataset_dir = 'dataset'  # Ganti dengan path dataset Anda

# Menggunakan ImageDataGenerator untuk augmentasi data
train_datagen = ImageDataGenerator(
    rescale=1./255,           # Normalisasi gambar
    rotation_range=30,        # Rotasi acak gambar
    width_shift_range=0.2,    # Geser gambar secara horizontal
    height_shift_range=0.2,   # Geser gambar secara vertikal
    shear_range=0.2,          # Menerapkan shear transformasi
    zoom_range=0.2,           # Zoom gambar
    horizontal_flip=True,     # Membalik gambar secara horizontal
    fill_mode='nearest'       # Mengisi piksel yang hilang dengan cara terdekat
)

train_generator = train_datagen.flow_from_directory(
    dataset_dir,            # Path ke dataset
    target_size=(150, 150), # Ukuran gambar
    batch_size=32,
    class_mode='binary'     # Dua kelas: kucing atau ayam
)

# Membuat model CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),  # Dropout untuk menghindari overfitting
    Dense(1, activation='sigmoid')  # Output biner: 0 untuk kucing, 1 untuk ayam
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Callback untuk menyimpan model terbaik
checkpoint = ModelCheckpoint('deteksi_hewan_model.h5', 
                             monitor='val_loss', 
                             save_best_only=True, 
                             mode='min', 
                             verbose=1)

# Callback untuk menghentikan pelatihan lebih awal jika model berhenti meningkatkan akurasi
early_stopping = EarlyStopping(monitor='val_loss', 
                               patience=5, 
                               restore_best_weights=True, 
                               verbose=1)

# Melatih model
history = model.fit(
    train_generator,
    epochs=20,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    callbacks=[checkpoint, early_stopping],
    validation_data=train_generator,  # Anda bisa menambahkan data validasi jika tersedia
    validation_steps=train_generator.samples // train_generator.batch_size
)

# Menyimpan model yang sudah dilatih (jika belum menggunakan checkpoint)
model.save('deteksi_hewan_model.h5')
