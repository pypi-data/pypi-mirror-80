# -*- coding: UTF-8 -*-
# example_advanced_plot.py
from BioCircos import BioCircos, getChrInfo, Group, colors
import copy
#获取基因组名，长度，颜色列表
CHRLIST = getChrInfo(open('data/hg19.fa.fai', 'r'))

#把blockangle角度设置为0
p = BioCircos(H=900, W=900, blockangles=5, firstangle=-90, chrlist=[CHRLIST[0]])

gobj = p.Genome(90, 100, open("data/karyotype.human.hg19.txt", 'r'), 
	labelnames=["chr1"], add_scale_tick=False)
histobj = p.dataplot(50, 85, open("data/sample_snp.txt", 'r'), 
	ptype="line",
	data_line_fmt={"strokeColor": colors.red})
lbobj = p.add_label(text_label_fmt={"_text": "原图", "fontSize":20, "y":0.5*p.H, "fontName": "song"})

#获取所有的绘图元素对象组合为allobj
allobj = Group()
for obj in gobj.contents:
	allobj.add(obj)
for obj in histobj.contents:
	allobj.add(obj)
allobj.add(lbobj.contents[0])
p.d.add(allobj)

#仅shit移动原图的基因组
shift_obj = copy.deepcopy(gobj)
shift_obj.shift(0, 300)
p.d.add(shift_obj)
p.d.add(p.add_label(text_label_fmt={
	"_text": "基因组图上移300", 
	"fontSize":20, 
	"y":750, 
	"x":450, 
	"fontName": "song"}))

#scale拉伸变换原图(所有横坐标变为原来的80%, 纵坐标变为原来的150%)
scale_obj = copy.deepcopy(allobj)
scale_obj.scale(0.8, 1.5)
scale_obj.shift(-200, -100)
scale_obj.contents[-1]._text="变形拉伸\nscale"
p.d.add(scale_obj)

#translate移动原图, 同shift
translate_obj = copy.deepcopy(allobj)
translate_obj.translate(300, 0)
translate_obj.contents[-1]._text="左移动300"
p.d.add(translate_obj)

#raotate旋转原图, 旋转中心是画布的左底角(0, 0)位置
rotate_obj = copy.deepcopy(allobj)
rotate_obj.rotate(-30)
rotate_obj.contents[-1]._text="左底角旋转\nrotate"
p.d.add(rotate_obj)

p.savefile("example_advanced_plot.pdf")