-- -*- lua -*-
-- Module file created by spack (https://github.com/spack/spack) on {{ timestamp }}
--
-- {{ spec.short_spec }}
--

{% block header %}
{% if short_description %}
whatis([[Name : {{ spec.name }}]])
whatis([[Version : {{ spec.version }}]])
whatis([[Target : {{ spec.target }}]])
whatis([[Short description : {{ short_description }}]])
{% endif %}
{% if configure_options %}
whatis([[Configure options : {{ configure_options }}]])
{% endif %}

{% if long_description %}
help([[{{ long_description| textwrap(72)| join() }}]])
{% endif %}
{% endblock %}

{%- block properties -%}
{# Add properties for a given package to the module #}
{% for property, value in module_property_tags %}
add_property("{{ property }}", "{{ value }}")
{% endfor -%}
{%- endblock -%}

{% block provides %}
{# Prepend the path I unlock as a provider of #}
{# services and set the families of services I provide #}
{% if has_modulepath_modifications %}
-- Services provided by the package
{% for name in provides %}
family("{{ name }}")
{% endfor %}

-- Loading this module unlocks the path below unconditionally
{% for path in unlocked_paths %}
prepend_path("MODULEPATH", "{{ path }}")
{% endfor %}

{# Try to see if missing providers have already #}
{# been loaded into the environment #}
{% if has_conditional_modifications %}
-- Try to load variables into path to see if providers are there
{% for name in missing %}
local {{ name }}_name = os.getenv("LMOD_{{ name|upper() }}_NAME")
local {{ name }}_version = os.getenv("LMOD_{{ name|upper() }}_VERSION")
{% endfor %}

-- Change MODULEPATH based on the result of the tests above
{% for condition, path in conditionally_unlocked_paths %}
if {{ condition }} then
  local t = pathJoin({{ path }})
  prepend_path("MODULEPATH", t)
end
{% endfor %}

-- Set variables to notify the provider of the new services
{% for name in provides %}
setenv("LMOD_{{ name|upper() }}_NAME", "{{ name_part }}")
setenv("LMOD_{{ name|upper() }}_VERSION", "{{ version_part }}")
{% endfor %}
{% endif %}
{% endif %}
{% endblock %}

{% block autoloads %}
{% for module in autoload %}
if not isloaded("{{ module }}") then
{% if verbose %}
    LmodMessage("Autoloading {{ module }}")
{% endif %}
    load("{{ module }}")
end
{% endfor %}
{% endblock %}

{% block environment %}
{% for command_name, cmd in environment_modifications %}
{% if command_name == 'PrependPath' %}
prepend_path("{{ cmd.name }}", "{{ cmd.value }}", "{{ cmd.separator }}")
{% elif command_name == 'AppendPath' %}
append_path("{{ cmd.name }}", "{{ cmd.value }}", "{{ cmd.separator }}")
{% elif command_name == 'RemovePath' %}
remove_path("{{ cmd.name }}", "{{ cmd.value }}", "{{ cmd.separator }}")
{% elif command_name == 'SetEnv' %}
setenv("{{ cmd.name }}", "{{ cmd.value }}")
{% elif command_name == 'UnsetEnv' %}
unsetenv("{{ cmd.name }}")
{% endif %}
{% endfor %}
{% endblock %}

{% block footer %}
{# In case the module needs to be extended with custom LUA code #}
{% endblock %}
