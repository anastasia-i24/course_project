import xml.dom.minidom as md

def process_definition(path, process_name, ids, variables, start_event, sequence_flows, parallel_gateways, exclusive_gateways, user_tasks, script_tasks, end_event):
  file = md.parse(path)

  #setting process name
  process = file.getElementsByTagName('process')[0]
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
    if variables[name]['editor']:
      config_value = f'ru.runa.wfe.extension.orgfunction.ExecutorByNameFunction({variables[name]['editor']})'
    else:
      config_value = ''
    cdata = file.createCDATASection(config_value)
    prop_config.appendChild(cdata)
    extension.appendChild(prop_config)

    lane.appendChild(extension)

    laneSet.appendChild(lane)

  #start event
  startEvent = file.getElementsByTagName('startEvent')[0]
  startEvent.setAttribute('id', f'ID{ids[name]}')
  startEvent.setAttribute('name', start_event['name'])

  extension = file.createElement('extensionElements')
  prop_lane = file.createElement('runa:property')
  prop_lane.setAttribute('name', 'lane')
  prop_lane.setAttribute('value', start_event['value'])

  extension.appendChild(prop_lane)
  startEvent.appendChild(extension)

  #sequence flows
  for flow in sequence_flows:
    sequenceFlow = file.createElement('sequenceFlow')
    sequenceFlow.setAttribute('id', ids[flow])
    sequenceFlow.setAttribute('name', flow)
    sequenceFlow.setAttribute('sourceRef', sequence_flows[flow]['from'])
    sequenceFlow.setAttribute('targetRef', sequence_flows[flow]['to'])

  #parallel gateways
  for pg in parallel_gateways:
    parallelGateway = file.createElement('parallelGateway')
    parallelGateway.setAttribute('id', ids[pg])
    parallelGateway.setAttribute('name', pg)

  #exclusive gateways
  for eg in exclusive_gateways:
    exclusiveGateway = file.createElement('exclusiveGateway')
    exclusiveGateway.setAttribute('id', ids[eg])
    exclusiveGateway.setAttribute('name', eg)

    if exclusive_gateways[eg]:
      extension = file.createElement('extensionElements')

      prop_class = file.createElement('runa:property')
      prop_class.setAttribute('name', 'class')
      prop_class.setAttribute('value', 'ru.runa.wfe.extension.decision.GroovyDecisionHandler')
      extension.appendChild(prop_class)

      prop_config = file.createElement('runa:property')
      prop_config.setAttribute('name', 'config')
      cdata = file.createCDATASection(exclusive_gateways[eg])
      prop_config.appendChild(cdata)
      extension.appendChild(prop_config)

      exclusiveGateway.appendChild(extension)
      
  #user tasks
  for ut in user_tasks:
    userTask = file.createElement('userTask')
    userTask.setAttribute('id', ids[ut])
    userTask.setAttribute('name', ut)

    extension = file.createElement('extensionElements')

    prop_lane = file.createElement('runa:property')
    prop_lane.setAttribute('name', 'lane')
    prop_lane.setAttribute('value', user_tasks[ut]['value'])
    extension.appendChild(prop_lane)

    if user_tasks[ut]['deadline']:
      prop_deadline = file.createElement('runa:property')
      prop_deadline.setAttribute('name', 'taskDeadline')
      prop_deadline.setAttribute('value', user_tasks[ut]['deadline'])
      extension.appendChild(prop_deadline)

    if user_tasks[ut]['reassign']:
      prop_reassign = file.createElement('runa:property')
      prop_reassign.setAttribute('name', 'reassign')
      prop_reassign.setAttribute('value', user_tasks[ut]['reassign'])
      extension.appendChild(prop_reassign)

    userTask.appendChild(extension) 

  #script tasks
  for st in script_tasks:
    scriptTask = file.createElement('scriptTask')
    scriptTask.setAttribute('id', ids[st])
    scriptTask.setAttribute('name', st)

    extension = file.createElement('extensionElements')

    prop_class = file.createElement('runa:property')
    prop_class.setAttribute('name', 'class')
    prop_class.setAttribute('value', f'ru.runa.wfe.extension.handler.{script_tasks[st]['value']}')
    extension.appendChild(prop_class)

    prop_config = file.createElement('runa:property')
    prop_config.setAttribute('name', 'config')
    cdata = file.createCDATASection(script_tasks[st]['config'])
    prop_config.appendChild(cdata)
    extension.appendChild(prop_config)

    scriptTask.appendChild(extension)


  #end event
  endEvent = file.getElementsByTagName('endEvent')[0]
  endEvent.setAttribute('id', ids[end_event])
  endEvent.setAttribute('name', end_event)

  with open(path, 'w', encoding='utf-8') as f:
    file.writexml(f, indent='', addindent='  ', newl='\n', encoding='utf-8')