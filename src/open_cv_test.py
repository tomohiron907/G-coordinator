import numpy as np
import cv2 as cv

img = cv.imread('pic_2.png',cv.IMREAD_GRAYSCALE)

#print(type(img)) #typeでオブジェクトの型を確認
#print(img[0,0])
'''for i in range(4):
    for j in range(4):
        print(img[i,j])
'''
N = 781

full_pic =[]
#斜めスライスアルゴリズム
'''for k in range(1,2 * N):
    if k < N :
        a_k = [img.item(N-k+i, i) for i in range(k)]
    else:
        a_k = [img.item(i, k-N+i) for i in range(2*N-k)]
    #print(a_k)
    full_pic.append(a_k)
'''
# 横スライスアルゴリズム
for k in range(N):
    a_k = [255-img[k,i] for i in range(N)]
    full_pic.append(a_k)
#print(full_pic)