import xml.dom.minidom as md

def variables_definition_parser(path, lanes):
    file = md.parse(path)
    laneSet = file.getElementsByTagName('laneSet')
    for i, name in enumerate(lanes, 1):
      lane = file.createElement('lane')
      lane.setAttribute('id', f'ID{i}')
      lane.setAttribute('name', name)
      

    
    



    <laneSet id="laneSet1">
      <lane id="ID3" name="Роль1">
        <extensionElements>
          <runa:property name="class" value="ru.runa.wfe.extension.assign.DefaultAssignmentHandler"/>
          <runa:property name="config"><![CDATA[ru.runa.wfe.extension.orgfunction.ExecutorByNameFunction(Managers)]]></runa:property>
        </extensionElements>
      </lane>
      <lane id="ID4" name="Роль2">
        <extensionElements>
          <runa:property name="class" value="ru.runa.wfe.extension.assign.DefaultAssignmentHandler"/>
          <runa:property name="config"><![CDATA[]]></runa:property>
        </extensionElements>
      </lane>
    </laneSet>