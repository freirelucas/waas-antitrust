# Glossário

Termos usados no projeto, em uma linha cada.

| Termo | Significado |
|-------|-------------|
| **Antitruste** | Área do direito que combate abusos de poder de mercado (cartéis, monopólios, condutas que prejudicam a concorrência). |
| **CADE** | Conselho Administrativo de Defesa Econômica — a autoridade antitruste brasileira. |
| **Leniência** | Acordo em que quem confessa e colabora com a investigação ganha imunidade ou redução de pena. |
| **Cartel** | Combinação entre empresas concorrentes (preços, divisão de mercado). É *coordenada* — por isso a leniência clássica funciona. |
| **Conduta unilateral** | Abuso cometido por **uma única** empresa dominante, sozinha — sem cúmplice para delatar. |
| **Denunciante interno** (*whistleblower*) | Funcionário que reporta uma infração cometida pela própria empresa. |
| **WaaS** (*Whistleblower-as-a-Service*) | O mecanismo proposto: recompensar o denunciante interno, com a recompensa abatida da multa via desconto. |
| **TCC** | Termo de Compromisso de Cessação — acordo em que a empresa para a conduta e paga uma contribuição, com possível desconto. |
| **Recompensa ($W$)** | Valor pago aos denunciantes internos. |
| **Desconto ($D$)** | Redução na contribuição do TCC concedida à empresa que colabora/ressarce. |
| **IC-F\*** | A condição $D > W$: o desconto supera a recompensa, tornando a colaboração vantajosa para a empresa. |
| **Dissuasão** | Efeito de desencorajar a infração: se a chance de ser pego sobe, menos empresas violam. |
| **Regimes A / B / C** | Cenários: A = hoje (sem WaaS); B = WaaS por resolução do CADE; C = WaaS por lei. |
| **Massa crítica ($k$)** | Número mínimo de denunciantes para disparar a investigação. |
| **Jogo global** | Modelo (Morris–Shin, 1998) em que cada pessoa decide com informação privada e ruidosa; seleciona um equilíbrio **único**. |
| **Contágio complexo** | Difusão (Centola–Macy) que exige reforço de vários vizinhos — não se espalha por um contato só. |
| **ABM / MBA** | *Agent-based model* / modelo baseado em agentes: simula indivíduos heterogêneos interagindo. |
| **Sobol** | Método de análise de sensibilidade: mede quanto cada parâmetro contribui para a variação do resultado. |
| **Dano (acumulado)** | Proxy de prejuízo social: soma das empresas violando ao longo do tempo (quanto menor, melhor). |
| **ODD** | Protocolo padrão (Grimm et al.) para descrever modelos baseados em agentes. |
| **Hirschman exit-with-equity** | Saída coletiva crível com vesting acelerado: funcionários "ameaçam ir embora juntos" e a cláusula contratual transfere parte do equity *non-vested* — preserva valor em vez de derretê-lo (R07). |
| **Vesting** | Esquema em que ações/opções do empregado são conquistadas ao longo do tempo (padrão YC: 4 anos com *cliff* de 1 ano). |
| **Cláusula acelerada** | Cláusula que antecipa o vesting em eventos específicos (aqui: gatilho de ação coletiva). |
| **Self-preferencing** | Auto-preferência: plataforma destaca/prioriza seus próprios produtos em busca ou marketplace. |
| **Tying / bundling** | Vinculação: obrigar a compra conjunta de produtos que poderiam ser separados. |
| **Predatory pricing** | Preços abaixo do custo para excluir concorrente; depois recupera com poder de mercado. |
| **Killer acquisition** | Aquisição de concorrente nascente para neutralizá-lo (Meta–Instagram, Meta–WhatsApp). |
| **Dark patterns** | Design de interface que dificulta saída ou induz consentimento via fricção assimétrica. |
| **MFN / paridade** | Cláusula obrigando vendedor a não cobrar menos em outros canais (Booking, Amazon). |
| **Exclusividade / retaliação em marketplace** | Exigência de exclusividade contratual a sellers ou retaliação contra quem também opera em concorrentes (iFood TCC 2023; indícios contra Mercado Livre 2024-2025). |
| **Anti-steering / IAP** | Em plataformas móveis (iOS, Android), bloqueio de informação ou redirecionamento de pagamento fora do *in-app purchase* do operador da plataforma (Apple Brasil — CADE dez/2025; Epic v. Apple, EUA 2021). |
| **Ator crítico interno** | Papel dentro da firma que mais frequentemente sabe da conduta e teria incentivo a denunciá-la via WaaS (engenharia, produto, design, corp dev, jurídico, **operações**, **financeiro**…). |
| **Ator adjacente** | Papel que não executa a conduta mas vê seu efeito imediato (métricas, decisões, P&L). No catálogo R08 ganha observabilidade intermediária (0,5) entre o primário (1,0) e o distal (0,1). |
| **MARKETPLACE_BR / BIGTECH_MADURA** | Presets da distribuição de papéis dentro da firma. `BIGTECH_MADURA` é eng-heavy (Google/Meta-like); `MARKETPLACE_BR` é operations-heavy (iFood/Mercado Livre-like). Calibração formal contra organogramas pendente (E05). |
| **Capital social organizacional** | Bem coletivo produzido como subproduto de relações de obrigação entre pessoas que se conhecem (Coleman 1990, *Foundations of Social Theory* cap. 12). Sob o reframe v2, a massa crítica de cooperação interna é capital social, não bem quase-público à Samuelson. |
| **Erosão por uso instrumental** | Hipótese Coleman 1990: instrumentalizar capital social (premiar denúncia em moeda regulatória) pode **destruir** o substrato de confiança horizontal que o produz. Operacionalizada no modelo via `alpha_erosao` (R26); falsificável por Proposição 5 candidata. |
| **Bem quase-público (Samuelson 1954)** | Bem com rivalidade parcial no consumo e excluibilidade parcial. Leitura econômica clássica da massa crítica — mantida como ponte didática, mas a categoria primária correta é **capital social Coleman**. |
| **Anti-commons (Heller 1998)** | Tragédia reversa: direitos de exclusão fragmentados levando à subutilização. Categoria correta para o vetor "sobre-denúncia frívola" do WaaS. |
| **Interesse público em detecção e cessação** | Categoria dogmática (Lei 9.784/99 Art. 2º) que substitui no reframe v2 a leitura constitutiva "atenuante por bem público". Sustenta a re-caracterização sob Art. 12 sem criar categoria nova. |
| **LAC Art. 7º VII-VIII (Lei 12.846/2013)** | Precedente brasileiro principal do reframe: a Lei Anticorrupção já trata mecanismos de detecção interna como bem juridicamente relevante na dosimetria. Análoga aplicável ao antitruste. |
| **Cₜ / Cᵩ / Cₚ (sub-regimes de C)** | Decomposição do Regime C por reserva constitucional: Cₜ (trabalhista, Art. 22 I — vesting Hirschman); Cᵩ (tributária, Art. 146 LC + LRF — crédito tributário); Cₚ (penal estrita, Art. 5º XXXIX — leniência criminal individual). |
| **Oportunista (arquétipo R24)** | Sexto arquétipo de `TrabalhadorAgent` (após ético, imitativo, racional, aleatório, fairminded). Utilidade puramente extrativa: `W_efetivo - prob_falso · sanção_calúnia`. Captura uso adversarial do WaaS (insider acionista, concorrente, chantagem, hedge fund ativista). |
| **Dissuasão erga omnes** | Externalidade positiva massiva do WaaS: dissuade não apenas a firma alvo de notificação, mas também firmas que CADE/MPF jamais investigariam. Operacionalizada via `valor_dissuasao_difusa_acum` (Eco B v2). |
| **Sinal Schelling / canal de conhecimento comum** | Mecanismo pelo qual `p_perc` (detecção percebida) sobe globalmente quando uma firma é notificada — todas as outras firmas re-calculam suas crenças. Acoplamento inter-firma sem grafo explícito. |
| **Limiar por posição (LCMC)** | Sob `modo_corrida=True`, o limiar Morris-Shin $x^\star$ vira família $\{x^\star_k\}$ — cada posição na fila intra-firma tem seu próprio limiar; oferta do bem coletivo é escalonada (Mat A v2). |
| **Canal de depósito condicional** (*information escrow*) | Mecanismo central da LCMC v3: o CADE recebe denúncias com cláusula de abertura condicional e as mantém em escrow até massa crítica intra-firma. Ayres-Unkovic 2012 (*Michigan L. Rev.* 111:145); análogo prático Callisto. Parâmetros no código: `usar_escrow_explicito`, `janela_escrow_tiques` (Δt). Forma canônica e sinônimos listados em [`TERMINOLOGIA.md`](TERMINOLOGIA.md). |
| **Abertura simultânea (all-or-nothing)** | Propriedade de desenho do canal: quando massa crítica é atingida em uma firma, N depósitos colapsam em um caso processual único (qualidade da prova = média; identidades preservadas até instauração). Ninguém foi "o primeiro" individualmente — análogo Kickstarter. Implementação: `AutoridadeAgent.abrir_escrow_se_massa_critica`. |
