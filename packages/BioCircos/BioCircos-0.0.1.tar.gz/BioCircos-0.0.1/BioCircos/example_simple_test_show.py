# -*- coding: UTF-8 -*-
# example_simple_test_show.py
from BioCircos import BioCircos, getChrInfo, colors

#获取基因组名，长度，颜色列表
CHRLIST = getChrInfo(open('data/hg19.fa.fai', 'r'))

#初始化画布及其参数
p = BioCircos(chrlist=CHRLIST)

#绘制基因组
p.d.add(p.Genome(280, 300, open("data/karyotype.human.hg19.txt", 'r')))

#dataplot-1 绘制测序深度
p.d.add(p.dataplot(250, 269, open("data/sample_depth.txt", 'r'),
	default_min_value = 0,
	default_max_value = 100,
	label_name = "测序深度",
	bg_label_name_fmt = {"fontName": "hei"},
	bg_grid_fmt = {"strokeColor": colors.toColor("rgba(255, 100, 255, 0.8)")} ))
	
#dataplot-2 绘制测序深度(镜像/反向)
p.d.add(p.dataplot(250, 229, open("data/sample_depth.txt", 'r'),))

#dataplot-3 绘制测序覆盖面积图
p.d.add(p.dataplot(200, 225, open("data/sample_coverage.txt", 'r'), 
	ptype="line-area", 
	label_name="covarage area"))

#dataplot-4 绘制测序覆盖线图
p.d.add(p.dataplot(180, 195, open("data/sample_coverage.txt", 'r'), 
	ptype="line", 
	label_name="covarage ratio", 
	data_line_fmt={"strokeColor": colors.red, "strokeWidth":1.5}))

#dataplot-5 绘制测序突变位点snp图
p.d.add(p.dataplot(150, 170, open("data/sample_snp.txt", 'r'), 
	ptype="points", 
	data_points_size=2, 
	label_name="variant freq"))

#dataplot-6,7,8 绘制bar热图
p.d.add(p.dataplot(130, 140, open("data/sample_bar1.txt", 'r'), background=False, add_tick_label=False))
p.d.add(p.dataplot(120, 130, open("data/sample_bar2.txt", 'r'), background=False, add_tick_label=False))
p.d.add(p.dataplot(110, 120, open("data/sample_bar3.txt", 'r'), background=False, add_tick_label=False))

#dataplot-9 绘制CNV拷贝数图
p.d.add(p.dataplot(80, 105, open("data/sample_cnv.txt", 'r'), 
	ptype="line-seg", 
	data_annotag_fmt={"fontSize":8}, 
	default_min_value=-3, 
	default_max_value=3, 
	label_name="CN", 
	label_name_shiftangle=10))

#dataplot-10 绘制融合基因, 结构变异SV的关联图
p.d.add(p.dataplot(0, 75, open("data/sample_sv.txt", 'r'), 
	ptype="link", 
	data_annotag_fmt={"fontSize":6}))

#绘制标题
p.d.add(p.add_label(text_label_fmt={"_text": "BioCircos 示例图", "fontSize":24, "y":750, "fontName": "hei"}))
	
#保存绘图
p.savefile("example_simple_test_show.pdf")

