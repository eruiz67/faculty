# -*- coding: utf-8 -*-
{
    'name': "faculty",

    'summary': """
        Aplicación creada por Ernesto Ruiz para la gestión de estudiantes, profesores, cursos y exámenes""",

    'description': """
Funcionalidades
Primeramente, es necesario la creación de usuarios en el panel de administración. Se crearán los usuarios para la aplicación a través del menú de configuración. Se crearán los usuarios internos y se le asignarán cualquiera de los siguientes roles
    • Admin
    • Estudiante
    • Profesor
Solamente se debe asignar un rol exclusivamente a un usuario.
El admin será encargado de la creación de estudiantes, profesores y cursos.
Para la creación de un estudiante será necesario asignarle un usuario creado previamente y llenar otros datos, entre ellos asignarle créditos para posteriormente matricular en cursos, este usuario deberá tener permisos de estudiante asignado. No se admitirá seleccionar el mismo usuario para diferentes estudiantes ni un usuario que no tenga permisos de estudiante.
Para la creación de un profesor será necesario asignarle un usuario creado previamente y llenar otros datos, este usuario deberá tener permisos de profesor asignado. No se admitirá seleccionar el mismo usuario para diferentes profesores ni un usuario que no tenga permisos de profesor.
Para crear un curso, se llenarán los datos y se le adicionarán una lista de profesores.
El admin podrá matricular un estudiante en un curso desde la vista formulario de un estudiante al dar clic en el botón matricular. Se desplegará un cuadro para seleccionar el curso a matricular y serán descontados los créditos del curso a los créditos del estudiante.
El admin también podrá adicionar un profesor a un curso desde la vista formulario del profesor. 
No admite que un usuario sea profesor y estudiante al mismo tiempo.

Estudiante:
El estudiante podrá loguearse en el sistema con su nombre de usuario y password. Al hacerlo tendrá acceso a sus opciones del menú. 
El estudiante tendrá el acceso a la lista de cursos, la lista de profesores de los cursos en los que esta matriculada y una lista de exámenes publicados para los cursos en los que está matriculado.
Para matricular en un curso un estudiante seleccionará un curso de la lista y en la vista formulario dará clic en el botón matricular.  Automáticamente se le descontaran los créditos necesarios para ese curso a sus créditos restantes.
El estudiante podrá darse de baja de un curso, pero sus créditos no les serán devueltos.
Profesor:
El profesor podrá loguearse en el sistema con su nombre de usuario y password. Al hacerlo tendrá acceso a sus opciones del menú. 
El profesor tendrá el acceso a la lista de cursos, la lista de estudiantes de los cursos de los que es profesor matriculada, una lista de exámenes para los cursos de los que es profesor, y una lista de respuestas enviadas por sus estudiantes a esos exámenes.
El profesor podrá crear un examen al asignarle un nombre descripción, fichera y curso. Un profesor solamente podrá crear exámenes para los cursos que imparte.  Una vez creado el examen, el profesor podrá publicarlo en ese momento o programar que sea publicado en una fecha y hora determinada.
Los estudiantes solamente podrán ver los exámenes que sean publicados.
Una vez publicado el estudiante podrá enviar su respuesta para estos exámenes. Para ello selecciona un examen de la lista y en la vista formulario selecciona “Enviar respuesta” (deberá suministrar un fichero y la descripción)
Un profesor podrá calificar las respuestas enviadas de los exámenes de los cursos que imparte.
Un profesor podrá, además asignar una nota global para un curso a un estudiante, para ello desde la vista formulario de un estudiante dará clic en la opción evaluar y seleccionara el curso a evaluar para ese estudiante. Los profesores solamente podrán evaluar los cursos que impartan.
    """,

    'author': "Ernesto Ruiz",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/user_views.xml',
        'views/course_views.xml',
        'views/professor_views.xml',
        'views/exam_views.xml',
        'wizards/program_course_wizard.xml',
        'wizards/response_exam_wizard.xml',
        'wizards/qualify_exam_wizard.xml',
        'wizards/course_global_score_wizard.xml',
        'wizards/enroll_wizard.xml',
        'views/actions.xml',
        'views/menus.xml',
        'data/cron.xml',
        'views/templates.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':
    True
}