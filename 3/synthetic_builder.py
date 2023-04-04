import os
import json
from PIL import Image
import random
import cv2                                      # opencv
import numpy as np                              # numpy
import matplotlib.pyplot as plt                 # sottomodulo pyplot di matplotlib
from mpl_toolkits.axes_grid1 import ImageGrid   # classe per la creazione di griglie immagini



class SyntheticBuilder:
        
    def __init__(self, json_path):
        file = open(json_path)
        data = json.load(file)
        self.as_png = data["params"]["as_png"]
        self.as_npz = data["params"]["as_npz"]
        self.output_folder = data["folders"]["out"]
        self.output_size = data["synth_image"]["output_size"]

        self.validation_objects = int(data["params"]["number_of_synthetic_objects"]*data["params"]["validation_percentage"])
        self.test_objects = int(data["params"]["number_of_synthetic_objects"]*data["params"]["test_percentage"])
        self.training_objects = int(data["params"]["number_of_synthetic_objects"] - self.test_objects - self.validation_objects)

        self.use_square, self.use_triangle, self.use_circle, self.use_pentagone, self.do_rotation, self.do_scaling, self.do_translation, self.do_flip = data["colored_shapes"].values()
        self.shapes_list = []
        if data["colored_shapes"]["use_square"]:
            self.shapes_list.append("square")
        if data["colored_shapes"]["use_circle"]:
            self.shapes_list.append("circle")
        if data["colored_shapes"]["use_triangle"]:
            self.shapes_list.append("triangle")
        return       

    def __create_synthetic_object(self):
        shape = random.choice(self.shapes_list)
        x = random.randint(50, 205)
        y = random.randint(0, 255)
        size = random.randint(50, 100)
        if shape == "circle":
            img = np.zeros(self.output_size, np.uint8)
            img = cv2.circle(img,(x,y), size, (0,255,0), -1)
        elif shape == "triangle":
            pts = np.array([[x,y], [x+size,y], [x+size/2,y-size]], np.int32)
            img = np.zeros(self.output_size, np.uint8)
            img = cv2.fillPoly(img,[pts],(0,0,255))
        elif shape == "square":
            img = np.zeros(self.output_size, np.uint8)
            img = cv2.rectangle(img,(x,y),(x+size,y+size),(0,255,255),-1)
        return img

    def __apply_preprocessing(self, img):
        if self.do_rotation:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        if self.do_scaling:
            img = cv2.resize(img, (0, 0), fx=2, fy=2)
        if self.do_translation:
            img = cv2.warpAffine(img, np.float32([[1,0,50],[0,1,25]]), (img.shape[1], img.shape[0]))
        if self.do_flip:
            img = cv2.flip(img, 0) # 0 for horizontal flip, 1 for vertical flip
        return img
    
    def __save_on_disk(self, img, i, folder):
        if(self.as_png):
                img_path = self.output_folder + "/output/"+ folder + "/" + str(i) + '.' + "png"
                cv2.imwrite(img_path, img)
        if(self.as_npz):
            img_array = np.asarray(img)
            np.savez(self.output_folder + "/output/" + folder + "/" + str(i) + '.' + "npz", data=img_array) 
        
    def build(self):
        for x in range(self.training_objects):
            img = self.__create_synthetic_object()
            processed_img = self.__apply_preprocessing(img)
            self.__save_on_disk(processed_img, x, "training")
        for y in range(self.test_objects):
            img = self.__create_synthetic_object()
            processed_img = self.__apply_preprocessing(img)
            self.__save_on_disk(processed_img, y, "test")
        for z in range(self.validation_objects):
            img = self.__create_synthetic_object()
            processed_img = self.__apply_preprocessing(img)
            self.__save_on_disk(processed_img, z, "validation")
        return
    
    def get_objects(self):
        print("Immagini di validazione: " + str(self.validation_objects))
        print("Immagini di test: " + str(self.test_objects))
        print("Immagini di training: " + str(self.training_objects))

    

if __name__ == '__main__':
    
    SB = SyntheticBuilder('./data.json')
    SB.get_objects()
    SB.build()
   
