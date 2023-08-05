import yaml
import pygna.converters as pc
import pygna.elaborators as pe


class YamlConfig:
    def __init__(self):
        pass

    def write_config(self, data, filename):
        with open(filename, "w") as outfile:
            yaml.dump(data, outfile, default_flow_style=True)

    def load_config(self, filename):
        with open(filename, "r") as stream:
            try:
                config = yaml.load(stream)
                return config

            except yaml.YAMLError as exc:
                return print(exc)


def convert_gmt(gmt_file: "gmt file to be converted",
                output_gmt_file: "output file",
                conversion: "e2s or s2e",
                converter_map_filename: "tsv table used to convert gene names",
                entrez_col: "name of the entrez column" = "NCBI Gene ID",
                symbol_col: "name of the symbol column" = "Approved symbol"):
    """
    This function is used to convert a GMT file, adding information about the Entrez ID or the symbol
    """
    pc.GmtToGmtEnriched(gmt_file, output_gmt_file, conversion, entrez_col, symbol_col, converter_map_filename)


def geneset_from_table(input_file: "input csv file",
                       setname: "name of the set",
                       output_gmt: "output gmt name" = None,
                       output_csv: "output csv name" = None,
                       name_column: "column with the names" = "Unnamed: 0",
                       filter_column: "column with the values to be filtered" = "padj",
                       alternative: "alternative to use for the filter, with less the filter is applied <threshold, "
                                    "otherwise >= threshold" = "less",
                       threshold: "threshold for the filter" = 0.01,
                       descriptor: "descriptor for the gmt file" = None):
    """
    This function converts a csv file to a GMT allowing to filter the elements using the values of one of the columns.
    The user can specify the column used to retrieve the name of the objects and the filter condition. The output
    can be either a GMT with the names of the genes that pass the filter or a csv with the whole filtered table,
    otherwise both can be created.
    """
    pc.CsvToGmt(input_file, setname, filter_column, alternative, threshold, output_gmt, output_csv, name_column,
                descriptor)


def filter_table(table: "input csv file",
                 filter_column: "column with the values to be filtered" = "padj",
                 alternative: "alternative to use for the filter, with less the filter is applied <threshold, "
                              "otherwise >= threshold" = "less",
                 threshold: "threshold for the filter" = 0.01):
    return pe.TableElaboration.filter_table(table, filter_column, alternative, threshold)


def generate_group_gmt(input_table: "table to get the geneset from",
                       output_gmt: "output gmt file",
                       name_col='Gene',
                       group_col='Cancer',
                       descriptor='cancer_genes'):
    """
    This function generates a GMT file of multiple setnames. From the table file, it groups the names in the
    group_col (the column you want to use to group them) and prints the genes in the name_col. Set the descriptor
    according to your needs
    """
    pc.GroupGmt(input_table, output_gmt, name_col, group_col, descriptor)


def convert_csv(csv_file: "csv file where to add a name column",
                conversion: "e2s or s2e",
                original_name_col: "column name to be converted",
                new_name_col: "name of the new column with the converted names",
                geneset: "the geneset to convert",
                converter_map_filename: "tsv table used to convert gene names" = "entrez_name.tsv",
                output_file: "if none, table is saved in the same input file" = None,
                entrez_col: "name of the entrez column" = "NCBI Gene ID",
                symbol_col: "name of the symbol column" = "Approved symbol"):
    """
    This function is used to add a column with the entrezID or Symbols to a CSV file
    """
    pc.CsvToCsvEnriched(csv_file, conversion, original_name_col, new_name_col, geneset, entrez_col, symbol_col,
                        converter_map_filename, output_file)


################################################################
########### Functions for corrected sampling ###################
################################################################

def get_bin(degree, map_bin, name=None):
    # For a node degree return the bin_name according to the ranges
    for r,i in map_bin.items():
        if (degree>=r[0]) & (degree<r[1]):
            return(i)

def get_node_bins_map(degree, bin_histogram):
    # Reshape the dictionary to have range:bin_number
    map_bin = {val['range']:i for i,val in bin_histogram.items()}
    # Get a map of the bin of each node node:bin_number
    node_2_bin = {d[0]:get_bin(d[1], map_bin) for d in degree}
    return node_2_bin

def get_sampling_p(mapped_geneset, network, bins, node_2_bin_map):
    # Reshape the dictionary to have range:bin_number
    map_bin = {val['range']:i for i,val in bins.items()}
    # Get the degree of the mapped geneset
    degree = network.degree(nbunch = mapped_geneset)
    # Get a map of the bin of each node node:bin_number
    node_2_bin = [get_bin(d[1], map_bin) for d in degree]
    # Count the mapped node for each bin
    counts = {k:node_2_bin.count(k) for k in bins.keys()}
    # Get the probability for each bin bin_number:probability
    # For each bin we have:
    #   - c = number of mapped nodes in the bin
    #   - nk = number of total nodes in the bin
    #   - m = total number of mapped nodes
    # p = c/nk/m, indeed c/m would be the probability of choosing the bin, 
    # c/nk/m becomes the probability of choosing one of the nodes in the bin
    bin_2_p_map = {(k):(counts[k]/val['nk']/len(mapped_geneset) if (val['nk']>0) else 0) for k,val in bins.items()}
    # Get the probability of sampling for each node
    p = [bin_2_p_map[int(k)] for n,k in node_2_bin_map.items()]
    return(p)