var cyStylesOptions = {
    "font-size": 10,
    defaultRelationshipStyle: {
        selector: 'edge[name == "Subtopic in"]',
        style: {
            label: ''
        }
    },
}
var cyStyles = {
    simpleStyle: [{
            selector: 'node',
            style: {
                'label': 'data(name)',
                'font-size': cyStylesOptions["font-size"],
                'background-image': 'data(imageURL)',
                'background-fit': 'cover'
            }
        },
        {
            selector: 'edge',
            style: {
                'label': 'data(name)',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
                'font-size': cyStylesOptions["font-size"],
                'text-rotation': 'autorotate',
                'line-style': 'solid',
                'width': 2,
            }
        },
        cyStylesOptions.defaultRelationshipStyle
    ],
    basicEditStyle: [{
            selector: ':selected',
            style: {
                'color': 'DarkMagenta'
            }
        },
        {
            selector: 'node',
            style: {
                'label': 'data(name)',
                'font-size': cyStylesOptions["font-size"],
                'background-color': 'grey',
            }
        },
        {
            selector: 'node.tempory',
            style: {
                'opacity': 0.25,
            }
        },
        {
            selector: 'edge',
            style: {
                'label': 'data(name)',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
                'font-size': cyStylesOptions["font-size"],
                'text-rotation': 'autorotate',
                'display': 'none',
                'line-color': 'grey',
                'target-arrow-color': 'grey',
            }
        }, {
            selector: 'edge[subject_value = "true"][workspace_value != "false"],[workspace_value = "true"]',
            style: {
                'line-style': 'solid',
                'width': 3,
                'display': 'element',
            }
        },
        cyStylesOptions.defaultRelationshipStyle
    ],
    diffEditStyle: [{
            selector: ':selected',
            style: {
                'color': 'DarkMagenta'
            }
        }, {
            selector: 'node',
            style: {
                'label': 'data(name)',
                'font-size': cyStylesOptions["font-size"],
                'background-color': 'grey',
            }
        }, {
            selector: 'edge.suppress',
            style: {
                'opacity': 0.15,
            }
        },
        {
            selector: 'node.tempory',
            style: {
                'opacity': 0.25,
            }
        },
        {
            selector: 'edge',
            style: {
                'label': 'data(name)',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
                'font-size': cyStylesOptions["font-size"],
                'text-rotation': 'autorotate',
                'width': 3,
                'line-color': 'grey',
                'target-arrow-color': 'grey',
            }
        }, {
            selector: 'edge[workspace_value = "true"][subject_value != "true"]',
            style: {
                'line-style': 'solid',
                'font-weight': 'bold',
            }
        }, {
            selector: 'edge[workspace_value = "false"][subject_value = "true"]',
            style: {
                'line-gradient-stop-colors': 'grey white white grey',
                'line-gradient-stop-positions': '10% 10% 77.5% 77.5%',
                'line-fill': 'linear-gradient ',
                'font-weight': 'bold',
            }
        }, {
            selector: 'edge[workspace_value = "true"][subject_value = "true"]',
            style: {
                'line-style': 'solid',
                'text-outline-color': 'black',
                'text-outline-width': 0.25,
                'color': 'white',
            }
        }, {
            selector: 'edge[workspace_value = "false"][subject_value != "true"]',
            style: {
                'line-gradient-stop-colors': 'grey white white grey',
                'line-gradient-stop-positions': '10% 10% 77.5% 77.5%',
                'line-fill': 'linear-gradient ',
                'text-outline-color': 'black',
                'text-outline-width': 0.25,
                'color': 'white',

            }
        }, {
            selector: 'edge[workspace_value = "false"][subject_value != "true"]:selected',
            style: {
                'text-outline-color': 'DarkMagenta',

            }
        }, {
            selector: 'edge[workspace_value = "undefined"][subject_value = "true"]',
            style: {
                'line-style': 'solid',
            }
        }, {
            selector: 'edge[workspace_value = "undefined"][subject_value = "false"]',
            style: {
                'line-style': 'dashed',
                'line-dash-pattern': '10%, 80%',
            }
        },
        cyStylesOptions.defaultRelationshipStyle
    ],
    previewStyle: [{
            selector: 'node',
            style: {
                'label': 'data(name)',
                'font-size': cyStylesOptions["font-size"],
                'background-image': 'data(imageURL)',
                'background-fit': 'cover'
            }
        },
        {
            selector: 'edge',
            style: {
                'label': 'data(name)',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
                'font-size': cyStylesOptions["font-size"],
                'text-rotation': 'autorotate',
                'line-style': 'solid',
                'opacity': 0
            }
        }, {
            selector: 'edge[preview_value != "false"][original_value = "true"]',
            style: {
                'line-style': 'solid',
                'width': 1,
                'opacity': 0.25
            }
        }, {
            selector: 'edge[preview_value != "true"][original_value = "false"]',
            style: {
                'line-gradient-stop-colors': 'grey white white grey',
                'line-gradient-stop-positions': '10% 10% 77.5% 77.5%',
                'line-fill': 'linear-gradient ',
                'width': 1,
                'opacity': 0.25
            }
        },
        {
            selector: 'edge[preview_value = "false"][original_value = "true"]',
            style: {
                'line-gradient-stop-colors': 'grey white white grey',
                'line-gradient-stop-positions': '10% 10% 77.5% 77.5%',
                'line-fill': 'linear-gradient ',
                'width': 5,
                'opacity': 1
            }
        },
        {
            selector: 'edge[preview_value = "true"][original_value = "false"]',
            style: {
                'width': 5,
                'opacity': 1
            }
        },
        {
            selector: 'edge[preview_value = "true"][original_value = "undefined"]',
            style: {
                'width': 5,
                'opacity': 1
            }
        },
        cyStylesOptions.defaultRelationshipStyle
    ],
    subjectStyle: [{
            selector: 'node',
            style: {
                'label': 'data(name)',
                'font-size': cyStylesOptions["font-size"],
                'background-image': 'data(imageURL)',
                'background-fit': 'cover'
            }
        },
        {
            selector: 'edge',
            style: {
                'label': 'data(name)',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
                'font-size': cyStylesOptions["font-size"],
                'text-rotation': 'autorotate',
                'line-style': 'solid',
                'opacity': 0
            }
        }, {
            selector: 'edge[original_value = "true"]',
            style: {
                'line-style': 'solid',
                'width': 1,
                'opacity': 1
            }
        }, {
            selector: 'edge[original_value = "false"]',
            style: {
                'line-gradient-stop-colors': 'grey white white grey',
                'line-gradient-stop-positions': '10% 10% 77.5% 77.5%',
                'line-fill': 'linear-gradient ',
                'width': 1,
                'opacity': 1
            }
        },
        cyStylesOptions.defaultRelationshipStyle
    ]

}