import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl

umidade = ctrl.Antecedent(np.arange(0, 101, 1), 'Umidade Relativa do ar (%)')
precipitacao = ctrl.Antecedent(np.arange(0, 21, 1), 'Precipitacao(mm)')
VFR = ctrl.Consequent(np.arange(-40, 16, 1), 'Variacao de Fator de Risco (VFR)')

umidade['muito baixa'] = fuzz.trimf(umidade.universe, [-1000, 20, 30])
umidade['baixa'] = fuzz.trimf(umidade.universe, [20, 37, 50])
umidade['média'] = fuzz.trimf(umidade.universe, [50, 55, 60])
umidade['alta'] = fuzz.trimf(umidade.universe, [60, 70, 80])
umidade['muito alta'] = fuzz.trimf(umidade.universe, [75, 85, 1000])
umidade.view()

precipitacao['muito baixa'] = fuzz.trimf(precipitacao.universe, [-1000, 2, 3])
precipitacao['baixa'] = fuzz.trimf(precipitacao.universe, [1, 4, 6])
precipitacao['média'] = fuzz.trimf(precipitacao.universe, [5, 7, 11])
precipitacao['alta'] = fuzz.trimf(precipitacao.universe, [9, 12, 14])
precipitacao['muito alta'] = fuzz.trimf(precipitacao.universe, [12, 14, 1000])
precipitacao.view()

VFR['alto negativo'] = fuzz.trimf(VFR.universe, [-1000, -35, -20])
VFR['médio negativo'] = fuzz.trimf(VFR.universe, [-30, -20, -10])
VFR['baixo negativo'] = fuzz.trimf(VFR.universe, [-15, 1, 3])
VFR['baixo positivo'] = fuzz.trimf(VFR.universe, [-1, 0, 1])
VFR['médio positivo'] = fuzz.trimf(VFR.universe, [2, 5, 7])
VFR['alto positivo'] = fuzz.trimf(VFR.universe, [5, 7, 1000])
VFR.view()

regra1 = ctrl.Rule(umidade['muito baixa'] & precipitacao['muito baixa'], VFR['alto positivo'])
regra2 = ctrl.Rule(umidade['baixa'] & precipitacao['média'], VFR['médio positivo'])
regra3 = ctrl.Rule(umidade['média'] & precipitacao['média'], VFR['baixo positivo'])
regra4 = ctrl.Rule(umidade['baixa'] & precipitacao['muito alta'], VFR['médio negativo'])
regra5 = ctrl.Rule(umidade['alta'] & precipitacao['muito alta'], VFR['alto negativo'])
regra6 = ctrl.Rule(umidade['muito alta'] & precipitacao['baixa'], VFR['baixo negativo'])
regra7 = ctrl.Rule(umidade['muito baixa'] & precipitacao['baixa'], VFR['alto positivo'])
regra8 = ctrl.Rule(umidade['muito baixa'] & precipitacao['média'], VFR['médio positivo'])
regra9 = ctrl.Rule(umidade['muito baixa'] & precipitacao['alta'], VFR['médio negativo'])
regra10 = ctrl.Rule(umidade['baixa'] & precipitacao['muito baixa'], VFR['alto positivo'])
regra11 = ctrl.Rule(umidade['baixa'] & precipitacao['baixa'], VFR['médio positivo'])
regra12 = ctrl.Rule(umidade['baixa'] & precipitacao['alta'], VFR['alto negativo'])
regra13 = ctrl.Rule(umidade['média'] & precipitacao['muito baixa'], VFR['médio positivo'])
regra14 = ctrl.Rule(umidade['média'] & precipitacao['baixa'], VFR['médio positivo'])
regra15 = ctrl.Rule(umidade['média'] & precipitacao['alta'], VFR['médio negativo'])
regra16 = ctrl.Rule(umidade['média'] & precipitacao['muito alta'], VFR['alto negativo'])
regra17 = ctrl.Rule(umidade['alta'] & precipitacao['muito baixa'], VFR['alto positivo'])
regra18 = ctrl.Rule(umidade['alta'] & precipitacao['baixa'], VFR['baixo positivo'])
regra19 = ctrl.Rule(umidade['alta'] & precipitacao['média'], VFR['médio positivo'])
regra20 = ctrl.Rule(umidade['alta'] & precipitacao['alta'], VFR['alto positivo'])
regra21 = ctrl.Rule(umidade['muito alta'] & precipitacao['muito baixa'], VFR['baixo negativo'])
regra22 = ctrl.Rule(umidade['muito alta'] & precipitacao['média'], VFR['médio negativo'])
regra23 = ctrl.Rule(umidade['muito alta'] & precipitacao['muito alta'], VFR['alto negativo'])

risco_queimadas = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9, regra10, regra11, regra12, regra13, regra14, regra15, regra16, regra17, regra18, regra19, regra20, regra21, regra22, regra23])
risco_queimadas = ctrl.ControlSystemSimulation(risco_queimadas)

risco_queimadas.input['Umidade Relativa do ar (%)'] = 52
risco_queimadas.input['Precipitacao(mm)'] = 3
risco_queimadas.compute()
print(risco_queimadas.output['Variacao de Fator de Risco (VFR)'])
VFR.view(sim=risco_queimadas)
