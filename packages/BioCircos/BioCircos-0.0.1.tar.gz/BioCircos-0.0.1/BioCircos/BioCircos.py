# -*- coding: UTF-8 -*-
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF, renderPM, renderSVG, renderPS
from reportlab.lib import colors, fonts

#注册中文字体
from reportlab.pdfbase import pdfmetrics, ttfonts
import platform
if platform.system() == "Windows":
	FontDir = "C:\Windows\Fonts"
else:
	FontDir = "/usr/share/fonts/Fonts"
try:
	pdfmetrics.registerFont(ttfonts.TTFont('song', "%s/simsun.ttc"%FontDir))
	pdfmetrics.registerFont(ttfonts.TTFont('hei', "%s/simhei.ttf"%FontDir))
	pdfmetrics.registerFont(ttfonts.TTFont('fang', "%s/simfang.ttf"%FontDir))
	pdfmetrics.registerFont(ttfonts.TTFont('yh', "%s/msyh.ttf"%FontDir))
	#常规字体设置为宋体
	fonts.addMapping('song', 0, 0, 'song')  #常规<宋体>
	fonts.addMapping('song', 0, 1, 'fang')	#斜体<仿宋>
	fonts.addMapping('song', 1, 0, 'hei')   #粗体<黑体>
	fonts.addMapping('song', 1, 1, 'yh')	#粗斜体
except:
	sys.stderr.write("Can't register default chinese font 'song'\n")
	
#from reportlab.pdfgen import canvas
#获取原有的可用字体名称
#print canvas.Canvas("test.pdf").getAvailableFonts()

from io import BytesIO, StringIO
import random
random.seed(123)
import copy

def getChrInfo(inputfp):
	fai_chrlist = []
	with inputfp as f:
		for line in f:
			if line.startswith("#"):continue ##  跳过"#"开头注释的行
			if not line.strip():continue ##  跳过空行
			line = [l.strip() for l in line.split("\t")]
			chrcolor = colors.pink
			if len(line) >= 3:
				try:
					chrcolor = colors.toColor(line[2])
				except:
					pass
			fai_chrlist.append([line[0], int(line[1]), chrcolor])
	return fai_chrlist

class BioCircos(object):

	def __init__(self, W=800, H=800, centerx=None, centery=None, blockangles=None, firstangle=90, u=1, chrlist=[['1', 1]]):
	
		self.chrlist = chrlist
		self.u = u   
		self.W = W * self.u
		self.H = H * self.u
		
		self.centerx = (0.5 * self.W  if centerx == None else centerx)
		self.centery = (0.5 * self.H  if centery == None else centery)
		
		self.firstangle = firstangle
		#self.blockangles = [2]*len(self.chrlist)
		#self.blockangles = [random.randint(1, 10) for i in range(len(self.chrlist))]
		if blockangles == None:
			self.blockangles = [1]*(len(self.chrlist)-1) + [30]
		elif isinstance(blockangles, list):
			self.blockangles = blockangles
		else:
			self.blockangles = [blockangles]*len(self.chrlist)
		
		self.cytobandfp = StringIO(u"1\t0\t1000\trgba(255, 0, 0, 0.5)")
		
		self.label_dr = 20 * self.u
		self.label_fmt = {
			'fontSize': 16 * self.u,
			'fontName': 'Times-Roman',
			'fillColor': colors.black,
			'strokeColor': None,
			'strokeWidth': 0.5 * self.u,
			'boxAnchor': 'c',
		}
		
		self.scale_label_dr = 5 * self.u
		self.scale_label_fmt = {
			'fontSize': 4 * self.u,
			'fontName': 'Times-Roman',
			'fillColor': colors.black,
			'strokeColor': None,
			'strokeWidth': 0.3 * self.u,
			'boxAnchor': 'c',
		}

		self.scale_tick_dr = 3 * self.u
		self.scale_tick_step = 10*1000*1000
		self.scale_tick_fmt = {
			'strokeColor': colors.black,
			'strokeWidth': 0.5 * self.u,
		}
	
		self.chr_ring_fmt = {
			#'fillColor': colors.toColor('rgba(255, 0, 255, 0.1)'),
			'strokeColor': colors.black,
			'strokeWidth': 1.5 * self.u,
			'strokeLineJoin': 1,
		}
		
		self.cyto_ring_fmt = {
			'strokeColor': None,
			'strokeWidth': 0.2 * self.u,
			'strokeLineJoin': 1,
		}
		self.cyto_label_fmt = {
			'fontSize': 8 * self.u, 
			'fontName': "Times-Roman",	
		}
		
		self.bg_fmt = {
			'fillColor': colors.Color(0.9, 0.9, 0.9, 0.5),
			'strokeColor': colors.black,
			'strokeWidth': 0.5 * self.u,
			'strokeLineJoin': 1,
			'strokeLineCap':1,
		}
		
		self.bg_grid_fmt = {
			'fillColor': None,
			'strokeColor': colors.grey,
			'strokeLineJoin': 1,
			'strokeLineCap':0,
			#'strokeWidth': 1 * self.u,
		}
		
		self.bg_tick_fmt = {
			'fillColor': None,
			'strokeColor': colors.black,
			'strokeLineJoin': 1,
			'strokeLineCap':1,
			'strokeWidth': 1 * self.u,
		}
		
		self.bg_label_fmt = {
			'fontSize': 6 * self.u, 
			'fontName': "Times-Roman",
			'fillColor': colors.black,
			'strokeColor': None,
			'boxAnchor':'e', 
		}
		self.bg_label_name_fmt = {
			'fontSize': 8 * self.u, 
			'fontName': "Times-Roman",
			'fillColor': colors.black,
			'strokeColor': None,
			'boxAnchor':'e', 
			'angle':0,
		}
		
		self.data_hist_fmt = {
			#'fillColor': colors.green,
			'strokeColor': None, #colors.white,
			'strokeLineJoin': 1,
			'strokeLineCap':1,
			'strokeWidth': 0.01 * self.u,
		}
		self.data_points_size = 1 * self.u
		self.data_points_fmt = {
			#'fillColor': colors.green,
			'strokeColor': None, #colors.black,
			'strokeLineJoin': 1,
			'strokeLineCap':1,
			'strokeWidth': 0.01 * self.u,			
		}
		self.data_line_fmt = {
			#'fillColor': colors.green,
			'strokeColor': colors.black,
			'strokeLineJoin': 1,
			'strokeLineCap':1,
			'strokeWidth': 0.5 * self.u,
		}
		self.data_line_area_fmt = {
			'fillColor': colors.Color(1, 0, 1, 0.5),
			'strokeColor': None,
			'strokeLineJoin': 1,
			'strokeLineCap':1,
			'strokeWidth': 0.5 * self.u,			
		}
		self.data_line_seg_fmt = {
			#'strokeColor': colors.green,
			'strokeLineJoin': 1,
			'strokeLineCap':1,
			'strokeWidth': 2 * self.u,
		}
		
		self.data_link_fmt = {}
		
		self.annotag_dr = 0 * self.u
		self.data_annotag_fmt = {
			'fontSize': 2 * self.u,
			'fontName': 'Times-Roman',
			#'fillColor': colors.grey,
		}
		
		self.text_label_fmt = {
			"_text": "",
			'fontSize': 24 * self.u,
			'fontName': "Times-Bold",
			'x': self.W * 0.5,
			'y': self.H - 50 * self.u
		}
		
		#print dir(colors)
		self.default_value_color = colors.pink
		self.default_annotag = None
		
		self.d = Drawing(self.W, self.H)
			
	#绘制扇形圆环
	def BaseRing(self, centerx, centery, innerradius, outerradius, startangle, endangle, **kw):
		RP = Path(**kw)
		innerArcPoints = getArcPoints(centerx, centery, innerradius, startangle, endangle)
		outerArcPoints = getArcPoints(centerx, centery, outerradius, startangle, endangle)
		RP.moveTo(innerArcPoints[0][0], innerArcPoints[0][1])
		for points in innerArcPoints[1:]:
			RP.lineTo(points[0], points[1])
		for points in outerArcPoints[::-1]:
			RP.lineTo(points[0], points[1])
		RP.closePath()
		return RP
	
	def default_assignment(self, v, default_v):
		return (v * self.u if v else default_v)
		
	def default_fmt(self, fmt, default_fmt):
		fmt = copy.deepcopy(fmt)  ##可变变量参数深拷贝, 改变了存储地址，使之不受上一层绘图参数设置的影响
		for k in default_fmt.keys():
			if k in ['fontSize', 'strokeWidth', 'dr']:
				fmt[k] = self.default_assignment(fmt.get(k, None), default_fmt[k])
			else:
				fmt[k] = fmt.get(k, default_fmt[k])
		return fmt
	
	def Genome(self, innerradius, outerradius, 
		cytobandfp=None,
		centerx = None, 
		centery = None,
		chrlist = None,
		chrtotalsize = None,
		labelnames=None,
		label_dr = None,
		scale_label_dr = None, 
		add_scale_tick = True,
		add_scale_label = True,
		add_chrlabel = True,
		scale_tick_dr = None, 
		scale_tick_step = None, 
		chr_ring_fmt = {},
		cyto_ring_fmt = {},
		cyto_label = False,
		cyto_label_fmt = {},
		label_fmt = {},
		scale_label_fmt = {},
		scale_tick_fmt = {},
		):
		
		beginangle = self.firstangle
		blockangles = self.blockangles
		chrlist = (chrlist if chrlist else self.chrlist)
		chrtotalsize = (chrtotalsize if chrtotalsize else sum([x[1] for x in self.chrlist])) 
		degrees = (360.0 - sum(self.blockangles)) / chrtotalsize
		
		cytobandfp = (cytobandfp if cytobandfp else  self.cytobandfp)
		
		
		centerx = self.default_assignment(centerx, self.centerx)
		centery = self.default_assignment(centery, self.centery)
		
		label_dr = self.default_assignment(label_dr, self.label_dr)
		scale_label_dr = self.default_assignment(scale_label_dr, self.scale_label_dr)
		scale_tick_dr = self.default_assignment(scale_tick_dr, self.scale_tick_dr)
		scale_tick_step = (scale_tick_step if scale_tick_step else self.scale_tick_step)
		
		chr_ring_fmt = self.default_fmt(chr_ring_fmt, self.chr_ring_fmt)
		cyto_ring_fmt = self.default_fmt(cyto_ring_fmt, self.cyto_ring_fmt)
		cyto_label_fmt = self.default_fmt(cyto_label_fmt, self.cyto_label_fmt)
		label_fmt = self.default_fmt(label_fmt, self.label_fmt)
		scale_label_fmt = self.default_fmt(scale_label_fmt, self.scale_label_fmt)
		scale_tick_fmt = self.default_fmt(scale_tick_fmt, self.scale_tick_fmt)
		
		innerradius = innerradius * self.u
		outerradius = outerradius * self.u
		#print(centerx, centery)
		
		#读取染色体条带region
		cytoband = {}
		if cytobandfp:
			with cytobandfp as f:
				for line in f:
					if not line.strip():continue
					if line.startswith("#"):continue
					line = [l.strip() for l in line.split("\t")]
					if line[0] not in cytoband.keys():
						cytoband[line[0]] = []
					cytocolor = (colors.toColor(line[3]) if len(line) >=4 else None)
					cytotag = (line[4] if len(line) >=5 else None)
					cytoband[line[0]].append((int(line[1]), int(line[2]), cytocolor, cytotag))
					
		g = Group()
		for bi, chrv in enumerate(chrlist):
			chrn, chrlen = chrv[:2]
			chrcolor = (chrv[2] if len(chrv) >= 3 else self.default_value_color)
			#print chrcolor
				
			startangle = beginangle - chrlen*degrees
			endangle = beginangle
			
			#绘制每个染色体的扇形圆环
			CHR_RING = self.BaseRing(centerx, centery, innerradius, outerradius, startangle, endangle, fillColor=chrcolor)
			for k in chr_ring_fmt.keys():
				exec("CHR_RING.%s = chr_ring_fmt['%s']"%(k, k))
			#print CHR_RING.strokeWidth
			g.add(CHR_RING)
			
			#绘制染色体的各个深浅明暗条带
			for cyto in cytoband.get(chrn, []):
				if cyto == []:continue
				if cyto[0]>chrlen  or cyto[1] > chrlen: continue
				cytostartangle = endangle - cyto[1] * degrees
				cytoendangle = endangle - cyto[0] * degrees
				cytomidleangle = (cytostartangle + cytoendangle)/2.0
				CYTO_RING = self.BaseRing(centerx, centery, innerradius, outerradius, cytostartangle, cytoendangle, fillColor=cyto[2])
				for k in cyto_ring_fmt.keys():
					exec("CYTO_RING.%s = cyto_ring_fmt['%s']"%(k, k))
				g.add(CYTO_RING)
				
				if cyto_label == True:
					cytopos = getArcPoints(centerx, centery, innerradius - 1, cytomidleangle, cytomidleangle)
					CYTO_LABEL = Label(_text=cyto[3], x=cytopos[0][0], y=cytopos[0][1], fillColor=cyto[2],
						angle = (cytomidleangle-180 if (90<cytomidleangle%360<270 or -270<cytomidleangle%360<-90) else cytomidleangle),
						boxAnchor = ('w' if (90<cytomidleangle%360<270 or -270<cytomidleangle%360<-90) else 'e'),
						)
					for k in cyto_label_fmt.keys():
						exec("CYTO_LABEL.%s = cyto_label_fmt['%s']"%(k, k))
					g.add(CYTO_LABEL)
				
			#添加染色体字符串标签
			if add_chrlabel:
				midleangle = (startangle + endangle)/ 2.0
				textArc = getArcPoints(centerx, centery, outerradius + label_dr, midleangle, midleangle)
				chrn_txt = (labelnames[bi] if labelnames != None else chrn)
				LB = Label(_text = chrn_txt, x=textArc[0][0], y=textArc[0][1], angle = midleangle - 90)
				#添加标签风格样式
				for k in label_fmt.keys():
					exec("LB.%s = label_fmt['%s']"%(k, k))
				g.add(LB)
					
			#添加染色体刻度
			sn = 0
			for i in range(0, chrlen, scale_tick_step):
				scaleangle = endangle - i*degrees
				if add_scale_tick:
					#添加刻度
					scaletickArc1 = getArcPoints(centerx, centery, outerradius, scaleangle, scaleangle)
					scaletickArc2 = getArcPoints(centerx, centery, outerradius + scale_tick_dr, scaleangle, scaleangle)
					SCALE_TICK = Line(scaletickArc1[0][0], scaletickArc1[0][1], scaletickArc2[0][0], scaletickArc2[0][1])
					for k in scale_tick_fmt.keys():
						exec("SCALE_TICK.%s = scale_tick_fmt['%s']"%(k, k))
					g.add(SCALE_TICK)
				
				#添加刻度标签
					if add_scale_label:
						scaleArc = getArcPoints(centerx, centery, outerradius + scale_label_dr, scaleangle, scaleangle)
						SCALE_LB = Label(_text=str(sn), x=scaleArc[0][0], y=scaleArc[0][1],
							angle = (scaleangle-180 if (90 < scaleangle%360 < 270 or -270 < scaleangle%360 < -90) else scaleangle),)
						for k in scale_label_fmt.keys():
							exec("SCALE_LB.%s = scale_label_fmt['%s']"%(k, k))
						g.add(SCALE_LB)
				sn += 1
			beginangle = startangle - blockangles[bi]
	
		return g	
		
	def dataplot(self, innerradius, outerradius, inputfp, 
		ptype='hist', 
		centerx = None,
		centery = None,
		drawchrlist = None,
		chrtotalsize = None,
		background=True,
		add_tick_label=True,
		label_name =None,
		label_name_shiftangle=6,
		default_max_value = None,
		default_min_value = None, 
		bg_grid_step = 0.1,
		bg_grid_block = 3,
		bg_grid_fmt = {},
		bg_tick_num = 2,
		bg_tick_fmt = {},
		bg_label_fmt = {},
		bg_label_name_fmt={},
		bg_fmt = {},
		data_points_size = None,
		data_points_fmt = {},
		data_line_fmt = {},
		data_line_seg_fmt = {},
		data_line_area_fmt = {},
		data_hist_fmt = {},
		data_link_fmt = {},
		add_annotag = True,
		annotag_dr = 1,
		data_annotag_fmt = {},
		):
		if bg_grid_block <= 1:
			sys.stderr.write("bg_grid_block must bigger then 1\n")
			sys.exit(1)
		if bg_tick_num <= 0:
			sys.stderr.write("bg_tick_num must bigger than 0\n")
			sys.exit(1)
			
		centerx = self.default_assignment(centerx, self.centerx)
		centery = self.default_assignment(centery, self.centery)
		
		data_points_size = self.default_assignment(data_points_size, self.data_points_size)
		annotag_dr = self.default_assignment(annotag_dr, self.annotag_dr)
		
		bg_fmt = self.default_fmt(bg_fmt, self.bg_fmt)
		bg_grid_fmt = self.default_fmt(bg_grid_fmt, self.bg_grid_fmt)
		bg_tick_fmt = self.default_fmt(bg_tick_fmt, self.bg_tick_fmt)
		bg_label_fmt = self.default_fmt(bg_label_fmt, self.bg_label_fmt)
		bg_label_name_fmt = self.default_fmt(bg_label_name_fmt, self.bg_label_name_fmt)
		data_hist_fmt = self.default_fmt(data_hist_fmt, self.data_hist_fmt)
		data_points_fmt = self.default_fmt(data_points_fmt, self.data_points_fmt)
		data_line_fmt = self.default_fmt(data_line_fmt, self.data_line_fmt)
		data_line_area_fmt = self.default_fmt(data_line_area_fmt, self.data_line_area_fmt)
		data_line_seg_fmt = self.default_fmt(data_line_seg_fmt, self.data_line_seg_fmt)
		data_annotag_fmt = self.default_fmt(data_annotag_fmt, self.data_annotag_fmt)
		data_link_fmt = self.default_fmt(data_link_fmt, self.data_link_fmt)
		
		beginangle = self.firstangle
		blockangles = self.blockangles
		#chrlist = (chrlist if chrlist else self.chrlist)
		chrlist = self.chrlist
		drawchrlist = (drawchrlist if drawchrlist else self.chrlist)
		drawchridlist = [c[0] for c in drawchrlist]
		chrtotalsize = (chrtotalsize if chrtotalsize else sum([x[1] for x in self.chrlist]))
		degrees = (360.0 - sum(self.blockangles)) / chrtotalsize
		
		innerradius = innerradius * self.u
		outerradius = outerradius * self.u
		
		g = Group()
		
		if ptype == "link": #二阶贝塞尔曲线, 默认圆中心为控制点
			genepos = []
			with inputfp as f:
				for line in f:
					if not line.strip():continue
					if line.startswith("#"):continue
					line = [l.strip() for l in line.split("\t")]
					chrn1, chrstart1, chrend1, gene1, chrn2, chrstart2, chrend2, gene2 = line[:8]
					dcolor = (colors.toColor(line[8]) if len(line) >= 9 else self.default_value_color)
					if chrn1 not in drawchridlist:continue
					if chrn2 not in drawchridlist:continue
					
					chrn1_idx = drawchridlist.index(chrn1)
					chrn2_idx = drawchridlist.index(chrn2)

					chrn1_startangle = beginangle - ((sum([v[1] for v in drawchrlist[:chrn1_idx]]) + int(chrstart1))*degrees + sum(blockangles[:chrn1_idx]))
					chrn1_endangle = beginangle - ((sum([v[1] for v in drawchrlist[:chrn1_idx]]) + int(chrend1))*degrees + sum(blockangles[:chrn1_idx]))
					chrn2_startangle = beginangle - ((sum([v[1] for v in drawchrlist[:chrn2_idx]]) + int(chrstart2))*degrees + sum(blockangles[:chrn2_idx]))
					chrn2_endangle = beginangle - ((sum([v[1] for v in drawchrlist[:chrn2_idx]]) + int(chrend2))*degrees + sum(blockangles[:chrn2_idx]))

					chrn1_pos_start = getArcPoints(centerx, centery, outerradius, chrn1_startangle, chrn1_startangle)
					chrn1_pos_end = getArcPoints(centerx, centery, outerradius, chrn1_endangle, chrn1_endangle)
					chrn2_pos_start = getArcPoints(centerx, centery, outerradius, chrn2_startangle, chrn2_startangle)
					chrn2_pos_end = getArcPoints(centerx, centery, outerradius, chrn2_endangle, chrn2_endangle)
					
					PLINK = Path(strokeColor=dcolor, strokeWidth=0.01*self.u, fillColor=dcolor)
					for k in data_link_fmt.keys():
						exec("PLINK.%s = data_link_fmt['%s']"%(k, k))
						
					PLINK.moveTo(chrn1_pos_start[0][0], chrn1_pos_start[0][1])
					control_center1 = getArcPoints(centerx, centery, innerradius, (chrn1_startangle + chrn2_endangle)/2.0, (chrn1_startangle + chrn2_endangle)/2.0)
					PLINK.curveTo(chrn1_pos_start[0][0], chrn1_pos_start[0][1], control_center1[0][0], control_center1[0][1], chrn2_pos_end[0][0], chrn2_pos_end[0][1])
					for ap in getArcPoints(centerx, centery, outerradius, chrn2_endangle, chrn2_startangle):
						PLINK.lineTo(ap[0], ap[1])
					control_center2 = getArcPoints(centerx, centery, innerradius, (chrn2_startangle + chrn1_endangle)/2.0, (chrn2_startangle + chrn1_endangle)/2.0)
					PLINK.curveTo(chrn2_pos_start[0][0], chrn2_pos_start[0][1], control_center2[0][0], control_center2[0][1], chrn1_pos_end[0][0], chrn1_pos_end[0][1])
					for ap in getArcPoints(centerx, centery, outerradius, chrn1_endangle, chrn1_startangle):
						PLINK.lineTo(ap[0], ap[1])
					PLINK.closePath()
					
					g.add(PLINK)
					
					gene1_midleangle = (chrn1_startangle+chrn1_endangle)/2.0
					gene1_pos = getArcPoints(centerx, centery, outerradius - annotag_dr, gene1_midleangle, gene1_midleangle)
					genepos.append((gene1_pos, gene1, gene1_midleangle))
					gene2_midleangle = (chrn2_startangle+chrn2_endangle)/2.0
					gene2_pos = getArcPoints(centerx, centery, outerradius - annotag_dr, gene2_midleangle, gene2_midleangle)
					genepos.append((gene2_pos, gene2, gene2_midleangle))
					
			if add_annotag == True:
				for pos, genename, geneangle in genepos:
					if genename:
						GENE_LABEL = Label(_text=genename, x=pos[0][0], y=pos[0][1], 
							angle=(geneangle-180 if (90<geneangle%360<270 or -270<geneangle%360<-90) else geneangle),  
							boxAnchor=('w' if (90<geneangle%360<270 or -270<geneangle%360<-90) else 'e'),
							)
						for k in data_annotag_fmt.keys():
							exec("GENE_LABEL.%s = data_annotag_fmt['%s']"%(k, k))
						g.add(GENE_LABEL)
			return g
			
		data = {}
		with inputfp as f:
			for line in f:
				if not line.strip():continue
				if line.startswith("#"):continue
				line = [l.strip() for l in line.split("\t")]
				chrname, chrstart, chrend, dvalue = line[0], int(line[1]), int(line[2]), float(line[3])
				dcolor = (colors.toColor(line[4]) if len(line) >= 5 else self.default_value_color)
				annotag = (line[5] if len(line) >= 6 else self.default_annotag)	
				if chrname not in data.keys():
					data[chrname] = []			
				if default_min_value != None and dvalue < default_min_value:
					dvalue = default_min_value
				if default_max_value != None and dvalue > default_max_value:
					dvalue = default_max_value
				data[chrname].append((chrstart, chrend, dvalue, dcolor, annotag))
		minvalue = min([min(map(lambda x:x[2], data.get(chrv[0], [(0, 0, 0, 0, None, None)]))) for chrv in chrlist])
		value_lim_min = (default_min_value if default_min_value else minvalue)
		maxvalue = max([max(map(lambda x: x[2], data.get(chrv[0], [(0, 0, 0, 0, None, None)]))) for chrv in chrlist])
		value_lim_max = (default_max_value if default_max_value else maxvalue)
		
		if (value_lim_max - value_lim_min)!=0:
			rd =  float(outerradius - innerradius)/(value_lim_max - value_lim_min)
		else:
			value_lim_min = 0
			if value_lim_max != 0:
				rd = float(outerradius - innerradius)/value_lim_max
			else:
				value_lim_max = 1
				rd = float(outerradius - innerradius)/value_lim_max
				
		for bi, chrv in enumerate(drawchrlist):
			chrn, chrlen = chrv[:2]
			startangle = beginangle - chrlen * degrees
			endangle = beginangle
			brd = float(outerradius - innerradius)/bg_tick_num
			#是否添加背景
			if background==True:
				BG_RING = self.BaseRing(centerx, centery, innerradius, outerradius, startangle, endangle)
				#BG_RING = self.BaseRing(centerx, centery, innerradius, outerradius, startangle, endangle, **bg_fmt) #multiple values error, 不能覆盖已有参数值
				for k in bg_fmt.keys():
					exec("BG_RING.%s = bg_fmt['%s']"%(k, k))
				g.add(BG_RING)

				if bg_tick_num > 1 :
					for i in range(bg_tick_num - 1):
						GRID_P = Path(strokeWidth=(innerradius + i* brd)/1000.0)
						for k in bg_grid_fmt.keys():
							exec("GRID_P.%s = bg_grid_fmt['%s']"%(k, k))

						prangle = startangle + 1 * bg_grid_step
						while prangle < endangle - bg_grid_step:
							pr1 = getArcPoints(centerx, centery, innerradius + (i+1)*brd, prangle, prangle)
							pr2 = getArcPoints(centerx, centery, innerradius + (i+1)*brd, prangle + bg_grid_step, prangle + bg_grid_step)
							GRID_P.moveTo(pr1[0][0], pr1[0][1])
							GRID_P.lineTo(pr2[0][0], pr2[0][1])
							prangle += bg_grid_block * bg_grid_step
						g.add(GRID_P)
						
			if add_tick_label ==True:		
				if bi == 0:
					sp1 = getArcPoints(centerx, centery, innerradius, endangle, endangle)
					sp2 = getArcPoints(centerx, centery, outerradius, endangle, endangle)
					TICKE_LINE = Path(strokeWidth=outerradius/500.0)
					for k in bg_tick_fmt.keys():
						exec("TICKE_LINE.%s = bg_tick_fmt['%s']"%(k, k))			
					TICKE_LINE.moveTo(sp1[0][0], sp1[0][1])
					TICKE_LINE.lineTo(sp2[0][0], sp2[0][1])

					for i in range(bg_tick_num + 1):
						sp1 = getArcPoints(centerx, centery, innerradius + i * brd, endangle, endangle)
						sp2 = getArcPoints(centerx, centery, innerradius + i * brd, endangle+0.5, endangle+0.5)
						TICKE_LINE.moveTo(sp1[0][0], sp1[0][1])
						TICKE_LINE.lineTo(sp2[0][0], sp2[0][1])
						
						sp3 = getArcPoints(centerx, centery, innerradius + i * brd, endangle+0.8, endangle+0.8)
						BG_LB = Label(_text= "%.2f"%(value_lim_min + i*brd/rd), x= sp3[0][0], y=sp3[0][1], angle = endangle+0.8-90)
						for k in bg_label_fmt.keys():
							if k == 'angle':
								exec("BG_LB.%s = endangle + 0.8 - 90 + bg_label_fmt['%s']" % (k, k))
							else:
								exec("BG_LB.%s = bg_label_fmt['%s']" % (k, k))
						g.add(BG_LB)						
					g.add(TICKE_LINE)
					
					if label_name:
						nameangle = endangle + label_name_shiftangle
						namepos = getArcPoints(centerx, centery, (innerradius+outerradius)/2.0,nameangle, nameangle)
						TICK_LABEL_NAME = Label(_text=label_name, x=namepos[0][0], y=namepos[0][1], angle = nameangle - 90,)
						for k in bg_label_name_fmt.keys():
							if k == 'angle':
								exec("TICK_LABEL_NAME.%s = nameangle - 90 + bg_label_name_fmt['%s']" % (k, k))
							else:
								exec("TICK_LABEL_NAME.%s = bg_label_name_fmt['%s']" % (k, k))
							
						g.add(TICK_LABEL_NAME)
						
			if ptype == 'hist':
				for v in sorted(data.get(chrn, []), key=lambda x:x[0]):
					if v[0] > chrlen or v[1] > chrlen: continue
					histstartangle = endangle - v[1] * degrees
					histendangle = endangle -v[0] * degrees
					midleangle = (histstartangle + histendangle)/2.0
					dv = (v[2] if default_min_value==None else v[2] - default_min_value)
					HIST_BAR=self.BaseRing(centerx, centery, innerradius, innerradius + rd * dv, histstartangle, histendangle, fillColor=v[3])
					for k in data_hist_fmt.keys():
						exec("HIST_BAR.%s = data_hist_fmt['%s']" % (k, k)) 
					g.add(HIST_BAR)
				
			if ptype == 'points':
				for v in sorted(data.get(chrn, []), key=lambda x:x[0]):
					if v[0] > chrlen or v[1] > chrlen: continue
					pointsstartangle = endangle - v[1] * degrees
					pointsendangle = endangle -v[0] * degrees
					midleangle = (pointsstartangle + pointsendangle)/2.0
					dv = (v[2] if default_min_value==None else v[2] - default_min_value)
					scater = getArcPoints(centerx, centery, innerradius + rd * dv, midleangle, midleangle)
					CIRCLE_POINTS = Circle(scater[0][0], scater[0][1],  data_points_size, fillColor=v[3])
					for k in data_points_fmt.keys():
						exec("CIRCLE_POINTS.%s = data_points_fmt['%s']" % (k, k))				
					g.add(CIRCLE_POINTS)

					
			if ptype == 'line':
				pn = 0
				PLINE = Path()
				for k in data_line_fmt.keys():
					exec("PLINE.%s = data_line_fmt['%s']" % (k, k))
						
				pointsstartangle = None
				pointsendangle = None
				for v in sorted(data.get(chrn, []), key=lambda x:x[0]):
					if v[0] > chrlen or v[1] > chrlen: continue
					pointsstartangle = endangle - v[1] * degrees
					pointsendangle = endangle -v[0] * degrees
					midleangle = (pointsstartangle + pointsendangle)/2.0
					dv = (v[2] if default_min_value==None else v[2] - default_min_value)
					scater = getArcPoints(centerx, centery, innerradius + rd * dv, midleangle, midleangle)
					if pn == 0:
						scater_start_v = getArcPoints(centerx, centery, innerradius + rd * dv, pointsendangle, pointsendangle)
						PLINE.moveTo(scater_start_v[0][0], scater_start_v[0][1])
						PLINE.lineTo(scater[0][0], scater[0][1])
					else:
						PLINE.lineTo(scater[0][0], scater[0][1])
					pn += 1
				if pointsstartangle:
					scater_end_v = getArcPoints(centerx, centery, innerradius + rd * v[2], pointsstartangle, pointsstartangle)
					PLINE.lineTo(scater_end_v[0][0], scater_end_v[0][1])
					g.add(PLINE)
			
			if ptype == "line-seg":
				for v in sorted(data.get(chrn, []), key=lambda x:x[0]):
					SEG_P = Path(strokeColor=v[3])
					for k in data_line_seg_fmt.keys():
						exec("SEG_P.%s = data_line_seg_fmt['%s']" % (k, k))
						
					if v[0] > chrlen or v[1] > chrlen:continue
					lstartangle = endangle - v[1] * degrees
					lendangle =  endangle -v[0] * degrees
					dv = (v[2] if default_min_value==None else v[2] - default_min_value)
					prs = getArcPoints(centerx, centery, innerradius + rd*dv, lstartangle, lendangle)
					for pn, pt in enumerate(prs):
						if pn == 0:
							SEG_P.moveTo(pt[0], pt[1])
						else:
							SEG_P.lineTo(pt[0], pt[1])
					g.add(SEG_P)
													
								
			if ptype == "line-area":
				pn = 0
				PLINE_AREA = Path()
				for k in data_line_area_fmt.keys():
					exec("PLINE_AREA.%s = data_line_area_fmt['%s']" % (k, k ))
				pstartangle = startangle
				pendangle = endangle
				pointsstartangle = None
				pointsendangle = None
				for v in sorted(data.get(chrn, []), key=lambda x:x[0]):
					if v[0] > chrlen or v[1] > chrlen: continue
					#print(v)
					pointsstartangle = endangle - v[1] * degrees
					pointsendangle = endangle -v[0] * degrees
					midleangle = (pointsstartangle + pointsendangle)/2.0
					dv = (v[2] if default_min_value==None else v[2] - default_min_value)
					scater = getArcPoints(centerx, centery, innerradius + rd * dv, midleangle, midleangle)
					if pn == 0:
						pstartangle = pointsendangle
						scater_start_innser = getArcPoints(centerx, centery, innerradius, pointsendangle, pointsendangle)
						scater_start_v = getArcPoints(centerx, centery, innerradius + rd * dv, pointsendangle, pointsendangle)
						PLINE_AREA.moveTo(scater_start_innser[0][0], scater_start_innser[0][1])
						PLINE_AREA.lineTo(scater_start_v[0][0], scater_start_v[0][1])
						PLINE_AREA.lineTo(scater[0][0], scater[0][1])
					else:
						PLINE_AREA.lineTo(scater[0][0], scater[0][1])
					pn += 1
					
				if pointsstartangle:
					scater_end_v = getArcPoints(centerx, centery, innerradius + rd * dv, pointsstartangle, pointsstartangle)
					scater_end_inner = getArcPoints(centerx, centery, innerradius, pointsstartangle, pointsstartangle)
					PLINE_AREA.lineTo(scater_end_v[0][0], scater_end_v[0][1])
					PLINE_AREA.lineTo(scater_end_inner[0][0], scater_end_inner[0][1])
				
					pendangle = pointsstartangle
					#print(startangle, endangle, pstartangle, pendangle)
					
					inner_points = getArcPoints(centerx, centery, innerradius, pendangle, pstartangle)
					#inner_points = getArcPoints(centerx, centery, innerradius, pstartangle, pendangle)
					for ips in inner_points:
						PLINE_AREA.lineTo(ips[0], ips[1])
				
					PLINE_AREA.closePath()
					g.add(PLINE_AREA)
					
			if add_annotag == True:
				for v in sorted(data.get(chrn, []), key=lambda x:x[0]):
					if v[0] > chrlen or v[1] > chrlen: continue
					posstartangle = endangle - v[1] * degrees
					posendangle = endangle -v[0] * degrees
					midleangle = (posstartangle + posendangle)/2.0
					dv = (v[2] if default_min_value==None else v[2] - default_min_value)
					if innerradius > outerradius:
						annotag_dr = - annotag_dr
					pos_midle = getArcPoints(centerx, centery, innerradius + rd * dv + annotag_dr, midleangle, midleangle)
					tag = v[4]
					if tag:
						if innerradius > outerradius:
							bac = ('w' if (90<midleangle%360<270 or -270<midleangle%360<-90) else 'e')
						else:
							bac = ('e' if (90<midleangle%360<270 or -270<midleangle%360<-90) else 'w')
						ANNO_TAG = Label(_text=tag, x=pos_midle[0][0], y=pos_midle[0][1],
							angle=(midleangle-180 if (90<midleangle%360<270 or -270<midleangle%360<-90) else midleangle),
							boxAnchor=bac,
							)
						for k in data_annotag_fmt.keys():
							exec("ANNO_TAG.%s = data_annotag_fmt['%s']" % (k, k))				
						g.add(ANNO_TAG)				
					
			beginangle = startangle - blockangles[bi]
		return g
		
	def add_label(self, text_label_fmt={}):
		text_label_fmt = self.default_fmt(text_label_fmt, self.text_label_fmt)
		g = Group()
		TEXT_LB = Label()
		for k in text_label_fmt.keys():
			exec("TEXT_LB.%s = text_label_fmt['%s']" % (k, k))
		g.add(TEXT_LB)	
		return g
		
	def savefile(self, outfilename):
		if outfilename.endswith(".pdf"):
			renderPDF.drawToFile(self.d, outfilename)
		elif outfilename.endswith(".png"):
			renderPM.drawToFile(self.d, outfilename)
		elif outfilename.endswith(".jpg"):
			renderPM.drawToFile(self.d, outfilename)
		else:
			sys.stderr.write("error output format\n")
			sys.exit(1)

##对参数中的字体、图形中的颜色字符串定义转化为 color
def ParasColor(paras):
	for pk, pv in paras.items():
		if pk in ["strokeColor", "fillColor", 'boxStrokeColor', 'boxFillColor']:
			paras[pk] = colors.toColor(paras[pk])
		if isinstance(pv, dict):
			for cks in ["strokeColor", "fillColor", 'boxStrokeColor', 'boxFillColor']:
				if pv.get(cks):
					pv[cks] = colors.toColor(pv[cks])
	return paras
				
if __name__ == "__main__":
	
	import argparse
	import json
	parser = argparse.ArgumentParser(prog='BioCircos.py')
	parser.add_argument('-F', '--fai', required=True, help='reference index file', )
	parser.add_argument('-L', '--label', required=False, help="image title label")
	parser.add_argument('-I', '--init-settings', default="{}", required=False, help='plot genomic parameters, json format. example: "{\\"innerradius\\":280, \\"outerradius\\":300}"')
	parser.add_argument('-G', '--genome-plot', help='plot genomic parameters, json format. example: "{\\"innerradius\\":280, \\"outerradius\\":300}"')
	parser.add_argument('-o', '--output',default="out.pdf", help="output file to sava image")
	parser.add_argument('--dataplot-1', help='data circos parameters, json format. example: "{\\"innerradius\\":280, \\"outerradius\\":300}"')
	for i in range(2, 21):
		parser.add_argument('--dataplot-%d'%i, help="data circos parameters, json format")

	args = parser.parse_args()
	
	fai_chrlist = getChrInfo(open(args.fai, 'r'))
	
	if args.label:
		txt_label_paras = json.loads(args.label, encoding="GB2312")
	else:
		txt_label_paras = {}
	txt_label_paras = ParasColor(txt_label_paras)

	init_paras = json.loads(args.init_settings)
	if "chrlist" not in init_paras.keys():
		init_paras['chrlist'] = fai_chrlist
	init_paras = ParasColor(init_paras)

	if args.genome_plot:
		genome_paras = json.loads(args.genome_plot)
	else:
		genome_paras = {}
		
	if genome_paras.get('cytobandfp'):
		genome_paras['cytobandfp'] = open(genome_paras['cytobandfp'], 'r')
	genome_paras = ParasColor(genome_paras)	

	dataplots_paras = []
	for arg_k, arg_v in args.__dict__.items():
		if arg_k.startswith("dataplot"):
			if arg_v == None:continue
			numid = int(arg_k.split("_")[1])
			paras = json.loads(arg_v, encoding="GB2312")
			if paras.get('inputfp'):
				paras['inputfp'] = open(paras['inputfp'], 'r')
			paras = ParasColor(paras)
				
			dataplots_paras.append([numid, paras])
	dataplots_paras = sorted(dataplots_paras)	
	
	outputfile = args.output

	p = BioCircos(**init_paras)
	if genome_paras:
		p.d.add(p.Genome(**genome_paras))
	for n, paras in dataplots_paras:
		p.d.add(p.dataplot(**paras))
	
	p.d.add(p.add_label(txt_label_paras))
	
	p.savefile(outputfile)


	
	