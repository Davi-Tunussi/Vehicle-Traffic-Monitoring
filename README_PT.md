Monitoramento de Veículos em Rodovias

Descrição Geral

Este projeto implementa um sistema para monitoramento de tráfego em rodovias utilizando a biblioteca OpenCV. Ele detecta, rastreia e calcula a velocidade de veículos em regiões de interesse (ROIs) definidas manualmente pelo usuário. O sistema também exibe a velocidade de cada veículo em pixels/frame e km/h.

Estrutura do Projeto

Main.py:

Arquivo principal do código que executa o sistema de monitoramento.

Pasta Data:

Contém o vídeo de entrada para análise (video_rodovia.mp4).

Pasta Output Example:

Inclui um exemplo de saída do sistema em funcionamento (Monitoramento_Rodovia.mp4).

Principais Funcionalidades

Definição de ROIs:

O usuário seleciona regiões de interesse (ROIs) no vídeo manualmente usando o mouse.

Para cada ROI, é definida uma linha de contagem para identificar veículos que atravessam essa linha.

Detecção e Rastreamento de Veículos:

Identifica veículos em movimento utilizando subtração de fundo e transformações morfológicas para reduzir ruídos.

Rastreamento de veículos é realizado com base nos centróides calculados a cada frame.

Cálculo de Velocidade:

Velocidade de cada veículo é calculada em:

Pixels/frame (taxa de deslocamento no vídeo).

Km/h (convertendo para uma unidade real com base no comprimento de cada pixel e a taxa de frames do vídeo).

Visualização:

Exibe a ID do veículo, a velocidade e as regiões de interesse diretamente no vídeo.

Instruções de Execução

Certifique-se de que o vídeo de entrada (video_rodovia.mp4) está localizado na pasta Data.

Substitua o caminho do vídeo na variável cap no arquivo Main.py, caso o vídeo esteja em outro local.

Instale as dependências do projeto:

pip install opencv-python-headless numpy

Execute o script Main.py.

No vídeo exibido:

Desenhe as ROIs clicando e arrastando o mouse.

Pressione 'q' para finalizar a seleção.

Após a seleção das ROIs, o sistema iniciará o monitoramento, exibindo:

Bounding boxes nos veículos detectados.

ID, velocidade (em pixels/frame e km/h) e total de veículos para cada ROI.

Pressione 'q' para encerrar.

Parâmetros Configuráveis

min_area: Área mínima para detectar um contorno como veículo (padrão: 150).

centroid_dist_threshold: Distância máxima entre centróides consecutivos para rastrear um veículo (padrão: 50 pixels).

pixel_length: Comprimento de cada pixel em cm (padrão: 7.2 cm).

frames_per_second: Taxa de quadros do vídeo (padrão: 30 fps).

Exemplo de Saída

Ao executar o script, o vídeo será processado e exibirá informações semelhantes a:

ROI 1: Total: 5
ROI 2: Total: 3
ID: 1, Vel: 12.50 px/frame, 32.40 km/h
ID: 2, Vel: 10.25 px/frame, 26.40 km/h

Observações

Certifique-se de que o vídeo fornecido tenha boa qualidade para uma detecção eficiente.

O sistema foi projetado para rodar em tempo real, mas o desempenho pode variar dependendo da resolução do vídeo e da capacidade de hardware.

Autor

Projeto desenvolvido com o objetivo de monitorar e analisar o tráfego em rodovias, fornecendo dados precisos de contagem e velocidade de veículos.