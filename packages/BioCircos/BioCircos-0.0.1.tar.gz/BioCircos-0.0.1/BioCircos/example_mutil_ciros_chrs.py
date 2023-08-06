# -*- coding: UTF-8 -*-
# example_multi_circos_chrs.py
from BioCircos import BioCircos, getChrInfo, colors

#获取基因组名，长度，颜色列表
CHRLIST = getChrInfo(open('data/hg19.fa.fai', 'r'))
p = BioCircos(W=1000, H=1000, blockangles=0.1, chrlist=CHRLIST)
#设置 5 X 5格 绘图
sH = p.H/5.0
sW = p.W/5.0
p.firstangle = -92
posi = 0
for ci, chrninfo in enumerate(CHRLIST):
	print chrninfo
	if ci == 12: 
		posi += 1
	xi = posi%5
	yi = int(posi/5)
	
	r = 0.5*min(sW, sH)  #每个小圈图绘图区的最大半径，使相邻圈图不重叠
	#通过设置调整圈图中心来控制绘图
	p.d.add(p.Genome(0.6*r, 0.65*r, open("data/karyotype.human.hg19.txt", 'r'), 
		centerx = (xi+0.5)*sW,
		centery = p.H - (yi+0.5)*sH,
		chrlist=[chrninfo], 
		labelnames=["chr" + chrninfo[0]],
		chrtotalsize=chrninfo[1])) 
	p.d.add(p.dataplot(0.45*r, 0.55*r, open("data/sample_depth.txt", 'r'), 
		centerx = (xi+0.5)*sW,
		centery = p.H - (yi+0.5)*sH,	
		drawchrlist=[chrninfo], 
		chrtotalsize=chrninfo[1],
		add_tick_label=False))
	p.d.add(p.dataplot(0.3*r, 0.4*r, open("data/sample_bar1.txt", 'r'), 
		centerx = (xi+0.5)*sW,
		centery = p.H - (yi+0.5)*sH,
		drawchrlist=[chrninfo], 
		chrtotalsize=chrninfo[1],
		add_tick_label=False))
	posi += 1
p.d.add(p.add_label(text_label_fmt={"_text": "Multi-Genome Circos", "fontSize":20, "y":0.5*p.H}))

p.savefile("example_multi_circos_chrs.pdf")