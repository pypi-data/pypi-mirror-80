#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author   : Serena Bonaretti
license  : GPL GNU v3.0
email    : serena.bonaretti.research@gmail.com
"""


"""
This module contains functions to visualize Scanco images

"""


import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk

from ipywidgets import * # for display
from ipywidgets import HBox, VBox
from ipywidgets import interactive
from ipywidgets import Layout
from ipywidgets import widgets as widgets


def show_sitk_slice(img, slice_id = -1, plane = "a"):

    """
    Shows one slice of an image. Slice id and plane are optional argument
    Inputs:
        - img: 3D image (type: SimpleITK)
        - slice_id: id of the slice to visualize. It is an optional argument. If not specified, the function shows the slice in the middle of the stack (type: integer)
        - plane: radiological plane to visualize. It is an optional argument with three options:
          - "a", for axial
          - "v", for vertical
          - "h", for horizontal
          If not specified, the function shows the slice in the axial plane. (type: string)
          More information on radiological planes for .isq images here: https://github.com/JCMSK/pyMSK/blob/master/doc/img/isq_image_directions.pdf
    """
    
    # --- checking inputs ----------------------------------------------------
    
    # check image file type
    if not isinstance(img, sitk.SimpleITK.Image):
        print ("Error: Supported image formats is SimpleITK")
        return 
               
    # check that the plane is either f, s, or a
    if plane != "v" and plane != "h" and plane != "a":
        print ("plane must be \"a\", \"v\" or \"h\"  ")
        return  
        
    # get number of voxels
    size_s = img.GetSize()[0] 
    size_a = img.GetSize()[1]
    size_f = img.GetSize()[2] 
             
    # get slice_id
    if   slice_id == -1 and plane == "v":
        slice_id = round(size_s / 2)
    elif slice_id == -1 and plane == "h":
        slice_id = round(size_a / 2)
    elif slice_id == -1 and plane == "a":
        slice_id = round(size_f / 2)
    else:
        slice_id = round(slice_id) # if the user enters a decimal, round it
       
    # check that slice_id is in range  
    if plane == "v":
        if slice_id <=0 or slice_id >= size_s:
            print ("slice_id out of range")
            return
    if plane == "h":
        if slice_id <=0 or slice_id >= size_a:
            print ("slice_id out of range")
            return
    if plane == "a":
        if slice_id <=0 or slice_id >= size_f:
            print ("slice_id out of range")
            return
    
    
    # --- preparing slice for visualization ----------------------------------   
    
    # get slice
    if   plane == "v":
        sitk_slice = img[slice_id,:,:] 
    elif plane == "h":
        sitk_slice = img[:,slice_id,:]
    elif plane == "a":
        sitk_slice = img[:,:,slice_id]
        
    # transform slice from SimpleITK to numpy
    np_slice = sitk.GetArrayViewFromImage(sitk_slice)

    # --- plotting with matplotlib -------------------------------------------
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.imshow(np_slice, 'gray', interpolation=None)
    ax.set_title("Slice " + str(slice_id))
    ax.axis('off')

    return 



def browse_sitk_image (img, plane = "a"):

    """
    This function allows the user to browse an image using a slider
    Inputs:
    - img: 3D image (type: SimpleITK)
    - plane: radiological plane to visualize. It is an optional argument with three options:
      - "a", for axial
      - "v", for vertical
      - "h", for horizontal
      If not specified, the function shows the slice in the axial plane. (type: string)
      More information on radiological planes for .isq images here: https://github.com/JCMSK/pyMSK/blob/master/doc/img/isq_image_directions.pdf
    """
    
    
    # -- checking inputs -----------------------------------------------------
    
    # check image file type
    if not isinstance(img, sitk.SimpleITK.Image):
        print ("Error: Supported image formats is SimpleITK")
        return 
               
    # check that the plane is either f, s, or a
    if plane != "v" and plane != "h" and plane != "a":
        print ("plane must be \"a\", \"v\" or \"h\"  ")
        return  


    # -- preparing image for visualization -----------------------------------
    
    # get number of voxels
    size_s = img.GetSize()[0] 
    size_a = img.GetSize()[1]
    size_f = img.GetSize()[2]
        
    # get first_slice_viz
    if   plane == "v":
        first_slice_viz = round(size_s / 2)
        n_of_slices = size_s
    elif plane == "h":
        first_slice_viz = round(size_a / 2)
        n_of_slices = size_a
    elif plane == "a":
        first_slice_viz = round(size_f / 2)
        n_of_slices = size_f


    # transform img from SimpleITK to numpy 
    np_img = sitk.GetArrayViewFromImage(img)
   

    # --- function for slider ------------------------------------------------
    def view_image(slider):

        # get slice of image
        if   plane == "v":
            slice_np_img = np_img[:,:,slider] 
        elif plane == "h":
            slice_np_img = np_img[:,slider,:]
        elif plane == "a":  
            slice_np_img = np_img[slider,:,:]        

        # show both
        plt.imshow(slice_np_img, cmap=plt.cm.gray,interpolation=None)
        plt.axis('off')


    # link sliders and its function
    slider_image = interactive(view_image,
                         slider = widgets.IntSlider(  min     = 0,
                                                      max     = n_of_slices-1,
                                                      value   = first_slice_viz,
                                                      step    = 1,
                                                      layout  = Layout(width='180px'),
                                                      readout = False,
                                                      continuous_update = False, # avoids intermediate image display,
                                                      description       = 'Slice n.'))
    # show figures before start interacting
    slider_image.update()

    # slice number scrolling
    text = widgets.BoundedIntText( min    = 0,
                                   max    = n_of_slices-1,
                                   value  = first_slice_viz,
                                   step   = 1,
                                   layout = Layout(width='50px'),
                                   continuous_update = False,
                                   description       = "") # BoundedIntText to avoid that displayed text goes outside of the range)

    # link slider and text
    widgets.jslink((slider_image.children[:-1][0], 'value'), (text, 'value'))

    # layout
    slider_box   = HBox(slider_image.children[:-1])
    widget_box   = HBox([slider_box, text])
    whole_box    = VBox([widget_box, slider_image.children[-1] ])

    return whole_box


