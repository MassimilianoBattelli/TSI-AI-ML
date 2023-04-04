import os
from PIL import Image
import cv2                                      # opencv
import numpy as np                              # numpy
import matplotlib.pyplot as plt                 # sottomodulo pyplot di matplotlib
from mpl_toolkits.axes_grid1 import ImageGrid   # classe per la creazione di griglie immagini



class PI:
        
    def __init__(self, input, output):
        if not self.__check_input_parameters(input):
            raise TypeError("invalid input path")
        if not self.__check_output_parameters(output):
            raise TypeError("invalid output path")
        self.input = input
        self.output = output
        self.l, self.r, self.s, self.t = False, False, False, False
        
    def __check_input_parameters(self, path):
        files = os.listdir(path)
        if not os.path.isdir(path):
            return False
        if not files:
            return False
        for file in files:
            allowed_extensions = {".bpm", ".png", ".jpg", ".jpeg"}
            file_path = os.path.join(path, file)
            extension = os.path.splitext(file_path)[1].lower()
            if extension in allowed_extensions:
                return True
            else:
                return False
            
    def __check_output_parameters(self, path):
        if not os.path.isdir(path):
            return False
        else:
            return True
    
    def __change_lum(self):
        print("Change lum in esecuzione:")
        i = len(os.listdir(self.output)) + 1
        for file in os.listdir(self.input):
            file_path = os.path.join(self.input, file)
            img = cv2.imread(file_path, cv2.IMREAD_COLOR)
            processed_img = cv2.convertScaleAbs(img, alpha=2, beta=0)
            output_img_path = self.output+ "/"+ str(i) + '.' + "png"
            cv2.imwrite(output_img_path, processed_img)
            print("Immagine " + str(i) +  " processata")
            i = i + 1
        print("Completato")
        return
    
    def __rotate (self):
        print("Rotate in esecuzione:")
        i = len(os.listdir(self.output)) + 1
        for file in os.listdir(self.input):
            file_path = os.path.join(self.input, file)
            img = cv2.imread(file_path, cv2.IMREAD_COLOR)
            processed_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            output_img_path = self.output+ "/"+ str(i) + '.' + "png"
            cv2.imwrite(output_img_path, processed_img)
            print("Immagine " + str(i) +  " processata")
            i = i + 1
        print("Completato")
        return
    
    def __scale(self):
        print("Scale in esecuzione:")
        i = len(os.listdir(self.output)) + 1
        for file in os.listdir(self.input):
            file_path = os.path.join(self.input, file)
            img = cv2.imread(file_path, cv2.IMREAD_COLOR)
            processed_img = cv2.resize(img, (0, 0), fx=1.5, fy=1.5)
            output_img_path = self.output+ "/"+ str(i) + '.' + "png"
            cv2.imwrite(output_img_path, processed_img)
            print("Immagine " + str(i) +  " processata")
            i = i + 1
        print("Completato")
        return
    
    def __translate(self):
        print("Translate in esecuzione:")
        i = len(os.listdir(self.output)) + 1
        for file in os.listdir(self.input):
            file_path = os.path.join(self.input, file)
            img = cv2.imread(file_path, cv2.IMREAD_COLOR)
            rows, cols = img.shape[0], img.shape[1]  
            transformation_matrix = np.float32([[1,0,50],[0,1,25]])                                                                                                                                  
            processed_img = cv2.warpAffine(img, transformation_matrix, (cols, rows))
            output_img_path = self.output+ "/"+ str(i) + '.' + "png"
            cv2.imwrite(output_img_path, processed_img)
            print("Immagine " + str(i) +  " processata")
            i = i + 1
        print("Completato")
        return
    
    def do_change_lum(self, exec):
        self.l = True if exec else False
        
    def do_rotation(self, exec):
        self.r = True if exec else False

    def do_scaling(self, exec):
        self.s = True if exec else False
        
    def do_translation(self, exec):
        self.t = True if exec else False

    def compute(self):
        self.__change_lum() if self.l else None
        self.__rotate() if self.r else None
        self.__scale() if self.s else None
        self.__translate() if self.t else None
        return       
        
if __name__ == '__main__':
    
    preprocessor = PI("./input", "./output")
    preprocessor.do_change_lum(True)
    preprocessor.do_rotation(True)
    preprocessor.do_scaling(True)
    preprocessor.do_translation(True)
    preprocessor.compute()

    
