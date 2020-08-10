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
                curr_entry = Pfam2GOEntry()
                curr_entry.from_line(line)
                yield curr_entry


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

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Pfam2GOEntry):
            return all([
                self.pfam_id == other.pfam_id,
                self.pfam_accession == other.pfam_accession,
                self.go_id == other.go_id,
                self.go_name == other.go_name
                ])
        return NotImplemented

    def __repr__(self):
        return "<{}, {}, {}, {}>".format(
            self.pfam_id, self.pfam_accession, self.go_id, self.go_name)

    def __str__(self):
        return "<{}, {}, {}, {}>".format(
            self.pfam_id, self.pfam_accession, self.go_id, self.go_name)


def parse_pfam_A_fasta(path):
    """Generator over the matching info in a Pfam-A.fasta file
    as found at
    ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam33.1/

    Args:
        path (str): Path to the Pfam-A.fasta file.
    """
    with open(path, 'r') as fin:
        for line in fin:
            if line.startswith(">"):
                curr_entry = UniProtMatch()
                curr_entry.from_line(line)
                yield curr_entry


class UniProtMatch:
    """docstring for UniProtMatch"""
    def __init__(self):
        self.uniprot_accession = None
        self.uniprot_entry_name = None
        self.location = None
        self.pfam_accession = None

    def from_line(self, line):
        """Set object attributes by parsing a description line
        from a Pfam-A.fasta file

        Args:
            line (str): A description line from a Pfam-A.fasta file.
        """
        if not line.startswith(">"):
            raise ValueError("Description lines have to start with '>'")
        else:
            fields = line.split()
            self.uniprot_accession = fields[1].split('.')[0]
            self.uniprot_entry_name, self.location = (
                fields[0].split('_')[1].split('/'))
            self.pfam_accession = fields[-1].split('.')[0]

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, UniProtMatch):
            return all([
                self.uniprot_accession == other.uniprot_accession,
                self.uniprot_entry_name == other.uniprot_entry_name,
                self.location == other.location,
                self.pfam_accession == other.pfam_accession
                ])
        return NotImplemented

    def __repr__(self):
        return "<{}, {}, {}, {}>".format(
            self.uniprot_accession, self.uniprot_entry_name,
            self.location, self.pfam_accession)

    def __str__(self):
        return "<{}, {}, {}, {}>".format(
            self.uniprot_accession, self.uniprot_entry_name,
            self.location, self.pfam_accession)
