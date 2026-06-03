# Bibliografia primária

> **Convenção.** Cada referência abaixo foi verificada via DOI/arXiv/URL estável,
> exceto quando explicitamente marcada com **[?]** (verificação não conclusiva
> nesta sessão — citação a confirmar antes da publicação).

## Teoria dos jogos e desenho de mecanismos

- Aubert, C., Rey, P., & Kovacic, W. E. (2006). The impact of leniency and whistle-blowing programs on cartels. *International Journal of Industrial Organization* 24(6): 1241–1266. DOI: 10.1016/j.ijindorg.2006.04.002
- Bigoni, M., Fridolfsson, S.-O., Le Coq, C., & Spagnolo, G. (2012). Fines, leniency, and rewards in antitrust. *RAND Journal of Economics* 43(2): 368–390. DOI: 10.1111/j.1756-2171.2012.00170.x
- Chen, Z., & Rey, P. (2013). On the design of leniency programs. *Journal of Law and Economics* 56(4): 917–957.
- Harrington, J. E., & Chang, M.-H. (2009). Modeling the birth and death of cartels with an application to evaluating competition policy. *Journal of the European Economic Association* 7(6): 1400–1435. DOI: 10.1162/JEEA.2009.7.6.1400
- Harrington, J. E., & Chang, M.-H. (2015). When can we expect a corporate leniency program to result in fewer cartels? *Journal of Law and Economics* 58(2): 417–449. DOI: 10.1086/684041
- Motta, M., & Polo, M. (2003). Leniency programs and cartel prosecution. *International Journal of Industrial Organization* 21(3): 347–379. DOI: 10.1016/S0167-7187(02)00057-7
- Morris, S., & Shin, H. S. (1998). Unique equilibrium in a model of self-fulfilling currency attacks. *American Economic Review* 88(3): 587–597.
- Apesteguia, J., Dufwenberg, M., & Selten, R. (2007). Blowing the whistle. *Economic Theory* 31(1): 143–166. DOI: 10.1007/s00199-006-0092-8
- Polinsky, A. M., & Shavell, S. (2000). The economic theory of public enforcement of law. *Journal of Economic Literature* 38(1): 45–76. DOI: 10.1257/jel.38.1.45
- Spagnolo, G. (2004). Divide et impera: Optimal leniency programs. *CEPR Discussion Paper* 4840. <https://cepr.org/publications/dp4840>

## Empírica de denúncia interna

- Dyck, A., Morse, A., & Zingales, L. (2010). Who blows the whistle on corporate fraud? *Journal of Finance* 65(6): 2213–2253. DOI: 10.1111/j.1540-6261.2010.01614.x
- Call, A. C., Martin, G. S., Sharp, N. Y., & Wilde, J. H. (2018). Whistleblowers and outcomes of financial misrepresentation enforcement actions. *Journal of Accounting Research* 56(1): 123–171. DOI: 10.1111/1475-679X.12177
- Stubben, S., & Welch, K. (2020). Evidence on the use and efficacy of internal whistleblowing systems. *Journal of Accounting Research* 58(2): 473–518. DOI: 10.1111/1475-679X.12303
- Wiedman, C. I., & Zhu, C. (2023). The deterrent effect of the SEC Whistleblower Program on financial reporting securities violations. *Contemporary Accounting Research* 40(4): 2711–2744. DOI: 10.1111/1911-3846.12884

## Contágio social e jogos globais

- Centola, D., & Macy, M. (2007). Complex contagions and the weakness of long ties. *American Journal of Sociology* 113(3): 702–734.
- Chwe, M. S.-Y. (2001). *Rational Ritual: Culture, Coordination, and Common Knowledge*. Princeton University Press.
- Granovetter, M. (1978). Threshold models of collective behavior. *American Journal of Sociology* 83(6): 1420–1443.
- Near, J. P., & Miceli, M. P. (1985). Organizational dissidence: The case of whistle-blowing. *Journal of Business Ethics* 4(1): 1–16. — *base do gradiente 3-níveis primário/adjacente/distal em R08.*

## Inequity aversion e evolução de preferências (base de R16)

- Fehr, E., & Schmidt, K. M. (1999). A theory of fairness, competition, and cooperation. *Quarterly Journal of Economics* 114(3): 817–868. DOI: 10.1162/003355399556151 — *modelo seminal de inequity aversion; base da utilidade `u_i = π_i − α·|π_i − π_j|` adotada pelo arquétipo fairminded.*
- Bolton, G. E., & Ockenfels, A. (2000). ERC: A theory of equity, reciprocity, and competition. *American Economic Review* 90(1): 166–193. DOI: 10.1257/aer.90.1.166 — *modelo alternativo (não-aditivo) de fairness preferences; comparação canônica com Fehr-Schmidt.*
- Güth, W., & Yaari, M. (1992). Explaining reciprocal behavior in simple strategic games: An evolutionary approach. Em U. Witt (ed.), *Explaining process and change*. University of Michigan Press. — *abordagem evolutiva indireta: dual payoff structure (utilidade subjetiva × payoff material).*
- Skyrms, B. (1996). *Evolution of the Social Contract*. Cambridge University Press. — *evolução de equilíbrios igualitários no jogo de demanda de Nash sob dinâmica replicador.*
- Huck, S., & Oechssler, J. (1999). The indirect evolutionary approach to explaining fair allocations. *Games and Economic Behavior* 28(1): 13–24. DOI: 10.1006/game.1998.0691
- Nowak, M. A., Page, K. M., & Sigmund, K. (2000). Fairness versus reason in the ultimatum game. *Science* 289(5485): 1773–1775. DOI: 10.1126/science.289.5485.1773
- Henrich, J., Boyd, R., Bowles, S., Camerer, C., Fehr, E., Gintis, H., & McElreath, R. (2001). In search of Homo Economicus: Behavioral experiments in 15 small-scale societies. *American Economic Review* 91(2): 73–78. DOI: 10.1257/aer.91.2.73
- **Torsell, C. (2026). Egalitarianism and evolution. *Theory and Decision*. DOI: 10.1007/s11238-026-10127-6** — *resultado central que motiva R16: aversão à inequidade prolifera em populações HE+FM sob qualquer dinâmica payoff-monotone, com aprendizado intra-geracional via fictitious play. O agente fairminded no `agents.py` é a adaptação direta da utilidade Fehr-Schmidt para o contexto WaaS.*
- Fudenberg, D., & Levine, D. (1998). *The Theory of Learning in Games*. MIT Press. — *fictitious play e aprendizado intra-geracional como motor dinâmico.*
- Camerer, C., & Hua Ho, T. (1999). Experience-weighted attraction learning in normal form games. *Econometrica* 67(4): 827–874. DOI: 10.1111/1468-0262.00054

## Modelagem baseada em agentes (foundational)

- Grimm, V. et al. (2020). The ODD protocol for describing agent-based and other simulation models: A second update. *JASSS* 23(2): 7.
- Hokamp, S., & Pickhardt, M. (2010). Income tax evasion in a society of heterogeneous agents. *International Economic Journal* 24(4): 541–553. DOI: 10.1080/10168737.2010.525994
- Tesfatsion, L., & Judd, K. L. (eds.) (2006). *Handbook of Computational Economics, Vol. 2: Agent-Based Computational Economics*. North-Holland. <https://faculty.sites.iastate.edu/tesfatsi/archive/tesfatsi/hbace.htm>
- Farmer, J. D., & Foley, D. (2009). The economy needs agent-based modelling. *Nature* 460(7256): 685–686. DOI: 10.1038/460685a
- LeBaron, B. (2006). Agent-based computational finance. Em Tesfatsion & Judd (eds.), *Handbook of Computational Economics, Vol. 2*, cap. 24.
- Wilensky, U., & Rand, W. (2015). *An Introduction to Agent-Based Modeling: Modeling Natural, Social, and Engineered Complex Systems with NetLogo*. MIT Press.
- Dawid, H., Gemkow, S., Harting, P., van der Hoog, S., & Neugart, M. (2018). Agent-based macroeconomic modeling and policy analysis: The Eurace@Unibi model. Em Chen, Kaboudan & Du (eds.), *Oxford Handbook of Computational Economics and Finance*. SSRN: <https://ssrn.com/abstract=2408969>

## Mercados digitais, plataformas e colusão algorítmica

- Rochet, J.-C., & Tirole, J. (2003). Platform competition in two-sided markets. *Journal of the European Economic Association* 1(4): 990–1029. DOI: 10.1162/154247603322493212
- Calvano, E., Calzolari, G., Denicolò, V., & Pastorello, S. (2020). Artificial intelligence, algorithmic pricing, and collusion. *American Economic Review* 110(10): 3267–3297. DOI: 10.1257/aer.20190623 — dois agentes Q-learning convergem a preços supracompetitivos sem comunicação.
- Calvano, E., Calzolari, G., Denicolò, V., & Pastorello, S. (2021). Algorithmic collusion with imperfect monitoring. *International Journal of Industrial Organization* 79: 102712. DOI: 10.1016/j.ijindorg.2021.102712
- Klein, T. (2021). Autonomous algorithmic collusion: Q-learning under sequential pricing. *RAND Journal of Economics* 52(3): 538–558. DOI: 10.1111/1756-2171.12383
- Ezrachi, A., & Stucke, M. E. (2016). *Virtual Competition: The Promise and Perils of the Algorithm-Driven Economy*. Harvard University Press.
- Cunningham, C., Ederer, F., & Ma, S. (2021). Killer acquisitions. *Journal of Political Economy* 129(3): 649–702. DOI: 10.1086/712506
- Caffarra, C., Crawford, G., & Valletti, T. (2020). "How tech rolls": Potential competition and "reverse" killer acquisitions. *VoxEU/CEPR*, maio 2020. <https://cepr.org/voxeu/blogs-and-reviews/how-tech-rolls-potential-competition-and-reverse-killer-acquisitions>
- Crémer, J., de Montjoye, Y.-A., & Schweitzer, H. (2019). *Competition Policy for the Digital Era*. European Commission. <https://op.europa.eu/en/publication-detail/-/publication/21dc175c-7b76-11e9-9f05-01aa75ed71a1>
- Mathur, A., Acar, G., Friedman, M. J., Lucherini, E., Mayer, J., Chetty, M., & Narayanan, A. (2019). Dark patterns at scale: Findings from a crawl of 11K shopping websites. *Proceedings of the ACM on Human-Computer Interaction* 3(CSCW): art. 81. DOI: 10.1145/3359183 · arXiv: 1907.07032

## Cibernética organizacional

- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Conant, R. C., & Ashby, W. R. (1970). Every good regulator of a system must be a model of that system. *International Journal of Systems Science* 1(2): 89–97.

## Fontes brasileiras e contexto institucional

### Lei e norma regulamentar
- Lei 12.529/2011 (arts. 85 a 87).
- Lei 13.608/2018, com redação dada pela Lei 13.964/2019 (arts. 4º-A, 4º-B, 4º-C).
- Resolução CADE nº 21/2018, em especial o art. 12.
- Câmara dos Deputados. PL 2768/2022 — regulação econômica concorrencial de plataformas digitais. <https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=2337417> — análogo nacional ao DMA europeu.

### CADE/DEE e outras fontes técnicas
- Saito, P. (2021). *Termo de Compromisso de Cessação na Lei nº 12.529/11*. CADE/PNUD.
- CADE, DEE, *Documento de Trabalho 003/2022 — Aprendizado de máquina e antitruste*. <https://cdn.cade.gov.br/Portal/centrais-de-conteudo/publicacoes/estudos-economicos/documentos-de-trabalho/2022/DOC_003-2022_Aprendizado-de-maquina-e-antitruste.pdf>
- CADE, DEE, *Documento de Trabalho 001/2024 — Benefícios de atuação do Cade em 2023*.
- Castro, R. M., Mundim, F. N., & Resende, G. M. (2022). *DEE/CADE — 10 anos da Lei 12.529/2011*. **[?]** RePEc: `atg/wpaper/2022060` (conferir publicação no portal CADE antes de citar verbatim).
- IPEA, Centro de Pesquisa em Ciência, Tecnologia e Sociedade. *Reflexões sobre o PL 2.768/2022* (2024). <https://www.ipea.gov.br/cts/pt/central-de-conteudo/artigos/artigos/376-regulacao-de-mercados-mediados-por-plataformas-digitais-no-brasil>
- Brasscom, *Monitor de Empregos e Salários* (09/04/2024).
- Brasscom, *Relatório Setorial 2024* (julho de 2025).

### Roquete e antitruste 3.0
- Roquete, F. L. V. — Superintendente-Adjunto do CADE (Coordenador-Geral de Análise Antitruste, SG/CADE); doutorando em Direito da Regulação (FGV Direito Rio). <https://direitorio.fgv.br/convidado/felipe-leitao-valadares-roquete>; conferência *Computational Antitrust: Exploring Antitrust 3.0* (Stanford, 15/12/2021) <https://conferences.law.stanford.edu/computational-antitrust-exploring-antitrust/speakers/felipe-roquete/>; coluna *Fronteiras Concorrência e Regulação* no JOTA <https://www.jota.info/autor/felipe-roquete>. **[?]** Atribuição direta de "Antitruste assimétrico em mercados digitais" (JOTA, 08/10/2021) requer verificação manual antes de citação verbatim. **D04** (`DECISIONS.md`) registra a possibilidade de co-autoria.

## §4 · Lacunas que o WaaS aborda (síntese pós-pesquisa)

A literatura ABM cobre (i) **leniência clássica entre cúmplices de cartel**
(Spagnolo; Motta-Polo; Harrington-Chang) e (ii) **denúncia interna em fraude
financeira** (Dyck-Morse-Zingales; Hokamp-Pickhardt; Stubben-Welch;
Wiedman-Zhu). A literatura sobre **colusão algorítmica** (Calvano et al.;
Klein) é oligopólio Bertrand sem agentes humanos; a literatura sobre
**plataformas digitais** (Rochet-Tirole; Crémer et al.; Cunningham-Ederer-Ma)
é majoritariamente reduzida a forma fechada ou empírica. O projeto WaaS é
distintivo nos seguintes pontos:

1. **Abuso unilateral, não colusivo, como objeto.** A leniência exige cúmplice
   para delatar; a denúncia interna é financeira, não antitruste. O WaaS
   modela como um trabalhador interno pode delatar abuso de posição dominante
   unilateral (*self-preferencing*, *anti-steering*, *killer acquisitions*).
2. **Acoplamento explícito** entre IC do trabalhador (Hokamp-Pickhardt), IR
   financeira da firma (Spagnolo) e IC institucional (Art. 12 da Resolução
   CADE 21/2018) — sem paralelo no corpus ABM antitruste.
3. **Hirschman exit-with-equity** como restrição contratual sobre IC-F*. O
   *exit-with-equity* como microfundamento da IC-F* da firma é original; a
   literatura de leniência trata apenas recompensa financeira direta.
4. **Calibração institucional brasileira granular** (Leis 12.529, 13.608,
   13.964; Resolução 21/2018; Brasscom 2024; Saito 2021; DEE/CADE 2022, 2024).
5. **Catálogo heterogêneo conduta × papel intra-firma** (`condutas.py`): nove
   condutas digitais (incluindo casos BR — iFood marketplace, Apple Brasil
   2025) cruzadas com dez papéis funcionais e gradiente 3-níveis
   primário/adjacente/distal (Near & Miceli 1985).

## §5 · Caveat metodológico

- Todas as referências acima foram verificadas via DOI/arXiv/URL no curso da
  pesquisa de junho/2026, com exceção das marcadas **[?]**, que aguardam
  confirmação manual antes de citação verbatim.
- A pesquisa **não conseguiu localizar** um pesquisador "Anderson Caputo
  Silva" ligado ao CADE/USP em antitruste (homônimo no Banco Mundial é
  especialista em finanças, não antitruste) — referência removida.
- A pesquisa **não confirmou** a existência de "Heitzman-Lefebvre" sobre
  *false reporting/gaming* — substituído por Stubben & Welch (2020),
  indexado.
