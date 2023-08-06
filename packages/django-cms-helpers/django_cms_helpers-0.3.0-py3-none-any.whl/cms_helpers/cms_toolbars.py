from cms.extensions.toolbar import ExtensionToolbar
from cms.utils import get_language_list
from django.utils.encoding import force_text
from django.utils.translation import get_language_info


class TitleExtensionToolbar(ExtensionToolbar):
    model = None
    insert_after = None

    def get_item_position(self, menu):
        position = None
        for items in menu._memo.values():
            for item in items:
                if force_text(getattr(item, 'name', None)) in (
                    force_text(self.insert_after),
                    '{0}...'.format(self.insert_after)
                ):
                    position = menu._item_position(item) + 1
                    break

        return position

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if not current_page_menu or not self.page:
            return

        languages = get_language_list(self.current_site.pk)
        is_single_lang = len(languages) < 2
        position = self.get_item_position(current_page_menu)
        urls = self.get_title_extension_admin()
        page = self._get_page()
        titleset = page.title_set.filter(language__in=languages)

        if hasattr(self.toolbar, 'edit_mode_active'):
            not_edit_mode = not self.toolbar.edit_mode_active
        else:
            not_edit_mode = not self.toolbar.edit_mode

        extended_menu = current_page_menu if is_single_lang else (
            current_page_menu.get_or_create_menu(
                key='{0}_menu'.format(self.model._meta.db_table),
                verbose_name=self.model._meta.verbose_name,
                position=position, disabled=not_edit_mode))

        nodes = [(title_extension, url, title) for (
            (title_extension, url), title) in zip(urls, titleset)]

        for title_extension, url, title in nodes:
            item_position = position if is_single_lang else None
            language_str = get_language_info(title.language)['name_translated']
            name = '{0}{1}'.format(
                '' if is_single_lang else (language_str + ' '),
                self.model._meta.verbose_name)
            extended_menu.add_modal_item(
                name, url=url, disabled=not_edit_mode, position=item_position)
