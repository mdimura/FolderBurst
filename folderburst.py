#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
from tqdm import tqdm
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk

rootPath='.'
if len(sys.argv)>1:
	rootPath=sys.argv[1]
rootPath=os.path.realpath(rootPath)

def size_tree(rootPath,level=0):
	d={}
	d['name']=os.path.basename(rootPath)
	d['children']=[]
	size=0
	for entry in tqdm(scandir(rootPath),position=level,leave=False,desc=('  '*level)+d['name']):
		if entry.is_symlink():
			continue
		if entry.is_file():
			size+= entry.stat().st_size
		if entry.is_dir():
			tmp=size_tree(entry.path,level+1)
			if 'children' in tmp or tmp['size']>0:
				d['children'].append(tmp)
	if len(d['children'])==0:
		tmp=d.pop('children')
		d['size']=size
	elif size>0:
		tmp={'name':'self','size':size}
		d['children'].append(tmp)
	return d

htmlPrefix='''
<head>
    <script src="https://unpkg.com/sunburst-chart"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.12.0/d3.min.js"></script>
    <style>body { margin: 0 }</style>
</head>
<body>
    <div id="chart"></div>
    <script>
        const data = JSON.parse(' '''
htmlSuffix=''' ');
        
        const color = d3.scaleOrdinal(d3.schemeCategory20);
        Sunburst()
            .data(data)
            .minSliceAngle(1.0)
            .showLabels(true)
            .size('size')
            .color(d => color(d.name))
            .tooltipContent((d, node) => `Size: <i>${node.value/1000} kB</i>`)
            (document.getElementById('chart'));
    </script>
</body>
'''
print(htmlPrefix+json.dumps(size_tree(rootPath))+htmlSuffix)