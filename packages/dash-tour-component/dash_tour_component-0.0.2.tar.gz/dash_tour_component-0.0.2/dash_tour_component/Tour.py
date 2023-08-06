# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tour(Component):
    """A Tour component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- accentColor (string; optional): Change --reactour-accent (defaults to accentColor on IE) css custom prop to apply color in Helper, number, dots, etc
Type: string
Default: string
- isOpen (boolean; optional): Whether the Tour component is currently open
- steps (dict; optional): The steps in the tour component. steps has the following type: list of dicts containing keys 'selector', 'content', 'position', 'action', 'style', 'stepInteraction', 'navDotAriaLabel'.
Those keys have the following types:
  - selector (string; optional)
  - content (a list of or a singular dash component, string or number | dash component; required)
  - position (list of numbers | a value equal to: 'top', 'right', 'bottom', 'left', 'center'; optional)
  - action (optional)
  - style (dict; optional)
  - stepInteraction (boolean; optional)
  - navDotAriaLabel (string; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accentColor=Component.UNDEFINED, isOpen=Component.UNDEFINED, steps=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accentColor', 'isOpen', 'steps']
        self._type = 'Tour'
        self._namespace = 'dash_tour_component'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accentColor', 'isOpen', 'steps']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tour, self).__init__(**args)
