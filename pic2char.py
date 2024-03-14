from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cv2
import numpy as np
import os
import subprocess as sp
global i

def ascii_art(file):
   im=Image.open(file)#打开图片文件
   sample_rate=0.15#用于缩小图片大小
   font=ImageFont.truetype("impact.ttf",size=16)#选择字符字体格式和大小
   bbox = font.getbbox("x")
   width = bbox[2]-bbox[0]
   height = bbox[3]-bbox[1]
   aspect_ratio=width / height#得到字符的宽高比
   new_im_size=np.array([im.size[0]*sample_rate,im.size[1]*sample_rate*aspect_ratio]).astype(int)#将图片高度乘以此宽高比
   # new_im_size=[int(x*sample_rate)for x in im.size]
   im=im.resize(new_im_size)
   im_color=np.array(im)#保留原视频的颜色
   im=im.convert("L")#转成灰度图片
   im=np.array(im)#将pillow的图像转换成numpy数组,方便我们对像素的读取
   symbols=np.array(list(" .-ovDGMM"))#定义字符画中用到的字符，按字符的亮度升序排列，生成字符画时会不停的查阅这个表
#把im规范化到[0,max_symbol)
   if im.max()!=im.min():#考虑分母是否为0
       im=(im-im.min())/(im.max()-im.min())*(symbols.size-1)
   ascii=symbols[im.astype(int)]

   letter_size = (width,height)#得到字符的宽高
    #创建一个新图片
   im_out_size = new_im_size*letter_size
   bg_color="black"
    #创建一个pillow图像
   im_out=Image.new("RGB",tuple(im_out_size),bg_color)
   #创建一个pillow中的ImageDraw对象，用它完成对文本的绘制
   draw=ImageDraw.Draw(im_out)

   y=0
   #两个循环每行每列的逐个绘制字符
   for i,line in enumerate(ascii):
       for j,ch in enumerate(line):
           color=tuple(im_color[i ,j]) #把之前的颜色值提取出来
           draw.text((letter_size[0]*j,y),ch,fill=color,font=font)
       y += letter_size[1] #把y用字母高度扩大

#保存绘制完的图像
       im_out.save(file+'.png')

if __name__=="__main__":
        path = input("Please input the unconverted image path(including name): ")
        ascii_art(path)
        
