import csv
from PIL import Image
from ho import pisa
import qrcode

__author__ = 'schannak'

import numpy

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)



if __name__ == '__main__':
    reader = csv.reader(open("code_list.csv", "rb"))

    code_list = []

    #to convert csv data to real string without quotes and brackets
    for row in reader:
        row = "".join(row)
        code_list.append(row)

    for row in code_list:

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(row[0])
        qr.make(fit=True)

        img = qr.make_image()
        #saves qr-code to directory qr-codes
        img.save('qr-codes/%s.png' % row)
        file = Image.new("RGB", (512, 512), "white")
        labelbag = Image.open("scantobuy_logo_no_qr.jpg")
        file.paste(labelbag, (-60,20))
        size = 170, 170

        """
        width, height = img.size
        m = -0.5
        xshift = abs(m) * width
        new_width = width + int(round(xshift))
        img = img.transform((new_width, height), Image.AFFINE,
                (1, m, -xshift if m > 0 else 0, 0, 1, 0), Image.BICUBIC)
        """
        img.thumbnail(size, Image.ANTIALIAS)

        file.paste(img, (190,150))
        file.save('qr-code-labelbags/%s.png' % row)

        size = 256, 256
        file.thumbnail(size, Image.ANTIALIAS)
        file.save('qr-code-labelbags-small/%s.png' % row)



    # convert HTML to PDF
    sourceHtml = "<html><body><p>"
    counter = 0
    for row in code_list:
        sourceHtml += "<img src='qr-code-labelbags-small/%s.png'>" % row
        counter += 1
        if counter % 3 == 0:
            sourceHtml += "<br/>"
    sourceHtml += "<p></body></html>"
    print sourceHtml
    outputFilename = "test.pdf"

    resultFile = open(outputFilename, "w+b")
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file