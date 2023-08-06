#
# Kiwi: a Framework and Enhanced Widgets for Python
#
# Copyright (C) 2003-2005 Async Open Source
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307
# USA
#
# Author(s): Christian Reis <kiko@async.com.br>
#            Gustavo Rahal <gustavo@async.com.br>
#            Lorenzo Gil Sanchez <lgs@sicem.biz>
#            Evandro Vale Miquelito <evandro@async.com.br>
#

"""GtkSpinButton support for the Kiwi Framework

"""

from gi.repository import Gtk, GObject

from kiwi.datatypes import number, ValueUnset
from kiwi.ui.proxywidget import ProxyWidgetMixin, ValidatableProxyWidgetMixin
from kiwi.utils import gsignal


class ProxySpinButton(Gtk.SpinButton, ValidatableProxyWidgetMixin):
    """
    A SpinButton subclass which adds supports for the Kiwi Framework.
    This widget supports validation
    The only allowed types for spinbutton are int and float.

    """
    __gtype_name__ = 'ProxySpinButton'

    data_type = GObject.Property(
        getter=ProxyWidgetMixin.get_data_type,
        setter=ProxyWidgetMixin.set_data_type,
        type=str, blurb='Data Type')
    mandatory = GObject.Property(type=bool, default=False)
    model_attribute = GObject.Property(type=str, blurb='Model attribute')
    gsignal('content-changed')
    gsignal('validation-changed', bool)
    gsignal('validate', object, retval=object)

    allowed_data_types = number

    def __init__(self, data_type=int):
        # since the default data_type is str we need to set it to int
        # or float for spinbuttons
        Gtk.SpinButton.__init__(self)
        ValidatableProxyWidgetMixin.__init__(self)
        self.props.data_type = data_type
        self.set_property('xalign', 1.0)
        self.set_property("truncate-multiline", True)

        # We need to do this because spinbuttons are supposed to accept only
        # numbers.
        self.set_numeric(True)

        # This used to be an override, but after the gtk3 migration if we
        # use the override or create a do_changed method GObject will break
        # the object in a way that it will be considered a Gtk.SpinButton
        # directly instead of a ProxySpinButton. The side effect of that
        # would be that out custom events (e.g. validate) would not exist.
        self.connect('changed', self._on_changed)

    def _on_changed(self, widget):
        """Called when the content of the spinbutton changes.
        """
        # This is a work around, because GtkEditable.changed is called too
        # often, as reported here: http://bugzilla.gnome.org/show_bug.cgi?id=64998
        if self.get_text() != '':
            self.emit('content-changed')

    def read(self):
        return self._from_string(self.get_text())

    def update(self, data):
        if data is None or data is ValueUnset:
            if self.props.mandatory and self.get_text() != "":
                self.emit('validation-changed', False)
            self.set_text("")
        else:
            if self.props.mandatory and self.get_text() == "":
                self.emit('validation-changed', True)
            # set_value accepts a float or int, no as_string conversion needed,
            # and since we accept only int and float just send it in.
            self.set_value(data)

    # Old IconEntry API

    def set_tooltip(self, text):
        self.set_property('primary-icon-tooltip-text', text)

    def set_pixbuf(self, pixbuf):
        # Spinbuttons are always right aligned
        self.set_property('primary-icon-pixbuf', pixbuf)

    def add_css_class(self, css_class):
        sc = self.get_style_context()
        sc.add_class(css_class)

    def remove_css_class(self, css_class):
        sc = self.get_style_context()
        sc.remove_class(css_class)

GObject.type_register(ProxySpinButton)
