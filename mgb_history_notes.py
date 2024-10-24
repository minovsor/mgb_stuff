'''
ATUALIZACOES DO MGB

MGB 1.0 
- Interface em Mapwindow GIS
- Inclui fonte de dados de chuva a partir de satélite MERGE-CPTEC

MGB 2.0 (2015)

- Interface completa (pré-processamento e simulação) em MapWindow GIS
- Plugin IPH Hydro-Tools substitui o PrePro
- Interface em Inglês
- Download dos dados da Agência Nacional de Águas (ANA)
- Rotinas do MGB iguais às da versão 2011


MGB 3.0 (2017)
- Inclui todos os recursos para simulação com o modelo de propagação inercial de vazões (Pontes et al., 2015).
- Novas ferramentas para uso de dados de chuva do TRMM e dados climáticos do CRU.



MGB 4.0 (01/04/2018)
- Integrada a versões do QGIS 2.14 e 2.18. No momento, a mesma está em fase de testes.


MGB 4.1 (25/10/2018)
- Atualiza a ferramenta que faz download automático de dados da Agência Nacional de Águas
(ferramenta “ANA Data Acquisition”)
- Altera o formato dos arquivos de entrada de clima diário,
- Incorpora na interface o valor do parâmetro “alpha” (associado à condição de Courant do modelo de propagação inercial)
- Atualiza a rotina de evapotranspiração e corrige alguns bugs internos.

É possível que os valores dos parâmetros calibráveis das versões anteriores do MGB 
tenham que ser modificados para a simulação com o MGB 4.1.


MGB 4.2 (07/10/2019)
- Atualiza a rotina de interpolação de dados de chuva, funcionando para um número maior de minibacias,
- Corrige bugs relacionados a interpolação dos dados climáticos do CRU (Climatic Research Unit)
- Corrige bugs relacionados a geração de escoamento na simulação com modelo inercial.


MGB 4.3 (19/12/2019)
- Interface atualizada para versão mais estável do software QGIS (3.4.14 ‘Madeira’.).
- Pequenas correções foram feitas no arquivo de criação de raster de chuva.
- Pequena alteração na c.c. de jusante do modelo de propagação de escoamento inercial
- Limpeza e organização do código-fonte.
- o IPH HydroTools também passa a funcionar para a versão do QGIS 3.4.14 ‘Madeira’.
- Produzido Manual, em versão, em espanhol


MGB 4.4 (18/07/2020)
- Mudança conceitual do modelo na unidade de resposta hidrológica (URH) tipo água, quando na propagação com o modelo inercial.
-- a área referente a URH tipo água é desconsiderada e distribuída proporcionalmente entre as demais já que a área inundada já é calculada internamente pelo método inercial.
- Atualização na leitura do arquivo cota-área para que exista uma área inundada considerada ainda no leito do rio. 
- Nova versão de código-fonte disponível para ser compilado em Gfortran.
- As demais versões eram exclusivas para Intel Fortran, embora existam meios simples para adaptação.
- Alteração a ordem das colunas do arquivo de leitura de clima diário, sendo agora a mesma das linhas do arquivo de entrada medias.cli
-- 1) Temperatura, 2) Umidade relativa, 3) Horas de Sol (SunHours),  4) Vento (Wind), 5) Pressão Atmosférica (AtmPres).


MGB 4.5 (07/08/2020) 
- Mudança conceitual na interação entre área inundada e solo quando usada a propagação de vazão pelo modelo inercial.
-- incluímos um possibilidade de fluxo de infiltração para o solo da área que está inundada
-- parte do balanço hídrico vertical (precipitação, evaporação e dsup) foi ajustado para considerar a fração inundada na minibacia

MGB 4.5 (02/11/2020) 
- Nova documentação em 4 manuais/apostilas, sendo manual de aplicação, manual de referência teórica, noções de fortran e guia prático do código-fonte.
- Upload de video-aulas no youtube.

MGB 4.6 (08/08/2021)
- Novo visualizador de resultados de balanço hídrico, chamado “MGB Water Balance”.
'''



