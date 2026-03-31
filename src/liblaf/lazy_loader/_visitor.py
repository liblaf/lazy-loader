import ast
import dataclasses

from ._getter import Getter, GetterImport, GetterImportFrom
from ._loader import LazyLoader


@dataclasses.dataclass(slots=True)
class StubVisitor(ast.NodeVisitor):
    """Parse a stub AST into getters and optional export names."""

    """Export names collected from `__all__`, if the stub defines it."""
    exports: list[str] | None = None
    """Mapping populated from explicit import statements in the stub."""
    getters: dict[str, Getter] = dataclasses.field(default_factory=dict)

    def finish(self, name: str, package: str | None) -> LazyLoader:
        """Build a loader from the imports collected so far."""
        getters: dict[str, Getter] = self.getters
        if self.exports is not None:
            exports: set[str] = set(self.exports)
            getters: dict[str, Getter] = {
                attr_name: getter
                for attr_name, getter in getters.items()
                if attr_name in exports
            }
        return LazyLoader(
            name=name, package=package, exports=self.exports, getters=getters
        )

    def visit_Assign(self, node: ast.Assign) -> None:
        """Capture `__all__ = [...]` assignments from the stub."""
        if len(node.targets) != 1:
            return
        target: ast.expr = node.targets[0]
        if not isinstance(target, ast.Name):
            return
        if target.id != "__all__":
            return
        self.exports = list(ast.literal_eval(node.value))

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """Capture annotated `__all__` assignments from the stub."""
        target: ast.expr = node.target
        if not isinstance(target, ast.Name):
            return
        if target.id != "__all__":
            return
        if node.value is None:
            return
        self.exports = list(ast.literal_eval(node.value))

    def visit_Import(self, node: ast.Import) -> None:
        """Convert `import ...` statements into getter entries."""
        for alias in node.names:
            getter: GetterImport = GetterImport(name=alias.name, asname=alias.asname)
            self.getters[getter.attr_name] = getter

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Convert `from ... import ...` statements into getter entries.

        Raises:
            ValueError: If the stub contains a wildcard import.
        """
        for alias in node.names:
            if alias.name == "*":
                msg: str = f"liblaf.lazy_loader does not support wild card form of import: `{ast.unparse(node)}`"
                raise ValueError(msg)
            getter: GetterImportFrom = GetterImportFrom(
                module=node.module,
                name=alias.name,
                asname=alias.asname,
                level=node.level,
            )
            self.getters[getter.attr_name] = getter
