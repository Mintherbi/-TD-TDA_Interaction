import matplotlib.pyplot as plt
import seaborn as sns

def set_architectural_style():
    """
    Sets matplotlib and seaborn style to a minimalist, architectural aesthetic.
    Prioritizes Roboto, Kozuka Gothic, and Helvetica fonts.
    """
    # Base Theme
    sns.set_theme(style="white")
    
    # Figure Settings
    plt.rcParams['figure.figsize'] = [10, 6]
    plt.rcParams['figure.dpi'] = 150
    
    # Font Settings
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Roboto', 'Kozuka Gothic Pr6N', 'Kozuka Gothic Pro', 'Helvetica', 'Arial', 'sans-serif']
    
    # Color & Line Settings
    plt.rcParams['axes.edgecolor'] = '#333333'
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['xtick.color'] = '#333333'
    plt.rcParams['ytick.color'] = '#333333'
    plt.rcParams['text.color'] = '#333333'
    plt.rcParams['axes.labelcolor'] = '#333333'
    
    # Typography
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    
    # Grid Settings
    plt.rcParams['grid.color'] = '#E0E0E0'
    plt.rcParams['grid.linestyle'] = '-'
    plt.rcParams['grid.linewidth'] = 0.5
    plt.rcParams['axes.grid'] = False # Default off, turn on selectively
    
    # Spines
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    
    print("Architectural plot style applied (Fonts: Roboto, Kozuka, Helvetica).")
