import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

def variogram(pairs_dict,VH,VAR,VAR2):
    # Calcular el máximo del 'step' y definir los límites de los bins
    max_step = np.max(pairs_dict['step'])
    bin_limits = list(range(0, int(max_step + VH), int(VH)))

    # Inicializar lista para almacenar los resultados
    results = []

    # Agrupar datos por sector
    for sector in np.unique(pairs_dict['sector']):
        # Filtrar datos del sector actual
        sector_indices = np.where(pairs_dict['sector'] == sector)[0]
        sector_steps = np.array(pairs_dict['step'])[sector_indices]
        sector_VAR = np.array(pairs_dict[VAR])[sector_indices]

        # Clasificar los steps de este sector en los bins
        sector_step_bins = np.digitize(sector_steps, bins=bin_limits, right=True)

        # Calcular medias de step y VAR por bin dentro del sector
        for bin_index in range(1, len(bin_limits)):
            # Máscara para datos en el bin actual
            bin_mask = sector_step_bins == bin_index

            if np.any(bin_mask):  # Solo si hay datos en el bin
                # Calcular media de 'step' y media de 'VAR' en el bin actual
                media_step = np.mean(sector_steps[bin_mask])
                media_VAR = np.mean(sector_VAR[bin_mask])  # VAR ya contiene el valor al cuadrado
            else:
                # Definir valores para bins vacíos
                media_step = (bin_limits[bin_index - 1] + bin_limits[bin_index]) / 2
                media_VAR = 0  # o np.nan si prefieres indicar que el bin está vacío

            # Agregar resultados a la lista
            results.append({
                'step_bin': bin_limits[bin_index - 1],
                'sector': sector,
                'media_VAR': media_VAR,
                'media_step': media_step
            })

    # Convertir los resultados en un DataFrame para graficar
    result_df = pd.DataFrame(results)

    # Graficar
    plt.figure(figsize=(10, 6))
    
    for sector in result_df['sector'].unique():
        sector_data = result_df[result_df['sector'] == sector]
        plt.plot(sector_data['media_step'], sector_data['media_VAR'], 
                 marker='o', label=f'Sector {sector}')
    
    plt.xlabel('Step')
    plt.ylabel('Media de VAR')
    plt.title('Variogram cloud')
    plt.legend(title='Sector')
    plt.grid(True)
    plt.show()

    return result_df