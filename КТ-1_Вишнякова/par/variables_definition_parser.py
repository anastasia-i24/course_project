import xml.dom.minidom as md

def variables_definition_parser(path, lanes):
    file = md.parse(path)
    for name, group in lanes:
        variable = file.createElement('variable')

        variable.setAttribute('name', name)
        variable.setAttribute('scriptingName', name)
        variable.setAttribute('format', "ru.runa.wfe.var.format.ExecutorFormat" )
        variable.setAttribute('swimlane', 'true')

        file.firstChild.appendChild(variable)
