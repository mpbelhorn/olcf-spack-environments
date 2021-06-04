{% extends "modules/modulefile.lua" %}
{% block footer %}
setenv('PERSIST_DIR', '/mnt/bb/' .. os.getenv('USER'))
setenv('PSF_DIR', os.getenv('MEMBERWORK') or '')
{% endblock %}
