import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

def variogram(pairs_dict, VH, VAR, VAR2,max_step):
    # Calcular el máximo del 'step' y definir los límites de los bins
    
    bin_limits = list(range(0, max_step, int(VH)))
    
    #TODO revisar si es necesario sumar VH 

    # Inicializar lista para almacenar los resultados
    results = []

    # Agrupar datos por sector
    for sector in np.unique(pairs_dict['sector']):
        # Filtrar datos del sector actual
        sector_indices = np.where(pairs_dict['sector'] == sector)[0]
        sector_steps = np.array(pairs_dict['step'])[sector_indices]
        sector_VAR = np.array(pairs_dict[VAR])[sector_indices]
        sector_VAR2 = np.array(pairs_dict[VAR2])[sector_indices]

        # Clasificar los steps de este sector en los bins
        sector_step_bins = np.digitize(sector_steps, bins=bin_limits, right=True)

        # Calcular medias de step, VAR y VAR2 por bin dentro del sector
        for bin_index in range(1, len(bin_limits)):
            # Máscara para datos en el bin actual
            bin_mask = sector_step_bins == bin_index

            if np.any(bin_mask):  # Solo si hay datos en el bin
                # Calcular media de 'step', 'VAR' y 'VAR2' en el bin actual
                media_step = np.mean(sector_steps[bin_mask])
                media_VAR = np.mean(sector_VAR[bin_mask]) / 2  # VAR ya contiene el valor al cuadrado
                media_VAR2 = np.mean(sector_VAR2[bin_mask]) / 2  # VAR2 ya contiene el valor al cuadrado
            else:
                # Definir valores para bins vacíos
                media_step = (bin_limits[bin_index - 1] + bin_limits[bin_index]) / 2
                media_VAR = 0  # o np.nan si prefieres indicar que el bin está vacío
                media_VAR2 = 0  # o np.nan si prefieres indicar que el bin está vacío

            # Agregar resultados a la lista
            results.append({
                'step_bin': bin_limits[bin_index - 1],
                'sector': sector,
                'media_VAR': media_VAR,
                'media_VAR2': media_VAR2,
                'media_step': media_step
            })

    # Convertir los resultados en un DataFrame para graficar
    result_df = pd.DataFrame(results)

    # Crear subplots
    fig, axes = plt.subplots(2, 1, figsize=(12, 12), sharex=True)

    # Subplot 1: VAR
    for sector in result_df['sector'].unique():
        sector_data = result_df[result_df['sector'] == sector]
        axes[0].plot(sector_data['media_step'], sector_data['media_VAR'], 
                     marker='o', linestyle='-', label=f'Sector {sector}')
    axes[0].set_title('Variogram - VAR')
    axes[0].set_ylabel('Media de VAR')
    axes[0].legend(title='Sector')
    axes[0].grid(True)

    # Subplot 2: VAR2
    for sector in result_df['sector'].unique():
        sector_data = result_df[result_df['sector'] == sector]
        axes[1].plot(sector_data['media_step'], sector_data['media_VAR2'], 
                     marker='s', linestyle='--', label=f'Sector {sector}')
    axes[1].set_title('Variogram - VAR2')
    axes[1].set_xlabel('Step')
    axes[1].set_ylabel('Media de VAR2')
    axes[1].legend(title='Sector')
    axes[1].grid(True)

    # Ajustar el espacio entre subplots
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()
    

    return result_df



