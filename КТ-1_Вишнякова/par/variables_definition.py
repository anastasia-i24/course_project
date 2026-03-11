import xml.dom.minidom as md

def variables_definition(path, lanes):
    file = md.parse(path)
    for name in lanes:
        variable = file.createElement('variable')

        variable.setAttribute('name', name)
        variable.setAttribute('scriptingName', name)
        variable.setAttribute('format', "ru.runa.wfe.var.format.ExecutorFormat" )
        variable.setAttribute('swimlane', 'true')
        
        if lanes[name] != '':
            variable.setAttribute('editor', 'SwimlaneElement.ManualLabel')

        file.firstChild.appendChild(variable)

        with open(path, 'w', encoding='utf-8') as f:
            file.writexml(f, indent='', addindent='  ', newl='\n', encoding='utf-8')
