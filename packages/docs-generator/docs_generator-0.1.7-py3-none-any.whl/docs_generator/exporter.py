from nbconvert.exporters import TemplateExporter


class MdExporter(TemplateExporter):
    file_extension = ".md"
    template_file = "markdown/index.md.j2"
