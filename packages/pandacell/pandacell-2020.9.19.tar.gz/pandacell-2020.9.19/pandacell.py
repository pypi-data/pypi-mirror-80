from IPython.core import magic_arguments
from IPython.core.magic import Magics, cell_magic, line_magic, magics_class


@magics_class
class PandasMagic(Magics):
    @line_magic("df")
    @cell_magic("df")
    @magic_arguments.magic_arguments()
    @magic_arguments.argument("line", default="", nargs="*", type=str)
    @magic_arguments.argument("--inplace", "-i", action="store_true")
    @magic_arguments.argument("--query", "-q", action="store_true")
    @magic_arguments.argument("--name", "-n", default="df", type=str)
    def execute(self, line: str = "", cell: str = ""):
        args = magic_arguments.parse_argstring(self.execute, line)
        if args.query and cell:
            raise ValueError("Query can only be used with single line magics (%df")
        if cell:
            # Remove lines containing only comments, they cause error
            cell = "\n".join(
                [line for line in cell.split("\n") if not line.strip().startswith("#")]
            )
        eval_text = " ".join(args.line) + "\n" + cell
        df_name = args.name
        try:
            df = self.shell.user_ns[df_name]
        except KeyError:
            raise NameError(f"No dataframe assigned to name {df_name}")
        kwargs = {"inplace": args.inplace, "local_dict": self.shell.user_ns}
        if args.query:
            return df.query(eval_text, **kwargs)
        return df.eval(eval_text, **kwargs)


def load_ipython_extension(ip):
    """Load the extension in IPython."""

    ip.register_magics(PandasMagic)
