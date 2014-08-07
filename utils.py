import os

from cfg import TMPL_DIR, TMPL_INC_TAG, TMPL_VAR_TAG, TMPL_404_PAGE, TMPL_DEFAULT_VARS

def render_template(filename, **kwargs):
	if not os.path.isfile(os.path.join(TMPL_DIR, filename)):
		return render_template(TMPL_404_PAGE)
	content = _parse_include(filename)
	content = _parse_variable(content, **TMPL_DEFAULT_VARS.update(kwargs))
	return content	

def content_rank(content_list, *args, clear=True):
	rank = [0 for content in content_list]
	for i,content in enumerate(content_list):
		for kw in args:
			if kw in content:
				rank[i] += 1
	sorted_list = sorted(zip(rank, content_list), key=lambda item: item[0], reverse=True)
	if clear:
		return [item[1] for item in sorted_list if item[0]>0]
	else:
		return [item[1] for item in sorted_list]

def _parse_include(filename):
	if not os.path.isfile(os.path.join(TMPL_DIR, filename)):
		return ''
	with open(os.path.join(TMPL, filename), 'r') as f:
		content = f.read()
	result = ''
	prev_tag = None
	for tag in TMPL_INC_TAG.finditer(content):
		if not prev_tag:
			result += content[0:tag.start()]
		else:
			result += content[prev_tag.end():tag.start()]
		included_file = tag.groupdict()['filename']
		if not os.path.isfile(os.path.join(TMPL_DIR, included_file)):
			result += _parse_include(included_file)
		prev_tag = tag
	if not prev_tag:
		return content
	if tag and tag.end() != len(content):
		result += content[tag.end():]
	return result

def _parse_variable(content, **kwargs):
	var_names = kwargs.keys()
	result = ''
	prev_tag = None
	for tag in TMPL_VAR_TAG.finditer(content):
		if not prev_tag:
			result += content[0:tag.start()]
		else:
			result += content[prev_tag.end():tag.start()]
		name = tag.groupdict()['varname']
		if name in var_names:
			result += kwargs[name]
	if not prev_tag:
		return content
	if tag and tag.end() != len(content):
		result += content[tag.end():]
	return result