
tasks = {
    'engine' : {
        'features' : 'cxxshlib',
        'source'   : '**/*.cpp',
        'includes' : '..',
        'ver-num'  : '0.1.0',
        'use' : 'core zmdep-b:calc zmdep-b:print',
    },
}

