import ast
import dataclasses

from ._loader import Loader, LoaderImport, LoaderImportFrom


@dataclasses.dataclass(slots=True)
class StubVisitor(ast.NodeVisitor):
    loaders: dict[str, Loader] = dataclasses.field(default_factory=dict)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self._register(LoaderImport(alias.name, alias.asname))

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            self._register(
                LoaderImportFrom(node.module, alias.name, alias.asname, node.level)
            )

    def _register(self, loader: Loader) -> None:
        self.loaders[loader.attr_name] = loader
