#
# Copyright (C) 2007-2008 by Async Open Source
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Author(s): Johan Dahlin <jdahlin@async.com.br>
#            George Kussumoto <george@async.com.br>
#
"""A dialog to manipulate a sequence of objects
"""
import gettext

from gi.repository import Gtk, GLib, GObject

from kiwi.enums import ListType
from kiwi.ui.delegates import SlaveDelegate
from kiwi.ui.dialogs import yesno
from kiwi.ui.objectlist import ObjectList
from kiwi.utils import gsignal

_ = lambda m: gettext.dgettext('kiwi', m)


class ListContainer(Gtk.Box):
    """A ListContainer is an :class:`ObjectList` with buttons to be able
    to modify the content of the list.
    Depending on the list_mode, @see :class:`set_list_mode` you will
    have add, remove and edit buttons.

    Signals
    =======
      - B{add-item} (returns item):
        - emitted when the add button is clicked, you're expected to
          return an object here
      - B{remove-item} (item, returns bool):
        - emitted when removing an item,
          you can block the removal from the list by returning False
      - B{edit-item} (item):
        - emitted when editing an item
          you can block the update afterwards by returning False

    :ivar add_button: add button
    :type add_button: :class:`Gtk.Button`
    :ivar remove_button: remove button
    :type remove_button: :class:`Gtk.Button`
    :ivar edit_button: edit button
    :type edit_button: :class:`Gtk.Button`
    """

    __gtype_name__ = 'ListContainer'
    gsignal('add-item', retval=object)
    gsignal('remove-item', object, retval=bool)
    gsignal('edit-item', object, retval=bool)
    gsignal('selection-changed', object)

    def __init__(self, columns, orientation=Gtk.Orientation.VERTICAL):
        """
        Create a new ListContainer object.
        :param columns: columns for the :class:`kiwi.ui.objectlist.ObjectList`
        :type columns: a list of :class:`kiwi.ui.objectlist.Columns`
        :param orientation: the position where the buttons will be
            placed: at the right (vertically) or at the bottom (horizontally)
            of the list. Defaults to the right of the list.
        :type: Gtk.Orientation.HORIZONTAL or Gtk.Orientation.VERTICAL
        """
        self._list_type = None

        super(ListContainer, self).__init__(orientation=Gtk.Orientation.HORIZONTAL)

        self._orientation = orientation

        self._create_ui(columns)
        self.set_list_type(ListType.NORMAL)

    # Private API

    def _create_ui(self, columns):
        self.list = ObjectList(columns)
        self.list.connect('selection-changed',
                          self._on_list__selection_changed)
        self.list.connect('row-activated',
                          self._on_list__row_activated)

        self.add_button = Gtk.Button(stock=Gtk.STOCK_ADD)
        self.add_button.connect('clicked', self._on_add_button__clicked)

        self.remove_button = Gtk.Button(stock=Gtk.STOCK_REMOVE)
        self.remove_button.set_sensitive(False)
        self.remove_button.connect('clicked', self._on_remove_button__clicked)

        self.edit_button = Gtk.Button(stock=Gtk.STOCK_EDIT)
        self.edit_button.set_sensitive(False)
        self.edit_button.connect('clicked', self._on_edit_button__clicked)

        self._vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        if self._orientation == Gtk.Orientation.VERTICAL:
            self.pack_start(self.list, True, True, 0)
            self.list.show()
            self._add_buttons_to_box(self._vbox)
            self._pack_vbox()
        elif self._orientation == Gtk.Orientation.HORIZONTAL:
            self._vbox.pack_start(self.list, True, True, 0)
            self.list.show()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            self._add_buttons_to_box(hbox)
            self._vbox.pack_start(hbox, False, True, 0)
            hbox.show()
            self._pack_vbox()
        else:
            raise TypeError(
                "buttons_orientation must be Gtk.Orientation.VERTICAL "
                " or Gtk.Orientation.HORIZONTAL")

    def _add_buttons_to_box(self, box):
        box.pack_start(self.add_button, False, True, 0)
        box.pack_start(self.remove_button, False, True, 0)
        box.pack_start(self.edit_button, False, True, 0)

    def _pack_vbox(self):
        self.pack_start(self._vbox, False, True, 6)
        self._vbox.show()

    def _set_child_packing(self, padding):
        expand = self._orientation == Gtk.Orientation.HORIZONTAL

        self.set_child_packing(self._vbox, expand, True, padding,
                               Gtk.PackType.START)

    def _add_item(self):
        retval = self.emit('add-item')
        if retval is None:
            return
        elif isinstance(retval, NotImplementedError):
            raise retval

        self.list.append(retval)
        self.list.refresh()

    def _remove_item(self, item):
        retval = self.emit('remove-item', item)
        if retval:
            self.list.remove(item)

    def _edit_item(self, item):
        retval = self.emit('edit-item', item)
        if retval:
            self.list.update(item)

    # Public API

    def add_item(self, item):
        """Appends an item to the list
        :param item: item to append
        """
        self.list.append(item)

    def add_items(self, items):
        """Appends a list of items to the list
        :param items: items to add
        :type items: a sequence of items
        """
        self.list.extend(items)

    def remove_item(self, item):
        """Removes an item from the list
        :param item: item to remove
        """
        self.list.remove(item)

    def update_item(self, item):
        """Updates an item in the list.
        You should call this if you change the object
        :param item: item to update
        """
        self.list.update(item)

    def default_remove(self, item):
        """Asks the user confirmation for removal of an item.
        :param item: a description of the item that will be removed
        :returns: True if the user confirm the removal, False otherwise
        """
        response = yesno(_('Do you want to remove %s ?') %
                        (GLib.markup_escape_text(str(item)),),
                         parent=None,
                         default=Gtk.ResponseType.OK,
                         buttons=((Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL),
                                  (Gtk.STOCK_REMOVE, Gtk.ResponseType.OK)))
        return response == Gtk.ResponseType.OK

    def set_list_type(self, list_type):
        """Sets the kind of list type.
        :param list_type:
        """
        if not isinstance(list_type, ListType):
            raise TypeError("list_type must be a ListType enum")

        self.add_button.set_property(
            'visible',
            list_type not in [ListType.READONLY, ListType.REMOVEONLY,
                              ListType.UNADDABLE])
        self.remove_button.set_property(
            'visible',
            list_type not in [ListType.READONLY, ListType.ADDONLY,
                              ListType.UNREMOVABLE])
        self.edit_button.set_property(
            'visible',
            list_type not in [ListType.READONLY, ListType.ADDONLY,
                              ListType.UNEDITABLE, ListType.REMOVEONLY])
        if list_type in [ListType.READONLY, ListType.REMOVEONLY]:
            padding = 0
        else:
            padding = 6
        self._set_child_packing(padding)
        self._list_type = list_type

    def clear(self):
        """Removes all the items in the list"""
        self.list.clear()

    # Callbacks

    def _on_list__selection_changed(self, list, selection):
        object_selected = selection is not None
        self.remove_button.set_sensitive(object_selected)
        self.edit_button.set_sensitive(object_selected)
        self.emit('selection-changed', selection)

    def _on_list__row_activated(self, list, item):
        if self._list_type not in [ListType.READONLY, ListType.ADDONLY,
                                   ListType.UNEDITABLE]:
            self._edit_item(item)

    def _on_add_button__clicked(self, button):
        self._add_item()

    def _on_remove_button__clicked(self, button):
        self._remove_item(self.list.get_selected())

    def _on_edit_button__clicked(self, button):
        self._edit_item(self.list.get_selected())


GObject.type_register(ListContainer)


class ListSlave(SlaveDelegate):
    columns = None
    list_type = ListType.NORMAL

    def __init__(self, columns=None, orientation=Gtk.Orientation.VERTICAL):
        columns = columns or self.columns
        if not columns:
            raise ValueError("columns cannot be empty")

        self.listcontainer = ListContainer(columns, orientation)
        self.listcontainer.connect(
            'add-item', self._on_listcontainer__add_item)
        self.listcontainer.connect(
            'remove-item', self._on_listcontainer__remove_item)
        self.listcontainer.connect(
            'edit-item', self._on_listcontainer__edit_item)
        self.listcontainer.connect(
            'selection-changed', self._on_listcontainer__selection_changed)

        self.listcontainer.set_border_width(6)
        self.listcontainer.show()

        self.refresh()

        SlaveDelegate.__init__(self, toplevel=self.listcontainer)

    def _on_listcontainer__add_item(self, listcontainer):
        try:
            return self.add_item()
        # Don't look, PyGObject workaround.
        except NotImplementedError as e:
            return e

    def _on_listcontainer__remove_item(self, listcontainer, item):
        retval = self.remove_item(item)
        if not isinstance(retval, bool):
            raise ValueError("remove-item must return a bool")
        return retval

    def _on_listcontainer__edit_item(self, listcontainer, item):
        retval = self.edit_item(item)
        if not isinstance(retval, bool):
            raise ValueError("edit-item must return a bool")
        return retval

    def _on_listcontainer__selection_changed(self, listcontainer, selection):
        self.selection_changed(selection)

    # Public API

    def set_list_type(self, list_type):
        """Set list type.
        @see: :class:`Listcontainer.set_list_type`
        """
        self.listcontainer.set_list_type(list_type)

    def add_list_item(self, item):
        """Add item to list.
        @see: :class:`Listcontainer.add_item`
        """
        self.listcontainer.add_item(item)

    def add_list_items(self, item):
        """Add items to list.
        @see: :class:`Listcontainer.add_items`
        """
        self.listcontainer.add_items(item)

    def remove_list_item(self, item):
        """Remove item from list.
        @see: :class:`Listcontainer.remove_item`
        """
        self.listcontainer.remove_item(item)

    def update_list_item(self, item):
        """Update item in list.
        @see: :class:`Listcontainer.edit_item`
        """
        self.listcontainer.update_item(item)

    def refresh(self):
        """Updates all the items in the list.
        Clears the list and calls "populate()"
        """
        self.listcontainer.clear()
        self.listcontainer.add_items(self.populate())

    # Overridables

    def add_item(self):
        """This must be implemented in a subclass if you want to be able
        to add items.

        It should return the model you want to add to the list or None
        if you don't want anything to be added, eg the user cancelled
        creation of the model
        """
        raise NotImplementedError(
            "You need to implement add_item in %s" %
            (type(self).__name__))

    def remove_item(self, item):
        """A subclass can implement this to get a notification after
        an item is removed.
        If it's not implemented :class:`ListContainer.default_remove` will be called
        :returns: False if the item should not be removed
        """
        return self.listcontainer.default_remove(item)

    def edit_item(self, item):
        """A subclass must implement this if you want to support editing
        of objects.
        :returns: False if the item should not be removed
        """
        raise NotImplementedError(
            "You need to implement edit_item in %s" %
            (type(self).__name__))

    def selection_changed(self, selection):
        """This will be called when the selection changes in the ListDialog
        :param selection: selected object or None if nothing is selected
        """

    def populate(self):
        """This will be called once after the user interface construction is done.
        It should return a list of objects which will initially be inserted
        :returns: object to insert
        :rtype: sequence of objects
        """
        return []


class ListDialog(Gtk.Dialog, ListSlave):
    """A ListDialog implements a :class:`ListContainer` in a L{Gtk.Dialog} with
    a close button.

    It's a simple Base class which needs to be subclassed to provide interesting
    functionality.

    Example::

        >>> from kiwi.python import Settable
        >>> from kiwi.ui.objectlist import Column
        >>> class MyListDialog(ListDialog):
        ...     columns = [Column('name')]
        ...     list_type = ListType.UNEDITABLE
        ...
        ...     def populate(self):
        ...         return [Settable(name='test')]
        ...
        ...     def add_item(self):
        ...         return Settable(name="added")

        >>> dialog = MyListDialog()
        >>> dialog.run()

    """

    def __init__(self, columns=None):
        Gtk.Dialog.__init__(self)
        self.add_button(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)

        ListSlave.__init__(self, columns)
        self.vbox.pack_start(self.listcontainer, True, True, 0)
