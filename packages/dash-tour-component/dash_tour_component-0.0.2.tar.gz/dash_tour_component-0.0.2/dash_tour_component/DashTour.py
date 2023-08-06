# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashTour(Component):
    """A DashTour component.


Keyword arguments:
- children (a list of or a singular dash component, string or number | string; optional): Content to be rendered
Type: node | elem
- id (string; optional): The ID used to identify this component in Dash callbacks.
- accentColor (string; optional): Change --reactour-accent (defaults to accentColor on IE) css custom prop to apply color in Helper, number, dots, etc
Type: string
Default: string
- isOpen (boolean; optional): Whether the Tour component is currently open
- steps (dict; optional): The steps in the tour component. steps has the following type: list of dicts containing keys 'selector', 'content', 'position', 'action', 'style', 'stepInteraction', 'navDotAriaLabel'.
Those keys have the following types:
  - selector (string; optional)
  - content (string; required)
  - position (list of numbers | a value equal to: 'top', 'right', 'bottom', 'left', 'center'; optional)
  - action (optional)
  - style (dict; optional)
  - stepInteraction (boolean; optional)
  - navDotAriaLabel (string; optional)
- className (string; optional): Custom class name to add to the Helper
Type: string
- closeWithMask (boolean; optional): Close the Tour by clicking the Mask
Type: bool
- disableDotsNavigation (boolean; optional): Disable interactivity with Dots navigation in Helper
Type: bool
- disableInteraction (boolean; optional): Disable the ability to click or intercat in any way with the Highlighted element
Type: bool
- disableKeyboardNavigation (a value equal to: PropTypes.bool, PropTypes.array; optional): Disable all keyboard navigation (next and prev step) when true, disable only selected keys when array
Type: bool | array(['esc', 'right', 'left'])
- CurrentStep (number; optional): The Current step
- goTopStep (number; optional): Programmatically change current step after the first render, when the value changes
- highlightedMaskClassName (string; optional): Custom class name to add to the element which is the overlay for the target element when disableInteraction
- inViewThreshold (number; optional): Tolerance in pixels to add when calculating if an element is outside viewport to scroll into view
- maskClassName (string; optional): Custom class name to add to the Mask
- maskSpace (number; optional): Extra Space between in pixels between Highlighted element and Mask
- rounded (number; optional): Beautify Helper and Mask with border-radius (in px)
- scrollDuration (number; optional): Smooth scroll duration when positioning the target element (in ms)
- scrollOffset (number; optional): Offset when positioning the target element after scroll to it
- showButtons (boolean; optional): Show/Hide Helper Navigation buttons
- showCloseButton (boolean; optional): Show/Hide Helper Close button
- showNavigation (boolean; optional): Show/Hide Helper Navigation Dots
- showNavigationNumber (boolean; optional): Show/Hide number when hovers on each Navigation Dot
- showNumber (boolean; optional): Show/Hide Helper Number Badge
- startAt (number; optional): Starting step when Tour is open the first time
- update (string; optional): Value to listen if forced update is needed
- updateDelay (number; optional): Delay time when forcing update. Useful when there are known animation/transitions"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, accentColor=Component.UNDEFINED, isOpen=Component.UNDEFINED, steps=Component.UNDEFINED, className=Component.UNDEFINED, closeWithMask=Component.UNDEFINED, disableDotsNavigation=Component.UNDEFINED, disableInteraction=Component.UNDEFINED, disableKeyboardNavigation=Component.UNDEFINED, CurrentStep=Component.UNDEFINED, goTopStep=Component.UNDEFINED, highlightedMaskClassName=Component.UNDEFINED, inViewThreshold=Component.UNDEFINED, maskClassName=Component.UNDEFINED, maskSpace=Component.UNDEFINED, rounded=Component.UNDEFINED, scrollDuration=Component.UNDEFINED, scrollOffset=Component.UNDEFINED, showButtons=Component.UNDEFINED, showCloseButton=Component.UNDEFINED, showNavigation=Component.UNDEFINED, showNavigationNumber=Component.UNDEFINED, showNumber=Component.UNDEFINED, startAt=Component.UNDEFINED, update=Component.UNDEFINED, updateDelay=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'accentColor', 'isOpen', 'steps', 'className', 'closeWithMask', 'disableDotsNavigation', 'disableInteraction', 'disableKeyboardNavigation', 'CurrentStep', 'goTopStep', 'highlightedMaskClassName', 'inViewThreshold', 'maskClassName', 'maskSpace', 'rounded', 'scrollDuration', 'scrollOffset', 'showButtons', 'showCloseButton', 'showNavigation', 'showNavigationNumber', 'showNumber', 'startAt', 'update', 'updateDelay']
        self._type = 'DashTour'
        self._namespace = 'dash_tour_component'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'accentColor', 'isOpen', 'steps', 'className', 'closeWithMask', 'disableDotsNavigation', 'disableInteraction', 'disableKeyboardNavigation', 'CurrentStep', 'goTopStep', 'highlightedMaskClassName', 'inViewThreshold', 'maskClassName', 'maskSpace', 'rounded', 'scrollDuration', 'scrollOffset', 'showButtons', 'showCloseButton', 'showNavigation', 'showNavigationNumber', 'showNumber', 'startAt', 'update', 'updateDelay']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashTour, self).__init__(children=children, **args)
