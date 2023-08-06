# coding: utf-8
from pyecharts import options as opts
from pyecharts.charts import Tree
import requests
import os
import json

def GetTree(rootPath):
    catalogue = {'filename': [], "path": []}
    fileNum = 0
    rootfile_sig = 0
    rootName = '根目录'
    for parent, dirnames, filenames in os.walk(rootPath, followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            # target = rootPath + file_path
            fileNum += 1
            catalogue['filename'].append(filename)
            catalogue['path'].append(file_path)
        if rootfile_sig == 0:
            rootName = parent.split('\\')[-1]
            rootfile_sig = 1
    return {"rootName":rootName,"catalogue": catalogue }


def dir2tree(rootName,data):
    c = (
        Tree(init_opts=opts.InitOpts(
            height='800px',
            width='100%',
        ))
            .add("", [data], collapse_interval=2)
            .set_global_opts(title_opts=opts.TitleOpts(title="catalog-" + rootName),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                           pos_top="top",
                                                           pos_left="right",
                                                           feature={
                                                               "saveAsImage": {},
                                                           }
                                                           ))
            .render("filestree.html")
    )


def GetTreeFile(rootPath):        #直接用这个函数
    p=GetTree(rootPath)
    rootName=p['rootName']
    data = {'catalogue': p['catalogue'] ,'rootPath':rootPath}
    data=json.dumps(data)
    with requests.post('https://api.lawtip.cn/file2tree',data=data ,timeout=(5,5),verify=False) as f:
        if f.status_code!=200:
            raise Exception('服务器或本地网络出错,响应码：'+str(f.status_code))
        result=f.text
        result = json.loads(result)
        print('result:',result)

    if result['code']=='909':
        raise Exception(result['msg'])

    if result['code'] == '1':

        item={"name": rootName, "children": result['data'] }
        dir2tree(rootName,item)



# if __name__=='__main__':
#     GetTreeFile(rootPath)