# -*- coding: UTF-8 -*-
# example_screw_plot.py
from BioCircos import BioCircos, getChrInfo, colors

#获取基因组名，长度，颜色列表
CHRLIST = getChrInfo(open('data/hg19.fa.fai', 'r'))
chrtotalsize = sum([x[1] for x in CHRLIST])

#把blockangle角度设置为0
p = BioCircos(blockangles=0, chrlist=CHRLIST)
screw_blockangle = 5
startangle = p.firstangle
r1 = 300 #初始内径为300

for ci, chrninfo in enumerate(CHRLIST):
	print(chrninfo)
	#通过设置chrtotalsize来控制绘图的扇形角度
	p.d.add(p.Genome(r1, r1+5, open("data/karyotype.human.hg19.txt", 'r'), 
		chrlist=[chrninfo], 
		chrtotalsize=10*chrninfo[1])) #1/10圈
	p.d.add(p.dataplot(r1-25, r1-5, open("data/sample_depth.txt", 'r'), 
		drawchrlist=[chrninfo], 
		chrtotalsize=10*chrninfo[1],
		add_tick_label=False))
	p.d.add(p.dataplot(r1-50, r1-30, open("data/sample_snp.txt", 'r'), 
		ptype="points", 
		drawchrlist=[chrninfo], 
		chrtotalsize=10*chrninfo[1],
		add_tick_label=False, 
		data_points_size=2))
	
	#重新定义绘图的起始角度
	p.firstangle = p.firstangle - 360.0/10 - screw_blockangle
	r1 = r1 - 10

p.savefile("example_screw_plot.pdf")