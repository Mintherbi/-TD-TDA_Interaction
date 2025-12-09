import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler
import networkx as nx
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

# Color Palette Constants (High Contrast for Dark Background)
BLUE = '#448AFF'      # Bright Blue
GREEN = '#69F0AE'     # Bright Green
RED = '#FF5252'       # Bright Red
YELLOW = '#FFFF00'    # Yellow
PURPLE = '#E040FB'    # Bright Purple
CYAN = '#18FFFF'      # Cyan
WHITE = '#FFFFFF'
GRAY = '#B0BEC5'      # Blue-ish Gray
BLACK = '#000000'     # Pure Black

def set_architectural_style():
    """
    Sets matplotlib and seaborn style to a dark, minimalist aesthetic.
    """
    # Base Theme
    plt.style.use('dark_background')
    
    # Figure Settings
    plt.rcParams['figure.figsize'] = [10, 6]
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['figure.facecolor'] = BLACK
    plt.rcParams['axes.facecolor'] = BLACK
    plt.rcParams['savefig.facecolor'] = BLACK
    
    # Font Settings
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Roboto', 'Kozuka Gothic Pr6N', 'Kozuka Gothic Pro', 'Helvetica', 'Arial', 'sans-serif']
    
    # Color Palette
    custom_colors = [BLUE, GREEN, RED, YELLOW, PURPLE, CYAN]
    plt.rcParams['axes.prop_cycle'] = cycler(color=custom_colors)
    
    # Colormap
    plt.rcParams['image.cmap'] = 'inferno'
    
    # Color & Line Settings
    plt.rcParams['axes.edgecolor'] = WHITE
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['xtick.color'] = WHITE
    plt.rcParams['ytick.color'] = WHITE
    plt.rcParams['text.color'] = WHITE
    plt.rcParams['axes.labelcolor'] = WHITE
    
    # Typography
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    
    # Grid Settings
    plt.rcParams['grid.color'] = '#333333'
    plt.rcParams['grid.linestyle'] = ':'
    plt.rcParams['grid.linewidth'] = 0.5
    plt.rcParams['axes.grid'] = False
    
    # Spines
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    
    print("Architectural plot style applied (Dark Mode).")

def format_axis(ax, title=None, xlabel=None, ylabel=None):
    """Applies clean architectural formatting to an axis."""
    if title:
        ax.set_title(title.upper(), loc='left', pad=15, fontsize=11, fontweight='bold', color=WHITE)
    if xlabel:
        ax.set_xlabel(xlabel.upper(), fontsize=9, labelpad=10, color=WHITE)
    if ylabel:
        ax.set_ylabel(ylabel.upper(), fontsize=9, labelpad=10, color=WHITE)
    
    ax.grid(axis='y', linestyle=':', linewidth=0.5, color='#333333')
    sns.despine(ax=ax, bottom=False, left=False)
    ax.tick_params(axis='both', which='major', labelsize=8, colors=WHITE)
    
    # Set spine colors
    ax.spines['bottom'].set_color(WHITE)
    ax.spines['left'].set_color(WHITE)

def plot_line(ax, x, y, color=WHITE, label=None, alpha=1.0, linewidth=1.5, linestyle='-'):
    """Plots a line with architectural style."""
    line, = ax.plot(x, y, color=color, label=label, alpha=alpha, linewidth=linewidth, linestyle=linestyle)
    return line

def plot_dual_axis(ax1, x1, y1, color1, label1, ylabel1, 
                   x2, y2, color2, label2, ylabel2, title=None):
    """Plots two series on dual axes with matching colors."""
    
    # Plot 1
    plot_line(ax1, x1, y1, color=color1, label=label1)
    ax1.set_ylabel(ylabel1.upper(), color=color1, fontsize=9)
    ax1.tick_params(axis='y', labelcolor=color1, colors=WHITE)
    ax1.spines['left'].set_color(color1)
    
    # Plot 2
    ax2 = ax1.twinx()
    plot_line(ax2, x2, y2, color=color2, label=label2)
    ax2.set_ylabel(ylabel2.upper(), color=color2, fontsize=9)
    ax2.tick_params(axis='y', labelcolor=color2, colors=WHITE)
    ax2.spines['right'].set_color(color2)
    sns.despine(ax=ax2, top=True, left=False, right=False, bottom=False)
    
    if title:
        ax1.set_title(title.upper(), loc='left', pad=15, fontsize=11, fontweight='bold', color=WHITE)

def plot_3d_trajectory(ax, x, y, z, c=None, cmap='inferno', title=None, xlabel="PC 1", ylabel="PC 2", zlabel="PC 3"):
    """Plots a 3D trajectory with architectural style."""
    # Background
    ax.set_facecolor(BLACK)
    
    # Pane settings
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor(WHITE)
    ax.yaxis.pane.set_edgecolor(WHITE)
    ax.zaxis.pane.set_edgecolor(WHITE)
    ax.grid(True, linestyle=':', linewidth=0.5, color='#333333')

    # Scatter
    sc = ax.scatter(x, y, z, c=c, cmap=cmap, s=15, alpha=0.9, edgecolors='none')
    
    # Line
    ax.plot(x, y, z, color=WHITE, linewidth=0.5, alpha=0.5)
    
    # Labels
    if title:
        ax.set_title(title.upper(), pad=20, color=WHITE)
    ax.set_xlabel(xlabel, labelpad=10, color=WHITE)
    ax.set_ylabel(ylabel, labelpad=10, color=WHITE)
    ax.set_zlabel(zlabel, labelpad=10, color=WHITE)
    
    # Ticks
    ax.tick_params(axis='x', colors=WHITE)
    ax.tick_params(axis='y', colors=WHITE)
    ax.tick_params(axis='z', colors=WHITE)
    
    return sc

def plot_bar(ax, x, y, color=CYAN, title=None, xlabel=None, ylabel=None, xticklabels=None):
    """Plots a bar chart with architectural style."""
    bars = ax.bar(x, y, color=color, width=0.6)
    
    # Formatting
    if title:
        ax.set_title(title.upper(), loc='left', pad=15, fontsize=11, fontweight='bold', color=WHITE)
    if xlabel:
        ax.set_xlabel(xlabel.upper(), fontsize=9, labelpad=10, color=WHITE)
    if ylabel:
        ax.set_ylabel(ylabel.upper(), fontsize=9, labelpad=10, color=WHITE)
        
    ax.grid(axis='y', linestyle=':', linewidth=0.5, color='#333333')
    
    # Axis lines
    ax.axhline(0, color=WHITE, linewidth=0.8)
    sns.despine(ax=ax, bottom=True, left=False)
    
    # Ticks
    if xticklabels is not None:
        ax.set_xticks(x)
        ax.set_xticklabels(xticklabels, rotation=0, fontsize=8, color=WHITE)
    else:
        ax.tick_params(axis='x', colors=WHITE)
    
    ax.tick_params(axis='y', colors=WHITE)
    ax.spines['left'].set_color(WHITE)
    
    return bars

def plot_heatmap(ax, data, xticklabels, yticklabels, title=None, cmap='inferno', cbar_label=None):
    """Plots a heatmap with architectural style."""
    sns.heatmap(data, annot=True, fmt=".2f", 
                xticklabels=xticklabels, yticklabels=yticklabels, 
                ax=ax, cmap=cmap, cbar_kws={'label': cbar_label} if cbar_label else None,
                square=True, linewidths=0.5, linecolor=BLACK)
    
    if title:
        ax.set_title(title.upper(), loc='left', fontsize=11, pad=15, color=WHITE)
    
    ax.tick_params(colors=WHITE)
    
    # Colorbar formatting
    if ax.collections:
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(colors=WHITE)
        if cbar_label:
            cbar.set_label(cbar_label, color=WHITE)

def plot_3d_connected_trajectory(ax, x, y, z, c, cmap='inferno', title=None, xlabel='X', ylabel='Y', zlabel='Z'):
    """
    Plots a 3D trajectory with connected lines and scatter points in architectural style.
    """
    # Background
    ax.set_facecolor(BLACK)
    ax.grid(True, linestyle=':', linewidth=0.5, color='#333333')
    
    # Panes (Make them transparent but keep grid)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor(WHITE)
    ax.yaxis.pane.set_edgecolor(WHITE)
    ax.zaxis.pane.set_edgecolor(WHITE)
    
    # 1. Trajectory Line (White, semi-transparent)
    ax.plot(x, y, z, color=WHITE, alpha=0.3, linewidth=1)
    
    # 2. Scatter Points (Colored by variable)
    sc = ax.scatter(x, y, z, c=c, cmap=cmap, s=20, alpha=0.9, edgecolors='none')
    
    # Labels
    ax.set_xlabel(xlabel, labelpad=10, color=WHITE, fontsize=10)
    ax.set_ylabel(ylabel, labelpad=10, color=WHITE, fontsize=10)
    ax.set_zlabel(zlabel, labelpad=10, color=WHITE, fontsize=10)
    
    # Ticks
    ax.tick_params(axis='x', colors=WHITE, labelsize=8)
    ax.tick_params(axis='y', colors=WHITE, labelsize=8)
    ax.tick_params(axis='z', colors=WHITE, labelsize=8)
    
    # Title
    if title:
        ax.set_title(title, pad=20, color=WHITE, fontsize=12, fontweight='bold')
        
    return sc

def plot_network_graph(ax, G, pos, node_colors=CYAN, node_size=50, 
                       edge_color=GRAY, edge_width=1.0, edge_alpha=0.5,
                       with_labels=False, label_font_size=8, 
                       cmap='turbo', title=None):
    """Plots a NetworkX graph with architectural style."""
    
    # Edges
    if isinstance(edge_width, list):
         nx.draw_networkx_edges(G, pos, width=edge_width, edge_color=edge_color, alpha=edge_alpha, ax=ax)
    else:
         nx.draw_networkx_edges(G, pos, width=edge_width, edge_color=edge_color, alpha=edge_alpha, ax=ax)

    # Nodes
    if isinstance(node_colors, list) or isinstance(node_colors, np.ndarray):
        nodes = nx.draw_networkx_nodes(G, pos, nodelist=list(G.nodes()), 
                                       node_size=node_size, 
                                       node_color=node_colors, 
                                       cmap=cmap, 
                                       ax=ax)
    else:
        nodes = nx.draw_networkx_nodes(G, pos, nodelist=list(G.nodes()), 
                                       node_size=node_size, 
                                       node_color=node_colors, 
                                       ax=ax)
        
    # Labels
    if with_labels:
        nx.draw_networkx_labels(G, pos, font_size=label_font_size, font_color=BLACK,
                                bbox=dict(facecolor=WHITE, alpha=0.7, edgecolor='none', pad=1), ax=ax)

    # Title & Axis
    if title:
        ax.set_title(title.upper(), color=WHITE, fontweight='bold')
    ax.axis("off")
    
    return nodes

def plot_network_with_images(ax, G, pos, frames, movie_template, 
                             branch_nodes, leaf_nodes, 
                             node_colors=None, cmap='turbo', title=None):
    """Plots a network with image overlays for branch and leaf nodes."""
    
    # 1. Draw Base Graph
    nx.draw_networkx_edges(G, pos, edge_color=GRAY, alpha=0.5, width=1.0, ax=ax)
    
    if node_colors is not None:
        nx.draw_networkx_nodes(G, pos, nodelist=list(G.nodes()), 
                               node_size=20, 
                               node_color=node_colors, 
                               cmap=cmap, 
                               alpha=0.6,
                               ax=ax)
    else:
        nx.draw_networkx_nodes(G, pos, nodelist=list(G.nodes()), 
                               node_size=20, 
                               node_color=CYAN, 
                               alpha=0.6,
                               ax=ax)

    # Center for offset calculation
    pos_values = np.array(list(pos.values()))
    center_pos = np.mean(pos_values, axis=0)
    
    # Colormap for borders
    norm = plt.Normalize(vmin=np.min(frames), vmax=np.max(frames))
    cm = plt.cm.get_cmap(cmap)

    def add_image_node(node_idx):
        frame_idx = int(frames[node_idx])
        border_color = cm(norm(frame_idx))
        
        if 0 <= frame_idx < movie_template.shape[0]:
            img_data = movie_template[frame_idx]
            
            node_pos = pos[node_idx]
            vec = node_pos - center_pos
            dist = np.linalg.norm(vec)
            
            if dist > 0:
                direction = vec / dist
            else:
                direction = np.array([1, 1]) / np.sqrt(2)
                
            # Random rotation for organic feel
            rand_angle = np.random.uniform(-0.3, 0.3)
            c, s = np.cos(rand_angle), np.sin(rand_angle)
            rot_mat = np.array([[c, -s], [s, c]])
            direction = np.dot(rot_mat, direction)
            
            offset_scale = 80
            offset = direction * offset_scale
            
            imagebox = OffsetImage(img_data, zoom=0.15, cmap='gray')
            ab = AnnotationBbox(imagebox, node_pos, 
                                xybox=offset,
                                boxcoords="offset points",
                                arrowprops=dict(arrowstyle="-", color=border_color, alpha=0.5),
                                frameon=True, pad=0.2,
                                bboxprops=dict(edgecolor=border_color, linewidth=2))
            ax.add_artist(ab)

    # Select top nodes to avoid overcrowding
    # Branch
    sorted_branches = sorted(branch_nodes, key=lambda n: G.degree(n), reverse=True)
    top_branches = sorted_branches[:25]
    
    # Leaf
    leaf_distances = [(n, np.linalg.norm(pos[n] - center_pos)) for n in leaf_nodes]
    sorted_leaves = sorted(leaf_distances, key=lambda x: x[1], reverse=True)
    top_leaves = [n for n, dist in sorted_leaves[:25]]
    
    for n in top_branches:
        add_image_node(n)
        
    for n in top_leaves:
        add_image_node(n)

    if title:
        ax.set_title(title.upper(), color=WHITE, fontweight='bold')
    ax.axis("off")