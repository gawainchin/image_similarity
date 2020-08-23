import os
import numpy as np
import imagehash
from PIL import Image
import argparse

def parseArgs(argv=None):
    parser = argparse.ArgumentParser(description="Image Similarity Args")
    parser.add_argument('-p', '--path', type=str, help='path')
    parser.add_argument('-thres', '--threshold', type=int, default=10, help="hash threshold")
    return parser.parse_args(argv)

class imageHash:
    def __init__(self, BASEPATH, threshold=10):
        self.BASEPATH = BASEPATH
        self.imagePaths = [os.path.join(BASEPATH, i) for i in os.listdir(BASEPATH) if "jpeg" in i]
        self.threshold = threshold
        self.returns = []

    def image_hash(self):
        returns = self.returns
        expepts = []
        threshold = self.threshold
        imagePaths = self.imagePaths

        for ix in range(len(imagePaths)):
            if ix in expepts:
                continue
            similar = []
            hash1 = imagehash.average_hash(Image.open(imagePaths[ix]))
            similar.append(imagePaths[ix])
            expepts.append(ix)
            for ox in range(ix+1 ,len(imagePaths)):
                if ox in expepts:
                    continue
                hash2 = imagehash.average_hash(Image.open(imagePaths[ox]))
                if (hash1 - hash2) < threshold:
                    similar.append(imagePaths[ox])
                    expepts.append(ox)
            returns.append(similar)
        return returns
    
    def save_returns(self):
        returns = self.returns
        BASEPATH = self.BASEPATH

        for i in range(len(returns)):
            NEW_FOLDERPATH = os.path.join(BASEPATH, "SORTED", str(i))
            if os.path.exists(NEW_FOLDERPATH):
                raise Exception("Target File: ./SORTED already exists")
            os.makedirs(NEW_FOLDERPATH)
            for file in returns[i]:
                os.system("cp {0} {1}".format(file, os.path.join(NEW_FOLDERPATH, file.split("/")[-1])))
        print("Program Done")

if __name__ == "__main__":
    args = parseArgs()
    imageH = imageHash(args.path, args.threshold)
    imageH.image_hash()
    imageH.save_returns()
