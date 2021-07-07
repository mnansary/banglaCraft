#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
# ---------------------------------------------------------
# imports
# ---------------------------------------------------------

import os
import tensorflow as tf 
from tqdm import tqdm
from glob import glob 
import cv2 
# ---------------------------------------------------------
# globals
# ---------------------------------------------------------
# number of images to store in a tfrecord
DATA_NUM  = 512



def create_dir(base,ext):
    '''
        creates a directory extending base
        args:
            base    =   base path 
            ext     =   the folder to create
    '''
    _path=os.path.join(base,ext)
    if not os.path.exists(_path):
        os.mkdir(_path)
    return _path
#---------------------------------------------------------------
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def get_bytes(img_path):
    img=cv2.imread(img_path)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img=cv2.resize(img,(512,512))
    _,coded = cv2.imencode('.png',img)
    _bytes=coded.tobytes()
    return _bytes



def to_tfrecord(image_paths,save_dir,r_num):
    '''	            
      Creates tfrecords from Provided Image Paths	        
      args:	        
        image_paths     :   specific number of image paths	       
        save_dir        :   location to save the tfrecords	           
        r_num           :   record number	
    '''
    # record name
    tfrecord_name='{}.tfrecord'.format(r_num)
    # path
    tfrecord_path=os.path.join(save_dir,tfrecord_name)
    with tf.io.TFRecordWriter(tfrecord_path) as writer:    
        for image_path in image_paths:
            
            char_path=str(image_path).replace('images','char_level')
            word_path=str(image_path).replace('images','word_level')
            
            # #image
            # with(open(image_path,'rb')) as fid:
            #     image_bytes=fid.read()
            # # char
            # with(open(char_path,'rb')) as fid:
            #     char_bytes=fid.read()
            
            # # word
            # with(open(word_path,'rb')) as fid:
            #     word_bytes=fid.read()
            
            
            data ={ 'image':_bytes_feature(get_bytes(image_path)),
                    'charmap':_bytes_feature(get_bytes(char_path)),
                    'wordmap':_bytes_feature(get_bytes(word_path))
            }
            # write
            features=tf.train.Features(feature=data)
            example= tf.train.Example(features=features)
            serialized=example.SerializeToString()
            writer.write(serialized)


def genTFRecords(_paths,mode_dir):
    '''	        
        tf record wrapper
        args:	        
            _paths    :   all image paths for a mode	        
            mode_dir  :   location to save the tfrecords	    
    '''
    for i in tqdm(range(0,len(_paths),DATA_NUM)):
        # paths
        image_paths= _paths[i:i+DATA_NUM]
        # record num
        r_num=i // DATA_NUM
        # create tfrecord
        to_tfrecord(image_paths,mode_dir,r_num)    


train_img="/home/apsisdev/IMPORTANT/banglaDetHor/train/images"
test_img ="/home/apsisdev/IMPORTANT/banglaDetHor/test/images"

save_path ="/home/apsisdev/IMPORTANT/banglaDetHor"
save_path =create_dir(save_path,"tfrecords")
train_save=create_dir(save_path,"train")
test_save =create_dir(save_path,"test")


train_paths=[img_path for img_path in tqdm(glob(os.path.join(train_img,"*.*")))]
test_paths =[img_path for img_path in tqdm(glob(os.path.join(test_img,"*.*")))]

genTFRecords(train_paths,train_save)
genTFRecords(test_paths,test_save)