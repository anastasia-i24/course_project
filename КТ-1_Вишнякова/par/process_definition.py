import xml.dom.minidom as md

def process_definition(path, lanes):
    file = md.parse(path)
    laneSet = file.getElementsByTagName('laneSet')[0]
    for i, name in enumerate(lanes, start=3):
      lane = file.createElement('lane')
      lane.setAttribute('id', f'ID{i}')
      lane.setAttribute('name', name)
      
      extension = file.createElement('extensionElements')

      prop_class = file.createElement('runa:property')
      prop_class.setAttribute('name', 'class')
      prop_class.setAttribute('value', 'ru.runa.wfe.extension.assign.DefaultAssignmentHandler')
      extension.appendChild(prop_class)

      prop_config = file.createElement('runa:property')
      prop_config.setAttribute('name', 'config')
      if lanes[name] != '':
        config_value = f'ru.runa.wfe.extension.orgfunction.ExecutorByNameFunction({lanes[name]})'
      else:
         config_value = ''
      cdata = file.createCDATASection(config_value)
      prop_config.appendChild(cdata)
      extension.appendChild(prop_config)

      lane.appendChild(extension)

      laneSet.appendChild(lane)

      with open(path, 'w', encoding='utf-8') as f:
        file.writexml(f, indent='', addindent='  ', newl='\n', encoding='utf-8')