import os
import hashlib
from PIL import Image
import cv2
import numpy
import os
from flask import Flask,redirect
from flask import abort
import requests
from flask import make_response
import yaml #读取文件

def colour(c1,c2,c3): #组合数据函数
    return round(c1),round(c2),round(c3)

def out_rgb(filname):
    try:
        myimg_blur = cv2.imread(filname) #读取图片

        size = (128,128) 

        myimg_blur_ys = cv2.resize(myimg_blur, size, interpolation=cv2.INTER_AREA) #压缩图片快速处理 免得服务器带不动((

        bblur = cv2.GaussianBlur(myimg_blur_ys, (2555,2555), 5)#进行高斯模糊处理

        cv2.imwrite('./tmp/dimg_blur.png', bblur)

        myimg = cv2.imread('./tmp/dimg_blur.png')

        os.remove('./tmp/dimg_blur.png')

        avg_color_per_row = numpy.average(myimg, axis=0)

        avg_color = numpy.average(avg_color_per_row, axis=0) #进行图片颜色平均值

        img_obj = Image.new('RGB', (800, 480), colour(avg_color[2],avg_color[1],avg_color[0]))  

        with open('./out_rgb/dimg.png','wb') as f:
                img_obj.save(f,'png')

        return True
    except Exception as rrr:
        print(rrr)
        return False



def diff_md5(file1,file2):
    def chick_md5(file):
        md5 = hashlib.md5()
        with open(file, 'rb') as f:
            while True:
                content = f.read(8192)
                if content:
                    md5.update(content)
                else:
                    break
        return md5.hexdigest()
    return chick_md5(file1) == chick_md5(file2)


def qqset():
    with open('settings.yml', 'r') as f: #读取配置文件?
        qq = yaml.load(f.read(),Loader=yaml.FullLoader)
        token = qq['QQnum']
    return token

app = Flask(__name__)
@app.route('/')
def index():
    return redirect('https://gmoe.cc', code=302)


@app.route('/rgb')
def rggbb_img():

    durl = "https://q1.qlogo.cn/g?b=qq&nk="+str(qqset())+"&s=640"
    if os.path.isfile('./tmp/dimg.png') == True:
        dwimg = requests.get(durl)
        
        with open("./tmp/dimg_tmp.png","wb")as f: #下载图片
            f.write(dwimg.content)
        
        if diff_md5('./tmp/dimg_tmp.png','./out_rgb/dimg.png') == False: #如果文件MD5不一样就重新生成
            if o.out_rgb("./tmp/dimg_tmp.png") == False: #检测图片生成时候出错
                return abort(400, '淦!生成图片时候出错了') 
            else:
                os.remove("./tmp/dimg.png")
                os.rename("./tmp/dimg_tmp.png", "./tmp/dimg.png")   
                image_data = open("./out_rgb/dimg.png", "rb").read()#读取图片
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/jpg'
                return response
        else:
            os.remove("./tmp/dimg_tmp.png")
            image_data = open("./out_rgb/dimg.png", "rb").read()#读取图片
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpg'
            return response

    else:
        dwimg = requests.get(durl)
        with open("./tmp/dimg.png","wb")as f: #下载图片
            f.write(dwimg.content)

        if out_rgb("./tmp/dimg_tmp.png") == False: #检测图片生成时候出错
            return abort(400, '淦生成图片时候出错了') 
        else:    
            image_data = open("./out_rgb/dimg.png", "rb").read()#读取图片
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpg'

            return response

@app.route('/img')
def qq_img():
    durl = "https://q1.qlogo.cn/g?b=qq&nk="+str(qqset())+"&s=640"
    if os.path.isfile('./qqimg/dimg.png') == True:
        dwimg = requests.get(durl)
        
        with open("./qqimg/qq_tmp.png","wb")as f: #下载图片
            f.write(dwimg.content)
        
        if diff_md5('./qqimg/qq_tmp.png','./qqimg/qq.png') == False: #如果文件MD5不一样就重新下载
            os.remove("./qqimg/qq.png")
            os.rename("./qqimg/qq_tmp.png", "./qqimg/qq.png")   
            image_data = open("./qqimg/qq.png", "rb").read()#读取图片
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpg'
            return response
        else:
            os.remove("./qqimg/qq_tmp.png")
            image_data = open("./qqimg/qq.png", "rb").read()#读取图片
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/jpg'
            return response

    else:
        dwimg = requests.get(durl)
        with open("./qqimg/qq.png","wb")as f: #下载图片
            f.write(dwimg.content)

        image_data = open("./qqimg/qq.png", "rb").read()#读取图片
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/jpg'
        return response

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=os.getenv("PORT", default=5000))