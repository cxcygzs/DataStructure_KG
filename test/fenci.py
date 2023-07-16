import jieba
import jieba.posseg as posseg

text = '计算机教育知识图谱，社会网络与舆情分析'
c = []
# seg_arr = jieba.lcut(text)
b = posseg.lcut(text)
for i in range(len(b)):
    if(b[i].flag != 'x'):
        c.append(b[i].word)
d = '   '.join(str(i) for i in c)
print(d)
# d = '   '.join(str(i) for i in c)
# print(a)
# for i in range(len(seg_arr1)):
#     # if(str(seg_arr1[i].flag) != 'x'):
#     #     seg_arr_target.append(seg_arr_target)
#     # seg_arr1 = '   '.join(str(i) for i in seg_arr_target)
#     print(type(seg_arr1[i].flag))
