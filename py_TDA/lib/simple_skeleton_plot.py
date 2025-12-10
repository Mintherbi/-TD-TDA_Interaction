import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import umap
import networkx as nx
import viz_style

# Ensure viz_style is set
viz_style.set_architectural_style()

def run_tda_pipeline_simple(session, region_acronym):
    print(f"\n{'='*40}")
    print(f"STARTING SIMPLE SKELETON PLOT FOR: {region_acronym}")
    print(f"{'='*40}")
    
    # Create output directory
    save_dir = os.path.join("..", "Results", "TDA_Iteration", "4_1Simple_Manifold_Skeleton")
    os.makedirs(save_dir, exist_ok=True)
    
    # 1. Filter Units
    region_units = session.units[session.units["ecephys_structure_acronym"] == region_acronym]
    n_units = len(region_units)
    
    if n_units < 10:
        print(f"Skipping {region_acronym}: Not enough units (<10).")
        return

    # 2. Construct Neural Response Matrix
    movie_table = session.get_stimulus_table("natural_movie_one")
    frame_duration = movie_table['duration'].mean()

    spike_counts_xr = session.presentationwise_spike_counts(
        stimulus_presentation_ids=movie_table.index.values,
        bin_edges=np.array([0, frame_duration]),
        unit_ids=region_units.index.values
    )

    response_matrix_all = spike_counts_xr.sum(dim="time_relative_to_stimulus_onset")
    
    df_response = pd.DataFrame(
        response_matrix_all.values,
        index=movie_table.index,
        columns=region_units.index
    )
    df_response['frame'] = movie_table['frame']
    average_response_matrix = df_response.groupby('frame').mean()
    X = average_response_matrix.values
    
    # 3. PCA & UMAP
    n_components_pca = min(50, n_units)
    pca = PCA(n_components=n_components_pca)
    X_pca = pca.fit_transform(StandardScaler().fit_transform(X))
    
    reducer = umap.UMAP(n_components=3, n_neighbors=15, min_dist=0.1, random_state=42)
    embedding_3d = reducer.fit_transform(X_pca)
    
    # 4. Spanning Tree
    k_all = 10
    nbrs_all = NearestNeighbors(n_neighbors=k_all + 1).fit(embedding_3d)
    dists_all, inds_all = nbrs_all.kneighbors(embedding_3d)

    G_all = nx.Graph()
    num_all = embedding_3d.shape[0]
    G_all.add_nodes_from(range(num_all))

    for i in range(num_all):
        for d, j in zip(dists_all[i][1:], inds_all[i][1:]):
            G_all.add_edge(i, j, weight=float(d))

    T_all_full = nx.minimum_spanning_tree(G_all, weight="weight")

    if not nx.is_connected(T_all_full):
        largest_cc_all = max(nx.connected_components(T_all_full), key=len)
        T_all = T_all_full.subgraph(largest_cc_all).copy()
    else:
        T_all = T_all_full
        
    # Layout
    try:
        pos_all = nx.kamada_kawai_layout(T_all, scale=2.0)
    except:
        pos_all = nx.spring_layout(T_all, k=0.1, iterations=50, seed=42)
        
    # Calculate Node Colors based on Frame Index
    frames_all = average_response_matrix.index.values
    nodelist = list(T_all.nodes())
    node_colors = [frames_all[n] for n in nodelist]

    # Plot Simple Skeleton
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor(viz_style.BLACK)
    ax.set_facecolor(viz_style.BLACK)

    viz_style.plot_network_graph(
        ax, T_all, pos_all, 
        node_colors=node_colors, 
        cmap='turbo',
        node_size=30,
        edge_width=1.0,
        with_labels=False,
        title=f"NEURAL MANIFOLD SKELETON (SIMPLE): {region_acronym}"
    )
    
    save_path = os.path.join(save_dir, f"{region_acronym}.png")
    plt.savefig(save_path, facecolor=viz_style.BLACK, dpi=150, bbox_inches='tight')
    print(f"Saved simple skeleton to: {save_path}")
    plt.show()
    plt.close(fig)

# Example usage (requires 'session' object to be defined):
# valid_regions = [r for r in session.units["ecephys_structure_acronym"].unique() if isinstance(r, str)]
# for region in valid_regions:
#     run_tda_pipeline_simple(session, region)
