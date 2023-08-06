# -*- coding: UTF-8 -*-
# example_significate_chrs_plot.py
from BioCircos import BioCircos, getChrInfo, colors

#获取基因组名，长度，颜色列表
CHRLIST = getChrInfo(open('data/hg19.fa.fai', 'r'))
chrtotalsize = sum([x[1] for x in CHRLIST])

p = BioCircos(blockangles=3, chrlist=CHRLIST)

#每个碱基对应的角度大小
degrees = (360.0 - sum(p.blockangles)) / chrtotalsize

startangle = p.firstangle
for ci, chrninfo in enumerate(CHRLIST):
	print(chrninfo)
	if chrninfo[0] in ['1', '3', '5', '11', '19']: # 通过设置绘图内径，外径, 突出显示染色体 1,3,5,11,19
		p.d.add(p.Genome(280, 300, open("data/karyotype.human.hg19.txt", 'r'), chrlist=[chrninfo]))
		p.d.add(p.dataplot(230, 270, open("data/sample_depth.txt", 'r'), 
			drawchrlist=[chrninfo], 
			add_tick_label=False,
			data_hist_fmt={"strokeColor":colors.red}))
		p.d.add(p.dataplot(180, 220, open("data/sample_snp.txt", 'r'), 
			ptype="points", 
			drawchrlist=[chrninfo], 
			add_tick_label=False, 
			data_points_size=2,
			data_annotag_fmt={"fontSize":4}))
	else:
		p.d.add(p.Genome(230, 250, open("data/karyotype.human.hg19.txt", 'r'), chrlist=[chrninfo]))
		p.d.add(p.dataplot(205, 225, open("data/sample_depth.txt", 'r'), 
			drawchrlist=[chrninfo], 
			add_tick_label=False))
		p.d.add(p.dataplot(180, 200, open("data/sample_snp.txt", 'r'), 
			ptype="points", 
			drawchrlist=[chrninfo], 
			add_tick_label=False, 
			data_points_size=1))
	
	#重新定义绘图的起始角度
	p.firstangle = p.firstangle - chrninfo[1]*degrees - p.blockangles[ci]

#恢复默认的绘图角度, 方便绘制其他图
p.firstangle = startangle
p.d.add(p.dataplot(0, 175, open("data/sample_sv.txt", 'r'), ptype="link", data_annotag_fmt={"fontSize":6}))
p.savefile("example_significate_chrs_plot.pdf")