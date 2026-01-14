
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')  # Suprimir advertencias de convergencia

def main(file_name):
    # ===========================================
    # 1. CARGAR Y PREPARAR DATOS
    # ===========================================
    try:
        datos = np.genfromtxt(file_name, delimiter=',')
        grados = datos[:, 0]
        cantidades = datos[:, 1]

        # Filtrar valores positivos
        mascara = cantidades > 0
        x = grados[mascara]
        y = cantidades[mascara]

        print(f"Datos cargados: {len(x)} puntos válidos")
        print(f"Rango de grados: {min(x)} - {max(x)}")
        print(f"Rango de cantidades: {min(y)} - {max(y)}")

        print(sum(y))
        y = y/sum(y)
    except Exception as e:
        print(f"Error cargando datos: {e}")
        return

    # ===========================================
    # 2. DEFINIR MODELOS
    # ===========================================
    def modelo_freeScale(x, a, b, c):
        return a * x**(-b) + c

    def modelo_exponencial(x, a, b, c):
        return a * np.exp(-x*b) + c

    def modelo_triple_exponencial(x, a1, b1, a2, b2, a3, b3, c):
        return a1 * np.exp(-x*b1) + a2 *np.exp(-x*b2) + a3 * np.exp(-x*b3) + c

    # ===========================================
    # 3. FUNCIÓN PARA CALCULAR MÉTRICAS
    # ===========================================
    def calcular_metricas(y_real, y_pred):
        # Error Cuadrático Medio (MSE)
        mse = np.mean((y_real - y_pred) ** 2)

        # Error Cuadrático Medio Relativo (RMSRE)
        # Evitar división por cero
        y_nonzero = y_real[y_real > 0]
        y_pred_nonzero = y_pred[y_real > 0]
        if len(y_nonzero) > 0:
            rmsre = np.sqrt(np.mean(((y_nonzero - y_pred_nonzero) / y_nonzero) ** 2))
        else:
            rmsre = np.inf

        # Coeficiente de determinación R²
        ss_res = np.sum((y_real - y_pred) ** 2)
        ss_tot = np.sum((y_real - np.mean(y_real)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else -np.inf

        return {
            'MSE': mse,
            'RMSRE': rmsre,
            'R²': r_squared
        }

    # ===========================================
    # 4. AJUSTAR MODELOS
    # ===========================================
    resultados = {}
    x_ajuste = np.linspace(min(x), max(x), 100000)

    # Modelo Exponencial Simple
    print("\n=== AJUSTANDO MODELO FREE SCALE ===")
    try:
        p0_exp = [max(y), 0.01, 0]
        bounds_exp = ([0, 0, 0], [max(y)*3, 10, max(y)])
        #param_exp, _ = curve_fit(modelo_freeScale, x, y, p0=p0_exp, bounds=bounds_exp, maxfev=10000)
        param_exp, _ = curve_fit(modelo_freeScale, x, y, p0=p0_exp)

        y_pred_exp = modelo_freeScale(x, *param_exp)
        metricas_exp = calcular_metricas(y, y_pred_exp)

        resultados['FreeScale'] = {
            'parametros': param_exp,
            'metricas': metricas_exp,
            'y_ajuste': modelo_freeScale(x_ajuste, *param_exp)
        }

        print(f"Parámetros: a={param_exp[0]:.4f}, b={param_exp[1]:.4f}, c={param_exp[2]:.4f}")
        print(f"MSE: {metricas_exp['MSE']:.8f}, R²: {metricas_exp['R²']:.4f}")

    except Exception as e:
        print(f"Error en ajuste free scale: {e}")

    # Modelo Doble Exponencial
    print("\n=== AJUSTANDO MODELO EXPONENCIAL ===")
    try:
        p0_doble = [max(y)*0.6, 0.5, min(y)*0.1]
        bounds_doble = ([0, 0, 0], [max(y)*3, 10, max(y)])
        param_doble, _ = curve_fit(modelo_exponencial, x, y, p0=p0_doble, bounds=bounds_doble, maxfev=10000)

        y_pred_doble = modelo_exponencial(x, *param_doble)
        metricas_doble = calcular_metricas(y, y_pred_doble)

        resultados['Exponencial'] = {
            'parametros': param_doble,
            'metricas': metricas_doble,
            'y_ajuste': modelo_exponencial(x_ajuste, *param_doble)
        }

        print(f"Parámetros: a1={param_doble[0]:.4f}, b1={param_doble[1]:.4f}, c={param_doble[2]:.4f}")
        print(f"MSE: {metricas_doble['MSE']:.8f}, R²: {metricas_doble['R²']:.4f}")

    except Exception as e:
        print(f"Error en ajuste exponencial: {e}")

    # Modelo Triple Exponencial
    print("\n=== AJUSTANDO MODELO TRIPLE EXPONENCIAL ===")
    try:
        p0_triple = [max(y)*0.4, 1.0, max(y)*0.3, 0.1, max(y)*0.2, 0.01, min(y)*0.1]
        bounds_triple = ([0, 0, 0, 0, 0, 0, 0], [max(y)*3, 10, max(y)*3, 10, max(y)*3, 10, max(y)])
        param_triple, _ = curve_fit(modelo_triple_exponencial, x, y, p0=p0_triple, bounds=bounds_triple, maxfev=20000)

        y_pred_triple = modelo_triple_exponencial(x, *param_triple)
        metricas_triple = calcular_metricas(y, y_pred_triple)

        resultados['Triple Exponencial'] = {
            'parametros': param_triple,
            'metricas': metricas_triple,
            'y_ajuste': modelo_triple_exponencial(x_ajuste, *param_triple)
        }

        print(f"Parámetros: a1={param_triple[0]:.4f}, b1={param_triple[1]:.4f}")
        print(f"            a2={param_triple[2]:.4f}, b2={param_triple[3]:.4f}")
        print(f"            a3={param_triple[4]:.4f}, b3={param_triple[5]:.4f}, c={param_triple[6]:.4f}")
        print(f"MSE: {metricas_triple['MSE']:.8f}, R²: {metricas_triple['R²']:.4f}")

    except Exception as e:
        print(f"Error en ajuste triple exponencial: {e}")

    # ===========================================
    # 5. COMPARACIÓN Y SELECCIÓN DEL MEJOR MODELO
    # ===========================================
    print("\n" + "="*50)
    print("COMPARACIÓN FINAL DE MODELOS")
    print("="*50)

    mejor_modelo = None
    mejor_mse = np.inf

    for nombre, resultado in resultados.items():
        mse = resultado['metricas']['MSE']
        r2 = resultado['metricas']['R²']
        print(f"{nombre:20} -> MSE: {mse:10.8f}, R²: {r2:8.4f}")

        if mse < mejor_mse:
            mejor_mse = mse
            mejor_modelo = nombre

    print(f"\nMEJOR MODELO: {mejor_modelo} (MSE más bajo)")

    # ===========================================
    # 6. GRAFICAR RESULTADOS
    # ===========================================
    plt.figure(figsize=(14, 10))

    # Colores para cada modelo
    colores = {
        'FreeScale': 'red',
        'Exponencial': 'blue',
        'Triple Exponencial': 'green'
    }

    # Graficar datos originales
    plt.scatter(x, y, alpha=0.7, label='Datos originales', color='black', s=50, zorder=5)

    # Graficar curvas ajustadas
    for nombre, resultado in resultados.items():
        color = colores.get(nombre, 'purple')
        plt.plot(x_ajuste, resultado['y_ajuste'],
                linewidth=2.5,
                label=f'{nombre}\nMSE: {resultado["metricas"]["MSE"]:.4f}\nR²: {resultado["metricas"]["R²"]:.4f}',
                color=color,
                zorder=4)

    plt.xlabel('Grado', fontsize=12)
    plt.ylabel('Cantidad de nodos', fontsize=12)
    plt.title('Comparación de Ajustes Exponenciales - Distribución de Grados', fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)

    # Usar escalas logarítmicas para mejor visualización
    plt.yscale('log')
    plt.xscale('log')

    plt.tight_layout()
    plt.savefig('multiple_'+file_name.split('_')[1].split('.')[0]+'.png')

    # ===========================================
    # 7. GRÁFICA ADICIONAL: RESIDUALES
    # ===========================================
    plt.figure(figsize=(14, 6))

    for i, (nombre, resultado) in enumerate(resultados.items()):
        color = colores.get(nombre, 'purple')
        y_pred = None
        if nombre == 'FreeScale':
            y_pred = modelo_freeScale(x, *resultado['parametros'])
        elif nombre == 'Exponencial':
            y_pred = modelo_exponencial(x, *resultado['parametros'])
        elif nombre == 'Triple Exponencial':
            y_pred = modelo_triple_exponencial(x, *resultado['parametros'])

        if y_pred is not None:
            residuales = y - y_pred
            plt.scatter(x, residuales, alpha=0.6, label=nombre, color=color, s=40)

    plt.axhline(y=0, color='black', linestyle='--', alpha=0.8)
    plt.xlabel('Grado', fontsize=12)
    plt.ylabel('Residuales (y_real - y_pred)', fontsize=12)
    plt.title('Análisis de Residuales por Modelo', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('linear')
    plt.xscale('log')
    plt.tight_layout()
    plt.savefig('check_'+file_name.split('_')[1].split('.')[0]+'.png')

distancias = [5,6,7,8,9]
condi = ['','No']
for d in distancias:
    for c in condi:
        archivo = 'nodesByDegree_d'+str(d)+c+'Lat.csv'
        try:
            print('#'*30)
            print('d'+str(d)+c+'Lat')
            print()
            main(archivo)
            print()
            print()
            print('#'*30)
            print('#'*30)

        except:
            continue
