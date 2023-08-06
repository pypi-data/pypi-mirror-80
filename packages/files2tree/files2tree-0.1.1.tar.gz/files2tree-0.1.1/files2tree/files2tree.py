# coding: utf-8
from pyecharts import options as opts
from pyecharts.charts import Tree

import os


class files2tree:
    def __init__(self, rootPath):
        self.rootPath = rootPath



    def GetTree(self):
        catalogue = {'filename': [], "path": []}
        fileNum = 0
        rootfie_sig=0
        rootName='根目录'
        for parent, dirnames, filenames in os.walk(self.rootPath, followlinks=True):
            for filename in filenames:
                file_path = os.path.join(parent, filename)
                # target = rootPath + file_path
                fileNum += 1
                catalogue['filename'].append(filename)
                catalogue['path'].append(file_path)
            if rootfie_sig==0:
                rootName=parent.split('\\')[-1]
                rootfie_sig=1
        # print('fileNum:', fileNum)
        # print('catalogue:', catalogue)

        res = []
        max = 0
        for i in catalogue['path']:

            _pre = i.split(self.rootPath)
            # print('_pre:', _pre)

            after = _pre[1]
            _after = after.split('\\')
            if _after[0] == '':
                _after.pop(0)
            # print('_after:', _after)

            # exit()
            _len = len(_after)
            if _len > max:
                max = _len
            t = {"len": _len, 'path_arr': _after, 'obj': {"name": _after[-1]}}
            res.append(t)
        # print('res len :', len(res), 'res:', res)

        for i in range(max, 0, -1):
            if i == max:  # 长度最长的肯定不是文件夹
                temp_arr = []
                for d in res:  # 把长度最长的全弄到一个列表里
                    if d['len'] == max:
                        temp_arr.append(d)

                while len(temp_arr) >= 1:


                    d = temp_arr[0]
                    temp_arr.pop(0)


                    n = {"name": d['path_arr'][-2], "children": [{"name": d['path_arr'][-1]}], 'len': i - 1,
                         'path_arr': d['path_arr'][0:-1]}
                    delete_arr = []
                    for k1 in range(len(res)):
                        # print('k1:',k1)
                        if '.'.join(res[k1]['path_arr']) == '.'.join(d['path_arr']):
                            delete_arr.append(k1)
                            # res.pop(k1)

                    for s in range(len(temp_arr) - 1, -1, -1):
                        # print('s:', s)
                        if '.'.join(d['path_arr'][0:-1]) == '.'.join(temp_arr[s]['path_arr'][0:-1]):
                            n['children'].append({"name": temp_arr[s]['path_arr'][-1]})

                            for k2 in range(len(res)):
                                if '.'.join(res[k2]['path_arr']) == '.'.join(temp_arr[s]['path_arr']):
                                    delete_arr.append(k2)
                            temp_arr.pop(s)

                    delete_arr = list(set(delete_arr))
                    delete_arr.sort(reverse=True)
                    # delete_set = set()
                    # for k3 in delete_arr:
                    #     delete_set.add(k3)
                    for delete_ind in delete_arr:
                        res.pop(delete_ind)
                    res.append(n)


            elif i < max and i > 1:

                temp_arr = []
                for d in res:  # 把长度最长的全弄到一个列表里
                    if d['len'] == i:
                        temp_arr.append(d)

                # exit()

                while len(temp_arr) >= 1:
                    d = temp_arr[0]
                    temp_arr.pop(0)
                    if 'children' in d:
                        # del d['len']
                        n = {"name": d['path_arr'][-2], "children": [d], 'len': i - 1, 'path_arr': d['path_arr'][0:-1]}
                    else:
                        n = {"name": d['path_arr'][-2], "children": [{"name": d['path_arr'][-1]}], 'len': i - 1,
                             'path_arr': d['path_arr'][0:-1]}
                    delete_arr = []
                    for k1 in range(len(res)):
                        if '.'.join(res[k1]['path_arr']) == '.'.join(d['path_arr']):
                            delete_arr.append(k1)
                    for s in range(len(temp_arr) - 1, -1, -1):

                        if '.'.join(d['path_arr'][0:-1]) == '.'.join(temp_arr[s]['path_arr'][0:-1]):
                            if 'children' in temp_arr[s]:
                                n['children'].append(temp_arr[s])
                            else:
                                n['children'].append({"name": temp_arr[s]['path_arr'][-1]})

                            for k2 in range(len(res)):
                                if '.'.join(res[k2]['path_arr']) == '.'.join(temp_arr[s]['path_arr']):
                                    delete_arr.append(k2)
                            temp_arr.pop(s)

                    delete_arr = list(set(delete_arr))
                    delete_arr.sort(reverse=True)

                    for delete_ind in delete_arr:
                        res.pop(delete_ind)
                    res.append(n)

            elif i == 1:
                for i in range(len(res)):
                    if len(res[i]['path_arr']) == 1 and 'name' not in res[i]:
                        res[i] = {"name": res[i]['obj']['name']}

        return {"fileNum":fileNum,"data":  {"name": rootName ,  "children": res  }  }





    def dir2tree(self):
        # rootPath = r"C:\坚果云\综合其他\py_project\TeaCases\python法律应用实务\大型非诉项目处理\尽职调查文件夹"
        fileTree=self.GetTree()
        c = (
            Tree(init_opts=opts.InitOpts(
                height='800px',
                width='100%',
            ))
                .add("", [fileTree['data']], collapse_interval=2)
                .set_global_opts(title_opts=opts.TitleOpts(title="catalog-"+fileTree['data']['name']), toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                                                                             pos_top="top",
                                                                                                             pos_left="right",
                                                                                                             feature={
                                                                                                                 "saveAsImage": {},
                                                                                                                 }
                                                                                                             ))
                .render("filestree.html")
        )



# p=files2tree(r"C:\坚果云\综合其他\py_project\TeaCases\python法律应用实务\大型非诉项目处理\尽职调查文件夹")
# p.dir2tree()