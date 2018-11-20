#coding=utf-8
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import glob
import os
import cv2
from tqdm import tqdm  # 添加一个进度条显示而已
def txtToXml(image_path, txt_path):
    for txt_file in tqdm(glob.glob(txt_path + '/*.txt')):
        txt_name_ = txt_file.split('/')[-1][:-4] #去掉后面的.jpg
        im = cv2.imread(image_path + '/' + txt_name_ +'.jpg')
        try:
            im.shape
        except:
            print("bad image")
            continue
        width = im.shape[0]
        height = im.shape[1]
        tree = open(txt_file, 'r', encoding='UTF-8')
        node_root = Element('annotation')
        img_type = SubElement(node_root, 'folder')
        img_name = SubElement(node_root, 'filename')
        node_size = SubElement(node_root, 'size')
        node_width = SubElement(node_size, 'width')
        node_width.text = str(width)
        node_height = SubElement(node_size, 'height')
        node_height.text = str(height)
        node_depth = SubElement(node_size, 'depth')
        node_depth.text = '3'
        if txt_path[-8:] == 'txt_9000':
            img_type.text = 'train_images'
        elif txt_path[-8:] == 'txt_1000':
            img_type.text = 'test_images'
        img_name.text = 'img_' + txt_name_ +'.jpg'

        root = tree.readlines()
        for i, line in enumerate(root):
            column = line.split(',')
            obj = SubElement(node_root,'object')
            node1 = SubElement(obj, 'difficlut')
            node2 = SubElement(obj, 'content')
            node3 = SubElement(obj, 'name')
            node4 = SubElement(obj, 'bnbox')
            node1.text = '1'
            node2.text = '###'
            node3.text = 'text'
            x1 = SubElement(node4, 'x1')
            x1.text = column[0].split('.')[0]
            y1 = SubElement(node4, 'y1')
            y1.text = column[1].split('.')[0]
            x2 = SubElement(node4, 'x2')
            x2.text = column[6].split('.')[0]
            y2 = SubElement(node4, 'y2')
            y2.text = column[7].split('.')[0]
            x3 = SubElement(node4, 'x3')
            x3.text = column[4].split('.')[0]
            y3 = SubElement(node4, 'y3')
            y3.text = column[5].split('.')[0]
            x4 = SubElement(node4, 'x4')
            x4.text = column[2].split('.')[0]
            y4 = SubElement(node4, 'y4')
            y4.text = column[3].split('.')[0]
            xmin = SubElement(node4, 'xmin')
            xmin.text = str(min(int(x1.text), int(x2.text), int(x3.text), int(x4.text)))
            ymin = SubElement(node4, 'ymin')
            ymin.text = str(min(int(y1.text), int(y2.text), int(y3.text), int(y4.text)))
            xmax = SubElement(node4, 'xmax')
            xmax.text = str(max(int(x1.text), int(x2.text), int(x3.text), int(x4.text)))
            ymax = SubElement(node4, 'ymax')
            ymax.text = str(max(int(y1.text), int(y2.text), int(y3.text), int(y4.text)))
            if xmax.text < xmin.text:
                tmpx = xmin.text
                xmin.text = xmax.text
                xmax.text = tmpx
            if ymax.text < ymin.text:
                tmpy = ymin.text
                ymin.text = ymax.text
                ymax.text = tmpy

        xml = tostring(node_root, pretty_print=True)  #格式化显示，该换行的换行
        dom = parseString(xml)
        # print (xml)
        if os.path.exists('xml_9000') == False:
            os.makedirs('xml_9000')
        xmls = os.path.join(os.getcwd(), 'xml_9000',txt_name_)
        #with open(txt_name_ + '.xml', 'w') as f:
        with open(xmls + '.xml', 'w') as f:
            # dom.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
            dom.writexml(f, indent='\t', addindent='\t', encoding="utf-8")

if __name__ == "__main__":
    data_path = os.path.join(os.getcwd(), 'txt_9000')  #os.getcwd()返回当前所在文件夹
    pic_path = os.path.join(os.getcwd(), 'image_9000')
    txtToXml(pic_path, data_path )
