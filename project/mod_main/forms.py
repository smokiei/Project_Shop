from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, widgets


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.
    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class FilterProductsForm(FlaskForm):
    Manufacturer = MultiCheckboxField('Производитель',
                                      choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
