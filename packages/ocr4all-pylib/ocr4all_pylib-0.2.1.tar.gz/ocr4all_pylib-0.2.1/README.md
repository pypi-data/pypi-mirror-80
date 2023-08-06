# ocr4all-pylib - common code for ocr4all related python projects

This package contains code used by several projects related to [OCR4all][1].

## Image to label mapping

For several classifiers, the file format of training and output data is images,
while the internal format is a 2d matrix with a very small range of values
(numbers denoting different labels).

The ImageMap class converts between color image representations and label matrices both ways.
It also provides JSON reading and writing of mappings between colors and labels.


[1]: https://github.com/OCR4all/OCR4all
