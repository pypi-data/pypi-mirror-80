# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class VegaComponent(Component):
    """A VegaComponent component.
VegaComponent is an wrapper for react-vega's Vega component that is used to render vega specs.
It takes a vega or vega-lite 'spec', and some 'data' to merge into the spec and returns the
rendered visualisation.
For more info see: https://github.com/vega/react-vega/tree/master/packages/react-vega

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- spec (dict; required): A vega/vega-lite spec in json format.
- data (dict; required): Data used to populate the vega spec. Data must be an Object with keys being dataset names defined in the spec's data field in json format."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, spec=Component.REQUIRED, data=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'spec', 'data']
        self._type = 'VegaComponent'
        self._namespace = 'vega_component'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'spec', 'data']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['spec', 'data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(VegaComponent, self).__init__(**args)
