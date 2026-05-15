import xml.dom.minidom as md

def process_definition(path, process_name, ids, variables, start_event):
  file = md.parse(path)

  #setting process name
  process = file.getElementsByTagName('process')
  process.setAttribute('name', process_name) 

  #lanes 
  laneSet = file.getElementsByTagName('laneSet')[0]
  for name in variables:
    lane = file.createElement('lane')
    lane.setAttribute('id', f'ID{ids[name]}')
    lane.setAttribute('name', name)
           
    extension = file.createElement('extensionElements')

    prop_class = file.createElement('runa:property')
    prop_class.setAttribute('name', 'class')
    prop_class.setAttribute('value', 'ru.runa.wfe.extension.assign.DefaultAssignmentHandler')
    extension.appendChild(prop_class)

    prop_config = file.createElement('runa:property')
    prop_config.setAttribute('name', 'config')
    if variables[name]['editor'] != '':
      config_value = f'ru.runa.wfe.extension.orgfunction.ExecutorByNameFunction({variables[name]['editor']})'
    else:
      config_value = ''
    cdata = file.createCDATASection(config_value)

    prop_config.appendChild(cdata)
    extension.appendChild(prop_config)
    lane.appendChild(extension)
    laneSet.appendChild(lane)

  #start event
  startEvent = file.getElementsByTagName('startEvent')
  

  with open(path, 'w', encoding='utf-8') as f:
    file.writexml(f, indent='', addindent='  ', newl='\n', encoding='utf-8')