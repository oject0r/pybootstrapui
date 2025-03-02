from typing import Literal, Optional
from pybootstrapui.components.base import HTMLElement



ColorBase = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark', 'body-secondary', 'body-tertiary', 'body', 'black', 'white', 'transparent']
ColorBasic = Literal[*ColorBase]

BackgroundColors = ColorBase + ['primary-subtle', 'secondary-subtle', 'success-subtle', 'danger-subtle', 'warning-subtle', 'info-subtle', 'light-subtle', 'dark-subtle']
BackgroundColor = Literal[*BackgroundColors]

TextColors = [color for color in ColorBase]
TextColor = Literal[*TextColors]

BorderClasses = Literal[
    'top', 'end', 'bottom', 'start', 'all'
]

Breakpoints = Literal['sm', 'md', 'lg', 'xl', 'xxl']

DisplayValues = ['none', 'inline', 'inline-block', 'block', 'grid', 'inline-grid', 'table', 'table-cell', 'table-row', 'flex', 'inline-flex']
FlexDirection = ['row', 'row-reverse', 'column', 'column-reverse']
JustifyContent = ['start', 'end', 'center', 'between', 'around', 'evenly']
AlignItems = ['start', 'end', 'center', 'baseline', 'stretch']
AlignSelf = ['start', 'end', 'center', 'baseline', 'stretch']
FlexWrap = ['nowrap', 'wrap', 'wrap-reverse']
OrderValues = [0, 1, 2, 3, 4, 5]

FloatValues = ['start', 'end', 'none']


SelectValues = ['all', 'auto', 'none']
PointerEventsValues = ['none', 'auto']


class BaseModifier:
    def __init__(self):
        self.classes = []

    def construct(self) -> str:
        return ' '.join(self.classes)

    def class_add(self, *classnames: str) -> 'BaseModifier':
        self.classes += classnames
        return self

    def apply(self, *elements: HTMLElement) -> list[HTMLElement] | HTMLElement:
        [element.add_class(*self.classes) for element in elements]
        if len(elements) > 1:
            return list(elements)

        return elements[0]

class __Modifier(BaseModifier):
    def background(self, color: BackgroundColor) -> 'Modifier':
        self.classes.append(f'bg-{color}')
        return self

    def background_gradient(self) -> 'Modifier':
        self.classes.append('bg-gradient')
        return self

    def border(self,
               placement: BorderClasses = 'all',
               color: Optional[BackgroundColor] = None,
               thickness: Optional[Literal[1, 2, 3, 4, 5]] = None
               ) -> 'Modifier':
        self.classes.append(f'border-{placement}' if placement != 'all' else 'border')

        if color:
            self.classes.append(f'border-{color}')

        if thickness:
            self.classes.append(f'border-{thickness}')

        return self

    def border_remove(self, placement: BorderClasses) -> 'Modifier':
        self.classes.append(f'border-{placement}-0' if placement != 'all' else 'border-0')
        return self

    def radius(self,
               placement: BorderClasses = 'all',
               size: Optional[Literal[0, 1, 2, 3, 4, 5]] = None,
               shape: Optional[Literal['circle', 'pill']] = None) -> 'Modifier':
        if size is not None:
            self.classes.append(f'rounded-{placement}-{size}')
        elif shape:
            self.classes.append(f'rounded-{placement}-{shape}')
        else:
            self.classes.append(f'rounded-{placement}')
        return self

    def opacity(self, value: Literal[0, 25, 50, 75, 100]) -> 'Modifier':
        self.classes.append(f'opacity-{value}')
        return self

    def overflow(self, mode: Literal['auto', 'hidden', 'visible', 'scroll'], dimension: Literal['x', 'y', 'all'] = 'all') -> 'Modifier':
        self.classes.append(f'overflow-{dimension}-{mode}' if dimension != 'all' else f'overflow-{mode}')
        return self

    def text_color(self, color: TextColor) -> 'Modifier':
        self.classes.append(f'text-{color}')
        return self

    def text_opacity(self, opacity: int) -> 'Modifier':
        self.classes.append(f'text-opacity-{opacity}')
        return self

    def link_opacity(self, opacity: int) -> 'Modifier':
        self.classes.append(f'link-opacity-{opacity}')
        return self

    def link_hover_opacity(self, opacity: int) -> 'Modifier':
        self.classes.append(f'link-opacity-{opacity}-hover')
        return self

    def link_underline_opacity(self, opacity: int) -> 'Modifier':
        self.classes.append(f'link-underline-opacity-{opacity}')
        return self

    def link_underline_color(self, color: ColorBasic):
        self.classes.append(f'link-underline-{color}')
        return self

    def link_underline_offset(self, offset: Literal[1, 2, 3]) -> 'Modifier':
        self.classes.append(f'link-offset-{offset}')
        return self

    def display(self, property_value: Literal['none', 'inline', 'inline-block', 'block', 'grid', 'inline-grid', 'table', 'table-cell', 'table-row', 'flex', 'inline-flex']) -> 'Modifier':
        self.classes.append(f'd-{property_value}')

        for breakpoint in ['sm', 'md', 'lg', 'xl', 'xxl']:
            self.classes.append(f'd-{breakpoint}-{property_value}')

        return self

    def flex_direction(self, direction: Literal['row', 'row-reverse', 'column', 'column-reverse']) -> 'Modifier':
        self.classes.append(f'flex-{direction}')
        return self

    def justify_content(self, value: Literal['start', 'end', 'center', 'between', 'around', 'evenly']) -> 'Modifier':
        self.classes.append(f'justify-content-{value}')
        return self

    def align_items(self, value: Literal['start', 'end', 'center', 'baseline', 'stretch']) -> 'Modifier':
        self.classes.append(f'align-items-{value}')
        return self

    def align_self(self, value: Literal['start', 'end', 'center', 'baseline', 'stretch']) -> 'Modifier':
        self.classes.append(f'align-self-{value}')
        return self

    def flex_wrap(self, value: Literal['nowrap', 'wrap', 'wrap-reverse']) -> 'Modifier':
        self.classes.append(f'flex-wrap-{value}')
        return self

    def order(self, value: Literal[0, 1, 2, 3, 4, 5]) -> 'Modifier':
        self.classes.append(f'order-{value}')
        return self

    def float(self, value: Literal['start', 'end', 'none'], size: Optional[Literal['sm', 'md', 'lg', 'xl', 'xxl']] = None) -> 'Modifier':
        if size:
            self.classes.append(f'float-{size}-{value}')
        else:
            self.classes.append(f'float-{value}')
        return self

    def user_select(self, value: Literal['all', 'auto', 'none']) -> 'Modifier':
        self.classes.append(f'user-select-{value}')
        return self

    def pointer_events(self, value: Literal['none', 'auto']) -> 'Modifier':
        self.classes.append(f'pe-{value}')
        return self

    def position(self, value: Literal['static', 'relative', 'absolute', 'fixed', 'sticky']) -> 'Modifier':
        self.classes.append(f'position-{value}')
        return self

    def top(self, value: Literal[0, 25, 50, 75, 100, 'auto']) -> 'Modifier':
        self.classes.append(f'top-{value}')
        return self

    def bottom(self, value: Literal[0, 25, 50, 75, 100, 'auto']) -> 'Modifier':
        self.classes.append(f'bottom-{value}')
        return self

    def start(self, value: Literal[0, 25, 50, 75, 100, 'auto']) -> 'Modifier':
        self.classes.append(f'start-{value}')
        return self

    def end(self, value: Literal[0, 25, 50, 75, 100, 'auto']) -> 'Modifier':
        self.classes.append(f'end-{value}')
        return self

    def margin(self, size: Literal[0, 1, 2, 3, 4, 5, 'auto'],
               side: Optional[Literal['t', 'b', 's', 'e', 'x', 'y', '']] = '') -> 'Modifier':
        self.classes.append(f'm{side}-{size}')
        return self

    def padding(self, size: Literal[0, 1, 2, 3, 4, 5],
                side: Optional[Literal['t', 'b', 's', 'e', 'x', 'y', '']] = '') -> 'Modifier':
        self.classes.append(f'p{side}-{size}')
        return self

    def width(self, value: Literal[25, 50, 75, 100, 'auto']) -> 'Modifier':
        self.classes.append(f'w-{value}')
        return self

    def height(self, value: Literal[25, 50, 75, 100, 'auto']) -> 'Modifier':
        self.classes.append(f'h-{value}')
        return self

    def max_width(self, value: Literal[100, 'sm', 'md', 'lg', 'xl', 'xxl']) -> 'Modifier':
        self.classes.append(f'mw-{value}')
        return self

    def max_height(self, value: Literal[100, 'sm', 'md', 'lg', 'xl', 'xxl']) -> 'Modifier':
        self.classes.append(f'mh-{value}')
        return self

    def visible(self, condition: bool) -> 'Modifier':
        self.classes.append('visible' if condition else 'invisible')
        return self

    def collapse(self, condition: bool) -> 'Modifier':
        self.classes.append('collapse' if condition else 'expand')
        return self

    def z_index(self, value: Literal[0, 1, 2, 3, 4, 5, 'auto']) -> 'Modifier':
        self.classes.append(f'z-{value}')
        return self

    def gap(self, size: Literal[0, 1, 2, 3, 4, 5]) -> 'Modifier':
        self.classes.append(f'gap-{size}')
        return self

    def shadow(self, level: Optional[Literal['sm', 'lg']] = None) -> 'Modifier':
        self.classes.append('shadow' if not level else f'shadow-{level}')
        return self

    def grid(self, columns: int, gap: Optional[int] = None) -> 'Modifier':
        self.classes.append(f'grid-cols-{columns}')
        if gap:
            self.classes.append(f'gap-{gap}')
        return self

    def text_align(self, align: Literal['start', 'center', 'end', 'justify']) -> 'Modifier':
        self.classes.append(f'text-{align}')
        return self

    def text_transform(self, transform: Literal['lowercase', 'uppercase', 'capitalize']) -> 'Modifier':
        self.classes.append(f'text-{transform}')
        return self

    def text_wrap(self, nowrap: bool) -> 'Modifier':
        self.classes.append('text-nowrap' if nowrap else 'text-wrap')
        return self

    def background_pattern(self, pattern: Literal['dots', 'lines', 'stripes', 'grid']) -> 'Modifier':
        self.classes.append(f'bg-pattern-{pattern}')
        return self

    def transition(self, property: Literal['all', 'color', 'background', 'opacity', 'transform'],
                   duration: Literal[1, 2, 3, 4, 5] = 3) -> 'Modifier':
        self.classes.append(f'transition-{property}-{duration}')
        return self

    def animate(self, animation: Literal['fade', 'slide', 'zoom', 'spin'],
                duration: Literal[1, 2, 3, 4, 5] = 3) -> 'Modifier':
        self.classes.append(f'animate-{animation}-{duration}')
        return self

    def align_content(self, value: Literal['start', 'end', 'center', 'stretch', 'between', 'around']) -> 'Modifier':
        self.classes.append(f'align-content-{value}')
        return self

Modifier = __Modifier()