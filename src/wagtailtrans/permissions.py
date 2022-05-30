from django.contrib.auth.models import Group, Permission
from wagtail.core.models import (
    Collection, GroupCollectionPermission, GroupPagePermission, PagePermissionTester, UserPagePermissionsProxy)

from wagtailtrans.conf import get_wagtailtrans_setting


def create_group_permissions(group, language):
    """create all required permissions on the translator group

    :param group:  Group instance
    :param language: Language instance
    """
    collection_perms = [
        Permission.objects.get_by_natural_key(
            'add_document', 'wagtaildocs', 'document'),
        Permission.objects.get_by_natural_key(
            'change_document', 'wagtaildocs', 'document'),
        Permission.objects.get_by_natural_key(
            'delete_document', 'wagtaildocs', 'document'),
        Permission.objects.get_by_natural_key(
            'change_image', 'wagtailimages', 'image'),
        Permission.objects.get_by_natural_key(
            'add_image', 'wagtailimages', 'image'),
        Permission.objects.get_by_natural_key(
            'delete_image', 'wagtailimages', 'image'),
    ]
    # access wagtail admin permission
    group.permissions.add(Permission.objects.get_by_natural_key(
        'access_admin', 'wagtailadmin', 'admin'
    ))

    collection = Collection.objects.filter(
        name='collection-%s' % language.code).first()
    if not collection:
        root = Collection.objects.first().get_root()
        collection = root.add_child(name='collection-%s' % language.code)
        for perm in collection_perms:
            GroupCollectionPermission.objects.create(
                permission=perm,
                group=group,
                collection=collection
            )


def get_or_create_language_group(language):
    """Create new translator group for language

    :param language: Language instance
    :return: Group
    """
    group, created = Group.objects.get_or_create(
        name='translator-%s' % language.code)
    if created:
        create_group_permissions(group, language)
    return group


def create_group_page_permission(page, language):
    """Create new GroupPagePermissions for
    the newly created page

    :param page: TranslatablePage instance
    :param language: Language instance
    """
    translator_perms = ['edit', 'publish']
    group = get_or_create_language_group(language)

    for perm in translator_perms:
        GroupPagePermission.objects.create(
            group=group,
            page=page,
            permission_type=perm
        )


class TranslatablePagePermissionTester(PagePermissionTester):
    """Custom permissions tester for translatable pages."""

    def can_delete(self, *args, **kwargs):
        """Check if a page can be deleted
        We make the check if the translated sites are kept in sync and
        if the page is a translated page (it has a canonical page)

        :return: Boolean

        """
        has_canonical = getattr(self.page.specific, 'canonical_page', False)
        if (
            has_canonical and get_wagtailtrans_setting('SYNC_TREE') and
            not self.user.is_superuser
        ):
            return False
        return super().can_delete(*args, **kwargs)


class TranslatableUserPagePermissionsProxy(UserPagePermissionsProxy):
    """Custom Permission proxy to insert our custom tester"""

    def for_page(self, page):
        """Get the user page permissions for this page
        We implement our custom  Permission tester here

        :param page: Page object
        :return: TranslatablePagePermissionsTester instance

        """
        return TranslatablePagePermissionTester(self, page)
