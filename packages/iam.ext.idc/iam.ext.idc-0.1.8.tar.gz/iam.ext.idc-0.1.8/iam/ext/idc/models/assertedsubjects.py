"""Declares :class:`AssertedSubject`."""
# pylint: disable=unused-argument,no-self-use
from django.db import models
from django.utils.translation import gettext_lazy as _


class AssertedSubject(models.Model):
    """Represents a :term:`Subject` that was asserted by an
    :term:`Identity Provider` or :term:`Asserting Party`.
    """
    USERNAME_FIELD = 'asid'
    REQUIRED_FIELDS = []

    #: Is always ``False``.
    is_anonymous = False

    #: Is always ``True``
    is_authenticated = True

    #: Is always ``True``
    is_active = True

    #: The local :term:`Subject Identifier`. This identifier must only be used
    #: within the scope of the consuming application.
    lsid = models.BigAutoField(
        verbose_name=_("Local Subject ID"),
        primary_key=True,
        blank=False,
        null=False,
        editable=False,
        db_column='lsid'
    )

    #: The identity that was asserted by an :term:`AP`/:term:`IdP` when the
    #: :class:`AssertedSubject` first authenticated with the consuming
    #: application.
    asid = models.CharField(
        verbose_name=_("Asserted Identity"),
        max_length=254,
        blank=False,
        null=False,
        unique=True,
        db_column='asid'
    )

    #: Indicates if the :term:`Asserted Subject` is considered external.
    #: Implementations should ensure that external :term:`Subjects` have
    #: as least privileges as possible, and all privileges that are granted
    #: by default to internal subjects are to be explicitely granted. Defaults
    #: to ``True``.
    external = models.BooleanField(
        verbose_name=_("External"),
        blank=False,
        null=False,
        default=True,
        db_column='is_external'
    )

    #: Indicates if the :term:`Subject` is a :term:`Super User`. Can not be
    #: ``True`` if :attr:`AssertedSubject.external` is also ``True``.
    is_superuser = models.BooleanField(
        verbose_name=_("Superuser"),
        blank=False,
        null=False,
        default=False,
        db_column='is_superuser'
    )

    @property
    def is_staff(self):
        """Return a boolean indicating if the user can access the admin
        pages.
        """
        return self.is_superuser

    @classmethod
    def new(cls):
        """Return a new :class:`AssertedSubject` instance."""
        return cls()

    def get_username(self):
        """Return :attr:`asid`."""
        return self.asid

    def set_password(self, *args, **kwargs):
        """Does nothing."""
        return None

    def check_password(self, *args, **kwargs):
        """Always returns ``False``, since an :term:`Asserted Subject`
        authenticates itself at the :term:`AP`/:term:`IdP`.
        """
        return False

    def set_unusable_password(self, *args, **kwargs):
        """Does nothing, exists for :mod:`django.contrib.auth` compatibility."""
        return None

    def has_perm(self, perm, obj=None):
        """Returns ``True`` if the user has the specified permission, where `perm`
        is in the format ``"<app label>.<permission codename>"``. (see documentation
        on permissions). If the user is inactive, this method will always return
        ``False``. For an active superuser, this method will always return ``True``.

        If `obj` is passed in, this method won’t check for a permission for the model,
        but for this specific object.
        """
        return self.is_superuser

    def has_module_perms(self, package_name):
        """Returns ``True`` if the user has any permissions in the given package
        (the Django app label). If the user is inactive, this method will always
        return ``False``. For an active superuser, this method will always return
        ``True``.
        """
        return self.is_staff or self.is_superuser

    def has_unusable_password(self, *args, **kwargs):
        """Always returns ``True``, since an :term:`Asserted Subject`
        authenticates itself at the :term:`AP`/:term:`IdP`.
        """
        return False

    class Meta: # pylint: disable=missing-class-docstring,too-few-public-methods
        app_label = 'idc'
        constraints = [
            models.CheckConstraint(
                name="assertedsubjects_not_superuser_and_external",
                check=~(models.Q(external=True) & models.Q(is_superuser=True))
            )
        ]
        db_table = 'assertedsubjects'
        default_permissions = []
        verbose_name = _("Asserted Subject")
        verbose_name_plural = _("Asserted Subjects")
