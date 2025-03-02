from .mod import BaseModifier


class __ButtonModifier(BaseModifier):
    def color(self, color: str) -> '__ButtonModifier':
        self.classes.append(f'btn-{color}')
        return self

    def size(self, size: str) -> '__ButtonModifier':
        self.classes.append(f'btn-{size}')
        return self

ButtonModifier = __ButtonModifier()