import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Sistema de Costeo con GIF y Tasas",
    page_icon="•",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 CSS CON TONOS ROSADOS COMPLETOS
st.markdown("""
<style>
    /* PALETA ROSA COMPLETA */
    :root {
        --primary-pink: #E83E8C;
        --secondary-pink: #F06292;
        --accent-pink: #F48FB1;
        --light-pink: #F8BBD0;
        --very-light-pink: #FCE4EC;
        --background-pink: #FFF5F7;
        --dark-pink: #C2185B;
        --text-dark: #2D3748;
        --text-light: #718096;
        --white: #FFFFFF;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--background-pink), var(--very-light-pink)) !important;
    }
    
    .main-header {
        font-size: 2.5rem !important;
        color: var(--dark-pink) !important;
        font-family: 'Arial', sans-serif;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(194, 24, 91, 0.1);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--very-light-pink), var(--light-pink));
        border-right: 3px solid var(--primary-pink);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, var(--primary-pink), var(--secondary-pink));
        color: var(--white);
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 3px 5px rgba(232, 62, 140, 0.3);
        font-size: 0.9rem;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, var(--dark-pink), var(--primary-pink));
        transform: translateY(-1px);
        box-shadow: 0 5px 8px rgba(232, 62, 140, 0.4);
    }
    
    .card {
        background: linear-gradient(135deg, var(--white), var(--very-light-pink));
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 4px solid var(--primary-pink);
        box-shadow: 0 3px 6px rgba(232, 62, 140, 0.1);
        margin-bottom: 1rem;
        border: 1px solid var(--light-pink);
    }
    
    .card-header {
        background: linear-gradient(135deg, var(--primary-pink), var(--accent-pink));
        color: var(--white);
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, var(--very-light-pink), var(--white));
        border: 2px solid var(--light-pink);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(232, 62, 140, 0.1);
    }
    
    [data-testid="metric-label"] {
        color: var(--primary-pink) !important;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    [data-testid="metric-value"] {
        color: var(--dark-pink) !important;
        font-size: 1.3rem !important;
        font-weight: bold;
    }
    
    h1, h2, h3 {
        color: var(--dark-pink) !important;
        font-family: 'Arial', sans-serif;
        font-weight: 600;
    }
    
    h1 {
        border-bottom: 2px solid var(--primary-pink);
        padding-bottom: 0.3rem;
    }
    
    h2 {
        background: linear-gradient(90deg, var(--primary-pink), transparent);
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        color: var(--white) !important;
        font-size: 1.2rem;
    }
    
    .badge-primary {
        background: linear-gradient(135deg, var(--primary-pink), var(--accent-pink));
        color: var(--white);
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: bold;
        box-shadow: 0 2px 3px rgba(232, 62, 140, 0.3);
    }
    
    .badge-secondary {
        background-color: var(--light-pink);
        color: var(--dark-pink);
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    .positive {
        color: #059669 !important;
        font-weight: bold;
        background-color: #D1FAE5;
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        font-size: 0.85rem;
    }
    
    .negative {
        color: var(--primary-pink) !important;
        font-weight: bold;
        background-color: var(--light-pink);
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        font-size: 0.85rem;
    }
    
    .gif-section {
        background: linear-gradient(135deg, #F0FFF4, #C6F6D5);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #38A169;
        margin: 1rem 0;
    }
    
    .gif-real {
        background: linear-gradient(135deg, #FEF5E7, #FEEBC8);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #DD6B20;
        margin: 1rem 0;
    }
    
    .tasas-section {
        background: linear-gradient(135deg, #EBF8FF, #BEE3F8);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3182CE;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Clases del sistema de costeo MODIFICADAS - TASAS SOLO EN ABC Y TRADICIONAL
class TraditionalCosting:
    @staticmethod
    def calculate_traditional_costing(data: Dict, include_gif: bool = False, use_tasas_estimadas: bool = False) -> Dict:
        products = data['products']
        
        # Usar tasas estimadas si están disponibles y se solicitan
        if use_tasas_estimadas and 'tasas_estimadas' in data:
            overhead_rate = data['tasas_estimadas'].get('tasa_tradicional', 0)
            total_overhead = sum(p['machine_hours'] for p in products.values()) * overhead_rate
        else:
            total_machine_hours = sum(p['machine_hours'] for p in products.values())
            total_overhead = data['total_overhead']
            overhead_rate = total_overhead / total_machine_hours if total_machine_hours > 0 else 0
        
        # Calcular GIF estimados si se incluyen
        if include_gif and 'gif_estimados' in data:
            total_overhead += sum(data['gif_estimados'].values())
        
        results = {}
        
        for product_name, product_data in products.items():
            prime_cost = product_data['prime_cost']
            units = product_data['units']
            overhead_allocated = product_data['machine_hours'] * overhead_rate
            total_cost = prime_cost + overhead_allocated
            
            # Agregar GIF reales si existen
            if include_gif and 'gif_reales' in data and product_name in data['gif_reales']:
                total_cost += data['gif_reales'][product_name]
                overhead_allocated += data['gif_reales'][product_name]
            
            unit_cost = total_cost / units if units > 0 else 0
            
            results[product_name] = {
                'prime_cost': prime_cost,
                'overhead_allocated': overhead_allocated,
                'total_cost': total_cost,
                'unit_cost': unit_cost,
                'overhead_rate': overhead_rate,
                'method': 'Tasas Estimadas' if use_tasas_estimadas else 'Calculada'
            }
        
        return results

class ABCCosting:
    @staticmethod
    def calculate_abc_costing(data: Dict, include_gif: bool = False, use_tasas_estimadas: bool = False) -> Dict:
        products = data['products']
        activities = data['activities']
        
        # Usar tasas estimadas de actividades si están disponibles
        if use_tasas_estimadas and 'tasas_abc_estimadas' in data:
            activity_rates = data['tasas_abc_estimadas']
        else:
            # Calcular tasas normalmente
            activity_rates = {}
            for activity_name, activity_data in activities.items():
                total_driver = sum(products[p].get(activity_data['driver'], 0) for p in products)
                activity_rates[activity_name] = activity_data['cost'] / total_driver if total_driver > 0 else 0
        
        # Incluir GIF estimados en actividades si se solicitan
        if include_gif and 'gif_estimados' in data:
            for activity_name, gif_amount in data['gif_estimados'].items():
                if activity_name in activities:
                    activities[activity_name]['cost'] += gif_amount
        
        results = {}
        
        for product_name, product_data in products.items():
            prime_cost = product_data['prime_cost']
            units = product_data['units']
            overhead_abc = 0
            
            for activity_name, activity_data in activities.items():
                driver_consumption = product_data.get(activity_data['driver'], 0)
                overhead_abc += driver_consumption * activity_rates[activity_name]
            
            total_cost = prime_cost + overhead_abc
            
            # Agregar GIF reales si existen
            if include_gif and 'gif_reales' in data and product_name in data['gif_reales']:
                total_cost += data['gif_reales'][product_name]
                overhead_abc += data['gif_reales'][product_name]
            
            unit_cost = total_cost / units if units > 0 else 0
            
            results[product_name] = {
                'prime_cost': prime_cost,
                'overhead_abc': overhead_abc,
                'total_cost': total_cost,
                'unit_cost': unit_cost,
                'activity_rates': activity_rates,
                'method': 'Tasas Estimadas' if use_tasas_estimadas else 'Calculada'
            }
        
        return results

class HighLowMethod:
    @staticmethod
    def calculate_high_low(high_data: Dict, low_data: Dict) -> Dict:
        # Calcular normalmente - SIN TASAS ESTIMADAS
        if high_data['activity'] == low_data['activity']:
            return {
                'variable_rate': 0,
                'fixed_cost': 0,
                'equation': "Y = 0.00 + 0.0000X (Error: mismos puntos)"
            }
            
        variable_rate = ((high_data['cost'] - low_data['cost']) / 
                        (high_data['activity'] - low_data['activity']))
        fixed_cost = high_data['cost'] - (variable_rate * high_data['activity'])
        equation = f"Y = {fixed_cost:.2f} + {variable_rate:.4f}X"
        
        return {
            'variable_rate': variable_rate,
            'fixed_cost': fixed_cost,
            'equation': equation
        }

class CostSheets:
    @staticmethod
    def calculate_cost_of_goods_sold(data: Dict, include_gif: bool = False) -> Dict:
        materials_used = (data['beginning_raw_materials'] + 
                         data['purchases_raw_materials'] - 
                         data['ending_raw_materials'])
        
        manufacturing_overhead = data['manufacturing_overhead']
        
        # Incluir GIF estimados si se solicitan
        if include_gif and 'gif_estimados' in data:
            manufacturing_overhead += sum(data['gif_estimados'].values())
        
        total_manufacturing_costs = (materials_used + 
                                   data['direct_labor'] + 
                                   manufacturing_overhead)
        
        cost_of_goods_manufactured = (data['beginning_wip'] + 
                                     total_manufacturing_costs - 
                                     data['ending_wip'])
        
        cost_of_goods_sold = (data['beginning_finished_goods'] + 
                             cost_of_goods_manufactured - 
                             data['ending_finished_goods'])
        
        # Incluir GIF reales si existen
        if include_gif and 'gif_reales' in data:
            cost_of_goods_sold += data['gif_reales'].get('costo_ventas', 0)
        
        return {
            'materials_used': materials_used,
            'total_manufacturing_costs': total_manufacturing_costs,
            'cost_of_goods_manufactured': cost_of_goods_manufactured,
            'cost_of_goods_sold': cost_of_goods_sold,
            'manufacturing_overhead': manufacturing_overhead
        }

# Interfaz principal
def main():
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #FFF5F7, #FCE4EC); border-radius: 15px; margin-bottom: 1.5rem; border: 1px solid #F8BBD0;'>
        <h1 class='main-header'>Sistema de Costeo</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class='card-header'>
            <h3 style='color: white; margin: 0; text-align: center;'>Menu Principal</h3>
            <p style='color: #FCE4EC; text-align: center; margin: 0.3rem 0 0 0; font-size: 0.9rem;'>Selecciona el ejercicio</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        exercise_type = st.selectbox(
            "Tipo de Ejercicio",
            [
                "Costeo Tradicional vs ABC",
                "Metodo Punto Alto-Punto Bajo", 
                "Estados de Costos",
                "Analisis de Costo Primo"
            ]
        )
        
        st.markdown("---")
        
        st.markdown("""
        <div class='card'>
            <h4 style='color: #E83E8C; margin-bottom: 0.5rem;'>Caracteristicas</h4>
            <p style='color: #718096; font-size: 0.8rem; margin: 0;'>
                • GIF en todos los metodos<br>
                • Tasas solo en ABC/Tradicional<br>
                • Calculos flexibles<br>
                • Comparacion de resultados
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Ejecutar modulo segun seleccion
    if exercise_type == "Costeo Tradicional vs ABC":
        render_traditional_vs_abc()
    elif exercise_type == "Metodo Punto Alto-Punto Bajo":
        render_high_low_method()
    elif exercise_type == "Estados de Costos":
        render_cost_sheets()
    elif exercise_type == "Analisis de Costo Primo":
        render_prime_cost_analysis()

def render_traditional_vs_abc():
    st.markdown("""
    <div class='card-header hover-lift'>
        <h2 style='color: white; margin: 0;'>Costeo Tradicional vs ABC</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Configuracion de opciones
    col_config, col_info = st.columns([2, 1])
    
    with col_config:
        include_gif = st.checkbox("Incluir GIF estimados y reales", value=False)
        use_tasas_estimadas = st.checkbox("Usar tasas estimadas en lugar de calcular", value=False)
    
    with col_info:
        if include_gif or use_tasas_estimadas:
            info_text = []
            if include_gif:
                info_text.append("• GIF activados")
            if use_tasas_estimadas:
                info_text.append("• Tasas estimadas activadas")
            
            st.markdown(f"""
            <div class='tasas-section'>
                <small><strong>Configuracion:</strong></small><br>
                <small>{'<br>'.join(info_text)}</small>
            </div>
            """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='card hover-lift'>
            <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Datos de Productos</h3>
            <p style='color: #718096; font-size: 0.85rem;'>Ingresa la informacion de cada producto</p>
        </div>
        """, unsafe_allow_html=True)
        
        num_products = st.number_input("Numero de productos:", min_value=1, max_value=5, value=1)
        
        products = {}
        for i in range(num_products):
            st.markdown(f"""
            <div class='card' style='background: linear-gradient(135deg, #FFFFFF, #FCE4EC);'>
                <h4 style='color: #F06292; margin: 0;'>Producto {i+1}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            name = st.text_input(f"Nombre del producto", value=f"Producto {i+1}", key=f"name_{i}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                units = st.number_input(f"Unidades", value=0, key=f"units_{i}", min_value=0)
                prime_cost = st.number_input(f"Costo Primo ($)", value=0.0, key=f"prime_{i}", min_value=0.0, format="%.2f")
            with col_b:
                machine_hours = st.number_input(f"Horas-Maquina", value=0, key=f"mh_{i}", min_value=0)
                material_moves = st.number_input(f"Movimientos", value=0, key=f"mm_{i}", min_value=0)
                setups = st.number_input(f"Arranques", value=0, key=f"setups_{i}", min_value=0)
            
            products[name] = {
                'units': units,
                'prime_cost': prime_cost,
                'machine_hours': machine_hours,
                'material_moves': material_moves,
                'setups': setups
            }
    
    with col2:
        # SECCION DE TASAS ESTIMADAS (solo en este metodo)
        tasas_estimadas = {}
        tasas_abc_estimadas = {}
        
        if use_tasas_estimadas:
            st.markdown("""
            <div class='tasas-section'>
                <h4 style='color: #22543D; margin: 0 0 0.5rem 0;'>Tasas Estimadas</h4>
                <p style='color: #22543D; font-size: 0.8rem; margin: 0;'>Ingresa las tasas predeterminadas</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_t1, col_t2 = st.columns(2)
            
            with col_t1:
                st.write("**Tasas Tradicional:**")
                tasa_tradicional = st.number_input("Tasa por Hora-Maquina ($):", value=0.0, min_value=0.0, format="%.4f", key="tasa_trad")
                if tasa_tradicional > 0:
                    tasas_estimadas['tasa_tradicional'] = tasa_tradicional
            
            with col_t2:
                st.write("**Tasas ABC:**")
                tasa_maquina = st.number_input("Tasa Operacion Equipo ($):", value=0.0, min_value=0.0, format="%.4f", key="tasa_abc_maq")
                tasa_material = st.number_input("Tasa Movimiento Material ($):", value=0.0, min_value=0.0, format="%.4f", key="tasa_abc_mat")
                tasa_setup = st.number_input("Tasa Arranques ($):", value=0.0, min_value=0.0, format="%.4f", key="tasa_abc_setup")
                
                if tasa_maquina > 0:
                    tasas_abc_estimadas['machine_operation'] = tasa_maquina
                if tasa_material > 0:
                    tasas_abc_estimadas['material_handling'] = tasa_material
                if tasa_setup > 0:
                    tasas_abc_estimadas['setups'] = tasa_setup
        
        # Solo mostrar costos indirectos si no se usan tasas estimadas
        if not use_tasas_estimadas:
            st.markdown("""
            <div class='card hover-lift'>
                <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Costos Indirectos</h3>
            </div>
            """, unsafe_allow_html=True)
            
            total_overhead = st.number_input("Costo Total Indirectos ($):", value=0.0, min_value=0.0, format="%.2f")
        else:
            total_overhead = 0.0
        
        # SECCION DE GIF ESTIMADOS (opcional)
        gif_estimados = {}
        if include_gif:
            st.markdown("""
            <div class='gif-section'>
                <h4 style='color: #22543D; margin: 0 0 0.5rem 0;'>GIF Estimados por Actividad</h4>
            </div>
            """, unsafe_allow_html=True)
            
            gif_machine = st.number_input("GIF Estimado - Operacion Equipo ($):", value=0.0, min_value=0.0, format="%.2f")
            gif_material = st.number_input("GIF Estimado - Movimiento Material ($):", value=0.0, min_value=0.0, format="%.2f")
            gif_setup = st.number_input("GIF Estimado - Arranques ($):", value=0.0, min_value=0.0, format="%.2f")
            
            if gif_machine > 0:
                gif_estimados['machine_operation'] = gif_machine
            if gif_material > 0:
                gif_estimados['material_handling'] = gif_material
            if gif_setup > 0:
                gif_estimados['setups'] = gif_setup
        
        # Solo mostrar actividades si no se usan tasas ABC estimadas
        if not use_tasas_estimadas:
            st.markdown("""
            <div class='card hover-lift'>
                <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Actividades para ABC</h3>
                <p style='color: #718096; font-size: 0.85rem;'>Configura las actividades del costeo ABC</p>
            </div>
            """, unsafe_allow_html=True)
            
            machine_cost = st.number_input("Costo Operacion Equipo ($):", value=0.0, min_value=0.0, format="%.2f")
            material_cost = st.number_input("Costo Movimiento Material ($):", value=0.0, min_value=0.0, format="%.2f")
            setup_cost = st.number_input("Costo Arranques ($):", value=0.0, min_value=0.0, format="%.2f")
            
            activities = {
                'machine_operation': {'cost': machine_cost, 'driver': 'machine_hours'},
                'material_handling': {'cost': material_cost, 'driver': 'material_moves'},
                'setups': {'cost': setup_cost, 'driver': 'setups'}
            }
        else:
            activities = {
                'machine_operation': {'cost': 0, 'driver': 'machine_hours'},
                'material_handling': {'cost': 0, 'driver': 'material_moves'},
                'setups': {'cost': 0, 'driver': 'setups'}
            }
        
        # SECCION DE GIF REALES (opcional)
        gif_reales = {}
        if include_gif:
            st.markdown("""
            <div class='gif-real'>
                <h4 style='color: #744210; margin: 0 0 0.5rem 0;'>GIF Reales por Producto</h4>
                <p style='color: #744210; font-size: 0.8rem; margin: 0;'>Costos indirectos reales incurridos</p>
            </div>
            """, unsafe_allow_html=True)
            
            for product_name in products.keys():
                gif_real = st.number_input(f"GIF Real - {product_name} ($):", value=0.0, min_value=0.0, format="%.2f", key=f"gif_real_{product_name}")
                if gif_real > 0:
                    gif_reales[product_name] = gif_real
    
    if st.button("Calcular Ambos Metodos", use_container_width=True):
        if not products:
            st.error("Por favor ingresa al menos un producto")
            return
            
        # Preparar datos
        data = {
            'products': products,
            'total_overhead': total_overhead,
            'activities': activities
        }
        
        # Agregar datos opcionales
        if include_gif:
            if gif_estimados:
                data['gif_estimados'] = gif_estimados
            if gif_reales:
                data['gif_reales'] = gif_reales
        
        if use_tasas_estimadas:
            if tasas_estimadas:
                data['tasas_estimadas'] = tasas_estimadas
            if tasas_abc_estimadas:
                data['tasas_abc_estimadas'] = tasas_abc_estimadas
        
        # Calcular con diferentes combinaciones
        traditional_normal = TraditionalCosting.calculate_traditional_costing(data, include_gif=False, use_tasas_estimadas=False)
        abc_normal = ABCCosting.calculate_abc_costing(data, include_gif=False, use_tasas_estimadas=False)
        
        traditional_avanzado = TraditionalCosting.calculate_traditional_costing(data, include_gif=include_gif, use_tasas_estimadas=use_tasas_estimadas)
        abc_avanzado = ABCCosting.calculate_abc_costing(data, include_gif=include_gif, use_tasas_estimadas=use_tasas_estimadas)
        
        # Mostrar resultados
        st.markdown("""
        <div class='card-header hover-lift'>
            <h3 style='color: white; margin: 0;'>Resultados Comparativos</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabla de resultados
        results_data = []
        for product_name in products.keys():
            # Metodo normal
            trad_normal = traditional_normal[product_name]['unit_cost']
            abc_normal_val = abc_normal[product_name]['unit_cost']
            
            # Metodo avanzado
            trad_avanzado = traditional_avanzado[product_name]['unit_cost']
            abc_avanzado_val = abc_avanzado[product_name]['unit_cost']
            
            # Diferencias
            diff_normal = abc_normal_val - trad_normal
            diff_avanzado = abc_avanzado_val - trad_avanzado
            efecto_gif_tasas = trad_avanzado - trad_normal
            
            results_data.append({
                'Producto': product_name,
                'Tradicional Normal': f"${trad_normal:.2f}",
                'ABC Normal': f"${abc_normal_val:.2f}",
                'Tradicional Avanzado': f"${trad_avanzado:.2f}" if (include_gif or use_tasas_estimadas) else "N/A",
                'ABC Avanzado': f"${abc_avanzado_val:.2f}" if (include_gif or use_tasas_estimadas) else "N/A",
                'Efecto GIF/Tasas': f"<span class='{'positive' if efecto_gif_tasas >= 0 else 'negative'}'>{efecto_gif_tasas:+.2f}</span>" if (include_gif or use_tasas_estimadas) else "N/A",
                'Metodo Trad': traditional_avanzado[product_name]['method'],
                'Metodo ABC': abc_avanzado[product_name]['method']
            })
        
        results_df = pd.DataFrame(results_data)
        st.markdown(results_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        # Resumen de configuracion
        if include_gif or use_tasas_estimadas:
            st.markdown("""
            <div class='tasas-section'>
                <h4 style='color: #22543D; margin: 0 0 0.5rem 0;'>Resumen de Configuracion</h4>
            </div>
            """, unsafe_allow_html=True)
            
            col_r1, col_r2 = st.columns(2)
            
            with col_r1:
                if include_gif and gif_estimados:
                    st.write("**GIF Estimados Aplicados:**")
                    for actividad, monto in gif_estimados.items():
                        st.write(f"- {actividad}: ${monto:.2f}")
                
                if include_gif and gif_reales:
                    st.write("**GIF Reales Aplicados:**")
                    for producto, monto in gif_reales.items():
                        st.write(f"- {producto}: ${monto:.2f}")
            
            with col_r2:
                if use_tasas_estimadas and tasas_estimadas:
                    st.write("**Tasas Estimadas Aplicadas:**")
                    for tasa, valor in tasas_estimadas.items():
                        st.write(f"- {tasa}: ${valor:.4f}")
                
                if use_tasas_estimadas and tasas_abc_estimadas:
                    st.write("**Tasas ABC Estimadas:**")
                    for actividad, tasa in tasas_abc_estimadas.items():
                        st.write(f"- {actividad}: ${tasa:.4f}")

def render_high_low_method():
    st.markdown("""
    <div class='card-header hover-lift'>
        <h2 style='color: white; margin: 0;'>Metodo Punto Alto-Punto Bajo</h2>
        <p style='color: #FCE4EC; margin: 0.3rem 0 0 0; font-size: 0.9rem;'>Calculo tradicional</p>
    </div>
    """, unsafe_allow_html=True)
    
    # SIN OPCION DE TASAS ESTIMADAS en este metodo
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='card hover-lift'>
            <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Punto Alto</h3>
        </div>
        """, unsafe_allow_html=True)
        high_activity = st.number_input("Nivel de Actividad (Alto):", value=0, min_value=0)
        high_cost = st.number_input("Costo Total (Alto) ($):", value=0.0, min_value=0.0, format="%.2f")
    
    with col2:
        st.markdown("""
        <div class='card hover-lift'>
            <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Punto Bajo</h3>
        </div>
        """, unsafe_allow_html=True)
        low_activity = st.number_input("Nivel de Actividad (Bajo):", value=0, min_value=0)
        low_cost = st.number_input("Costo Total (Bajo) ($):", value=0.0, min_value=0.0, format="%.2f")
    
    if st.button("Calcular Ecuacion", use_container_width=True):
        if high_activity == 0 and low_activity == 0:
            st.error("Ingresa datos de actividad diferentes de cero")
            return
            
        high_data = {'activity': high_activity, 'cost': high_cost}
        low_data = {'activity': low_activity, 'cost': low_cost}
        
        result = HighLowMethod.calculate_high_low(high_data, low_data)
        
        st.markdown("""
        <div class='card-header hover-lift'>
            <h3 style='color: white; margin: 0;'>Resultados</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Costo Variable Unitario", f"${result['variable_rate']:.4f}")
        with col_b:
            st.metric("Costo Fijo", f"${result['fixed_cost']:.2f}")
        with col_c:
            st.metric("Metodo", "Calculado")
        
        st.markdown("""
        <div class='card hover-lift'>
            <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Ecuacion de Costos</h3>
            <p style='color: #718096; font-size: 1.1rem; font-family: monospace;'>{}</p>
        </div>
        """.format(result['equation']), unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card hover-lift'>
            <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Prediccion</h3>
        </div>
        """, unsafe_allow_html=True)
        
        predict_activity = st.number_input("Nivel para Predecir:", value=0, min_value=0)
        predicted_cost = result['fixed_cost'] + (result['variable_rate'] * predict_activity)
        st.metric(f"Costo para {predict_activity} unidades", f"${predicted_cost:.2f}")

def render_cost_sheets():
    st.markdown("""
    <div class='card-header hover-lift'>
        <h2 style='color: white; margin: 0;'>Estados de Costos</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # SIN OPCION DE TASAS ESTIMADAS en este metodo
    include_gif = st.checkbox("Incluir GIF en Estados de Costos", value=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='card hover-lift'>
            <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Inventarios</h3>
        </div>
        """, unsafe_allow_html=True)
        beginning_raw = st.number_input("Inv. Inicial Materiales ($):", value=0.0, min_value=0.0, format="%.2f")
        purchases_raw = st.number_input("Compras Materiales ($):", value=0.0, min_value=0.0, format="%.2f")
        ending_raw = st.number_input("Inv. Final Materiales ($):", value=0.0, min_value=0.0, format="%.2f")
        beginning_wip = st.number_input("Inv. Inicial PEP ($):", value=0.0, min_value=0.0, format="%.2f")
        ending_wip = st.number_input("Inv. Final PEP ($):", value=0.0, min_value=0.0, format="%.2f")
    
    with col2:
        st.markdown("""
        <div class='card hover-lift'>
            <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Costos de Produccion</h3>
        </div>
        """, unsafe_allow_html=True)
        direct_labor = st.number_input("Mano de Obra Directa ($):", value=0.0, min_value=0.0, format="%.2f")
        manufacturing_overhead = st.number_input("Gastos Indirectos ($):", value=0.0, min_value=0.0, format="%.2f")
        beginning_finished = st.number_input("Inv. Inicial Terminados ($):", value=0.0, min_value=0.0, format="%.2f")
        ending_finished = st.number_input("Inv. Final Terminados ($):", value=0.0, min_value=0.0, format="%.2f")
    
    # Seccion de GIF para estados de costos
    gif_estimados = {}
    gif_reales = {}
    
    if include_gif:
        st.markdown("""
        <div class='gif-section'>
            <h4 style='color: #22543D; margin: 0 0 0.5rem 0;'>GIF para Estados de Costos</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.write("**GIF Estimados:**")
            gif_depreciacion = st.number_input("GIF Estimado - Depreciacion ($):", value=0.0, min_value=0.0, format="%.2f")
            gif_mantenimiento = st.number_input("GIF Estimado - Mantenimiento ($):", value=0.0, min_value=0.0, format="%.2f")
            
            if gif_depreciacion > 0:
                gif_estimados['depreciacion'] = gif_depreciacion
            if gif_mantenimiento > 0:
                gif_estimados['mantenimiento'] = gif_mantenimiento
        
        with col_g2:
            st.write("**GIF Reales:**")
            gif_real_ventas = st.number_input("GIF Real - Costo de Ventas ($):", value=0.0, min_value=0.0, format="%.2f")
            
            if gif_real_ventas > 0:
                gif_reales['costo_ventas'] = gif_real_ventas
    
    if st.button("Generar Estado", use_container_width=True):
        data = {
            'beginning_raw_materials': beginning_raw,
            'purchases_raw_materials': purchases_raw,
            'ending_raw_materials': ending_raw,
            'direct_labor': direct_labor,
            'manufacturing_overhead': manufacturing_overhead,
            'beginning_wip': beginning_wip,
            'ending_wip': ending_wip,
            'beginning_finished_goods': beginning_finished,
            'ending_finished_goods': ending_finished
        }
        
        if include_gif:
            if gif_estimados:
                data['gif_estimados'] = gif_estimados
            if gif_reales:
                data['gif_reales'] = gif_reales
        
        results = CostSheets.calculate_cost_of_goods_sold(data, include_gif=include_gif)
        
        st.markdown("""
        <div class='card-header hover-lift'>
            <h3 style='color: white; margin: 0;'>Estado de Costos de Produccion y Ventas</h3>
        </div>
        """, unsafe_allow_html=True)
        
        cost_data = {
            'Concepto': [
                'Materiales Directos Utilizados',
                '(+) Mano de Obra Directa', 
                '(+) Gastos Indirectos de Fabricacion',
                '(=) Costo Total de Manufactura',
                '(+) Inventario Inicial PEP',
                '(-) Inventario Final PEP',
                '(=) Costo de Articulos Producidos',
                '(+) Inventario Inicial Terminados',
                '(-) Inventario Final Terminados',
                '(=) COSTO DE VENTAS'
            ],
            'Monto': [
                f"${results['materials_used']:,.2f}",
                f"${direct_labor:,.2f}",
                f"${results['manufacturing_overhead']:,.2f}",
                f"${results['total_manufacturing_costs']:,.2f}",
                f"${beginning_wip:,.2f}",
                f"${ending_wip:,.2f}",
                f"${results['cost_of_goods_manufactured']:,.2f}",
                f"${beginning_finished:,.2f}",
                f"${ending_finished:,.2f}",
                f"${results['cost_of_goods_sold']:,.2f}"
            ]
        }
        
        cost_df = pd.DataFrame(cost_data)
        st.dataframe(cost_df, hide_index=True)
        
        # Mostrar resumen de GIF si se incluyeron
        if include_gif and (gif_estimados or gif_reales):
            st.markdown("""
            <div class='gif-real'>
                <h4 style='color: #744210; margin: 0 0 0.5rem 0;'>Efecto de los GIF</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Calcular sin GIF para comparar
            results_sin_gif = CostSheets.calculate_cost_of_goods_sold(data, include_gif=False)
            
            col_e1, col_e2 = st.columns(2)
            
            with col_e1:
                st.metric("Gastos Indirectos Sin GIF", f"${manufacturing_overhead:,.2f}")
                st.metric("Gastos Indirectos Con GIF", f"${results['manufacturing_overhead']:,.2f}")
            
            with col_e2:
                efecto_gif = results['manufacturing_overhead'] - manufacturing_overhead
                st.metric("Incremento por GIF", f"${efecto_gif:,.2f}")

def render_prime_cost_analysis():
    st.markdown("""
    <div class='card-header hover-lift'>
        <h2 style='color: white; margin: 0;'>Analisis de Costo Primo</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # El costo primo no incluye GIF ni tasas estimadas por definicion
    st.markdown("""
    <div class='card hover-lift'>
        <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Datos del Producto</h3>
        <p style='color: #718096; font-size: 0.85rem;'>El costo primo solo incluye materiales y mano de obra directa</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("Nombre del Producto:", value="Mi Producto")
        units = st.number_input("Unidades Producidas:", value=0, min_value=0)
        
        st.markdown("""
        <div class='card hover-lift'>
            <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Materiales Directos ($)</h3>
        </div>
        """, unsafe_allow_html=True)
        material1 = st.number_input("Material 1:", value=0.0, min_value=0.0, format="%.2f")
        material2 = st.number_input("Material 2:", value=0.0, min_value=0.0, format="%.2f")
        material3 = st.number_input("Material 3:", value=0.0, min_value=0.0, format="%.2f")
    
    with col2:
        st.markdown("""
        <div class='card hover-lift'>
            <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Mano de Obra Directa ($)</h3>
        </div>
        """, unsafe_allow_html=True)
        labor1 = st.number_input("Trabajo 1:", value=0.0, min_value=0.0, format="%.2f")
        labor2 = st.number_input("Trabajo 2:", value=0.0, min_value=0.0, format="%.2f")
    
    if st.button("Calcular Costo Primo", use_container_width=True):
        total_materials = material1 + material2 + material3
        total_labor = labor1 + labor2
        prime_cost = total_materials + total_labor
        prime_cost_unit = prime_cost / units if units > 0 else 0
        
        st.markdown("""
        <div class='card-header hover-lift'>
            <h3 style='color: white; margin: 0;'>Resultados del Costo Primo</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Costo Primo Total", f"${prime_cost:.2f}")
        with col_b:
            st.metric("Costo Primo Unitario", f"${prime_cost_unit:.2f}")
        with col_c:
            st.metric("Unidades", f"{units}")
        
        st.markdown("""
        <div class='card hover-lift'>
            <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Composicion del Costo Primo</h3>
        </div>
        """, unsafe_allow_html=True)
        
        composition_data = {
            'Componente': ['Materiales Directos', 'Mano de Obra Directa'],
            'Monto': [f"${total_materials:.2f}", f"${total_labor:.2f}"],
            'Porcentaje': [
                f"{(total_materials / prime_cost * 100):.1f}%" if prime_cost > 0 else "0%",
                f"{(total_labor / prime_cost * 100):.1f}%" if prime_cost > 0 else "0%"
            ]
        }
        
        composition_df = pd.DataFrame(composition_data)
        st.dataframe(composition_df, hide_index=True)
        
        st.markdown("""
        <div class='card hover-lift'>
            <h3 style='color: #E83E8C; margin-bottom: 0.5rem;'>Distribucion Grafica</h3>
        </div>
        """, unsafe_allow_html=True)
        
        chart_data = pd.DataFrame({
            'Componente': ['Materiales', 'Mano de Obra'],
            'Monto': [total_materials, total_labor]
        })
        st.bar_chart(chart_data.set_index('Componente'))

if __name__ == "__main__":
    main()
