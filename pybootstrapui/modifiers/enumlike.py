class BaseConstants:
    @classmethod
    def values(cls):
        return [
            value for key, value in cls.__dict__.items()
            if not key.startswith('__') and not callable(value)
        ]


class ColorBase(BaseConstants):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    SUCCESS = 'success'
    DANGER = 'danger'
    WARNING = 'warning'
    INFO = 'info'
    LIGHT = 'light'
    DARK = 'dark'
    BODY_SECONDARY = 'body-secondary'
    BODY_TERTIARY = 'body-tertiary'
    BODY = 'body'
    BLACK = 'black'
    WHITE = 'white'
    TRANSPARENT = 'transparent'


class BackgroundColor(ColorBase):
    PRIMARY_SUBTLE = 'primary-subtle'
    SECONDARY_SUBTLE = 'secondary-subtle'
    SUCCESS_SUBTLE = 'success-subtle'
    DANGER_SUBTLE = 'danger-subtle'
    WARNING_SUBTLE = 'warning-subtle'
    INFO_SUBTLE = 'info-subtle'
    LIGHT_SUBTLE = 'light-subtle'
    DARK_SUBTLE = 'dark-subtle'

    @classmethod
    def values(cls):
        return super().values() + [
            cls.PRIMARY_SUBTLE, cls.SECONDARY_SUBTLE, cls.SUCCESS_SUBTLE,
            cls.DANGER_SUBTLE, cls.WARNING_SUBTLE, cls.INFO_SUBTLE,
            cls.LIGHT_SUBTLE, cls.DARK_SUBTLE
        ]


class TextColor(ColorBase):
    pass


class BorderClasses(BaseConstants):
    TOP = 'top'
    END = 'end'
    BOTTOM = 'bottom'
    START = 'start'
    ALL = 'all'


class SizeBase(BaseConstants):
    SM = 'sm'
    SMALL = 'sm'
    LG = 'lg'
    LARGE = 'lg'


class Breakpoints(SizeBase):
    MD = 'md'
    XL = 'xl'
    XXL = 'xxl'


class DisplayValues(BaseConstants):
    NONE = 'none'
    INLINE = 'inline'
    INLINE_BLOCK = 'inline-block'
    BLOCK = 'block'
    GRID = 'grid'
    INLINE_GRID = 'inline-grid'
    TABLE = 'table'
    TABLE_CELL = 'table-cell'
    TABLE_ROW = 'table-row'
    FLEX = 'flex'
    INLINE_FLEX = 'inline-flex'


class FlexDirection(BaseConstants):
    ROW = 'row'
    ROW_REVERSE = 'row-reverse'
    COLUMN = 'column'
    COLUMN_REVERSE = 'column-reverse'


class JustifyContent(BaseConstants):
    START = 'start'
    END = 'end'
    CENTER = 'center'
    BETWEEN = 'between'
    AROUND = 'around'
    EVENLY = 'evenly'


class AlignItems(BaseConstants):
    START = 'start'
    END = 'end'
    CENTER = 'center'
    BASELINE = 'baseline'
    STRETCH = 'stretch'


class AlignSelf(AlignItems):
    pass


class FlexWrap(BaseConstants):
    NOWRAP = 'nowrap'
    WRAP = 'wrap'
    WRAP_REVERSE = 'wrap-reverse'


class OrderValues(BaseConstants):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class FloatValues(BaseConstants):
    START = 'start'
    END = 'end'
    NONE = 'none'


class SelectValues(BaseConstants):
    ALL = 'all'
    AUTO = 'auto'
    NONE = 'none'


class PointerEventsValues(BaseConstants):
    NONE = 'none'
    AUTO = 'auto'


class Position(BaseConstants):
    STATIC = 'static'
    RELATIVE = 'relative'
    ABSOLUTE = 'absolute'
    FIXED = 'fixed'
    STICKY = 'sticky'


class Opacity(BaseConstants):
    ZERO = 0
    TWENTY_FIVE = 25
    FIFTY = 50
    SEVENTY_FIVE = 75
    HUNDRED = 100


class Spacing(BaseConstants):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    AUTO = 'auto'


class Size(BaseConstants):
    TWENTY_FIVE = 25
    FIFTY = 50
    SEVENTY_FIVE = 75
    HUNDRED = 100
    AUTO = 'auto'


class ZIndex(BaseConstants):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    AUTO = 'auto'


class Gap(BaseConstants):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Shadow(BaseConstants):
    SM = 'sm'
    SMALL = SM
    LG = 'lg'
    LARGE = LG


class TextAlign(BaseConstants):
    START = 'start'
    CENTER = 'center'
    END = 'end'
    JUSTIFY = 'justify'


class TextTransform(BaseConstants):
    LOWERCASE = 'lowercase'
    UPPERCASE = 'uppercase'
    CAPITALIZE = 'capitalize'


class BackgroundPattern(BaseConstants):
    DOTS = 'dots'
    LINES = 'lines'
    STRIPES = 'stripes'
    GRID = 'grid'


class TransitionProperty(BaseConstants):
    ALL = 'all'
    COLOR = 'color'
    BACKGROUND = 'background'
    OPACITY = 'opacity'
    TRANSFORM = 'transform'


class Animation(BaseConstants):
    FADE = 'fade'
    SLIDE = 'slide'
    ZOOM = 'zoom'
    SPIN = 'spin'


class AlignContent(BaseConstants):
    START = 'start'
    END = 'end'
    CENTER = 'center'
    STRETCH = 'stretch'
    BETWEEN = 'between'
    AROUND = 'around'


class ButtonStyle(ColorBase, SizeBase):
    PRIMARY_OUTLINE = "outline-primary"
    SECONDARY_OUTLINE = "outline-secondary"
    SUCCESS_OUTLINE = "outline-success"
    DANGER_OUTLINE = "outline-danger"
    WARNING_OUTLINE = "outline-warning"
    INFO_OUTLINE = "outline-info"
    LIGHT_OUTLINE = "outline-light"