#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author   : Serena Bonaretti
license  : GPL GNU v3.0
email    : serena.bonaretti.research@gmail.com
"""

"""
This module contains functions to and write files
"""

import SimpleITK as sitk



def write_mha_image(img, file_name, keys = None, values=None):

    """
    This function saves a SimpleITK image to metafile (.mha) adding metadata if present
    Inputs:
        - img: image to save (type: SimpleITK image)
        - file_name: file name of the image file to be written (type: str)
        - keys: keys of the metadata. It is an optional argument (type: list of string)
        - value: values of the metadata. It is an optional argument (type: list of string)
    """

    # if there are no keys nor values, just write the image
    if keys==None and values==None:
        print ("The image will be saved with no header information")

    # if keys and values do not have the same length, print out an error and stop the function
    else:
        if len(keys) != len(values):
            print ("The lists do not have the same length: keys contains " + str(len(keys)) + " elements, \
                   whereas values contains "  + str(len(values)) + "elements" )
            return

        # add metadata to the image
        else:
            for i in range(0,len(keys)):
                img.SetMetaData(str(keys[i]), str(values[i]))

    # write image
    sitk.WriteImage(img, file_name)
