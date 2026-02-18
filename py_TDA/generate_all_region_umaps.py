"""
Generate UMAP embeddings for all brain regions from Allen Brain Visual Coding dataset
Saves results as CSV files for each region
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import umap

# AllenSDK
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache

print("="*60)
print("UMAP Generation for All Brain Regions")
print("Allen Brain Visual Coding Dataset")
print("="*60)

# --- 1. Setup Paths ---
output_dir = Path("../Dataset/RAW")
manifest_path = output_dir / "manifest.json"
cache = EcephysProjectCache.from_warehouse(manifest=str(manifest_path))

# Output directory for UMAP CSVs
umap_output_dir = Path("../Dataset/Processed/UMAP_by_Region")
umap_output_dir.mkdir(parents=True, exist_ok=True)

# --- 2. Session Selection ---
session_id = 750749662  # Primary session with multiple brain regions
print(f"\nLoading Session {session_id}...")
session = cache.get_session_data(session_id)

# --- 3. Get All Brain Regions ---
all_regions = session.units["ecephys_structure_acronym"].unique()
valid_regions = [r for r in all_regions if isinstance(r, str)]
print(f"\nFound {len(valid_regions)} brain regions: {sorted(valid_regions)}")

# --- 4. UMAP Parameters ---
UMAP_PARAMS = {
    'n_components': 3,
    'n_neighbors': 15,
    'min_dist': 0.1,
    'random_state': 42
}

PCA_COMPONENTS = 50
MIN_UNITS_THRESHOLD = 10  # Skip regions with fewer units

# --- 5. Process Each Region ---
summary_data = []

for region_idx, region_acronym in enumerate(sorted(valid_regions), 1):
    print(f"\n{'='*60}")
    print(f"[{region_idx}/{len(valid_regions)}] Processing: {region_acronym}")
    print(f"{'='*60}")
    
    try:
        # Filter units for this region
        region_units = session.units[
            session.units["ecephys_structure_acronym"] == region_acronym
        ]
        n_units = len(region_units)
        
        print(f"Units found: {n_units}")
        
        # Check minimum threshold
        if n_units < MIN_UNITS_THRESHOLD:
            print(f"⚠ Skipping {region_acronym}: Only {n_units} units (< {MIN_UNITS_THRESHOLD})")
            summary_data.append({
                'region': region_acronym,
                'n_units': n_units,
                'status': 'skipped_too_few_units',
                'n_frames': 0,
                'umap_shape': 'N/A'
            })
            continue
        
        # --- Construct Neural Response Matrix ---
        print("Calculating neural responses...")
        movie_table = session.get_stimulus_table("natural_movie_one")
        frame_duration = movie_table['duration'].mean()
        
        spike_counts_xr = session.presentationwise_spike_counts(
            stimulus_presentation_ids=movie_table.index.values,
            bin_edges=np.array([0, frame_duration]),
            unit_ids=region_units.index.values
        )
        
        # Sum spikes within frame window
        response_matrix_all = spike_counts_xr.sum(dim="time_relative_to_stimulus_onset")
        
        # Create DataFrame and average across repeats
        df_response = pd.DataFrame(
            response_matrix_all.values,
            index=movie_table.index,
            columns=region_units.index
        )
        df_response['frame'] = movie_table['frame']
        average_response_matrix = df_response.groupby('frame').mean()
        
        X = average_response_matrix.values
        n_frames = X.shape[0]
        print(f"Response matrix shape: {X.shape} (Frames × Neurons)")
        
        # --- PCA Reduction ---
        n_pca = min(PCA_COMPONENTS, n_units)
        print(f"Running PCA (n_components={n_pca})...")
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        pca = PCA(n_components=n_pca)
        X_pca = pca.fit_transform(X_scaled)
        
        variance_explained = pca.explained_variance_ratio_.sum()
        print(f"PCA variance explained: {variance_explained:.2%}")
        
        # --- UMAP Embedding ---
        print(f"Running UMAP (3D)...")
        reducer = umap.UMAP(**UMAP_PARAMS)
        embedding_3d = reducer.fit_transform(X_pca)
        
        print(f"UMAP embedding shape: {embedding_3d.shape}")
        
        # --- Save to CSV ---
        # Create DataFrame with UMAP coordinates
        umap_df = pd.DataFrame({
            'frame': average_response_matrix.index.values,
            'UMAP_1': embedding_3d[:, 0],
            'UMAP_2': embedding_3d[:, 1],
            'UMAP_3': embedding_3d[:, 2],
            'region': region_acronym,
            'n_units': n_units
        })
        
        # Save individual region file
        csv_filename = f"{region_acronym}_umap_3d.csv"
        csv_path = umap_output_dir / csv_filename
        umap_df.to_csv(csv_path, index=False)
        print(f"✓ Saved: {csv_filename}")
        
        # Record summary
        summary_data.append({
            'region': region_acronym,
            'n_units': n_units,
            'n_frames': n_frames,
            'pca_components': n_pca,
            'variance_explained': variance_explained,
            'umap_shape': f"{embedding_3d.shape[0]}×{embedding_3d.shape[1]}",
            'status': 'success',
            'csv_file': csv_filename
        })
        
    except Exception as e:
        print(f"✗ Error processing {region_acronym}: {str(e)}")
        summary_data.append({
            'region': region_acronym,
            'n_units': n_units if 'n_units' in locals() else 0,
            'status': f'error: {str(e)[:50]}',
            'n_frames': 0,
            'umap_shape': 'N/A'
        })

# --- 6. Create Combined CSV ---
print(f"\n{'='*60}")
print("Creating combined CSV...")
print(f"{'='*60}")

# Combine all successful UMAPs
all_umap_files = list(umap_output_dir.glob("*_umap_3d.csv"))
if all_umap_files:
    combined_dfs = []
    for csv_file in all_umap_files:
        df = pd.read_csv(csv_file)
        combined_dfs.append(df)
    
    combined_df = pd.concat(combined_dfs, ignore_index=True)
    combined_path = umap_output_dir / "all_regions_umap_3d_combined.csv"
    combined_df.to_csv(combined_path, index=False)
    print(f"✓ Combined CSV saved: {combined_path}")
    print(f"  Total rows: {len(combined_df)}")
    print(f"  Regions included: {combined_df['region'].nunique()}")

# --- 7. Save Summary Report ---
summary_df = pd.DataFrame(summary_data)
summary_path = umap_output_dir / "_summary_report.csv"
summary_df.to_csv(summary_path, index=False)

print(f"\n{'='*60}")
print("PROCESSING COMPLETE")
print(f"{'='*60}")
print(f"\nSummary:")
print(f"  Total regions processed: {len(summary_data)}")
print(f"  Successful: {sum(1 for s in summary_data if s['status'] == 'success')}")
print(f"  Skipped: {sum(1 for s in summary_data if 'skipped' in s['status'])}")
print(f"  Errors: {sum(1 for s in summary_data if 'error' in s['status'])}")
print(f"\nOutput directory: {umap_output_dir}")
print(f"Summary report: _summary_report.csv")

print("\n" + "="*60)
print("Summary Table:")
print("="*60)
print(summary_df.to_string(index=False))
