import os

class FileList():
    def __init__(self):
        pass

    #遍历文件和文件夹
    def fileList(self,path):
        list = {'d':[],'f':[]}

        print(path)
        if os.path.isdir(path):
            for root,dis,files in os.walk(path):
                #遍历文件夹
                for d in dis :
                    list['d'].append(d)
                #遍历文件
                for f in files :
                    list['f'].append(f)
        else:
            os.mkdir(path)

        # if list['d'] == [] :
        #     list['d'].append('这里什么都没有！')
        # if list['f'] == [] :
        #     list['f'].append('这里什么都没有！')

        return list['d'],list['f']