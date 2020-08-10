def parse_pfam2go(path):
    """Generator over the entries in a pfam2go
    mapping file, as found at
    http://current.geneontology.org/ontology/external2go/pfam2go

    Args:
        path (str): Path to the pfam2go file.
    """
    with open(path, 'r') as fin:
        for line in fin:
            if not line.startswith("!"):
                yield line


class Pfam2GOEntry:
    """docstring for Pfam2GOEntry"""
    def __init__(self):
        self.pfam_id = None
        self.pfam_accession = None
        self.go_id = None
        self.go_name = None

    def from_line(self, line):
        """Set object attributes by parsing
        a line from a pfam2go file.

        Args:
            line (str): A line from a pfam2go file.
        """
        if line.startswith("!"):
            raise ValueError("Lines with leading '!' do  \
                not contain mapping entries")
        else:
            fields = line.split()
            self.pfam_accession = fields[0].replace("Pfam:", "")
            self.pfam_id = fields[1]
            self.go_id = fields[-1]
            self.go_name = line.split("GO:")[1].strip(" ; ")