import logging
import argh
import pygna.command as cmd
import pygna.painter as paint
import pygna.utils as utils
import pygna.block_model as bm
import pygna.degree_model as dm

"""
autodoc
"""

logging.basicConfig(level=logging.INFO)


def main():
    argh.dispatch_commands([
        # network summary and graph file
        cmd.network_summary,
        cmd.network_graphml,
        cmd.get_connected_components,
        # geneset network topology analyses
        cmd.test_topology_total_degree,
        cmd.test_topology_internal_degree,
        cmd.test_topology_module,
        cmd.test_topology_sp,
        cmd.test_topology_rwr,
        cmd.test_diffusion_hotnet,
        # comparison analysis
        cmd.test_association_sp,
        cmd.test_association_rwr,
        # building functions
        cmd.build_distance_matrix,
        cmd.build_rwr_diffusion,
        # paint
        paint.paint_datasets_stats,
        paint.paint_comparison_matrix,
        paint.plot_adjacency,
        paint.paint_volcano_plot,

        paint.paint_summary_gnt,
        # utils
        utils.convert_gmt,
        utils.geneset_from_table,
        utils.convert_csv,
        utils.generate_group_gmt,
        # simulations
        bm.generate_gnt_sbm,
        bm.generate_gna_sbm,
        dm.generate_hdn_network,
        bm.generate_sbm_network,
        bm.generate_sbm2_network,

        dm.hdn_add_partial,
        dm.hdn_add_extended,
        dm.hdn_add_branching,

         ], )

if __name__ == "__main__":
    """
    MAIN
    """
    main()
