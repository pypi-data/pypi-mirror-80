import collections
from io import StringIO
from functools import lru_cache
import numpy as np
import pandas as pd
import xml.etree.cElementTree as ET
import h5py


col2format = { 'Mass':'{:.4f}',
               'MassSD':'{:.4f}',
               'IntensitySD':'{:.2f}',
               'AverageCharge':'{:.2f}',
               'RT':'{:.4f}',
               'RTSD':'{:.4e}',
               'FWHM':'{:.4f}',
               'Mobility':'{:.3f}',
               'MobilitySD':'{:.3f}',
               'LiftOffRT':'{:.4f}',
               'InfUpRT':'{:.4f}',
               'InfDownRT':'{:.4f}',
               'TouchDownRT':'{:.4f}' }


class XMLparser(object):
    """General xml parsing capabilities."""
    def __init__(self, data_path, col2format=col2format):
        self.data_path = data_path
        self.col2format = col2format

    def __del__(self):
        if hasattr(self, 'root'):
            self.root.clear()

    def __iter__(self):
        events = ET.iterparse(self.data_path, events=("start", "end",))
        _, root = next(events)  # Grab the root element.    
        for event, elem in events:
            if event == "end":
                yield elem
                root.clear()

    def iter(self, tag=None):
        if tag is None:
            yield from self
        else:
            for el in self:
                if el.tag == tag:
                    yield el 

    @lru_cache(maxsize=1)
    def get_tag_counts(self):
        """Count the top level tags.

        Returns:
            collections.Counter: count of each first-level tag.
        """
        return collections.Counter(c.tag for c in self)

    def attributes_iter(self, tag):
        for el in self:
            if el.tag == tag:
                yield el.attrib
    
    def element2df(self, xml_element, column_names, sep=' ', skipinitialspace=True, **kwds):
        """Represent the text data as a DataFrame.

        Args:
            xml_element (xml.etree.cElementTree.Element): One of the xml tree nodes.
            columns (list): Names of columns for the reported data frame.

        Returns:
            pd.DataFrame: Data contained in the text field of the xml_element, nicely parsed into a data frame.
        """
        return pd.read_table(StringIO(xml_element.text), 
                             names=column_names,
                             sep=' ',
                             skipinitialspace=True,
                             **kwds).dropna()

    def write(self, path):
        """Write back the xml file."""
        path = str(path)
        self.tree.write(path)

    @property
    def LE(self):
        raise NotImplementedError
    
    @property
    def HE(self):
        raise NotImplementedError

    def to_hdf(self, path,
               opts={'compression':'gzip',
                     'compression_opts':9,
                     'shuffle':True}):
        """Save to hdf5 as packed as possible."""
        with h5py.File(path, "a") as f:
            LE = self.LE
            f.create_dataset('LE', data=LE.values, **opts)
            f['LE'].attrs['columns'] = list(LE.columns)
            del LE
            HE = self.HE
            f.create_dataset('HE', data=HE.values, **opts)
            f['HE'].attrs['columns'] = list(HE.columns)
            del HE

    @staticmethod 
    def hdf2pd(path, ms_level=1):
        assert ms_level in (1,2), f"Pass in 'ms_level' either 1 or 2."
        with h5py.File(path, "r") as f:
            x = 'LE' if ms_level == 1 else 'HE'
            return pd.DataFrame(f[x][()], columns=f[x].attrs['columns'])


def df2text(df, col2format=col2format, copy=True):
    """Translate df to data compatible with the used xml format."""
    if copy:
        df = df.copy()
    cols = df.columns
    col2format = {c:col2format[c] for c in set(cols) & set(col2format)}
    for col, formatter in col2format.items():
        df.loc[:,col] = df.loc[:,col].apply(lambda x: formatter.format(x))
    cols_simple2str = [c for c in cols if c not in col2format]
    df.loc[:,cols_simple2str] = df[cols_simple2str].astype(np.str)
    df = df.iloc[:,0].astype(str).str.cat(df.iloc[:,1:].astype(str), sep=" ")
    return "\n      "+"\n      ".join(df)

# def df2text2(df):
#     return "\n      "+"\n      ".join(" ".join(row.astype(str)) for row in df.values)

# def df2text3(df):
#     x = df.iloc[:,0].astype(str).str.cat(df.iloc[:,1:].astype(str), sep=" ")
#     return "\n      "+"\n      ".join(x)



class Pep3Dparser(XMLparser):
    @property
    def LE_columns(self):
        """Get low energy column names."""
        return [el.attrib['NAME'] for el in next(self.iter('FORMAT'))]

    @property
    def LE_element(self):
        """Get low energy xml-tree element."""
        return next(self.iter('DATA'))

    @property
    def LE(self):
        """Get low energy ions, or the unfragmented spectra."""
        return self.element2df(self.LE_element, self.LE_columns)

    @LE.setter
    def LE(self, df):
        self.LE_element.text = df2text(df, self.col2format)

    @property
    def HE_columns(self):
        """Get high energy column names."""
        it = self.iter('FORMAT')
        _ = next(it)
        return [f.attrib['NAME'] for f in next(it)]

    @property
    def HE_element(self):
        """Get high energy xml-tree element."""
        return next(self.iter('HE_DATA'))

    @property
    def HE(self):
        """Get high energy ions, or the spectra of fragments."""
        return self.element2df(self.HE_element, self.HE_columns)

    @HE.setter
    def HE(self, df):
        self.HE_element.text = df2text(df, self.col2format)



class Apex3Dparser(XMLparser):
    @property
    def columns(self):
        """Get column names."""
        return [f.attrib['NAME'] for f in next(self.iter('DATAFORMAT'))]

    @property
    def LE_columns(self):
        """Get low energy column names."""
        return self.columns

    @property
    def HE_columns(self):
        """Get low energy column names."""
        return self.columns

    @property
    def LE_element(self):
        """Get low energy xml-tree element."""
        return next(self.iter('LE'))

    @property
    def HE_element(self):
        """Get low energy xml-tree element."""
        return next(self.iter('HE'))

    @property
    def LE(self):
        """Get low energy ions, or the unfragmented spectra."""
        return self.element2df(self.LE_element, self.LE_columns)

    @property
    def HE(self):
        """Get high energy ions, or the spectra of fragments."""
        return self.element2df(self.HE_element, self.HE_columns)

    @HE.setter
    def HE(self, df):
        raise NotImplementedError

    @LE.setter
    def LE(self, df):
        raise NotImplementedError





class iaDBsXMLparser(XMLparser):
    """Parser of iaDBs xml files."""

    @lru_cache(maxsize=1)
    def prot_ids(self):
        """Get the number each protein id occured in the XML file.

        Returns:
            collections.Counter: counts of id's.
        """
        return collections.Counter(a["ID"] for a in self.attributes_iter('PROTEIN'))

    @lru_cache(maxsize=1)
    def proteins(self):
        """Get all protein information from the XML file.
    
        Returns:
            pd.DataFrame: Protein information.
        """
        return pd.DataFrame(self.attributes_iter('PROTEIN'))

    @lru_cache(maxsize=1)
    def products(self):
        """Get all products information from the XML file.

        Returns:
            pd.DataFrame: Products information.
        """
        return pd.DataFrame(self.attributes_iter('PRODUCT'))

    def iter_peptides(self):
        for el in self:
            if el.tag == "PEPTIDE":
                res = el.attrib.copy()
                mods = " ".join(f"{m.attrib['NAME']}__{m.attrib['POS']}" for m in el)
                if mods:
                    res['MOD'] = mods
                yield res

    @lru_cache(maxsize=1)
    def peptides(self):
        """Get all products information from the XML file.

        Returns:
            pd.DataFrame: Products information.
        """
        return pd.DataFrame(self.iter_peptides())

    @lru_cache(maxsize=1)
    def parameters(self):
        """Get iaDBs parameters.

        Returns:
            dict: Parameter-value.
        """
        res = {}
        for el in self:
            if el.tag == "PARAM":
                k, v = el.attrib.values()
                res[k] = v
                if k == "SampleDescription":
                    break
        return res

    def iter_query_masses(self):
        for el in self:
            if el.tag == "QUERY_MASS":
                r = el.attrib.copy()
                i = 0
                for i, matched_mass in enumerate(el):
                    r.update(matched_mass.attrib)
                if i > 0:
                    raise NotImplementedError("The case of multiple MASS_MATCH per query is not coded in.")
                yield r

    @lru_cache(maxsize=1)
    def query_masses(self):
        """Get all query mass information from the XML file.

        Returns:
            pd.DataFrame: Products information.
        """
        return pd.DataFrame(self.iter_query_masses())

    @lru_cache(maxsize=1)
    def count_proteins_per_hit(self):
        """Count how many times a given number of proteins were assigned to one hit.

        Returns:
            collections.Counter: Distribution of proteins number per hit.
        """
        return collections.Counter(len(el) for el in self if el.tag == 'HIT')

    def iter_hits(self):
        """Get all information on the hits.

        Each hit can consist of multiple proteins.
        Each protein can have several sequence matches.
        Each row of the result corresponds to such match.
        """
        hit_id = 0
        for el in self:
            if el.tag == "HIT":
                for prot in el:
                    prot_attrib = {f'PROT_{k}':v for k,v in prot.attrib.items()}
                    seq_matches = []
                    for node in prot:
                        if node.tag == 'SEQUENCE_MATCH':
                            seq_match = node.attrib
                            seq_match['fragment_ion'] = ";".join(fii.attrib['IDS'] for fii in node.iter('FRAGMENT_ION')).replace(',','')
                            seq_matches.append(seq_match)
                        else:
                            prot_attrib[f'PROT_{node.tag}'] = node.text
                    prot_attrib['HIT'] = hit_id
                    for seq_att in seq_matches:
                        row = {f"SEQ_{k}":v for k,v in seq_att.items()}
                        row.update(prot_attrib)
                        yield row
                hit_id += 1

    @lru_cache(maxsize=1)
    def hits(self):
        return pd.DataFrame(self.iter_hits())

    def info(self):
        """Return core information about the seach outcomes."""
        out = {}
        tag_counts = self.get_tag_counts()
        params = self.parameters()
        out['raw_file'] = params['RawFile']
        out['acquired_name'] = params['AcquiredName']
        out['sample_description'] = params['SampleDescription']
        out['queries_cnt'] = tag_counts['QUERY_MASS']
        out['hits_cnt'] = tag_counts['HIT']
        out['peptides_cnt'] = tag_counts['PEPTIDE']
        out['proteins_cnt'] = len(self.prot_ids())
        return out



def get_search_stats(iadbs_out):
    X = iaDBsXMLparser(iadbs_out)
    info = X.info()
    del X
    return info    
