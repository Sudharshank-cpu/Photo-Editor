# Importing Modules
import os
from PIL import Image, ImageFilter, ImageEnhance
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QComboBox,QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# Creating Main Application
app=QApplication([])
mainWindow=QWidget()
mainWindow.setWindowTitle("Photo Editor with QT")
mainWindow.resize(900,700)

# Creating Widgets
btnFolder = QPushButton("Folder")
fileList = QListWidget()
btnLeft = QPushButton("Left")
btnRight = QPushButton("Right")
mirror = QPushButton("Mirror")
sharpness = QPushButton("Sharpness")
grey = QPushButton("Black/White")
saturation = QPushButton("Color")
contrast = QPushButton("Contrast")
blur = QPushButton("Blur")

# Adding Filter Box Items
filterBox = QComboBox()
filterBox.addItem("Original")
filterBox.addItem("Left")
filterBox.addItem("Right")
filterBox.addItem("Mirror")
filterBox.addItem("Sharpness")
filterBox.addItem("Black/White")
filterBox.addItem("Color")
filterBox.addItem("Contrast")
filterBox.addItem("Blur")
pictureBox = QLabel("Image will appear here")

# Designing Layout
masterLayout = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btnFolder)
col1.addWidget(fileList)
col1.addWidget(filterBox)
col1.addWidget(btnLeft)
col1.addWidget(btnRight)
col1.addWidget(mirror)
col1.addWidget(sharpness)
col1.addWidget(grey)
col1.addWidget(saturation)
col1.addWidget(contrast)
col1.addWidget(blur)
col2.addWidget(pictureBox)
masterLayout.addLayout(col1,20) #Second Argument is Stretch 
masterLayout.addLayout(col2,80)
mainWindow.setLayout(masterLayout)

# Adding files to Filter Box
def filter(files, extensions):
    results=[]
    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                results.append(file)
    return results

# Gathering Work Directory
workingDirectory=""
def getWorkDirectory():
    global workingDirectory
    workingDirectory=QFileDialog.getExistingDirectory()
    extensions=['.jpg', '.jpeg', '.png', '.svg']
    filenames=filter(os.listdir(workingDirectory), extensions)
    fileList.clear()
    for filename in filenames:
        fileList.addItem(filename)

# Editor Class to Edit and Save Images
class Editor():
    def __init__(self):
        self.image=None
        self.original=None
        self.filename=None
        self.saveFolder="edits/"

    # Loads the Image
    def loadImage(self, filename):
        self.filename=filename
        fullname=os.path.join(workingDirectory, self.filename)
        self.image=Image.open(fullname)
        self.original=self.image.copy()

    # Saves the Image
    def saveImage(self):
        path=os.path.join(workingDirectory, self.saveFolder)
        if not os.path.exists(path):
            os.mkdir(path)
        fullname=os.path.join(path, self.filename)
        self.image.save(fullname)

    # Shows the Image
    def showImage(self, path):
        pictureBox.hide()
        image=QPixmap(path)
        w,h=pictureBox.width(), pictureBox.height()
        image=image.scaled(w, h, Qt.KeepAspectRatio)
        pictureBox.setPixmap(image)
        pictureBox.show()

    # Transform the Image
    def transformImage(self, transformation):
        transformations={
            "Black/White":lambda image: image.convert("L"),
            "Color":lambda image: ImageEnhance.Color(image).enhance(1.2),
            "Contrast": lambda image: ImageEnhance.Contrast(image).enhance(1.2),
            "Blur": lambda image: image.filter(ImageFilter.BLUR),
            "Left": lambda image: image.transpose(Image.ROTATE_90),
            "Right": lambda image: image.transpose(Image.ROTATE_270),
            "Mirror": lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
            "Sharpness": lambda image: image.filter(ImageFilter.SHARPEN)
        }
        transformFunction=transformations.get(transformation)
        if transformFunction:
            self.image=transformFunction(self.image)
            self.saveImage()
        self.saveImage()
        imagePath=os.path.join(workingDirectory, self.saveFolder, self.filename)
        self.showImage(imagePath)

    # Apply Filters to Image
    def applyFilter(self,filterName):
        if filterName=="Original":
            self.image=self.original.copy()
        else:
            filterMap={
                "B/W":lambda image: image.convert("L"),
                "Color":lambda image: ImageEnhance.Color(image).enhance(1.2),
                "Contrast": lambda image: ImageEnhance.Contrast(image).enhance(1.2),
                "Blur": lambda image: image.filter(ImageFilter.BLUR),
                "Left": lambda image: image.transpose(Image.ROTATE_90),
                "Right": lambda image: image.transpose(Image.ROTATE_270),
                "Mirror": lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
                "Sharpness": lambda image: image.filter(ImageFilter.SHARPEN)
            }
            filterFunction=filterMap.get(filterName)
            if filterFunction:
                self.image=filterFunction(self.image)
                self.saveImage()
                imagePath=os.path.join(workingDirectory, self.saveFolder, self.filename)
                self.showImage(imagePath)
            pass
        self.saveImage()
        imagePath=os.path.join(workingDirectory, self.saveFolder, self.filename)
        self.showImage(imagePath)

# Handles Filters
def handleFilter():
    if fileList.currentRow()>=0:
        selectFilter=fileList.currentItem()
        main.applyFilter(selectFilter)

# Display the Image
def displayImage():
    if fileList.currentRow()>=0:
        filename=fileList.currentItem().text()
        main.loadImage(filename)
        main.showImage(os.path.join(workingDirectory, main.filename))
 
main = Editor()

# Trigger Events
btnFolder.clicked.connect(getWorkDirectory)
fileList.currentRowChanged.connect(displayImage)
filterBox.currentTextChanged.connect(handleFilter)

grey.clicked.connect(lambda: main.transformImage("B/W"))
btnLeft.clicked.connect(lambda: main.transformImage("Left"))
btnRight.clicked.connect(lambda: main.transformImage("Right"))
sharpness.clicked.connect(lambda: main.transformImage("Sharpness"))
saturation.clicked.connect(lambda: main.transformImage("Color"))
contrast.clicked.connect(lambda: main.transformImage("Contrast"))
blur.clicked.connect(lambda: main.transformImage("Blur"))
mirror.clicked.connect(lambda: main.transformImage("Mirror"))

# Show and Execute the App
mainWindow.show()
app.exec_()
