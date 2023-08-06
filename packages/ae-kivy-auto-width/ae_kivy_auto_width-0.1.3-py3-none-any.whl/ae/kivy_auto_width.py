"""
automatic container width with opening animation for kivy apps
==============================================================

This ae portion is providing the mixin class
:class:`ContainerChildrenAutoWidthBehavior`
for to open any container widget with an increasing
width animation and automatic detection that the
label and button texts of the container children
are fully visible/displayed.

"""
from kivy.animation import Animation                                                        # type: ignore
from kivy.core.window import Window                                                         # type: ignore
from kivy.metrics import sp                                                                 # type: ignore
# pylint: disable=no-name-in-module
from kivy.properties import NumericProperty                                                 # type: ignore # noqa: E0611
from kivy.uix.label import Label                                                            # type: ignore
from kivy.uix.widget import Widget                                                          # type: ignore


__version__ = '0.1.3'


class ContainerChildrenAutoWidthBehavior:
    """ mixin class for containers for to determine minimum width at opening with animation.

    If none of the classes mixing-in this class has a `container` attribute, then it will be
    automatically created just before the width animation starts by the
    :meth:`~ContainerChildrenAutoWidthBehavior.open` method.

    """
    container: Widget           #: widget to add the dynamic children to (property provided by container or other mixin)
    width: float                #: width of widget where an instance of this class get mixed-in (can be != container)

    auto_width_duration: float = NumericProperty(0.9)
    """ Duration in seconds of the width animation until the :attr:`auto_width_maximum` width is reached.

    :attr:`auto_width_duration` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.9 seconds.
    """

    auto_width_maximum: float = NumericProperty(Window.width - sp(96))
    """ Maximum widget width in pixels (if the width animation is reaching its end-point).

    :attr:`auto_width_maximum` is a :class:`~kivy.properties.NumericProperty` and
    defaults to the current Window.width - 96sp.
    """

    auto_width_minimum: float = NumericProperty(sp(369))
    """ Minimum widget width in pixels (before the width animation will be stopped).

    :attr:`auto_width_minimum` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 369sp.
    """

    auto_width_padding: float = NumericProperty(sp(87))
    """ Space in pixels of the horizontal padding (as total/sum of left and right padding).

    :attr:`auto_width_padding` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 87sp.
    """

    auto_width_start: float = NumericProperty(sp(3))
    """ Widget width in pixels at the start of the width animation.

    :attr:`auto_width_start` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 3sp.
    """

    _width_anim: Animation = None

    def open(self, *_args, **kwargs):
        """ start optional open animation after calling open method if exists in inheriting container/layout widget.

        :param _args:           unused argument (for to have compatible signature for Popup/ModalView widgets).
        :param kwargs:          extra arguments that are removed before to be passed to the inheriting open method:

                                * 'open_width_animation': `False` will disable the `width` animation (default=True).
        """
        anim_width = kwargs.pop('open_width_animation', True)

        if callable(getattr(super(), 'open', None)):
            # noinspection PyUnresolvedReferences
            super().open(*_args, **kwargs)

        if anim_width:
            if not hasattr(super(), 'container'):
                self.container = getattr(self, '_container', self)  # Popup has _container attribute, BoxLayout=self
            self._width_anim = Animation(width=self.auto_width_maximum, t='in_out_sine', d=self.auto_width_duration)
            self._width_anim.bind(on_progress=self._open_width_progress)
            self.width = self.auto_width_start
            self._width_anim.start(self)

    def _open_width_progress(self, _anim: Animation, _self: Widget, _progress: float):
        if self.width > self.auto_width_minimum:
            if all(chi.texture_size[0] + self.auto_width_padding < self.width
                   for chi in self.container.children if isinstance(chi, Label)):
                self._width_anim.stop(self)
