import cv2                                      # opencv
import numpy as np                              # numpy
import matplotlib.pyplot as plt                 # sottomodulo pyplot di matplotlib
from mpl_toolkits.axes_grid1 import ImageGrid   # classe per la creazione di griglie immagini



class IM:
        
    def read_as_is(paths):
        images_list = []
        if isinstance(paths, list):
            for path in paths:
                images_list.append(cv2.imread(path))
            return images_list
        else:
            return cv2.imread(paths)
    
    def read_as_color(paths):
        images_list = []
        if isinstance(paths, list):
            for path in paths:
                images_list.append(cv2.imread(path, cv2.IMREAD_COLOR))
            return images_list
        else:
            return cv2.imread(paths, cv2.IMREAD_COLOR)

    def read_as_mono(paths):
        images_list = []
        if isinstance(paths, list):
            for path in paths:
                images_list.append(cv2.imread(path, cv2.IMREAD_GRAYSCALE))
            return images_list
        else:
            return cv2.imread(paths, cv2.IMREAD_GRAYSCALE)   
        
    def to_disk(img, name, type, path):
        full_path = path + name + '.' + type
        cv2.imwrite(full_path, img)

    def get_info(image):
        info = image.shape
        print(f'Dimensioni:\t{info}')

    def show(img):
        plt.imshow(img)
        plt.show()

    def as_rgb(images):
        images_list = []
        if isinstance(images, list):
            for img in images:
                images_list.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            return images_list
        else:
            return cv2.cvtColor(images, cv2.COLOR_BGR2RGB)

    def as_bgr(images):
        images_list = []
        if isinstance(images, list):
            for img in images:
                images_list.append(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            return images_list
        else:
            return cv2.cvtColor(images, cv2.COLOR_RGB2BGR)

    def print_plane(img, int):
        match int:
            case 0:
                print(f'Larghezza:\t{img.shape[int]}')
            case 1:
                print(f'Altezza:\t{img.shape[int]}')
            case 2:
                print(f'Numero di canali:\t{img.shape[int]}')
        
    def merge(planes):
        merged_img = cv2.merge(planes)              
        plt.imshow(merged_img)
        plt.show()

    def grid(images : list[np.array], rows : int, cols : int, size : int, colors : list[str] = None) -> None:
        fig = plt.figure(figsize=(size,size))
        grid = ImageGrid(fig, 111, nrows_ncols=(rows, cols), axes_pad=0.1)
        if colors is not None:
            counter = 0
            for ax, im in zip(grid, images):
                ax.imshow(im, cmap=colors[counter])
                counter = (counter + 1) % len(colors)
            plt.show()
        else:
            for ax, im in zip(grid, images):
                ax.imshow(im)
            plt.show()


if __name__ == '__main__':
    
    imgdefault = IM.read_as_is("./imgs/pig/color.png")
    imgcolor = IM.read_as_color("./imgs/pig/color.png")
    imggray = IM.read_as_mono("./imgs/pig/color.png")
    IM.show(imgdefault)
    IM.show(imgcolor)
    IM.show(imggray)
    IM.print_plane(imgdefault, 0)

    lista_percorsi = ['./imgs/rgb/b.png', './imgs/rgb/g.png', './imgs/rgb/r.png' ]
    lista_immagini = IM.read_as_mono(lista_percorsi)
    IM.show(lista_immagini[0])
    IM.show(lista_immagini[1])
    IM.show(lista_immagini[2])
    IM.merge(lista_immagini)

    IM.get_info(imgdefault)
    IM.get_info(imgcolor)
    IM.get_info(imggray)    

    lista_immagini_convertite = IM.as_bgr([imgdefault, imgcolor, imggray])
    IM.show(lista_immagini_convertite[0])
    IM.show(lista_immagini_convertite[1])
    IM.show(lista_immagini_convertite[2])

    IM.grid([lista_immagini_convertite[0], lista_immagini_convertite[1], lista_immagini_convertite[2]], 1, 3, 1)
    
