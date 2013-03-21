'''
    The Home Page for ContactManager
'''

import os

import logging as log
from WebElements import UITemplate, ClientSide
from Models.Contact import Contact

try:
    from WebBot import Page, PageControls
except ImportError:
    from ...WebBot import Page, PageControls

APP_DIR = os.path.dirname(__file__) + "/"

class Home(Page):
    class ContentControl(PageControls.TemplateControl):
        template = UITemplate.fromFile(APP_DIR + "Template.wui")

        def initUI(self, ui, request):
            ui.search.clientSide.focus()
            ui.search.clientSide.on('keyup', ClientSide.hide('contact')(self.contacts.clientSide.get(timeout=500)))
            ui.create.clientSide.on('click', self.contacts.clientSide.put())
            ui.contacts.replaceWith(self.contacts)
            ui.editor.replaceWith(self.editor)

        class Contacts(PageControls.TemplateControl):
            template = UITemplate.fromFile(APP_DIR + "Contacts.wui")
            grabFields = ('search', )

            def initUI(self, ui, request):
                ui.pager.connect('jsIndexChanged', None, self.clientSide, 'get', True)

            def processPut(self, ui, request):
                newContact = Contact(name="New Contact")
                newContact.save()

                contactId = str(newContact.key().id())
                request.fields['contact'] = contactId
                ui.clientSide(self.parentHandler.editor.clientSide.get(params="contact=%s" % contactId))

            def setUIData(self, ui, request):
                results = Contact.all().order('-created')

                search = request.fields.get('search')
                if search:
                    results = results.search(search)

                results = ui.pager.currentPageItems(results, request.fields)
                selectedContact = request.fields.get('contact')
                for result in results:
                    contact = ui.contacts.addRow()
                    contact.id = str(result.key().id())
                    contact.setCell('', self.buildElement('gravatar', properties={'email':result.email or ""}))
                    contact.cell('Name').setText(result.name)
                    contact.cell('Email').setText(result.email or "")
                    contact.cell('Phone Number').setText(result.phone or "")
                    if contact.id == selectedContact:
                        contact.addClass("selected")

                    contact.addClass("Clickable")
                    contact.clientSide.on('click',
                                          contact.clientSide.stealClassFromPeer('selected')(
                                           self.parentHandler.editor.clientSide.get(
                                                                        params='contact=%s' % contact.id)))

        class Editor(PageControls.TemplateControl):
            template = UITemplate.fromFile(APP_DIR + "Editor.wui")

            def initUI(self, ui, request):
                contact = request.fields.get('contact')
                if not contact:
                    ui[0].remove()
                    self.contact = None
                    return
                self.contact = Contact.get_by_id(int(contact))

                ui.delete.clientSide.on('click', self.clientSide.delete(params='contact=%s' % contact))
                for field in (ui.contactName, ui.email, ui.phone):
                    field.clientSide.on('change', self.clientSide.post(True, 'contact=%s' % contact))

            def validPost(self, ui, request):
                ui.insertVariables(request.fields.copy())
                return not ui.query().filter(classes__contains="WError")

            def processPost(self, ui, request):
                self.contact.name = request.fields.get('contactName')
                self.contact.email = request.fields.get('email')
                self.contact.phone = request.fields.get('phone')
                self.contact.save()

                ui.clientSide(self.parentHandler.contacts.clientSide.get(True,
                                                                         'contact=%s' % self.contact.key().id()))

            def processGet(self, ui, request):
                if not self.contact:
                    return

                ui.contactName.setValue(self.contact.name)
                ui.email.setValue(self.contact.email)
                ui.phone.setValue(self.contact.phone)

            def processDelete(self, ui, request):
                if self.contact:
                    self.contact.delete()
                    ui.contact.hide()
                    ui.clientSide(self.parentHandler.clientSide.get())

            def setUIData(self, ui, request):
                ui.gravatar.email = self.contact and self.contact.email or ""

