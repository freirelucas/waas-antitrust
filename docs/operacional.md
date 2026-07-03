# Operacionalização da LCMC — do modelo formal ao procedimento administrativo

<p class="deck">Passagem do desenho conceitual da LCMC para a operação institucional concreta no horizonte 2024–2027: o que o CADE pode fazer hoje sob a Resolução 21/2018 e a Lei 9.784/1999, que ato administrativo seria necessário para implementar o canal de depósito condicional, quais cláusulas contratuais privadas ficam tensionadas e como o gradiente Saito da R20 dialoga com a dosimetria do Art. 45 da Lei 12.529/2011.</p>

<p class="byline"><em>Anexo direito-institucional</em> · operacionalização · rascunho v0.2.0</p>

<p class="lede">Esta página atende a duas leituras críticas registradas na <a href="/waas-antitrust/revisao_personas/">simulação por personas</a>: a do conselheiro do CADE, que ao ler o <a href="/waas-antitrust/procedimento_cade/">procedimento administrativo</a> sentiu falta da ligação dosimétrica com o Art. 45 e do desenho operacional da Resolução que viabilizaria o canal; e a do compliance officer da Big Tech, que ao ler o <a href="/waas-antitrust/compliance_corporativo/">compliance corporativo</a> sentiu falta de uma resposta jurídica defensiva — quais cláusulas contratuais ficam afetadas e como reagir. Sem prejuízo do caveat substantivo de que esta é leitura acadêmica especulativa, não aconselhamento jurídico.</p>

## Camada institucional — o que o CADE pode fazer sem nova lei

A LCMC é implementável por **ato infralegal do CADE** sob duas bases normativas autônomas, em duas configurações distintas.

### Configuração mínima (canal puro)

A versão mais conservadora — o canal de depósito condicional **sem qualquer instrumento monetário acoplado** — tem base normativa autônoma na conjugação:

- **Art. 4º, II e III, da Lei nº 12.529/2011** — atribuições do CADE de "decidir sobre a existência de infração à ordem econômica e aplicar as penalidades previstas em lei" e "decidir os processos administrativos para imposição de sanções administrativas por infrações à ordem econômica instaurados pela Superintendência-Geral".
- **Lei nº 9.784/1999** — processo administrativo federal, em particular o Art. 24 sobre o dever de zelar pelo sigilo da informação obtida em fase pré-instaurada e a Art. 27 sobre forma do ato administrativo.

A leitura: o CADE tem competência para **regulamentar como recebe denúncias qualificadas** sem precisar de lei nova. Disciplinar o procedimento de recepção qualificada (depósito condicional, prazo, sigilo, abertura simultânea) é matéria que cabe em Resolução. O risco principal é F6 (anulação judicial por construção excessivamente finalística), mas o risco do canal puro é materialmente menor que o do acoplamento monetário, porque o canal não cria nova categoria de pagamento — apenas estrutura como o CADE recebe informação.

### Configuração com recompensa via TCC (Regime B)

Quando se acopla a recompensa via TCC (o instrumento *Whistleblower-as-a-Service*), a base normativa precisa adicionalmente do **Art. 12 da Resolução CADE nº 21/2018**, que autoriza considerar como circunstância atenuante, no cálculo da contribuição pecuniária do TCC, o ressarcimento extrajudicial ou judicial das vítimas (Art. 45, V e VI da Lei nº 12.529/2011).

A construção que sustenta a LCMC sob o Art. 12 é a **re-caracterização do pagamento ao denunciante interno como ressarcimento de vítima coletiva**. É construção controvertida. A jurisprudência sobre o Art. 12 tem, até hoje, tratado vítimas como categoria coletiva (consumidores, concorrentes, erário). O denunciante interno é, dogmaticamente, **testemunha qualificada** — não a coletividade lesada. Re-caracterizar o pagamento exige construção finalística que o Judiciário pode rejeitar em sede de controle. Esse é o falsificador conhecido como F6 do desenho, calibrado no modelo pelo parâmetro `p_anulacao_tcc`.

## Anatomia do ato administrativo proposto

Sob a configuração mínima (canal puro), o ato administrativo que viabilizaria a LCMC tem cinco componentes mínimos.

| Componente | Conteúdo regulatório | Base normativa |
|---|---|---|
| Definição do canal | O CADE recebe denúncia qualificada com cláusula de abertura condicional sob *escrow*. | Art. 4º II/III Lei 12.529; Art. 27 Lei 9.784 |
| Gatilho de massa crítica | Define `q_min` como fração mínima de cooperadores intra-firma para abertura simultânea. | Discricionariedade regulatória |
| Sigilo durante o *escrow* | Identidade do depositante e conteúdo da denúncia permanecem sob sigilo até o gatilho. | Art. 24 Lei 9.784; Art. 5º X CF/88 |
| Procedimento de abertura | Quando o gatilho dispara, instauração de Procedimento Preparatório de Inquérito Administrativo (PPIA) ou Inquérito Administrativo, conforme o caso. | Regimento Interno do CADE |
| Trânsito com a SG | Encaminhamento à Superintendência-Geral para instrução; CGAA atua na fase pré-instaurada quando a denúncia for de conduta digital qualificada. | Regimento Interno do CADE |

Nenhum dos cinco componentes exige inovação legislativa — todos são exercícios de competência regulatória já reconhecida. A questão jurídica residual está na **interação com a Resolução 21/2018** caso o ato proposto contemple acoplamento da recompensa via TCC.

## Compatibilidade com a dosimetria do Art. 45

A pergunta substantiva é se o gradiente Saito (2021) — que descreve, empiricamente, os descontos médios concedidos pela SG em TCCs de leniência clássica para a 1ª (43,43 %), 2ª (34,51 %), 3ª (20,22 %) e ≥ 9ª (15 %, piso) firmas na fila — é compatível com os critérios de dosimetria do **Art. 45 da Lei nº 12.529/2011**.

O Art. 45 lista oito incisos sobre fixação da pena: I. gravidade da infração; II. boa-fé do infrator; III. vantagem auferida; IV. consumação ou não; V. grau de lesão; VI. efeitos econômicos negativos; VII. situação econômica do infrator; VIII. reincidência. O gradiente Saito reflete a aplicação prática desses critérios pela SG em casos concretos — e portanto **não é alternativa ao Art. 45, é a calibração empírica do Art. 45 sob a leniência clássica**.

Sob a LCMC, o mesmo gradiente é aplicado em duas dimensões novas:

- **Inter-firma (R20):** firmas distintas que correm para o canal recebem desconto decrescente pela mesma lógica Art. 45 já praticada — exatamente como na leniência clássica do Art. 86. Não há novidade dosimétrica.
- **Intra-firma pós-abertura (R29):** trabalhadores que aderem em janela pós-abertura recebem desconto progressivo. Esta é a única extensão genuinamente nova, e o gradiente normativo (calibração contra Saito) está formalizado em `cascata_adesao_saito_calibrada` — não é arbitrário.

A Coordenação de Dosimetria do CADE, por essa leitura, não precisa endossar nova teoria; precisa endossar a **extensão de uma calibração empírica que já pratica para o domínio intra-firma**.

## Cláusulas contratuais privadas tensionadas

Esta seção atende a leitura do compliance officer da Big Tech. Sob LCMC operante, cinco categorias de cláusula contratual padrão ficam tensionadas — não necessariamente inválidas, mas com risco de ineficácia jurídica em sede de controle.

### Cláusulas de não-disparagement (*anti-disparagement clauses*)

Cláusulas que proíbem o ex-funcionário de fazer declarações desabonadoras à empresa após o desligamento. Em interação com o canal LCMC, ficam expostas ao argumento de que **violam o direito de petição e de acesso à autoridade pública** (Art. 5º XXXIV CF/88) e a proteção horizontal do denunciante de boa-fé na Lei nº 13.608/2018 (com a redação da Lei nº 13.964/2019). O CADE, em interpretação da SG, já considerou inválidas cláusulas que impedem trabalhadores de cooperarem com autoridades antitruste. A LCMC potencializa esse efeito porque a denúncia condicional é, por construção, ato de cooperação com autoridade pública.

### Acordos de confidencialidade abrangentes (NDAs)

NDAs que cobrem informação sobre conduta potencialmente anticompetitiva têm tensão estrutural com a **exceção de denúncia a autoridade pública** reconhecida tanto na Diretiva (UE) 2019/1937 (Art. 21, parágrafo 7) quanto, em construção brasileira, na conjugação Art. 5º XXXIII e XXXIV da CF/88 com a Lei nº 13.608/2018. NDAs sobre conduta anticompetitiva tendem a ser inválidos no que tange à barreira ao canal de denúncia legítimo — independentemente da LCMC. O que muda com a LCMC é o **volume esperado** de testes desse argumento em sede de controle.

### Cláusulas de arbitragem obrigatória sobre direito trabalhista

Cláusulas que submetem demandas trabalhistas a arbitragem privada têm restrição clara no Brasil (Súmula 277 TST, alterada em 2012; jurisprudência consolidada do TST). Mas sob LCMC, a discussão muda de patamar quando a represália por denúncia é alegada: o trabalhador que sofre demissão por ter depositado denúncia condicional invoca proteção do Art. 5º XXXIV CF/88 e da Lei nº 13.608/2018, e a competência para julgar essa pretensão é da Justiça do Trabalho. **Arbitragem privada sobre represália em LCMC é potencialmente inválida**.

### Cláusulas de aceleração de vesting condicionadas a "boa saída"

A camada Hirschman do desenho (vesting acelerado por gatilho de ação coletiva) só é viável em Regime C — exigem lei nova, por reserva contratual padrão (Art. 22 I CF/88). Mas em sentido inverso: **cláusulas que retardam vesting ou permitem clawback em caso de denúncia** são juridicamente frágeis sob o desenho LCMC pelo mesmo argumento das cláusulas de não-disparagement. Compliance corporativo prudente revisa essas cláusulas em antecipação.

### Cláusulas de garantia de mediação interna prévia

Cláusulas que exigem do trabalhador esgotar o canal interno de compliance antes de denunciar externamente. Sob a Diretiva (UE) 2019/1937, há proteção da denúncia direta a autoridade pública mesmo sem prévio acionamento de canal interno (Art. 7º). No Brasil, a construção análoga decorre da Lei nº 13.608/2018 c/c Art. 5º XXXIV CF/88. **Cláusulas que condicionam a denúncia externa ao prévio esgotamento interno são juridicamente frágeis** quando aplicadas a conduta anticompetitiva — e a LCMC torna essa fragilidade testável em volume.

## Onde a operacionalização ainda tem incerteza substantiva

O quadro acima não fecha o desenho operacional. Três pontos seguem em aberto:

1. **Fluxo Resolução nova vs Res. 21/2018 vigente.** A LCMC pode entrar como Resolução autônoma específica ou como alteração da 21/2018. A escolha tem implicações sobre o controle judicial (Resolução autônoma é mais fácil de defender; alteração da 21/2018 tem o ônus adicional de demonstrar coerência com a interpretação consolidada do Art. 12).
2. **Papel da CGAA na fase pré-instaurada.** Como a Coordenação-Geral de Análise Antitruste interage com o *escrow*: ela tem acesso aos depósitos pendentes? Apenas estatística agregada? Apenas após abertura? Cada escolha tem impacto sobre a percepção de garantia de sigilo pelo depositante.
3. **Integração com leniência clássica do Art. 86.** O cenário em que a firma sob LCMC opta por buscar acordo de leniência clássica (Art. 86) na mesma conduta gera concorrência de instrumentos. O modelo trata como ambiguidade no falsificador F7; resolução institucional fica pendente.

Esses três pontos viram itens explícitos no [brainstorm de revisão](brainstorm_revisao.md) e são candidatos a aprofundamento em rodadas subsequentes do trabalho.