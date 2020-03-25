#coding utf-8
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import copy
from IPython.display import Image,display
#from ipywidgets import widgets

def prepare_img(img_path):
    img = cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0,0,100], dtype=np.uint8)
    upper_white = np.array([170,30,255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    rev_img = cv2.bitwise_not(mask)
    res = cv2.medianBlur(rev_img,15)
    return res

def detect_circle(img):
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                               param1=100, param2=10, minRadius=10, maxRadius=30)
    df_pos = pd.DataFrame(data=circles[0,:], columns=['x', 'y', 'r'])
    df_pos = df_pos.sort_values('x').reset_index()
    xy_loc = np.array(df_pos.iloc[:,1:3])
    return df_pos,xy_loc

def make_distance_matrix(xy_loc):
    all_diffs = np.expand_dims(xy_loc, axis=1) - np.expand_dims(xy_loc, axis=0)
    dist_mx = np.sqrt(np.sum(all_diffs ** 2, axis=-1))
    return dist_mx

def extract_near_point(dist_mx, distance):
    num_loc = len(dist_mx)
    near_loc = []
    for i in range(num_loc-1):
        ar = dist_mx[i]
        x_posi = ar[i+1:]
        near_loc.append(list(np.where(x_posi < distance)[0]))
    return near_loc

def connect_candidate_point(df):
    candidate = []
    for n,l in enumerate(df):
        candidate.append([n])
        for j in l:
            for c in candidate:
                if c[-1]==n:
                    cc = copy.copy(c)
                    cc.append(n+j+1)
                    candidate.append(cc)
    candidate = [i for i in candidate if len(i) >= 4]
    return candidate

def identify_position(candidate, position):
    dissection = []
    for i in candidate:
        y_distance = [position.at[i[n+1], "y"] - position.at[i[n], "y"] for n in range(len(i)-1)]
        if max(y_distance) - min(y_distance) < 10:
            dissection.append(i)
    smpl_list = list(set((list(itertools.chain.from_iterable(dissection)))))
    return position.loc[smpl_list,:]

def detect_sampling_point(img_path, distance):
    img = prepare_img(img_path)
    df_point, mx_point = detect_circle(img)
    distance_matrix = make_distance_matrix(mx_point)
    near_loc = extract_near_point(distance_matrix, distance)
    candidate = connect_candidate_point(near_loc)
    sampling_pos = identify_position(candidate, df_point)
    return sampling_pos

def marker_sampling_point(img_path, location):
    img = cv2.imread(img_path)
    for i in location.itertuples():
        cv2.circle(img, (int(i[2]),int(i[3])), int(i[4]), (0,255,0), 2)
        cv2.circle(img, (int(i[2]),int(i[3])), 2, (0,0,255), 3)
    return img