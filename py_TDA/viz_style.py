import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler

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